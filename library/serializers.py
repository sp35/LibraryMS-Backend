from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Book, BorrowedBook, Student

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("static_id", "name")


class BookIssuedSerializer(serializers.ModelSerializer):

    book = BookSerializer()

    class Meta():
        model = BorrowedBook
        fields = ("book", "borrower", "issuer")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        book = data.pop("book")
        for field in book:
            data[field] = book[field]
        data["borrower"] = instance.borrower.auth_user.username
        data["issuer"] = instance.issuer.auth_user.username
        return data
