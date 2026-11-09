from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('guests_web', '0001_initial')]
    operations = [
        migrations.AlterField(model_name='guest',
                              name='name', field=models.CharField(
                                  max_length=120, verbose_name='Имя')),
        migrations.AlterField(model_name='guest',
                              name='email', field=models.EmailField(
                                  max_length=254, verbose_name='Электронная почта')),
    ]
