from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse

from django_website.logger.managers import ChannelManager


class Channel(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    objects = ChannelManager()

    class Meta:
        db_table = "irc_channel"  # for backward compatibility

    def __unicode__(self):
        return self.name

    def clean_name(self):
        return self.name[0] == "#" and self.name[1:] or self.name

    def top_talkers(self, count=10):
        return Channel.objects.top_talkers(self, count)

    @models.permalink
    def get_absolute_url(self):
        return ("channel_detail", (), {"channel_name": self.clean_name()})


class Message(models.Model):
    channel = models.ForeignKey(Channel, db_index=True)
    nickname = models.CharField(max_length=19, db_index=True)
    text = models.TextField()
    is_action = models.BooleanField(default=False)
    logged = models.DateTimeField(default=datetime.now, db_index=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = "irc_message"  # for backward compatibility
        ordering = ("logged",)

    def __unicode__(self):
        return u"<%s> %s [%s]" % (self.nickname, self.text, self.logged)

    def get_absolute_url(self):
        return reverse("channel_detail_day", [], {
            'channel_name': self.channel.name,
            'year': self.logged.year,
            'month': self.logged.month,
            'day': self.logged.day,
        })
