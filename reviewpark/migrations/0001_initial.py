# Generated by Django 4.1.1 on 2022-10-25 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stars', models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], help_text='Rate your expericence at WaterLand, from 1 to 5 stars')),
                ('feedback_text', models.TextField(help_text='Tell your experience here', max_length=300)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faq_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ask', models.TextField(help_text='Write your question here', max_length=300)),
                ('answare', models.TextField(default=None, help_text="Answare to the customer's question here", max_length=500, null=True)),
                ('answare_date', models.DateTimeField(default=None, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'FAQ',
            },
        ),
    ]
