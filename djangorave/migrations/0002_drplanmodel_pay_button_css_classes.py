# Generated by Django 3.1.4 on 2020-12-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangorave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drplanmodel',
            name='pay_button_css_classes',
            field=models.CharField(blank=True, help_text='css classes to be applied to pay button in template.', max_length=200, null=True),
        ),
    ]