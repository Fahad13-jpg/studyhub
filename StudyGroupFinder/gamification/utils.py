from django.db.models import Count
from .models import Badge, UserBadge, StudyStreak, UserPoints, Achievement, UserAchievement

def check_and_award_badges(user):
    """Check user activity and award appropriate badges"""
    from groups.models import StudyGroup
    from user_sessions.models import StudySession, SessionRSVP
    from chat.models import GroupMessage
    
    badges_earned = []
    
    # Get user stats
    groups_created = StudyGroup.objects.filter(creator=user).count()
    groups_joined = user.joined_groups.count()
    sessions_created = StudySession.objects.filter(created_by=user).count()
    sessions_attended = SessionRSVP.objects.filter(user=user, status='attending').count()
    messages_sent = GroupMessage.objects.filter(sender=user).count()
    
    # Group Founder Badges
    founder_tiers = [
        (1, 'bronze', 'fa-seedling', '#cd7f32'),
        (3, 'silver', 'fa-tree', '#c0c0c0'),
        (5, 'gold', 'fa-crown', '#ffd700'),
        (10, 'platinum', 'fa-gem', '#e5e4e2'),
    ]
    
    for count, tier, icon, color in founder_tiers:
        if groups_created >= count:
            badge, created = Badge.objects.get_or_create(
                badge_type='founder',
                tier=tier,
                defaults={
                    'name': f'{tier.capitalize()} Founder',
                    'description': f'Created {count}+ study groups',
                    'icon': icon,
                    'color': color,
                    'requirement_value': count,
                    'requirement_description': f'Create {count} study groups',
                    'points': count * 10
                }
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                badges_earned.append(badge)
                award_points(user, badge.points, 'badges')
    
    # Session Creator Badges
    session_creator_tiers = [
        (5, 'bronze', 'fa-calendar-plus', '#cd7f32'),
        (15, 'silver', 'fa-calendar-check', '#c0c0c0'),
        (30, 'gold', 'fa-calendar-star', '#ffd700'),
        (50, 'platinum', 'fa-calendar-day', '#e5e4e2'),
    ]
    
    for count, tier, icon, color in session_creator_tiers:
        if sessions_created >= count:
            badge, created = Badge.objects.get_or_create(
                badge_type='session_creator',
                tier=tier,
                defaults={
                    'name': f'{tier.capitalize()} Organizer',
                    'description': f'Created {count}+ study sessions',
                    'icon': icon,
                    'color': color,
                    'requirement_value': count,
                    'requirement_description': f'Create {count} sessions',
                    'points': count * 5
                }
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                badges_earned.append(badge)
                award_points(user, badge.points, 'badges')
    
    # Perfect Attendance Badges
    attendance_tiers = [
        (10, 'bronze', 'fa-check-circle', '#cd7f32'),
        (25, 'silver', 'fa-check-double', '#c0c0c0'),
        (50, 'gold', 'fa-medal', '#ffd700'),
        (100, 'platinum', 'fa-trophy', '#e5e4e2'),
    ]
    
    for count, tier, icon, color in attendance_tiers:
        if sessions_attended >= count:
            badge, created = Badge.objects.get_or_create(
                badge_type='perfect_attendance',
                tier=tier,
                defaults={
                    'name': f'{tier.capitalize()} Attendee',
                    'description': f'Attended {count}+ study sessions',
                    'icon': icon,
                    'color': color,
                    'requirement_value': count,
                    'requirement_description': f'Attend {count} sessions',
                    'points': count * 3
                }
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                badges_earned.append(badge)
                award_points(user, badge.points, 'badges')
    
    # Social Butterfly Badges (messages sent)
    social_tiers = [
        (50, 'bronze', 'fa-comments', '#cd7f32'),
        (200, 'silver', 'fa-comment-dots', '#c0c0c0'),
        (500, 'gold', 'fa-comment-medical', '#ffd700'),
        (1000, 'platinum', 'fa-comment-alt', '#e5e4e2'),
    ]
    
    for count, tier, icon, color in social_tiers:
        if messages_sent >= count:
            badge, created = Badge.objects.get_or_create(
                badge_type='social_butterfly',
                tier=tier,
                defaults={
                    'name': f'{tier.capitalize()} Communicator',
                    'description': f'Sent {count}+ messages',
                    'icon': icon,
                    'color': color,
                    'requirement_value': count,
                    'requirement_description': f'Send {count} messages',
                    'points': count // 10
                }
            )
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                badges_earned.append(badge)
                award_points(user, badge.points, 'badges')
    
    # Streak Master Badge
    streak = StudyStreak.objects.filter(user=user).first()
    if streak:
        streak_tiers = [
            (4, 'bronze', 'fa-fire', '#cd7f32'),
            (8, 'silver', 'fa-fire-alt', '#c0c0c0'),
            (12, 'gold', 'fa-fire-flame-curved', '#ffd700'),
            (20, 'platinum', 'fa-fire-flame-simple', '#e5e4e2'),
        ]
        
        for count, tier, icon, color in streak_tiers:
            if streak.longest_streak >= count:
                badge, created = Badge.objects.get_or_create(
                    badge_type='streak_master',
                    tier=tier,
                    defaults={
                        'name': f'{tier.capitalize()} Streak Master',
                        'description': f'{count}+ week study streak',
                        'icon': icon,
                        'color': color,
                        'requirement_value': count,
                        'requirement_description': f'Maintain {count} week streak',
                        'points': count * 20
                    }
                )
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    badges_earned.append(badge)
                    award_points(user, badge.points, 'badges')
    
    return badges_earned


def update_user_streak(user):
    """Update study streak for user activity"""
    streak, created = StudyStreak.objects.get_or_create(user=user)
    
    # Update activity counts
    from user_sessions.models import SessionRSVP
    streak.total_sessions_attended = SessionRSVP.objects.filter(
        user=user,
        status='attending'
    ).count()
    streak.total_groups_joined = user.joined_groups.count()
    streak.total_sessions_created = user.created_sessions.count()
    
    # Update streak
    streak.update_streak()
    
    return streak


def award_points(user, points, category='other'):
    """Award points to user"""
    user_points, created = UserPoints.objects.get_or_create(user=user)
    user_points.add_points(points, category)
    return user_points


def check_achievements(user):
    """Check and award achievements"""
    from user_sessions.models import SessionRSVP
    
    achievements_earned = []
    
    # Define achievements
    achievement_definitions = [
        {
            'name': 'Early Adopter',
            'description': 'Joined a group within its first week',
            'type': 'early_joiner',
            'value': 1,
            'icon': 'fa-rocket',
            'color': '#667eea',
            'points': 50
        },
        {
            'name': 'Marathon Learner',
            'description': 'Attended 5+ sessions in a single week',
            'type': 'weekly_sessions',
            'value': 5,
            'icon': 'fa-running',
            'color': '#38ef7d',
            'points': 100
        },
        {
            'name': 'Group Hopper',
            'description': 'Join 10+ different study groups',
            'type': 'groups_joined',
            'value': 10,
            'icon': 'fa-users',
            'color': '#f093fb',
            'points': 75
        },
        {
            'name': 'Mentor',
            'description': 'Help create 20+ successful study sessions',
            'type': 'sessions_created',
            'value': 20,
            'icon': 'fa-user-graduate',
            'color': '#ffd700',
            'points': 150
        },
    ]
    
    for achievement_def in achievement_definitions:
        achievement, created = Achievement.objects.get_or_create(
            requirement_type=achievement_def['type'],
            requirement_value=achievement_def['value'],
            defaults={
                'name': achievement_def['name'],
                'description': achievement_def['description'],
                'icon': achievement_def['icon'],
                'color': achievement_def['color'],
                'points_reward': achievement_def['points']
            }
        )
        
        # Check if user qualifies
        qualifies = False
        progress = 0
        
        if achievement_def['type'] == 'groups_joined':
            count = user.joined_groups.count()
            progress = count
            qualifies = count >= achievement_def['value']
        elif achievement_def['type'] == 'sessions_created':
            count = user.created_sessions.count()
            progress = count
            qualifies = count >= achievement_def['value']
        
        if qualifies:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'progress': progress}
            )
            if created:
                achievements_earned.append(achievement)
                award_points(user, achievement.points_reward, 'badges')
    
    return achievements_earned


def get_user_gamification_data(user):
    """Get all gamification data for a user"""
    # Ensure all objects exist
    streak, _ = StudyStreak.objects.get_or_create(user=user)
    points, _ = UserPoints.objects.get_or_create(user=user)
    
    # Get badges
    earned_badges = UserBadge.objects.filter(user=user).select_related('badge')
    
    # Get achievements
    earned_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    
    return {
        'streak': streak,
        'points': points,
        'badges': earned_badges,
        'achievements': earned_achievements,
        'badges_count': earned_badges.count(),
        'achievements_count': earned_achievements.count()
    }