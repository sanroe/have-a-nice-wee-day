from app.app import create_app, talisman

app = talisman(create_app())

if __name__ == '__main__':
    app.run()