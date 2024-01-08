from project import create_app

app = create_app()


# != production
def check_routes():
    all_routes = app.url_map.iter_rules()

    for route in all_routes:
        print(f"Endpoint: {route.endpoint}, Methods: {route.methods}, Path: {route.rule}")


if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', '80')
