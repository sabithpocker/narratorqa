from django.db import models

# Create your models here.
class Catalog(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    ministry_department = models.CharField(max_length=150,null=True,blank=True)
    state_department = models.CharField(max_length=150,null=True,blank=True)
    data_sets_actual_count = models.IntegerField(default=0)
    data_sets_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField('last updated')
    url = models.URLField(max_length=200)
    def __str__(self):
        return self.title


class Node(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    node = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    def __str__(self):
        return self.title
