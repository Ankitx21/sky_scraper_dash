from django.db import models


class Website(models.Model):
    name = models.URLField(unique=True)
    scraped_articles_24hrs = models.IntegerField(default=0)
    automation_running = models.BooleanField(default=False)
    source_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
