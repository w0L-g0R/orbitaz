# https://rednafi.github.io/digressions/python/2020/03/26/python-contextmanager.html

from contextlib import contextmanager


# @contextmanager
# def errhandler():
#     try:
#         yield
#     except ZeroDivisionError:
#         print("This is a custom ZeroDivisionError message.")
#         raise
#     except TypeError:
#         print("This is a custom TypeError message.")
#         raise


# import logging
# from contextlib import contextmanager
# import traceback
# import sys

# logging.getLogger(__name__)

# logging.basicConfig(
#     level=logging.INFO,
#     format="\n(asctime)s [%(levelname)s] %(message)s",
#     handlers=[logging.FileHandler("./debug.log"), logging.StreamHandler()],
# )


# class Calculation:
#     """Dummy class for demonstrating exception decoupling with contextmanager."""

#     def __init__(self, a, b):
#         self.a = a
#         self.b = b

#     @contextmanager
#     def errorhandler(self):
#         try:
#             yield
#         except ZeroDivisionError:
#             print(
#                 f"Custom handling of Zero Division Error! Printing "
#                 "only 2 levels of traceback.."
#             )
#             logging.exception("ZeroDivisionError")

#     def main_func(self):
#         """Function that we want to save from nasty error handling logic."""

#         with self.errorhandler():
#             return self.a / self.b


# obj = Calculation(2, 0)
# print(obj.main_func())
