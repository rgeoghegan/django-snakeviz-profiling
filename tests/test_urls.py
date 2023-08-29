from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import path


def test_view(_request):
    return HttpResponse(f"There are {User.objects.all().count()} users.")


urlpatterns = [
    path(r"view", test_view),
]
