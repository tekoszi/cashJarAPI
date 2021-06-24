from django.db import models

class Jar(models.Model):
    CURRENCY_CHOICES = [
        ('EUR', 'EURO'),
        ('USD', 'DOLLAR'),
        ('PLN', 'ZLOTY'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cash = models.FloatField(default=0)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='PLN',
    )

class Transaction(models.Model):
    jar = models.ForeignKey(Jar, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    cash = models.FloatField()