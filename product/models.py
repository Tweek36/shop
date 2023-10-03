from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название категории')

    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название атрибута')
    units = models.CharField(max_length=10, blank=True, null=True, verbose_name='Единицы измерения')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['name', 'category'], name='unique_attribute')
        ]

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество в наличии')
    image = models.ImageField(upload_to='products/', default='img\default.jpg', verbose_name='Изображение товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    attributes = models.ManyToManyField(Attribute, through='ProductAttribute', verbose_name='Атрибуты товара')

    def __str__(self):
        return self.title
    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='Атрибут')
    value = models.CharField(max_length=255, verbose_name='Значение атрибута')

    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['product', 'attribute'], name='unique_product_attribute')
        ]

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='Родительский комментарий')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Комментарий от {self.user.username} к товару {self.product.title}"

    def delete(self, *args, **kwargs):
        if not self.parent:
            Comment.objects.filter(parent=self).delete()
        super().delete(*args, **kwargs)