# Generated by Django 3.0.4 on 2020-03-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('api_key', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'api_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movieid', models.CharField(db_column='MovieID', max_length=10, primary_key=True, serialize=False)),
                ('movietitle', models.CharField(db_column='MovieTitle', max_length=30)),
                ('releasedate', models.DateField(db_column='ReleaseDate')),
                ('genereid', models.CharField(blank=True, db_column='GenereID', max_length=10, null=True)),
                ('directorid', models.CharField(blank=True, db_column='DirectorID', max_length=10, null=True)),
                ('imageurl', models.CharField(db_column='ImageUrl', max_length=250)),
                ('description', models.CharField(db_column='Description', max_length=250)),
            ],
            options={
                'db_table': 'movie',
                'managed': False,
            },
        ),
    ]
