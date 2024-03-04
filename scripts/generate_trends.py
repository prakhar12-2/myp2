import os
import sys
import django
from collections import Counter
from datetime import timedelta
from django.utils import timezone
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","myp2.settings")
django.setup()

from post.models import Post,Trends

def extract_trends(text,trends):
    for word in text.split():
        if word[0]=='#':
            trends.append(word[1:])
    return trends

for trend in Trends.objects.all():
    trend.delete()

#posts=Post.objects.all()
trends=[]
this_hour=timezone.now().replace(minute=0,second=0,microsecond=0)
twenty_four_hours=this_hour-timedelta(hours=24)
print(Post.objects.filter(created_at__gte=twenty_four_hours))
for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    hashtags=extract_trends(post.body,trends)

trend_count=(Counter(trends)).most_common(10)

for trend in trend_count:
    Trends.objects.create(hashtag=trend[0],occurances=trend[1])

print(Trends.objects.all())