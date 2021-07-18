from django.contrib.auth.forms import UserCreationForm
from app_users.models import ChatUser


class ChatUserRegistration(UserCreationForm):

    class Meta:
        model = ChatUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
