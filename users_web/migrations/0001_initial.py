# Generated for PR9 (equivalent to Django 5.2 makemigrations output).
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Организатор',
                'verbose_name_plural': 'Организаторы',
                'ordering': ['name', 'pk'],
            },
        ),
    ]
