from django.db import models


class Customer(models.Model):
    GENDER_TYPES = (
        ("m", "Male"),
        ("f", "Female"),
        ("n", "Not provided"),
    )

    STATUS_TYPES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("late", "Default of payment"),
        ("subscribed", "Subscribed, but no payment confirmation"),
    )

    ABO_TYPES = (
        ("premium", "API, Dashboard and report access"),
        ("api", "Only API access"),
        ("report", "Only report service"),
        ("dashboard", "Only dashboard access"),
    )

    gender = models.CharField(choices=GENDER_TYPES, max_length=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    telefon = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(choices=STATUS_TYPES, max_length=15)
    access = models.CharField(choices=ABO_TYPES, max_length=15)
