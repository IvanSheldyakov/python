from django.db import migrations, models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Now
from django.utils import timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('short_name', models.CharField(max_length=10)),
                ('foundation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('father_name', models.CharField(max_length=20)),
                ('entrance_year', models.PositiveIntegerField(validators=[
                    MinValueValidator(0),
                    MaxValueValidator(timezone.now().year)  # Заменено на текущий год
                ])),
                ('university', models.ForeignKey(null=True, on_delete=models.SET_NULL, to='educational_service.university', verbose_name='university')),
            ],
        ),
        migrations.AddConstraint(
            model_name='university',
            constraint=models.CheckConstraint(check=models.Q(foundation_date__lte=Now()), name='uni_foundation_date_constraint'),
        ),
    ]
