from django.contrib import admin
from django.urls import path

from .views import BookIssueAPI, BookIssueRequestCreateAPI, BookListAPI, BookIssueRequestListAPI, BookReturnAPI, LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('books/', BookListAPI.as_view()),
    path('issue-requests/', BookIssueRequestListAPI.as_view()),
    path('create-issue-request/', BookIssueRequestCreateAPI.as_view()),
    path('issue/', BookIssueAPI.as_view()),
    path('return/', BookReturnAPI.as_view()),
]
