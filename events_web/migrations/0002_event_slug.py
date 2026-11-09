from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('events_web', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='event', name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=180,
                                   null=True, unique=True, verbose_name='URL-идентификатор'),
        ),
        migrations.AlterField(
            model_name='event', name='name',
            field=models.CharField(max_length=200, verbose_name='Название события'),
        ),
        migrations.AlterField(
            model_name='event', name='date',
            field=models.DateField(db_index=True, verbose_name='Дата проведения'),
        ),
        migrations.AlterField(
            model_name='event', name='user',
            field=models.ForeignKey(blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL, related_name='events',
                to='users_web.user', verbose_name='Организатор'),
        ),
    ]
