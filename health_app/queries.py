from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q, F
from django.contrib.auth import get_user_model

from health_app.models import AppleHealthStat

def get_users_with_less_sleep():
    one_week_ago = timezone.now() - timedelta(days=7)
    users = get_user_model().objects.all()
    users_with_less_sleep = []
    
    for user in users:
        total_sleep = 0
        health_stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
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
        apple_health_stat__stepCount__gte = 10000
    ).distinct()

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
    )
    
    filtered_users = users.filter(
        steps_last_week__lt=F('steps_week_before_last') / 2
    )

    return filtered_users

def get_absent_users():
    User = get_user_model()
    users_absent_days = {}
    
    for user in User.objects.all():
        last_stat = AppleHealthStat.objects.filter(user=user).order_by('-created_at').first()
        
        if last_stat:
            days_absent = (timezone.now().date() - last_stat.created_at.date()).days
            if days_absent > 0:
                users_absent_days[user.username] = days_absent
        else:
            days_absent = (timezone.now().date() - user.date_joined.date()).days
            users_absent_days[user.username] = days_absent

    return users_absent_days
