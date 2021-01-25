# Generated by Django 3.1.5 on 2021-01-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('user_email', models.CharField(max_length=200)),
                ('up_price', models.FloatField(default=0)),
                ('low_price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.IntegerField(default=0)),
            ],
        ),
    ]
