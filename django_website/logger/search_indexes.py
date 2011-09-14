from haystack import indexes, site

from django_website.logger.models import Message


class MessageIndex(indexes.ModelSearchIndex):
    channel_name = indexes.CharField(model_attr='channel__name')
    channel_id = indexes.CharField(model_attr='channel__id')
    content = indexes.CharField(model_attr='text')

    class Meta:
        pass


site.register(Message, MessageIndex)
