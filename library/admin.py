from django.contrib import admin

from .models import Book, BorrowedBook, Librarian, Student


admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(BorrowedBook)
