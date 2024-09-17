# Generated by Django 5.1.1 on 2024-09-17 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('group', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('group', models.IntegerField()),
                ('win', models.PositiveSmallIntegerField()),
                ('draw', models.PositiveSmallIntegerField()),
                ('loss', models.PositiveSmallIntegerField()),
                ('point', models.PositiveSmallIntegerField()),
                ('point_alt', models.PositiveSmallIntegerField()),
                ('rank', models.PositiveSmallIntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_one', models.PositiveIntegerField()),
                ('goal_two', models.PositiveIntegerField()),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t1', to='backend.team')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t2', to='backend.team')),
            ],
        ),
    ]
