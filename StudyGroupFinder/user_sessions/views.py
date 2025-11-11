from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from .models import StudySession, SessionRSVP
from groups.models import StudyGroup
from .forms import StudySessionForm, RSVPForm

@login_required
def create_session(request, group_id):
    """Create a new study session for a group"""
    group = get_object_or_404(StudyGroup, pk=group_id)
    
    # Check if user is a member of the group
    if request.user not in group.members.all():
        messages.error(request, 'You must be a member to create sessions.')
        return redirect('groups:group_detail', pk=group_id)
    
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.group = group
            session.created_by = request.user
            session.save()
            
            # Notify all group members
            from notifications.utils import notify_session_created
            notify_session_created(session)
            
            messages.success(request, 'Study session created successfully!')
            return redirect('user_sessions:session_detail', pk=session.pk)
    else:
        form = StudySessionForm()
    
    return render(request, 'user_sessions/create_session.html', {
        'form': form,
        'group': group
    })


@login_required
def session_detail(request, pk):
    """View session details and RSVP"""
    session = get_object_or_404(StudySession, pk=pk)
    group = session.group
    is_member = request.user in group.members.all()
    
    user_rsvp = None
    if is_member:
        user_rsvp = SessionRSVP.objects.filter(session=session, user=request.user).first()
    
    # Get all RSVPs grouped by status
    attending = session.rsvps.filter(status='attending').select_related('user')
    maybe = session.rsvps.filter(status='maybe').select_related('user')
    cannot = session.rsvps.filter(status='cannot').select_related('user')
    
    context = {
        'session': session,
        'group': group,
        'is_member': is_member,
        'user_rsvp': user_rsvp,
        'attending': attending,
        'maybe': maybe,
        'cannot': cannot,
    }
    return render(request, 'user_sessions/session_detail.html', context)


@login_required
def rsvp_session(request, pk, status):
    """RSVP to a session"""
    session = get_object_or_404(StudySession, pk=pk)
    
    # Check if user is a member
    if request.user not in session.group.members.all():
        messages.error(request, 'Only group members can RSVP.')
        return redirect('user_sessions:session_detail', pk=pk)
    
    # Update or create RSVP
    rsvp, created = SessionRSVP.objects.update_or_create(
        session=session,
        user=request.user,
        defaults={'status': status}
    )
    
    # Update gamification (streak and badges)
    if status == 'attending':
        from gamification.utils import update_user_streak, check_and_award_badges, award_points
        update_user_streak(request.user)
        check_and_award_badges(request.user)
        award_points(request.user, 5, 'sessions')  # 5 points for attending
    
    messages.success(request, f'RSVP updated to: {rsvp.get_status_display()}')
    return redirect('user_sessions:session_detail', pk=pk)


@login_required
def group_sessions(request, group_id):
    """View all sessions for a group"""
    group = get_object_or_404(StudyGroup, pk=group_id)
    is_member = request.user in group.members.all()
    
    # Get upcoming and past sessions
    now = datetime.now()
    upcoming = group.sessions.filter(date__gte=now.date(), is_cancelled=False).order_by('date', 'time')
    past = group.sessions.filter(date__lt=now.date()).order_by('-date', '-time')
    
    context = {
        'group': group,
        'is_member': is_member,
        'upcoming_sessions': upcoming,
        'past_sessions': past,
    }
    return render(request, 'user_sessions/group_sessions.html', context)


@login_required
def cancel_session(request, pk):
    """Cancel a session"""
    session = get_object_or_404(StudySession, pk=pk)
    
    # Only creator or group creator can cancel
    if request.user != session.created_by and request.user != session.group.creator:
        messages.error(request, 'Only the session creator or group creator can cancel sessions.')
        return redirect('user_sessions:session_detail', pk=pk)
    
    session.is_cancelled = True
    session.save()
    
    # Notify all group members
    from notifications.utils import notify_session_cancelled
    notify_session_cancelled(session)
    
    messages.success(request, 'Session cancelled successfully.')
    return redirect('user_sessions:group_sessions', group_id=session.group.pk)


@login_required
def delete_session(request, pk):
    """Delete a session"""
    session = get_object_or_404(StudySession, pk=pk)
    group_id = session.group.pk
    
    # Only creator or group creator can delete
    if request.user != session.created_by and request.user != session.group.creator:
        messages.error(request, 'Only the session creator or group creator can delete sessions.')
        return redirect('user_sessions:session_detail', pk=pk)
    
    session.delete()
    messages.success(request, 'Session deleted successfully.')
    return redirect('user_sessions:group_sessions', group_id=group_id)