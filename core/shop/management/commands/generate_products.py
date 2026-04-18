import random
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Product , ProductStatus , ProductImage , ProductCategory
from django.utils.text import slugify
from accounts.models import  User , UserType

cat_list =[
    'ps5',
    'xbox',
    'لوازم جانبی ساعت هوشمند',
    'ساعت هوشمند سامسونگ',
]
class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        fake=Faker(locale="fa_IR")
        user_obj = User.objects.get(type=UserType.admin.value)
        categories = ProductCategory.objects.filter(title__in =cat_list )
        images = ProductImage.objects.all()
        for _ in range(10):
            user=user_obj
            number= random.randint(1,3)
            selected_categories=(list(categories))[number]
            selected_images=random.sample(list(images),number)
            title=fake.word()
            slug=slugify(title,allow_unicode=True)
            description = fake.paragraph(nb_sentences=10)
            brief_description= fake.paragraph(nb_sentences=1)
            stock= fake.random_int(min=0,max=10)
            status= random.choice(ProductStatus.choices)[0]
            price = fake.random_int(min=100000,max=10000000)
            discount_percent = fake.random_int(min=0,max=60)
            product_obj = Product.objects.create(
                user=user,
                title=title,
                slug=slug,
                category=selected_categories,
                description=description,
                 brief_description= brief_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent
            )
            product_obj.image.set(selected_images)
        self.stdout.write(self.style.SUCCESS(
            'successfully generated fake products'
        ))