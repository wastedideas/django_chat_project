from django import forms
from app_users.models import ChatUser
from app_chat.models import Message
from chat_project.settings import AUTH_USER_MODEL


class FindChatOpponent(forms.Form):
    opponent_username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Find your companion..'}))

    def clean(self):
        cleaned_data = super().clean()
        friend_nickname = cleaned_data.get('opponent_username')

        if friend_nickname not in [i_user.username for i_user in ChatUser.objects.all()] or friend_nickname == AUTH_USER_MODEL:
            self.add_error('opponent_username', 'Opponent for dialog not found.')
        return cleaned_data


class NewMessage(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text',)
