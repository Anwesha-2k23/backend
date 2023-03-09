# Generated by Django 4.1.5 on 2023-03-05 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_events_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayUTxn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mihpayid', models.CharField(blank=True, max_length=100, null=True)),
                ('mode', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('txnid', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('addedon', models.CharField(blank=True, max_length=100, null=True)),
                ('productinfo', models.CharField(blank=True, max_length=100, null=True)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('field1', models.CharField(blank=True, max_length=100, null=True)),
                ('field2', models.CharField(blank=True, max_length=100, null=True)),
                ('field3', models.CharField(blank=True, max_length=100, null=True)),
                ('field4', models.CharField(blank=True, max_length=100, null=True)),
                ('field5', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='payment_key',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='events',
            name='payment_link',
            field=models.URLField(blank=True),
        ),
    ]