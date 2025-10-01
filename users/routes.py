from flask import Blueprint, request, jsonify, make_response
from users.schemas import UserSchema
from users.services import (create_user,
                            get_user_by_id,
                            get_user_by_email,
                            delete_user,
                            update_user,
                            get_all_users_count,
                            get_all_users,
                            authenticate_user
                            )

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/create-user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    schema = UserSchema()
    errors = schema.validate(data)
    if errors:
        print(errors.items())
        return jsonify(errors=errors), 400
    try:
        user = create_user(data['email'], data['password'])
        return jsonify({"id": user.id, "email": user.email}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@bp.route('/get-user-by-id', methods=['GET'])
def get_user_by_id_route():
    user = get_user_by_id(request.args.get('id'))
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({"id": user.id, "email": user.email}), 200

@bp.route('/get-user-by-email', methods=['GET'])
def get_user_by_email_route():
    user = get_user_by_email(request.args.get('email'))
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({"id": user.id, "email": user.email}), 200


@bp.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    delete_user(user)
    return jsonify({"message": f"User {user_id} deleted"})

@bp.route('/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    updated_user = update_user(user, data.get("email"), data.get("password"))
    return jsonify({"message": f"User {updated_user.id} updated"})

@bp.route('/get-users-count', methods=['GET'])
def get_users_count_route():
    answer = get_all_users_count()
    return jsonify({"count": answer}), 200

@bp.route('/get-all-users', methods=['GET'])
def get_all_users_route():
    users = get_all_users()
    return jsonify([{"id":u.id,"email":u.email} for u in users]), 200

@bp.route('/auth', methods=['POST'])
def auth_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 401

    result = authenticate_user(email, password)
    if not result:
        return jsonify({"error": "Invalid email or password"}), 401
    user, token = result

    response = make_response(jsonify({"message":"Login successful","id":user.id,"email":user.email}))
    response.set_cookie(
        "token",
        token,
        httponly=True,
        secure= False,
        samesite="Strict",
        max_age=60*15,
    )
    return response

