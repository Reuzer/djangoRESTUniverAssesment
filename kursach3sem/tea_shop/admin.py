"""Admin panel configuration for TeaCategory and TeaProduct models."""

from import_export.admin import ExportMixin
from import_export import resources
from import_export.fields import Field
from django.contrib import admin
from .models import TeaCategory, TeaProduct


class TeaCategoryResource(resources.ModelResource):
    """Resource class for handling export operations related to TeaCategory."""

    custom_field = Field()

    class Meta:
        """Meta information for TeaCategoryResource."""
        model = TeaCategory

    def get_export_queryset(self, queryset, *args, **kwargs):
        """Filters categories containing 'Green' in their name."""
        return queryset.filter(name__icontains="Green")

    def dehydrate_custom_field(self, obj):
        """Adds a custom description to the exported data."""
        return f"{obj.name} - Custom Description: {obj.description[:20]}"


class TeaProductResource(resources.ModelResource):
    """Resource class for handling export operations related to TeaProduct."""

    price_with_tax = Field()

    class Meta:
        """Meta information for TeaProductResource."""
        model = TeaProduct

    def get_export_queryset(self, queryset, *args, **kwargs):
        """Filters products with stock greater than 0."""
        return queryset.filter(stock__gt=0)

    def dehydrate_price_with_tax(self, obj):
        """Calculates price with tax for the export."""
        return float(obj.price) * 1.2


@admin.register(TeaCategory)
class TeaCategoryAdmin(ExportMixin, admin.ModelAdmin):
    """Admin panel configuration for TeaCategory."""
    resource_class = TeaCategoryResource
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)


@admin.register(TeaProduct)
class TeaProductAdmin(ExportMixin, admin.ModelAdmin):
    """Admin panel configuration for TeaProduct."""
    resource_class = TeaProductResource
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    ordering = ('price',)
    fields = ('name', 'category', 'price', 'description', 'stock')
