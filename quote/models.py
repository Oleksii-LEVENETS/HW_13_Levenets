from django.db import models
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    """Model representing an author of quote."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('quote:author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name} '


class Quote(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because quote can only have one author, but authors can have multiple quotes
    text = models.TextField(max_length=1000)

    class Meta:
        ordering = ['author', 'title']

    def get_absolute_url(self):
        return reverse('quote:quote-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
