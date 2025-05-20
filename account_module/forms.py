from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import Student, Proff


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[validators.EmailValidator(),
                    validators.MaxLengthValidator(100)],
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        validators=[validators.MaxLengthValidator(100)],
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        validators=[validators.MaxLengthValidator(100)],
    )

    #first_name = forms.CharField(
    #    label='First Name',
    #    validators=[validators.MaxLengthValidator(100)],
    #)

    #last_name = forms.CharField(
    #    label='Last Name',
    #    validators=[validators.MaxLengthValidator(100)],
    #)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
            # raise ValidationError('Passwords do not match')

        raise ValidationError('Passwords do not match')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[validators.MaxLengthValidator(100),
                    validators.EmailValidator()
        ],
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        validators=[validators.MaxLengthValidator(100)],
    )


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_num', 'faculty', 'field_of_study', 'education_level']


class ProfProfileForm(forms.ModelForm):
    class Meta:
        model = Proff
        fields = ['teacher_num', 'field_of_study', 'education_level']


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('Passwords do not match')
