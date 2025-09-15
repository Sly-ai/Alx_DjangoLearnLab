# bookshelf/forms.py
from django import forms
from .models import Book
import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "published_at"]
        widgets = {
            "published_at": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        # Additional normalization/validation here if needed
        return title

    def clean_published_at(self):
        published_at = self.cleaned_data.get("published_at")
        if published_at and published_at > datetime.date.today():
            raise forms.ValidationError("Published date cannot be in the future.")
        return published_at

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=200)

    def clean_q(self):
        q = self.cleaned_data.get("q", "").strip()
        # further sanitization if required; keep simple and validated length
        return q
