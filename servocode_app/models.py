from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[MinValueValidator(-90),MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180),MaxValueValidator(180)])
    address = models.CharField(max_length=300,null=True)

    def __str__(self):
        return 'name: {}, latitude: {}, longitude: {}'.format(self.name, self.latitude, self.longitude)
