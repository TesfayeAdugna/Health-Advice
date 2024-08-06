from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q, F
from django.contrib.auth import get_user_model

from health_app.models import AppleHealthStat

# def get_users_with_less_sleep():
#     one_week_ago = timezone.now() - timedelta(days=7)
#     print(get_user_model().objects.all())
#     users = get_user_model().objects.filter(
#         apple_health_stat__created_at__gte=one_week_ago
#     ).annotate(
#         total_sleep=Sum('apple_health_stat__sleepAnalysis__sleep_time')
#     ).filter(total_sleep__lt=6*3600)  # 6 hours in seconds
#     print(users, "hello here")
#     return users

def get_users_with_less_sleep():
    one_week_ago = timezone.now() - timedelta(days=7)
    users = get_user_model().objects.all()[:1]
    users_with_less_sleep = []
    print(users, one_week_ago)
    
               
    for user in users:
        total_sleep = 0
        health_stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)[:1]
        count = 0
        for stat in health_stats:
            sleep_analyses = stat.sleepAnalysis  # Assuming sleepAnalysis is a list of dictionaries
            total_sleep += sum(sleep['sleep_time'] for sleep in sleep_analyses)
            count += 1

        if total_sleep/7 < 6 * 3600:  # 6 hours in seconds
            users_with_less_sleep.append(user)

    return users_with_less_sleep

def get_users_with_10000_steps_today():
    today = timezone.now().date()
    users = get_user_model().objects.filter(
        apple_health_stat__created_at__date=today,
        apple_health_stat__stepCount__gte =10000
    )
    return users

def get_users_with_50_percent_less_steps():
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)

    users = get_user_model().objects.annotate(
        steps_last_week=Sum(
            'apple_health_stat__stepCount',
            filter=Q(apple_health_stat__created_at__date__gte=one_week_ago)
        ),
        steps_week_before_last=Sum(
            'apple_health_stat__stepCount',
            filter=Q(apple_health_stat__created_at__date__gte=two_weeks_ago) & Q(apple_health_stat__created_at__date__lt=one_week_ago)
        )
    ).filter(
        steps_last_week__lt=F('steps_week_before_last') / 2
    )
    return users
