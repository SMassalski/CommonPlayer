from main.models import User


def create_test_user(username="test_user", password="pass"):
    return User.objects.create_user(username=username, password=password)
