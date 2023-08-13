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
    start_chapter = models.IntegerField()
    end_chapter = models.IntegerField()
    start_verse = models.IntegerField()
    end_verse = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sermons'