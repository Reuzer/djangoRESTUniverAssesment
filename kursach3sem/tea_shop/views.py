"""View definitions for the Tea Shop application."""

from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import TeaCategory, TeaProduct
from .serializers import TeaCategorySerializer, TeaProductSerializer


def main(request):
    """Renders the main page."""
    return render(request, 'tea_shop/main.html')


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination settings for API views."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class BaseModelViewSet(viewsets.ModelViewSet):
    """Base class to handle common ancestor limit."""

    pagination_class = StandardResultsSetPagination


class TeaCategoryViewSet(BaseModelViewSet):
    """API viewset for TeaCategory."""
    queryset = TeaCategory.objects.all()
    serializer_class = TeaCategorySerializer


class TeaProductViewSet(BaseModelViewSet):
    """API viewset for TeaProduct."""
    queryset = TeaProduct.objects.all()
    serializer_class = TeaProductSerializer

    @action(methods=['GET'], detail=False)
    def search(self, request):
        """Searches for tea products based on query parameters."""
        query = request.query_params.get('q', '')
        products = self.queryset.filter(Q(name__icontains=query))
        page = self.paginate_queryset(products)
        if page is not None:
            return self.get_paginated_response(
                self.serializer_class(page, many=True).data
            )
        return Response(self.serializer_class(products, many=True).data)

    @action(methods=['POST', 'GET'], detail=True)
    def reduce_stock(self, request, pk=None):
        """Reduces the stock of a product."""
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
            return Response({'status': 'stock reduced', 'remaining_stock': product.stock})
        return Response({'status': 'not enough stock'}, status=400)
    
    @action(methods=['GET'], detail=False)
    def filter_complex_one(self, request):
        """
        Complex filter using ~, &, and |.
        Returns products that:
        - Are not in stock (`~Q(stock=0)`),
        - And (have a price greater than 50 or name contains "premium").
        """
        products = self.queryset.filter(
            ~Q(stock=0) & (Q(price__gt=50) | Q(name__icontains="premium"))
        )
        return Response(self.serializer_class(products, many=True).data)

    @action(methods=['GET'], detail=False)
    def filter_complex_two(self, request):
        """
        Another complex filter using ~, &, and |.
        Returns products that:
        - has name
        - Or (are in stock and have a name containing "classic").
        """
        products = self.queryset.filter(
            ~Q(name='') | (Q(stock__gt=0) & Q(name__icontains="classic"))
        )
        return Response(self.serializer_class(products, many=True).data)

    @action(methods=['GET'], detail=False)
    def filter_by_price_range(self, request):
        """
        Filters products by price range.
        Returns products that:
        - Have a price between 20 and 200.
        """
        products = self.queryset.filter(Q(price__gte=20) & Q(price__lte=200))
        return Response(self.serializer_class(products, many=True).data)

    @action(methods=['GET'], detail=False)
    def filter_by_stock_and_category(self, request):
        """
        Filters products based on stock and category.
        Returns products that:
        - Are in stock and belong to a category containing 'Green'.
        """
        products = self.queryset.filter(
            Q(stock__gt=0) & Q(category__name__icontains="Зелёный")
        )
        return Response(self.serializer_class(products, many=True).data)

    @action(methods=['GET'], detail=False)
    def filter_not_in_stock_or_expensive(self, request):
        """
        Filters products that are either:
        - Not in stock,
        - Or have a price greater than 200.
        """
        products = self.queryset.filter(
            Q(stock=0) | Q(price__gt=200)
        )
        return Response(self.serializer_class(products, many=True).data)
