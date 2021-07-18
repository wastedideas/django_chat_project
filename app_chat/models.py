from django.db import models
from chat_project.settings import AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='sender', related_name='message_sender')
    send_at = models.DateTimeField(auto_now_add=True, verbose_name='send at')
    text = models.TextField(max_length=10000, verbose_name='message text')
    recipient = models.ForeignKey(to='app_users.ChatUser', on_delete=models.CASCADE, verbose_name='recipient', related_name='message_recipient')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, verbose_name='chat', related_name='chat_messages')


class Chat(models.Model):
    owner = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='chat owner', related_name='chat_owner')
    opponent = models.ForeignKey(to='app_users.ChatUser', on_delete=models.CASCADE, verbose_name='opponent',
                                  related_name='chat_opponent')
