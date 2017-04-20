from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.utils import html
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from django.conf import settings
from .models import Book, Subscription
from .forms import AccountForm, AccountEditForm,ProfileEditForm


# Create your views here.
def index(request):
    context = {'nbar': 'home', 
                'heading': 'Amazing Textbook Store',
                'mission': 'home of amazingly cheap college textbooks',
                'deals': [('black friday deal', 'https://placehold.it/150x80?text=IMAGE', 'Buy 50 mobiles and get a gift card'),
                ('christmas deal', 'https://placehold.it/150x80?text=No+Image', 'Buy 1 mobile and get 1 free')]
            }
    return render(request, 'books/index.html', context)

def book_list(request):
    context = {
                'nbar': 'books',
                'pageTitle': 'Books',
                #'books': Book.objects.all(),
                'books': Book.objects.filter(available=True)
            }
    return render(request, 'books/list.html', context)

def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug, available=True)
    context = {
                'nbar': 'books',
                'pageTitle': book.title,
                'book': book
    }
    return render(request, 'books/detail.html', context)

def subscribe(request):
    errors = []
    context = {}
    if 'email' in request.GET:
        email_id = request.GET.get('email', '')
        if not email_id:
            errors.append('Please enter a valid email address.')
        else:
            subs = Subscription.objects.create(email=email_id)
            context['pageTitle']= 'Thank you!'
            context['panelTitle'] = 'Thank you!'
            context['panelBody'] = 'Thank you for subscribing to our mailing list.'
            return render(request, 'books/static.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deals(request):
    context = {
        'nbar': 'deals',
        'pageTitle': 'Deals',
        'panelTitle': 'Deals',
        'panelBody': '<strong>Sorry, no deals at this time. Sign up to get deals delivered right to your inbox...</strong>'
    }
    return render(request, 'books/static.html', context)

def contact(request):
    context = {
        'nbar': 'contact',
        'pageTitle': 'Contact',
        'panelTitle': 'Contact',
        'panelBody': """
            <!-- List group -->
            <ul class="list-group">
            <li class="list-group-item"><strong>Corporate Office: </strong><br />
                <address>111 University Blvd<br>
                        Grand Junction, CO 81501 <br>
                        &phone;: (970) 123-4567<br>
                        <span class="glyphicon glyphicon-envelope"></span>: help@amazing.com<br>
                </address>
            </li>
            <li class="list-group-item"><strong>Denver Office: </strong><br />
                <address>123 Amazing Street</br>
                        Denver, CO 81111 <br>
                        &phone;: (970) 123-1234<br>
                        <span class="glyphicon glyphicon-envelope"></span>: denver@amazing.com<br>
                </address>
            </li>
            <li class="list-group-item">Porta ac consectetur ac</li>
            <li class="list-group-item">Vestibulum at eros</li>
            </ul>
            
        """,
    }
    return render(request, 'books/static.html', context)

def login(request):
    # print('site = ', request.get_host())
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        valid = False
        error_message = []
        if not username or not password:
            error_message = ['You must fill in all of the fields.']
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # correct password, and the user is marked active
                    auth.login(request, user)
                    request.session['user_id'] = user.id
                    valid = True
                else:
                    error_message = ["User accocount has not been activated."]

            else:
                error_message = ["Invalid username or password."]

        if valid:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request,
                          'books/login.html',
                          {
                           'errorMessage': ' '.join(error_message),
                           'username': username,
                           'password': password,
                           })

    else:
        # No context variables to pass to the template system, hence blank
        # dictionary object...
        return render(request,
                      'books/login.html',
                      {
                          'pageTitle': 'Login',
                      })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):
    valid = False
    error_message = []
    message_type = 'info'
    # path = request.get_full_path()
    # print('path = ', path)
    if request.user.is_authenticated():
        # user already has an account and is authenticated; don't let them register again
        error_message = [u'''You are logged in as {username}. If you'd like to register another account,
                         <a href="{url}">Logout</a> first.
                         '''.format(username=html.escape(request.user.username), url=settings.LOGOUT_URL)]
        valid = False
    # If it's a HTTP POST, we're interested in processing form data.
    elif request.method == 'POST':
        accForm = AccountForm(data=request.POST)
        if accForm.is_valid():
            # check for duplicate username
            user = auth.models.User.objects.filter(username=accForm.cleaned_data['username'])
            if user:
                url = '/recover/'
                error_message = [u'''Account with email {username} already exists. <a href="{url}">
                                 Forgot your password? </a>
                                 '''.format(username=html.escape(accForm.cleaned_data['username']), url=url)]
                valid = False
            else:
                try:
                    validate_password(accForm.cleaned_data['password'])
                    valid = True
                except ValidationError as ex:
                    valid = False
                    for e in ex: #ex is list of error messages
                        error_message.append(e)
        else:
            valid = False
            for k in accForm.errors:
                error_message.append('<br>'.join(accForm.errors[k]))

        if valid:
            # Save the user's form data to the database.
            user = accForm.save(commit=False)
            user.set_password(accForm.cleaned_data['password']) # set the password using default hashing
            user.is_active = True #set it to False if verifcation is required
            user.is_superuser = False
            user.is_staff = False
            user.save()
            # generate_activation_key_and_send_email(site_url, user)
            # send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=True)
            # Update our variable to tell the template registration was successful.
            error_message = [u'''The account is created. Follow the link to login...<a
                                     href="{url}">Login</a>.
                                     '''.format(url=reverse('login'))]
            return render(request,
                        'books/message.html',
                        {
                            'pageTitle': 'Feedback',
                            'messageType': 'success',
                            'message': ' '.join(error_message),
                        })

        else:
            return render(request,
                        'books/signup.html',
                        {
                            'pageTitle': 'Account Registration',
                            'panelTitle': 'Account Registration',
                            'accountForm': accForm,
                            'errorMessage': '<br>'.join(error_message),
                        })

        
    else:
        accForm = AccountForm()
        return render(request,
                      'books/signup.html',
                      {
                          'pageTitle': 'Account Registration',
                          'panelTitle': 'Account Registration',
                          'accountForm': accForm,
                      })

    
@login_required  
def dashboard(request):
    context = {
        'pageTitle': 'Dashboard',
        'panelTitle': 'Dashboard',
        'panelBody': '<strong>TBD... Display account dashboard here...</strong>'
    }
    return render(request, 'books/static.html', context)


@login_required
def account(request):
    errorMessage = []
    errorType = 'danger'
    if request.method == 'POST':
        accForm = AccountEditForm(instance=request.user,
                                 data=request.POST,
                                 )
        profileForm = ProfileEditForm(instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if accForm.is_valid() and profileForm.is_valid():
            accForm.save()
            profileForm.save()
            errorMessage.append('Account update successful!')
            errorType = 'success'
        else:
            for k in accForm.errors:
                errorMessage.append(accForm.errors[k])
    else:
        accForm = AccountEditForm(instance=request.user)
        profileForm = ProfileEditForm(instance=request.user.profile)

    return render(request, 'books/account.html', 
                    {   
                        'pageTitle': 'Account Update',
                        'panelTitle': 'Account Update',
                        'accountForm': accForm,
                        'profileForm': profileForm,
                        'errorMessage': '<br>'.join(errorMessage),
                        'errorType': errorType
                    })


def search(request):
    context = {}
    if 'search' in request.GET:
        q = request.GET.get('search', '')
        if q:
            books = Book.objects.filter(title__icontains=q)
            context['pageTitle']= 'Search results'
            context['panelTitle'] = '%d matching results'%len(books)
            context['books'] = books
            return render(request, 'books/search_results.html', context)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))