from django.db import models

class Sermons(models.Model):
    title = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)
    book = models.TextField()
    speaker = models.TextField(blank=True, null=True)
    square_url = models.TextField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    duration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sermons'