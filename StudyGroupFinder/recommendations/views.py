from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import calculate_recommendations, update_recommendation_cache
from .models import RecommendationScore

@login_required
def recommendations_page(request):
    """Display personalized recommendations page"""
    
    # Try to get cached recommendations
    cached_recommendations = RecommendationScore.objects.filter(
        user=request.user
    ).select_related('group')[:20]
    
    # If no cached recommendations or user wants fresh ones
    if not cached_recommendations or request.GET.get('refresh'):
        recommendations = calculate_recommendations(request.user, limit=20)
    else:
        # Convert cached to expected format
        recommendations = []
        for rec in cached_recommendations:
            recommendations.append({
                'group': rec.group,
                'score': rec.score,
                'reasons': rec.reasons
            })
    
    context = {
        'recommendations': recommendations,
        'title': 'Recommended Groups'
    }
    return render(request, 'recommendations/recommendations.html', context)


@login_required
def refresh_recommendations(request):
    """Manually refresh recommendations"""
    update_recommendation_cache(request.user)
    return redirect('recommendations:recommendations_page')