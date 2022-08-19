from faker import Faker
from model_bakery.recipe import Recipe

from .models import User

fake = Faker('pt-BR')

user = Recipe(
    User,
    name=fake.name,
    email=fake.email,
)
