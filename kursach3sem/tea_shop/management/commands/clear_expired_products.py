from django.core.management.base import BaseCommand
from django.utils.timezone import now
from tea_shop.models import TeaProduct

class Command(BaseCommand):
    help = 'Clears expired tea products from the inventory'

    def handle(self, *args, **kwargs):
        expired_products = TeaProduct.objects.filter(stock=0)
        count = expired_products.count()
        expired_products.delete()
        self.stdout.write(self.style.SUCCESS(f'{count} expired products were deleted.'))