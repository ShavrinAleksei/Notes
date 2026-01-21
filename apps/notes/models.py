from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='notes',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'owner')

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    class Meta:
        unique_together = ('name', 'owner')
    
    def __str__(self):
        return self.name

