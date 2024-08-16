from django import forms
from .models import book, Author

class AuthorForm(forms.ModelForm):
    class Meta: 
        """to pass some additional informations inside forms
            used to tell about the data        
        """
        model = Author
        fields = ['name']

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "write name of author"
            }),
        }

    
class BookForm(forms.ModelForm):
    class Meta:
        model = book
        fields = '__all__'

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder":"enter the title"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder":"enter the Price"
            }),
            "author": forms.Select(attrs={
                "class": "form-control",
                "placeholder":"enter the price"
            }),
        }