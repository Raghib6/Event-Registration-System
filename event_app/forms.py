from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Password does not match !")


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["title", "description", "time", "date","location","total_slots","image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "total_slots": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"})
        }
