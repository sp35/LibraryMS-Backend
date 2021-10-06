from django.contrib.auth.models import User
from django.db import models

import uuid


BORROWED_BOOK_STATUS_CHOICES = (
    ("requested", "requested"),
    ("issued", "issued"),
    ("denied", "denied"),
    ("returned", "returned"),
)

class Book(models.Model):
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    
    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.auth_user.username


class Librarian(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.auth_user.username


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    issuer = models.ForeignKey(Librarian, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=BORROWED_BOOK_STATUS_CHOICES, default="requested")

    class Meta:
        verbose_name = "Borrowed Book"
        verbose_name_plural = "Borrowed Books"

    def __str__(self) -> str:
        return f"Book: {self.book}, Borrower: {self.borrower}"
