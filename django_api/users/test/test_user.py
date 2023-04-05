import pytest
from faker import Faker

from django_api.users.models.users import User

fake = Faker()

def test_example():
    assert 1 == 1

@pytest.mark.django_db
def test_user_create():
    User.objects.create_superuser(
        email='user@gmail.com', 
        password=fake.phone_number(),
        identification_number='123456789',
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    count = User.objects.all().count()
    print(count)
    assert count == 1