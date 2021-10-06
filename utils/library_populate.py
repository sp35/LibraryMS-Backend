from faker import Faker

import os
import django
import sys
sys.path.append("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_ms.settings")
django.setup()
from library.models import Book, Librarian, Student
from django.contrib.auth.models import User


faker = Faker()


for _ in range(50):
    Book.objects.get_or_create(
        name=faker.name()
    )
    profile = faker.profile()
    user, _ = User.objects.get_or_create(
        username=profile["username"]
    )
    Student.objects.get_or_create(
        auth_user=user
    )


for _ in range(2):
    profile = faker.profile()
    user, _ = User.objects.get_or_create(
        username=profile["username"]
    )
    Librarian.objects.get_or_create(
        auth_user=user
    )
