from django.contrib.postgres.operations import AddIndex
from django.contrib.postgres.indexes import GinIndex
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0010_previous_migration'), 
    ]
    operations = [
            AddIndex(
                model_name='Product',
                index=GinIndex(fields=['title'], name='product_title_gin_idx' , opclasses=['gin_trgm_ops'], ),
            ),]