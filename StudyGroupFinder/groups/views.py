from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import StudyGroup, GroupMember, JoinRequest
from .forms import StudyGroupForm, JoinRequestForm
from user_sessions.models import StudySession  # Assuming your session model is here

@login_required
def create_group(request):
    """Create a new study group"""
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            GroupMember.objects.create(user=request.user, group=group, role='creator')
            messages.success(request, 'Study group created successfully!')
            return redirect('groups:group_detail', pk=group.pk)
    else:
        form = StudyGroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_detail(request, pk):
    """View group details"""
    group = get_object_or_404(StudyGroup, pk=pk)
    is_member = request.user in group.members.all()
    is_creator = group.creator == request.user
    pending_request = JoinRequest.objects.filter(user=request.user, group=group, status='pending').first()
    pending_requests = JoinRequest.objects.filter(group=group, status='pending') if is_creator else None

    # Separate upcoming and past sessions
    now = timezone.now()
    upcoming_sessions = group.sessions.filter(date__gte=now.date(), is_cancelled=False).order_by('date', 'time')
    past_sessions = group.sessions.filter(date__lt=now.date()).order_by('-date', '-time')

    context = {
        'group': group,
        'is_member': is_member,
        'is_creator': is_creator,
        'pending_request': pending_request,
        'pending_requests': pending_requests,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
    }
    return render(request, 'groups/group_detail.html', context)

@login_required
def browse_groups(request):
    """Browse and search groups"""
    groups = StudyGroup.objects.annotate(member_count=Count('members'))
    search = request.GET.get('search', '')
    location = request.GET.get('location', '')
    
    if search:
        groups = groups.filter(
            Q(name__icontains=search) | Q(course_name__icontains=search) | Q(course_code__icontains=search)
        )
    if location:
        groups = groups.filter(meeting_location__icontains=location)
    
    context = {'groups': groups, 'search': search, 'location': location}
    return render(request, 'groups/browse_groups.html', context)

@login_required
def my_groups(request):
    """View user's groups"""
    created_groups = request.user.created_groups.all()
    joined_groups = request.user.joined_groups.exclude(creator=request.user)
    return render(request, 'groups/my_groups.html', {
        'created_groups': created_groups,
        'joined_groups': joined_groups
    })

@login_required
def join_group(request, pk):
    """Join a group"""
    group = get_object_or_404(StudyGroup, pk=pk)
    
    if request.user in group.members.all():
        messages.warning(request, 'You are already a member!')
        return redirect('groups:group_detail', pk=pk)
    
    if group.is_full():
        messages.error(request, 'Group is full!')
        return redirect('groups:group_detail', pk=pk)
    
    if group.group_type == 'public':
        GroupMember.objects.create(user=request.user, group=group)
        messages.success(request, 'You joined the group!')
    else:
        JoinRequest.objects.get_or_create(user=request.user, group=group)
        messages.info(request, 'Join request sent!')
    
    return redirect('groups:group_detail', pk=pk)

@login_required
def leave_group(request, pk):
    """Leave a group"""
    group = get_object_or_404(StudyGroup, pk=pk)
    if group.creator == request.user:
        messages.error(request, 'Creator cannot leave. Delete the group instead.')
        return redirect('groups:group_detail', pk=pk)
    
    GroupMember.objects.filter(user=request.user, group=group).delete()
    messages.success(request, 'You left the group.')
    return redirect('groups:my_groups')

@login_required
def delete_group(request, pk):
    """Delete group (creator only)"""
    group = get_object_or_404(StudyGroup, pk=pk, creator=request.user)
    group.delete()
    messages.success(request, 'Group deleted successfully.')
    return redirect('groups:my_groups')

@login_required
def approve_request(request, request_id):
    """Approve join request"""
    join_req = get_object_or_404(JoinRequest, pk=request_id, group__creator=request.user)
    if not join_req.group.is_full():
        GroupMember.objects.create(user=join_req.user, group=join_req.group)
        join_req.status = 'approved'
        join_req.save()
        messages.success(request, f'{join_req.user.username} approved!')
    else:
        messages.error(request, 'Group is full!')
    return redirect('groups:group_detail', pk=join_req.group.pk)

@login_required
def reject_request(request, request_id):
    """Reject join request"""
    join_req = get_object_or_404(JoinRequest, pk=request_id, group__creator=request.user)
    join_req.status = 'rejected'
    join_req.save()
    messages.info(request, 'Request rejected.')
    return redirect('groups:group_detail', pk=join_req.group.pk)
