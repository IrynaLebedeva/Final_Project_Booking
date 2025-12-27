import os
from datetime import timedelta

import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory import fuzzy

from booking.models import (
    User,
    Reviews,
    Property,
    Listings,
    Bookings,
    ROLE_CHOICES,
    PROPERTY_CHOICES,
    STATUS_CHOICES
)

faker_ = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: faker_.unique.user_name())
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@gmail.com")
    # email = factory.Factory('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    age = factory.Faker('pyint', min_value=18, max_value=90)
    # role = factory.LazyAttribute(lambda _: random.choice([
    role = factory.LazyFunction(lambda: random.choice([choice[0] for choice in ROLE_CHOICES]))
    is_active = True
    is_staff = False
    date_joined = factory.LazyFunction(timezone.now)
    password = factory.LazyFunction(lambda: make_password('qwerty123456'))


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Property

    title = factory.Faker('sentence', nb_words=4)
    owner = factory.SubFactory(UserFactory)
    description = factory.Faker('text', max_nb_chars=300)
    city = factory.Faker('city')
    # location = factory.LazyAttribute(lambda  obj: f"{obj.country}, {obj.city}, {obj.street}")
    location = factory.LazyAttribute(lambda obj: f"{obj.city}, {faker_.street_address()}")
    property_type = factory.LazyFunction(lambda: random.choice([choice[0] for choice in PROPERTY_CHOICES]))
    price = fuzzy.FuzzyInteger(300, 500)
    rooms = fuzzy.FuzzyInteger(1,10)


class ListingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listings

    property = factory.SubFactory(PropertyFactory)
    user = factory.SubFactory(UserFactory, role=factory.LazyFunction(lambda: random.choice(['host', 'landlord'])))
    # user = factory.LazyAttribute("property.owner")
    active = True
    # active = factory.LazyAttribute(lambda: random.choice([True, False]))


class BookingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookings

    listing = factory.SubFactory(ListingsFactory)
    user = factory.SubFactory(UserFactory, role='guest')
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyAttribute(lambda  obj: obj.start_date+timedelta(days=random.randint(1,30)))
    status = factory.LazyFunction(lambda: random.choice([choice[0] for choice in STATUS_CHOICES]))


class ReviewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reviews

    property = factory.SubFactory(PropertyFactory)
    user = factory.SubFactory(UserFactory, role='guest')
    rating = fuzzy.FuzzyInteger(1,10)
    comment = factory.Faker('text', max_nb_chars=600)


if __name__ == '__main__':
    print("!!!!   HERE WE GO   !!!!")
    UserFactory.create_batch(15)
    PropertyFactory.create_batch(25)
    ListingsFactory.create_batch(20)
    BookingsFactory.create_batch(35)
    ReviewsFactory.create_batch(30)
    print("!!!!       DONE     !!!!")




