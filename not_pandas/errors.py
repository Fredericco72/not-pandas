"""
Custom exception classes used within the Not-Pandas library
"""


class NotPandasError(Exception):
    """
    Common base class for all Non-Pandas exceptions
    """


class LengthError(NotPandasError):
    """
    Generic LengthError exception
    """
