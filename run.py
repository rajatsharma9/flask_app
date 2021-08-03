from app import create_app # noqa


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
