import uuid, os
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth import models as authModels

# Create your models here.
from django.db import models

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('books/img', filename)

def getProfilePath(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profiles/img', filename)

def get_slug(instance, *argv):
    slug = ''
    for arg in argv:
        slug += slugify(arg)
    return slug

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30, db_index=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'%s %s'%(self.first_name, self.last_name)

    class Meta:
        ordering = ('first_name', 'last_name')
        index_together = (('id', 'slug'),)

class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id, self.slug])


class Subscription(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email

#Extending User model
class Profile(models.Model):
    user = models.OneToOneField(authModels.User)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=getProfilePath, blank=True)
    
    def __str__(self):
        return 'Profile: {}'.format(self.user.username)
