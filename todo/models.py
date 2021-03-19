from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name


class TodoList(models.Model):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    PRIORITY_LIST = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_LIST, default=MEDIUM)
    createdAt = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(
        Category, default="general", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return self.title
