from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


PROPERTY_CHOICES = [
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('studio', 'Studio'),
    ('flat', 'Flat'),
]
ROLE_CHOICES = [
    ('host', 'Host'),
    ('guest', 'Guest'),
    ('landlord', 'Landlord'),
]
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed')
]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(90), MinValueValidator(18)],
                                           null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='guest')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

class Property(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property')
    description = models.TextField()
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255, choices=PROPERTY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    rooms = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property'

    def __str__(self):
        return self.title




class Listings(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='listings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listings'

    def __str__(self):
        return f"Listing {self.id} - {self.property.title}"


class Bookings(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'bookings'

    def __str__(self):
        return f"{self.user.username} - {self.listing.property.title}  {self.status}"


class Reviews(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ('property', 'user')

    def __str__(self):
        return f"{self.property.title} - {self.rating}"




