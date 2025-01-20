from django.core.management.base import BaseCommand
from tea_shop.models import TeaCategory, TeaProduct

class Command(BaseCommand):
    help = "Populate initial data for tea shop"

    def handle(self, *args, **kwargs):
        categories = ["Чёрный чай", "Зелёный чай", "Травяной чай", "Белый чай"]
        for category_name in categories:
            category, created = TeaCategory.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(f"Добавлена категория: {category_name}")
        
        products = [
            {"name": "Чёрный Ассам", "category": "Чёрный чай", "price": 150.00, "stock": 50},
            {"name": "Зелёный Сенча", "category": "Зелёный чай", "price": 200.00, "stock": 30},
            {"name": "Ромашковый чай", "category": "Травяной чай", "price": 100.00, "stock": 40},
        ]
        
        for product_data in products:
            category = TeaCategory.objects.get(name=product_data["category"])
            TeaProduct.objects.get_or_create(
                name=product_data["name"],
                category=category,
                price=product_data["price"],
                stock=product_data["stock"]
            )
            self.stdout.write(f"Добавлен продукт: {product_data['name']}")
