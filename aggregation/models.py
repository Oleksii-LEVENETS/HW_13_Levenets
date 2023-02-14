from django.db import models
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def get_absolute_url(self):
        return reverse('aggregation:author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('aggregation:publisher-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def get_absolute_url(self):
        return reverse('aggregation:book-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    def get_absolute_url(self):
        return reverse('aggregation:store-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
