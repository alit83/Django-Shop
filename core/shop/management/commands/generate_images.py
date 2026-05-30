from django.core.management.base import BaseCommand
from shop.models import ProductImage
from django.core.files import File
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Command(BaseCommand):
    help = "Generate fake categories"

    def handle(self, *args, **options):
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
        ]

        for i in range(8):
            file = File(
                file=open(BASE_DIR / image_list[i], "rb"),
                name=Path(image_list[i]).name,
            )
            ProductImage.objects.get_or_create(file=file)
        self.stdout.write(
            self.style.SUCCESS("successfully generated fake images")
        )
