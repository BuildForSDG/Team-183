import re


def validate_user_data(user):
    """this funtion validates the user data"""
    user = dict(user)
    user['username'] = user['username'].lower()

    if user['username'] == '':
        return {'warning': 'username is a required field'}, 200

    # Check for empty email
    elif user['email'] == '':
        return {'warning': 'email is a required field'}, 200

    # Check for empty password
    elif user['password'] == '':
        return {'warning': 'password is a required field'}, 200

    elif user['password'] == 'password':
        return {'warning': "password cannot be 'password'"}, 200

    elif user['password'].strip(' ').isdigit():
        return {'warning': 'password should be alphanumeric'}, 200

    elif user['password'] != user['confirm']:
        return {'warning': 'password mismatch!'}, 200

    # Check for a valid user name
    if not re.match(
        r'^[a-zA-Z0-9_.+-]+$',
            user['username'].strip(' ')):
        return {'warning': 'Enter a valid username'}, 200

    if user['username'].strip(' ').isdigit():
        return {'warning': 'Enter a non digit username'}, 200

    # Check for a valid email
    if not re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            user['email'].strip(' ')):
        return {'warning': 'Enter a valid email address'}, 200

    # check for a valid password
    if not user["password"].strip():
        return {"warning": "Enter a valid password"}, 200

    # Check for large/long inputs
    if len(user['username']) > 15:
        return {'warning': 'username is too long'}, 200

    elif len(user['email']) > 40:
        return {'warning': 'email is too long'}, 200

    elif len(user['password']) < 6:
        return {'warning': 'password requires atlest 6 characters'}, 200


def validate_reset_user_data(user):
    """this funtion validates the user data"""
    user = dict(user)
    # Check for empty password
    if user['password'] == '':
        return {'warning': 'password is a required field'}, 200

    elif user['password'] == 'password':
        return {'warning': "password cannot be 'password'"}, 200

    elif user['password'].strip(' ').isdigit():
        return {'warning': 'password should be alphanumeric'}, 200

    elif user['password'] != user['confirm']:
        return {'warning': 'password mismatch!'}, 200

    # Check for a valid email
    if not re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            user['email'].strip(' ')):
        return {'warning': 'Enter a valid email address'}, 200

    # check for a valid password
    if not user["password"].strip():
        return {"warning": "Enter a valid password"}, 200

    elif len(user['password']) < 6:
        return {'warning': 'password requires atlest 6 characters'}, 200
