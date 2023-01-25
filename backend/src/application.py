def collect_odms() -> None:
    pass


def start_api() -> None:
    from api.api import app
    app.run()


if __name__ == '__main__':
    collect_odms()
    start_api()
