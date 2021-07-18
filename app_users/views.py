from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from app_users.forms import ChatUserRegistration


class ChatUserRegisterView(FormView):
    form_class = ChatUserRegistration
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('chats_list')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        raw_password = self.request.POST['password1']
        user = authenticate(
            username=username,
            password=raw_password,
        )
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'app_users/logout.html'
