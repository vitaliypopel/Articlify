from flask import Blueprint, request, jsonify, make_response

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/change-theme', methods=['POST'])
def change_theme():
    response = make_response(jsonify())
    req = request.get_json()

    if req:
        theme = req['theme']
        response.set_cookie('theme', theme)
    else:
        return response, 400

    return response, 200
