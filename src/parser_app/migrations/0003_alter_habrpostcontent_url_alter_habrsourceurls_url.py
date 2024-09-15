from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parser_app", "0002_urlhabrparser_is_enable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habrpostcontent",
            name="url",
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name="habrsourceurls",
            name="url",
            field=models.URLField(unique=True),
        ),
    ]
