"""The entry point of the backend.

First collects all odms, then starts the api.
"""


def collect_odms() -> None:
    pass


if __name__ == '__main__':
    collect_odms()

    import api.api as api
    api.start()
