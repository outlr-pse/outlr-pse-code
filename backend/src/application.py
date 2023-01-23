class Application:
    def start_api(self):
        from api.api import app
        app.run()


if __name__ == '__main__':
    Application().start_api()
