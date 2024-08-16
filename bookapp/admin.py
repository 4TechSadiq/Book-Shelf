from django.contrib import admin
from .models import book,Author

# Register your models here.

admin.site.register(book)
admin.site.register(Author)