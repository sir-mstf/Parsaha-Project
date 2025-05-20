from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from account_module.models import User, Student, Proff


class EditProfileStudModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_num', 'faculty', 'field_of_study']
        widgets = {
            'student_num': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'student_num': 'Student Number',
            'faculty': 'Faculty',
            'field_of_study': 'Field of Study',
        }

#class ChangePasswordForm(forms.Form):
#    current_password = forms.CharField(
#        label='current Password',
#        widget=forms.PasswordInput(
#            attrs={'class': 'form-control',}
#        ),
#        validators=[
#            validators.MaxLengthValidator(100),
#        ],
#    )
#    new_password = forms.CharField(
#        label='new Password',
#        widget=forms.PasswordInput(
#            attrs={'class': 'form-control',}
#        ),
#        validators=[
#            validators.MaxLengthValidator(100),
#        ],
#    )
#    confirm_password = forms.CharField(
#        label='Confirm Password',
#        widget=forms.PasswordInput(
#            attrs={'class': 'form-control',}
#        ),
#        validators=[
#            validators.MaxLengthValidator(100),
#        ],
#    )


