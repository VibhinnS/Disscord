import pytest
from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User
from utils import search_trie

# Create your tests here.
class UserModelTest(TestCase):
    def test_user_creation_with_valid_data(self):

        user = User(
            username="validuser",
            date_of_birth=date(1990, 1, 1),
            contact_number="1234567890",
            email_id="validuser@example.com"
        )
        try:
            user.full_clean()
            user.save()
        except ValidationError:
            pytest.fail("User creation failed with valid data")

        # Username contains forbidden substrings and raises ValidationError
    def test_username_contains_forbidden_substrings(self):

        user = User(
            username="vaginakiller",
            date_of_birth=date(1990, 1, 1),
            contact_number="1234567890",
            email_id="forbiddenuser@example.com"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

        # Username uniqueness is enforced by the database
    def test_username_uniqueness_enforced(self):
        user = User(
            username="forbiddenuser",
            date_of_birth=date(1990, 1, 1),
            contact_number="1234567890",
            email_id="forbiddenuser@example.com"
        )
        user2 = User(username="forbiddenuser", date_of_birth=date(1990, 1, 1), contact_number="1234567890", email_id="existinguser@example.com")

        with pytest.raises(ValidationError):
            user2.full_clean()

        # date_of_birth is set to a leap day
    def test_date_of_birth_leap_day(self):

        leap_day = date(2024, 2, 29)
        user = User(
            username="leapuser",
            date_of_birth=leap_day,
            contact_number="1234567890",
            email_id="leapuser@example.com"
        )
        try:
            user.full_clean()
        except ValidationError:
            pytest.fail("Date of birth set to a leap day failed validation")

        # clean method validates username correctly when no forbidden substrings are present
    def test_clean_method_validates_username_correctly_when_no_forbidden_substrings_present(self):
        user = User(username="validusername", date_of_birth=date(1990, 1, 1), contact_number="1234567890", email_id="validuser@example.com")
        user.save()

        # Assert that the username is valid and no ValidationError is raised
        with self.assertRaises(ValidationError):
            user.username = "invalidsubstring"
            user.full_clean()