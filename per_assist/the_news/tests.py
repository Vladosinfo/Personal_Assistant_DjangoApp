from django.test import TestCase, Client
from django.urls import reverse
from .models import News


class NewsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_news_list_view(self):
        response = self.client.get(reverse('the_news:news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_news_detail_view(self):
        news = News.objects.create(title='Test News', content='Test content', category='general')
        response = self.client.get(reverse('the_news:news_detail', args=[news.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')
