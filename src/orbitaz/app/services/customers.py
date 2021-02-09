from orbitaz.app.models.customer import Customer


def send_confirmation_email(customer: Customer) -> None:
    """ Logic to create confirmation emails """
    return


def create_profile(*, email: str, name: str) -> User:
    """ Logic to create customer profiles"""
    return Customer


def create_user(*, email: str, name: str) -> User:
    user = Customer(email=email)
    user.full_clean()
    user.save()

    create_profile(user=user, name=name)
    send_confirmation_email(user=user)

    return user