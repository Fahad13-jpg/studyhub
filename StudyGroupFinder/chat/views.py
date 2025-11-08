from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from groups.models import StudyGroup
from .models import GroupMessage, MessageRead
from .forms import MessageForm

@login_required
def group_chat(request, group_id):
    """Display group chat interface"""
    group = get_object_or_404(StudyGroup, pk=group_id)
    
    # Check if user is a member
    if request.user not in group.members.all():
        messages.error(request, 'You must be a member to access group chat.')
        return redirect('groups:group_detail', pk=group_id)
    
    # Get all messages
    chat_messages = group.messages.select_related('sender', 'sender__profile').all()
    
    # Mark messages as read
    unread_messages = chat_messages.exclude(
        read_by__user=request.user
    ).exclude(sender=request.user)
    
    for msg in unread_messages:
        MessageRead.objects.get_or_create(message=msg, user=request.user)
    
    # Handle new message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.group = group
            new_message.sender = request.user
            new_message.save()
            
            # Mark as read by sender
            MessageRead.objects.create(message=new_message, user=request.user)
            
            return redirect('chat:group_chat', group_id=group_id)
    else:
        form = MessageForm()
    
    context = {
        'group': group,
        'messages': chat_messages,
        'form': form,
    }
    return render(request, 'chat/group_chat.html', context)


@login_required
def delete_message(request, message_id):
    """Delete a message (only sender can delete)"""
    message = get_object_or_404(GroupMessage, pk=message_id, sender=request.user)
    group_id = message.group.pk
    message.delete()
    messages.success(request, 'Message deleted.')
    return redirect('chat:group_chat', group_id=group_id)


@login_required
def edit_message(request, message_id):
    """Edit a message (only sender can edit)"""
    message = get_object_or_404(GroupMessage, pk=message_id, sender=request.user)
    
    if request.method == 'POST':
        new_text = request.POST.get('message', '').strip()
        if new_text:
            message.message = new_text
            message.is_edited = True
            message.save()
            messages.success(request, 'Message updated.')
    
    return redirect('chat:group_chat', group_id=message.group.pk)


@login_required
def get_unread_count(request, group_id):
    """API endpoint to get unread message count"""
    group = get_object_or_404(StudyGroup, pk=group_id)
    
    if request.user not in group.members.all():
        return JsonResponse({'count': 0})
    
    unread_count = GroupMessage.objects.filter(
        group=group
    ).exclude(
        read_by__user=request.user
    ).exclude(
        sender=request.user
    ).count()
    
    return JsonResponse({'count': unread_count})