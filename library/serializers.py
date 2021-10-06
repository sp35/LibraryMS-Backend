from django.core.exceptions import ValidationError as DVE
from rest_framework import serializers

from .models import Book, BorrowedBook, Student

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("static_id", "name")
        read_only_fields = ("name",)


class StudentSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ("static_id", "username")
        read_only_fields = ("username",)
    
    def get_username(self, instance):
        return instance.auth_user.username


class LibrarianSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ("static_id", "username")
        read_only_fields = ("username",)
    
    def get_username(self, instance):
        return instance.auth_user.username


class BookIssuedSerializer(serializers.ModelSerializer):

    book = BookSerializer()
    borrower = StudentSerializer()
    issuer = LibrarianSerializer()

    class Meta():
        model = BorrowedBook
        fields = ("book", "borrower", "issuer", "static_id")


class BookRequestSerializer(serializers.Serializer):

    book_static_id = serializers.UUIDField(write_only=True)

    class Meta():
        fields = ("book_static_id",)
    
    def create(self, validated_data):
        book_qs = Book.objects.filter(static_id=validated_data["book_static_id"])
        borrower_qs = Student.objects.filter(auth_user=self.context["request"].user)
        if not book_qs.exists():
            raise serializers.ValidationError("Book doesn't exist")
        if not borrower_qs.exists():
            raise serializers.ValidationError("Borrower doesn't exist")
        try:
            return BorrowedBook.objects.create(
                book=book_qs[0],
                borrower=borrower_qs[0]
            )
        except DVE as e:
            raise serializers.ValidationError(str(e))

