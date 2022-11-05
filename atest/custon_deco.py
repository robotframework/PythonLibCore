import functools


def custom_deco(arg1, arg2):
    print(arg1, arg2)

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("BEFORE")
            value = func(*args, **kwargs)
            print("AFTER")
            return value
        return wrapper
    return actual_decorator
