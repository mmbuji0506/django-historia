from django.db import models

class HistoricalEvent(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    event_description = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    search_query = models.CharField(max_length=255, null=True, blank=True) #add search query

    def __str__(self):
        return f"Event at ({self.latitude}, {self.longitude})"