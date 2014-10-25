from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
	first_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("First Name"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
	last_name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Last Name"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Email address"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Confirm Password"))
    
	def clean_email(self):
		try:
			user = User.objects.get(email__iexact=self.cleaned_data['email'])
		except User.DoesNotExist:
			return self.cleaned_data['email']
		raise forms.ValidationError(("The email already exists. Please try another one."))
			
	def clean_username(self):
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError(("The username already exists. Please try another one."))
			
	def clean_password(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(("The two password fields did not match."))
		return self.cleaned_data

class LoginForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
	password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
	
