from django.db.models import Count, Q, F
from django.contrib.auth.models import User
from groups.models import StudyGroup
from .models import SearchHistory, GroupView, RecommendationScore


def calculate_recommendations(user, limit=10):
    """
    Calculate personalized group recommendations for a user
    Returns list of (group, score, reasons) tuples
    """
    recommendations = []
    
    # Get user profile
    profile = user.profile
    
    # ✅ FIX: Use annotation instead of non-existent 'current_member_count' field
    available_groups = (
        StudyGroup.objects.annotate(num_members=Count('members'))
        .exclude(members=user)
        .filter(num_members__lt=F('max_capacity'))
    )
    
    for group in available_groups:
        score = 0.0
        reasons = []
        
        # 1. Same Department (High Weight: +30)
        if profile.department and profile.department.lower() in group.course_name.lower():
            score += 30
            reasons.append(f"Matches your department: {profile.department}")
        
        # 2. Same Semester/Year (Medium Weight: +20)
        if profile.semester or profile.year:
            same_level_members = group.members.filter(
                Q(profile__semester=profile.semester) | 
                Q(profile__year=profile.year)
            ).count()
            if same_level_members > 0:
                score += 20
                reasons.append(f"{same_level_members} students from your semester/year")
        
        # 3. Search History Match (Medium Weight: +25)
        recent_searches = SearchHistory.objects.filter(user=user)[:10]
        for search in recent_searches:
            if (search.query.lower() in group.name.lower() or 
                search.query.lower() in group.course_name.lower() or
                search.query.lower() in group.course_code.lower()):
                score += 25
                reasons.append(f"Matches your search: '{search.query}'")
                break
        
        # 4. Popular in Similar Profile (Medium Weight: +15)
        similar_users = User.objects.filter(
            profile__department=profile.department,
            profile__semester=profile.semester
        ).exclude(id=user.id)[:50]
        
        similar_user_members = group.members.filter(id__in=similar_users).count()
        if similar_user_members > 0:
            score += 15
            reasons.append(f"{similar_user_members} students with similar profile joined")
        
        # 5. Recently Viewed Groups (Low Weight: +10)
        recently_viewed = GroupView.objects.filter(user=user, group=group).exists()
        if recently_viewed:
            score += 10
            reasons.append("You viewed this group recently")
        
        # 6. Public Groups (Small Weight: +5)
        if group.group_type == 'public':
            score += 5
            reasons.append("Public group - join instantly")
        
        # 7. Active Groups (Small Weight: +8)
        recent_sessions = group.sessions.filter(is_cancelled=False).count()
        if recent_sessions > 0:
            score += 8
            reasons.append(f"{recent_sessions} active study sessions")
        
        # 8. Well-Populated Groups (Small Weight: +5)
        member_ratio = group.members.count() / group.max_capacity
        if 0.3 <= member_ratio <= 0.8:
            score += 5
            reasons.append(f"Active with {group.members.count()} members")
        
        # Only add groups with positive scores
        if score > 0:
            recommendations.append({
                'group': group,
                'score': score,
                'reasons': reasons
            })
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations[:limit]


def update_recommendation_cache(user):
    """Update cached recommendations for a user"""
    recommendations = calculate_recommendations(user, limit=20)
    
    # Clear old recommendations
    RecommendationScore.objects.filter(user=user).delete()
    
    # Save new recommendations
    for rec in recommendations:
        RecommendationScore.objects.create(
            user=user,
            group=rec['group'],
            score=rec['score'],
            reasons=rec['reasons']
        )


def track_group_view(user, group):
    """Track when a user views a group (for recommendation algorithm)"""
    GroupView.objects.create(user=user, group=group)


def track_search(user, query):
    """Track user search queries (for recommendation algorithm)"""
    if query.strip():
        SearchHistory.objects.create(user=user, query=query.strip())
