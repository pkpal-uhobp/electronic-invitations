from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users_web', '0001_initial')]
    operations = [
        migrations.AlterField(model_name='user',
                              name='name', field=models.CharField(
                                  max_length=120, verbose_name='Имя')),
        migrations.AlterField(model_name='user',
                              name='email', field=models.EmailField(
                                  max_length=254, verbose_name='Электронная почта')),
    ]
