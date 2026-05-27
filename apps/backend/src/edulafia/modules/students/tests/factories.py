import uuid
from datetime import date, timedelta

import factory

from edulafia.modules.students.models import Student


class StudentFactory(factory.AsyncFactory):
    class Meta:
        model = Student

    id = factory.LazyFunction(uuid.uuid4)
    school_id = factory.LazyFunction(uuid.uuid4)
    admission_number = factory.Sequence(lambda n: f"EDU/2024/{n:04d}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_of_birth = factory.LazyFunction(
        lambda: date.today() - timedelta(days=365 * 14)
    )
    gender = factory.Iterator(["male", "female"])
    status = "active"
    admission_date = factory.LazyFunction(lambda: date.today() - timedelta(days=30))
    nationality = "Nigerian"
