from datetime import date, datetime


def is_weekday(date: datetime.date) -> bool:

    """
    This check function returns True if the passed date is a weekday.
    Uses the current day as default.

    Note
    ----
        datetime.date.weekday() returns: 5==Sat, 6==Sun
    """

    assert isinstance(
        date, datetime.date
    ), "Passed 'date' object is not a valid datetime.date object."

    if date.weekday() < 5:
        return True
    return False


def is_date_format_correct(func: callable):
    def func_wrapper(*args, **kwargs):

        if kwargs["date"]:
            pass

        # except Exception as e:

        #     print(e)
        #     return None

    return func_wrapper
