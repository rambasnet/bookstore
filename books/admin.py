from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Book, Publisher, Author, Subscription

# Register your models here.

class BookAdmin(SummernoteModelAdmin):
    list_display = ('title', 'publisher', 'available', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)
    prepopulated_fields = {'slug': ('title',)}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')
    prepopulated_fields = {'slug': ('first_name', 'middle_name', 'last_name',)}


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed')
    search_fields = ('email',)
    list_filter = ('email',)

admin.site.register(Book, BookAdmin)
admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
