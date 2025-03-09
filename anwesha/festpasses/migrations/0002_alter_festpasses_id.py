from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festpasses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festpasses',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
