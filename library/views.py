from rest_framework import generics


from .models import Book, BorrowedBook
from .serializers import BookIssuedSerializer, BookSerializer


class BookListAPI(generics.ListAPIView):

    def get_queryset(self):
        qs = Book.objects.all()
        book_status = self.request.query_params.get("status", None)

        if book_status == "available":
            qs = Book.objects.exclude(borrowed_books__status="issued")
        elif book_status == "issued":
            qs = BorrowedBook.objects.filter(status="issued")

        return qs
    
    def get_serializer_class(self):
        book_status = self.request.query_params.get("status", None)
        if book_status == "issued":
            return BookIssuedSerializer
        return BookSerializer
