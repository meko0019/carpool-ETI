# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-12 06:15
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('street', models.CharField(default='', max_length=255)),
                ('city', models.CharField(default='', max_length=100)),
                ('zipcode', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Carpool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('date', models.DateTimeField()),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_address', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(99999)])),
                ('full_address', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool.Trip')),
            ],
        ),
        migrations.AddField(
            model_name='carpool',
            name='start',
            field=models.ManyToManyField(related_name='carpool_start', to='carpool.Waypoint'),
        ),
        migrations.AddField(
            model_name='carpool',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpool.Trip'),
        ),
        migrations.AddField(
            model_name='carpool',
            name='waypoint',
            field=models.ManyToManyField(related_name='carpool_waypoint', to='carpool.Waypoint'),
        ),
    ]