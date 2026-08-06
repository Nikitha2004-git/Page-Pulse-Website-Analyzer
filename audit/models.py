from django.db import models


class WebsiteAnalysis(models.Model):

    url = models.URLField()

    title = models.CharField(max_length=300)

    seo_score = models.IntegerField()

    status_code = models.IntegerField()

    response_time = models.CharField(max_length=30)

    word_count = models.IntegerField()

    total_links = models.IntegerField()

    total_images = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url