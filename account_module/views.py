from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
#from django.views.generic import CreateView
#from django.views.generic.base import TemplateView
from django.contrib.auth import login, logout
from django.views import View
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import UpdateView
from django.contrib import messages
from utils.email_service import send_email

#form utils.email_service import send_mail
from . import forms
from .models import User, Proff, Student


# Create your views here.

#class LoginView(CreateView):
#    model = User
#    template_name = 'account_module/login_page.html'


class RegisterView(View):
    def get(self, request):
        register_form = forms.RegistrationForm()
        context = {'register_form': register_form}
        return render(request, 'account_module/registration.html', context)

    def post(self, request):
        register_form = forms.RegistrationForm(request.POST)

        if register_form.is_valid():
            user_email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            if User.objects.filter(email__iexact=user_email).exists():
                register_form.add_error('email', 'Email already registered')
            else:
                new_user = User(email=user_email, email_active_code=get_random_string(72),
                                is_active=False, username=user_email)
                new_user.set_password(password)

                if new_user.email.endswith('.ac.ir'):
                    new_user.role = 'proff'
                else:
                    new_user.role = 'student'
                new_user.save()
                # todo: send email containing active code
                #send_email('account activation', new_user.email, {'user': new_user},
                #           'emails/activation_account.html')
                messages.success(request, 'email containing activation code is sent')
                return redirect('home_module')

        context = {'register_form': register_form}
        return render(request, 'account_module/registration.html', context)


class CompleteProfileView(View):
    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(User, id=kwargs['user_id'])
        if self.user_obj != request.user:
            return HttpResponse('permission denied')
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.user_obj.role == 'proff':
            return forms.ProfProfileForm
        elif self.user_obj.role == 'student':
            return forms.StudentProfileForm
        raise Http404

    def get(self, request, *args, **kwargs):

        if hasattr(self.user_obj, 'proff') or hasattr(self.user_obj, 'student'):
            raise PermissionDenied("You have already completed your profile.")

        #if self.user_obj.is_active:
        form_class = self.get_form_class()
        form = form_class()
        context = {'user_obj': self.user_obj, 'form': form}
        return render(request, 'account_module/complete_profile.html', context)
        #else:
        #    raise Http404

    def post(self, request, *args, **kwargs):
        #if self.user_obj.is_active:
        form_class = self.get_form_class()
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.user_obj
            obj.save()
            return redirect('user-panel-dashboard', pk=self.request.user.id)
        context = {'user_obj': self.user_obj, 'form': form}
        return render(request, 'account_module/complete_profile.html', context)
        #else:
        #    raise Http404


class LoginView(View):
    def get(self, request):
        login_form = forms.LoginForm()
        context = {'login_form': login_form}
        return render(request, 'account_module/login_page.html', context)

    def post(self, request):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['email']
            user_password = login_form.cleaned_data['password']
            user = User.objects.filter(email__iexact=user_email).first()
            if user:
                if not user.is_active:
                    login_form.add_error('email', 'account is not active')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('user-panel-dashboard', kwargs={'pk': self.request.user.id}))
                    login_form.add_error('email', 'wrong password or username')
            else:
                login_form.add_error('email', 'wrong password or username')

        context = {'login_form': login_form}
        return render(request, 'account_module/login_page.html', context)


class ActiveAccountView(View):
    def get(self, request, email_active_code):
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user:
            if user.is_active == False:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'your account has been activated successfully')
                return redirect('home_module')
            else:
                return HttpResponse('your account is already activated, you can Login now')
        raise Http404


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-page')


class EditProfileView(UpdateView):
    model = User
    template_name = 'account_module/edit_profile.html'
    # error to this field below:
    fields = ['first_name', 'last_name', 'avatar', 'about_user']

    def get_success_url(self):
        return reverse('user-panel-dashboard', kwargs={'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = self.request.user.id
        return context

    def get_queryset(self):
        query = User.objects.filter(id=self.request.user.id)
        return query


class ForgetPasswordView(View):
    def get(self, request):
        forget_pass_form = forms.ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        forget_pass_form = forms.ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                #todo: send email containing active code
                #send_email('password retrieval', user.email, {'user': user},
                #           'emails/forgot_password.html')
                return redirect(reverse('home-module'))

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = forms.ResetPasswordForm()

        context = {'reset_pass_form': reset_pass_form,
                   'user': user}
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request, active_code):
        reset_pass_form = forms.ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))

            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {'reset_pass_form': reset_pass_form,
                    'user': user}
        return render(request, 'account_module/reset_password.html', context)

