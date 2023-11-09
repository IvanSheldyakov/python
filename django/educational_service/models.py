from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Now

class University(models.Model):
    name = models.CharField(max_length=70)
    short_name = models.CharField(max_length=10)
    foundation_date = models.DateField()

    def __str__(self):
        return self.short_name

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(foundation_date__lte=Now()),
                name='uni_constraint'
            )
        ]

class Student(models.Model):
    @staticmethod
    def current_year():
        return timezone.now().date().year

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    father_name = models.CharField(max_length=20)
    entrance_year = models.PositiveIntegerField(
        default=current_year,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(current_year)
        ]
    )
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="university"
    )

    def __str__(self):
        return f"{self.surname} {self.name} {self.father_name}, {self.entrance_year}, {self.university.short_name}"
