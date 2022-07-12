"""Helper functions for tests"""
from main.models import User


def create_test_user(username="test_user", password="pass"):
    """Create a user

    Parameters
    ----------
    username : str
    password : str

    Returns
    -------
    User
    """
    return User.objects.create_user(username=username, password=password)
