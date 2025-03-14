from django.db import models
from users.models import CustomUser


class NamedModel(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(NamedModel):
    class Meta:
        verbose_name_plural = 'Categories'


class Brand(NamedModel):
    pass


class Discount(NamedModel):
    start_date = models.DateField()
    exp_date = models.DateField()
    percent = models.PositiveIntegerField()


class Promo(NamedModel):
    percent = models.PositiveIntegerField()
    is_cumulative = models.BooleanField(default=False)


class Product(models.Model):
    name = models.CharField(max_length=500)
    article = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField(null=True, blank=True)
    stock_amount = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    discount = models.ManyToManyField(Discount)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.article}: {self.name}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image for {self.product}'


class Cashback(models.Model):
    percent = models.PositiveIntegerField()
    limit = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.percent}'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True, blank=True)


class Order(models.Model):
    STATUSES = (
        ('In process', 'In process'),
        ('On the way', 'On the way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Received', 'Received')
    )

    PAYMENT_STATUSES = (
        ('Waiting', 'Waiting'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled')
    )

    DELIVERY_METHODS = (
        ('Courier', 'Courier'),
        ('Post', 'Post'),
        ('Self-delivery', 'Self-delivery')
    )

    NOTIFICATION_OPTIONS = (
        (24, 24),
        (6, 6),
        (1, 1)
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUSES, default='In process')
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUSES, default='Waiting')
    delivery_method = models.CharField(max_length=100, choices=DELIVERY_METHODS, default='Self-delivery')
    notification_time = models.PositiveIntegerField(choices=NOTIFICATION_OPTIONS, default=1)
    is_notif_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}: {self.user.email}'


class OrderProductsM2M(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
