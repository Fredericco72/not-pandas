"""
Various utilities used within the Not-Pandas library
"""


def to_list(obj) -> list:
    """
    To make processing unified, we sometimes only want to deal with lists. This function
    takes any object and if it is not a list we encapsulate it within a list.

    ```
    print(to_list("abc"))
    # ["abc"]
    print(to_list([1, 2]))
    # [1, 2]
    ```
    """

    if isinstance(obj, list):
        return obj
    else:
        return [obj]


def to_tuple(obj) -> tuple:
    """
    To make processing unified, we sometimes only want to deal with tuples. This
    function takes any object and if it is not a tuple we encapsulate it within a tuple.

    ```
    print(to_tuple("abc"))
    # ("abc")
    print(to_tuple([1, 2]))
    # (1, 2)
    ```
    """

    if isinstance(obj, tuple):
        return obj
    else:
        return (obj,)
