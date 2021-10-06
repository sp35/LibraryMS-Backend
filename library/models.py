from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.auth_user.username


class Librarian(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.auth_user.username


class BorrowedBook(models.Model):
    static_id = models.UUIDField(default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, related_name="borrowed_books", on_delete=models.CASCADE)
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    issuer = models.ForeignKey(Librarian, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=16, choices=BORROWED_BOOK_STATUS_CHOICES, default="requested")

    class Meta:
        verbose_name = "Borrowed Book"
        verbose_name_plural = "Borrowed Books"
    
    def clean(self) -> None:
        if self.status == "issued":
            if BorrowedBook.objects.filter(book=self.book, status=self.status).count() >= 1:
                raise ValidationError("Book has already been issued")
        if self.status == "requested":
            if BorrowedBook.objects.filter(book=self.book, borrower=self.borrower, status=self.status).count() >= 1:
                raise ValidationError("You have already created an issue request for this book")
        return super().clean()

    def __str__(self) -> str:
        return f"Book: {self.book}, Borrower: {self.borrower}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
