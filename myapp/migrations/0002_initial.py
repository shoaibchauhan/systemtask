# Generated by Django 5.1.4 on 2024-12-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=255)),
                ('process_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('pid', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'indexes': [models.Index(fields=['system_name', 'timestamp'], name='myapp_proce_system__88504b_idx'), models.Index(fields=['pid'], name='myapp_proce_pid_4e6896_idx')],
            },
        ),
    ]
