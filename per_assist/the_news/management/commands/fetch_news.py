import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from the_news.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        api_key = settings.API_KEY
        categories = 'business,science,politics'
        limit = 10

        url = f'https://api.thenewsapi.com/v1/news/all?api_token={api_key}&categories={categories}&limit={limit}&language=en'
        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()
            for item in data['data']:
                title = item['title']
                # content = item['description']
                category = ", ".join(item['categories'])
                category = item['categories'][0]
                url = item["url"]
                published_date = item['published_at']


                News.objects.create(title=title, content=content, category=category, url=url, published_date=published_date)
            self.stdout.write(self.style.SUCCESS('News fetched successfully'))
        else:
            self.stdout.write(self.style.ERROR(f'Error fetching news: {response.status_code}'))
