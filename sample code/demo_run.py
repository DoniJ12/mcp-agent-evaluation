import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

here = os.path.dirname(__file__)
if here not in sys.path:
    sys.path.insert(0, here)

from user_service import get_user


def main():
    print("Fetch existing user (id=1):")
    print(get_user(1))

    print("Fetch missing user (id=2):")
    print(get_user(2))

    print("Demonstrate validation error:")
    try:
        get_user("bad_id")
    except Exception as e:
        print("Expected error:", type(e).__name__, e)


if __name__ == "__main__":
    main()
