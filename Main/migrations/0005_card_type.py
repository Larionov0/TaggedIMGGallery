# Generated by Django 4.2.3 on 2023-08-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_remove_tag_parents_tag_parent_alter_card_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='type',
            field=models.IntegerField(choices=[(1, 'image'), (2, 'video')], default=1),
        ),
    ]