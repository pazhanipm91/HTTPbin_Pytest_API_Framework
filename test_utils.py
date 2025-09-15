from faker import Faker
import random

fake = Faker()

def generate_random_user_data():
    """
    Generates a dictionary with randomized user data using Faker.
    This is useful for POST, PUT, and PATCH requests.
    """
    return {
        "name": fake.name(),
        "address": fake.address(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "job": fake.job()
    }

def generate_random_string(length=10):
    """
    Generates a random string of a specified length.
    Useful for testing endpoints that accept dynamic string data.
    """
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(characters) for i in range(length))
