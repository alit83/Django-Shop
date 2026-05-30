from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0009_attributegroup_attribute_productattribute"),
    ]

    operations = [
        TrigramExtension(),
    ]
