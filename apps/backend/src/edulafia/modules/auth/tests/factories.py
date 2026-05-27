import uuid

import factory

from edulafia.core.security import hash_password


class UserFactory(factory.AsyncFactory):
    class Meta:
        model = None  # Will be set to User model

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    phone = None
    password_hash = factory.LazyFunction(lambda: hash_password("TestPass123!"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = "school_admin"
    status = "active"
    school_id = factory.LazyFunction(uuid.uuid4)
    mfa_enabled = False
