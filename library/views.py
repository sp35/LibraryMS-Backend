from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework.exceptions import ValidationError

from library.permissions import IsLibrarian, IsStudent
from .models import Book, BorrowedBook, Librarian, Student
from .serializers import BookIssuedSerializer, BookRequestSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_type = request.data.get("choice")
        username = request.data.get("username")
        password = request.data.get("password")

        model = None

        if user_type == "librarian":
            model = Librarian
        elif user_type == "student":
            model = Student
        else:
            raise ValidationError("Invalid `user_type` (student or librarian)")

        qs = model.objects.filter(auth_user__username=username)
        if not qs.exists():
            return Response({"message": f"No such {user_type}.", "status": 0})
        if qs[0].auth_user.check_password(password):
            refresh = RefreshToken.for_user(qs[0].auth_user)
            return Response({
                'token': str(refresh.access_token), "status": 1
            })
        else:
            return Response({
                'message': "Incorrect credentials", "status": 0
            })


class BookListAPI(generics.ListAPIView):

    permission_classes = (IsAuthenticated, IsStudent|IsLibrarian,)

    def get_permissions(self):
        book_status = self.request.query_params.get("status", None)
        if book_status == "issued":
            return (IsAuthenticated(), IsLibrarian(),)
        return super().get_permissions()

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


class BookIssueRequestListAPI(generics.ListAPIView):
    queryset = BorrowedBook.objects.filter(status="requested")
    serializer_class = BookIssuedSerializer
    permission_classes = (IsAuthenticated, IsLibrarian)


class BookIssueRequestCreateAPI(generics.CreateAPIView):
    serializer_class = BookRequestSerializer
    permission_classes = (IsAuthenticated, IsStudent)


class BookIssueAPI(APIView):
    permission_classes = (IsAuthenticated, IsLibrarian)
    
    def post(self, request):
        qs = BorrowedBook.objects.filter(static_id=self.request.query_params.get("static_id"), status="requested")
        if qs.exists():
            status = request.data.get("status", None)
            if status == "issued" or status == "denied":
                # checks
                instance = qs[0]
                instance.status = status
                instance.issuer = Librarian.objects.get(auth_user=request.user)
                instance.save()
            else:
                raise ValidationError("Invalid `status` for book issue")
            return Response({"message": "Issue request updated", "status": 1})
        else:
            return Response({"message": "No such book requested", "status": 0})


class BookReturnAPI(APIView):
    permission_classes = (IsAuthenticated, IsStudent)
    
    def post(self, request):
        qs = BorrowedBook.objects.filter(static_id=self.request.query_params.get("static_id"), status="issued")
        if qs.exists():
            # checks
            instance = qs[0]
            if instance.status == "returned":
                return Response({"message": "Book already returned", "status": 0})
            instance.status = "returned"
            instance.save()
            return Response({"message": "Book return success", "status": 1})
        else:
            return Response({"message": "No such book issued", "status": 0})
