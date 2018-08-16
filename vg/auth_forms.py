from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def save(self, commit=True):
        model_instance = super(ProfileUpdateForm, self).save(commit=False)
        model_instance.first_name = self.cleaned_data['first_name']
        model_instance.save()
        return model_instance

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio']

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4})
        }


