from django.http import HttpResponseRedirect
from django.shortcuts import render
from app_chat.models import Chat, Message
from app_chat.forms import FindChatOpponent, NewMessage
from app_users.models import ChatUser
from django.urls import reverse_lazy, reverse
from itertools import chain


def chats_list_view(request):
    user_chats = []
    if request.user.is_authenticated:
        user_chats = chain(Chat.objects.filter(owner=request.user), Chat.objects.filter(opponent=request.user))
    find_friend = FindChatOpponent(request.POST if request.POST else None)
    if request.method == 'POST':
        if find_friend.is_valid():
            friend_nickname = find_friend.cleaned_data.get('opponent_username')
            new_chat_with = ChatUser.objects.get(username=friend_nickname).username
            return HttpResponseRedirect(reverse('new_chat_page', args=[new_chat_with],))

    context = {
            'user_chats': user_chats,
            'find_friend': find_friend,
    }
    return render(request, 'app_chat/chats.html', context)


def new_message_view(request, new_chat_with):
    if request.user.is_authenticated:
        new_opponent = ChatUser.objects.get(username=new_chat_with)
        if request.method == 'POST':
            new_message_form = NewMessage(request.POST)
            if new_message_form.is_valid():
                message_text = new_message_form.cleaned_data.get('text')

                if not Chat.objects.filter(
                    owner=new_opponent,
                    opponent=request.user,
                ).exists():
                    new_chat = Chat.objects.get_or_create(
                        owner=request.user,
                        opponent=new_opponent,
                    )
                    new_chat = new_chat[0]
                else:
                    new_chat = Chat.objects.get(
                        owner=new_opponent,
                        opponent=request.user,
                    )
                message_in_new_chat = Message.objects.create(
                    sender=request.user,
                    text=message_text,
                    recipient=new_opponent,
                    chat=new_chat,
                )
                message_in_new_chat.save()
                new_chat.save()
                return HttpResponseRedirect(reverse_lazy('chats_list'))
        else:
            new_message_form = NewMessage()
        return render(
            request,
            'app_chat/new_dialog.html',
            context={
                'new_message_form': new_message_form,
                'new_chat_with': new_chat_with,
            },
        )
    else:
        return HttpResponseRedirect(reverse_lazy('chats_list'))


def dialog_view(request, chat_id):
    if request.user.is_authenticated:
        choose_chat = Chat.objects.get(id=chat_id)
        if choose_chat.opponent.id == request.user.id:
            recipient_user = choose_chat.owner
        else:
            recipient_user = choose_chat.opponent
        all_messages_with_opponent = Message.objects.filter(chat=choose_chat)
        if request.method == 'POST':
            new_message_form = NewMessage(request.POST)
            if new_message_form.is_valid():
                message_text = new_message_form.cleaned_data.get('text')
                message_in_new_chat = Message.objects.create(
                    sender=request.user,
                    text=message_text,
                    recipient=choose_chat.opponent,
                    chat=choose_chat
                )
                message_in_new_chat.save()
            return HttpResponseRedirect(request.path)
        else:
            new_message_form = NewMessage()
        return render(
            request,
            'app_chat/dialog.html',
            context={
                'all_messages_with_opponent': all_messages_with_opponent,
                'new_message_form': new_message_form,
                'choose_chat': choose_chat,
                'recipient_user': recipient_user,
            },
        )
    else:
        return HttpResponseRedirect(reverse_lazy('chats_list'))
