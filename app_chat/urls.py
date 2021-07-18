from django.urls import path
from app_chat.views import chats_list_view, new_message_view, dialog_view

urlpatterns = [
    path(
        'chats_list/',
        chats_list_view,
        name='chats_list',
    ),
    path(
        'new_chat/<str:new_chat_with>',
        new_message_view,
        name='new_chat_page',
    ),
    path(
        'chat_with/<int:chat_id>',
        dialog_view,
        name='chat_with',
    ),
]
