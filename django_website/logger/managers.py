from django.db import models

class ChannelManager(models.Manager):

    def top_talkers(self, channel, count=10):
        """
        Returns a list of dicts containing nickname and message counts
        for the top talkers in the given channel.
        """
        return channel.message_set.all().annotate(
            message_count=models.Count('id'),
        ).values(
            "nickname", "message_count",
        ).order_by("-message_count")[0:count]
