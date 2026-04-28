from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Brand(models.Model):

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Flavor(models.Model):

    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Chips(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    flavors = models.ManyToManyField(Flavor)
    image = models.ImageField(upload_to='chips_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0
        return sum(review.rating for review in reviews) / reviews.count()


class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    chips = models.ForeignKey(Chips, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.chips.price * self.quantity


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Review(models.Model):
    chips = models.ForeignKey(Chips, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.chips.name} by {self.author}"