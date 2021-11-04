from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Question

class LatestQuestionsFeed(Feed):
    title = "Hoesung's Blog"
    link = '/board/'
    description = 'New Post'

    def items(self):
        return Question.objects.order_by("-create_date")[:2]

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('pybo:detail', args=[item.pk])


