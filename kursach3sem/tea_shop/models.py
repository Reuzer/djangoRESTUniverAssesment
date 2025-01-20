"""Model definitions for the Tea Shop application."""

from django.db import models
from simple_history.models import HistoricalRecords


class TeaCategory(models.Model):
    """Represents a category of tea products."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class TeaProduct(models.Model):
    """Represents a tea product."""
    name = models.CharField(max_length=100, verbose_name="Название чая")
    category = models.ForeignKey(
        TeaCategory, on_delete=models.CASCADE, related_name="products", verbose_name="Категория"
    )
    description = models.TextField(blank=True, verbose_name="Описание чая")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Represents a customer."""
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    email = models.EmailField(unique=True, verbose_name="Email")
    address = models.TextField(verbose_name="Адрес")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Номер телефона")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.name


class Order(models.Model):
    """Represents a customer order."""
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "В обработке"), ("completed", "Завершён"), ("canceled", "Отменён")],
        default="pending",
        verbose_name="Статус заказа"
    )

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer.name}"


class OrderItem(models.Model):
    """Represents an item in an order."""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ"
    )
    product = models.ForeignKey(
        TeaProduct, on_delete=models.CASCADE, related_name="order_items", verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Заказ #{self.order.id})"
