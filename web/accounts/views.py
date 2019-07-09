from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.contrib.auth import login

from authtools import views as authviews

from braces import views as bracesviews
from . import forms


class LoginView(bracesviews.AnonymousRequiredMixin, authviews.LoginView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('projects:project_list')


class LogoutView(authviews.LogoutView):
    url = reverse_lazy('projects:project_list')


class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):

    template_name = 'signup.html'
    success_url = reverse_lazy('profiles:edit_profile')
    form_class = forms.SignUpForm
    form_valid_message = "You're signed up!"

    def form_valid(self, form):
        resp = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return resp
