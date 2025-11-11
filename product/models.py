from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('kitchen', 'Kitchen & Home'),
        ('beauty', 'Beauty & Personal Care'),
        ('sports', 'Sports & Fitness'),
        ('books', 'Books'),
        ('others', 'Others'),
        ('slippers', 'Slippers'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others')
    custom_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    def __str__(self):
        return self.name
