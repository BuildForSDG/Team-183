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


def validate_profile_data(user_profile):
    """this funtion validates the user data"""
    user_profile = dict(user_profile)
    # Check for empty password
    if user_profile['first_name'] == '' or None:
        return {'warning': 'first_name is a required field'}, 200

    elif user_profile['last_name'] == '' or None:
        return {'warning': 'last_name is a required field'}, 200

    # elif user_profile['username'] == '' or None:
    #     return {'warning': 'username is a required field'}, 200

    elif user_profile['phone_number'] == '' or None:
        return {'warning': 'phone_number is a required field'}, 200

    elif user_profile['address'] == '' or None:
        return {'warning': 'address is a required field'}, 200

    elif user_profile['city'] == '' or None:
        return {'warning': 'password is a required field'}, 200

    elif user_profile['country'] == '' or None:
        return {'warning': 'country is a required field'}, 200

    elif user_profile['postal_code'] == '' or None:
        return {'warning': 'postal_code is a required field'}, 200

    elif user_profile['bio'] == '' or None:
        return {'warning': 'bio is a required field'}, 200

    elif user_profile['is_farmer'] == '' or None:
        return {'warning': 'user type is is_vendor or is_farmer is a required field'}, 200

    elif user_profile['is_vendor'] == '' or None:
        return {'warning': 'user type is is_vendor or is_farmer is a required field'}, 200

    elif user_profile['image_url'] == '' or None:
        return {'warning': 'image_url is a required field'}, 200

    # elif user_profile['password'] == '' or None:
    #     return {'warning': 'password is a required field'}, 200

    # elif user_profile['password'] == 'password':
    #     return {'warning': "password cannot be 'password'"}, 200

    # elif user_profile['password'].strip(' ').isdigit():
    #     return {'warning': 'password should be alphanumeric'}, 200

    # elif user['password'] != user['confirm']:
    #     return {'warning': 'password mismatch!'}, 200

    # # Check for a valid email
    # if not re.match(
    #     r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
    #         user['email'].strip(' ')):
    #     return {'warning': 'Enter a valid email address'}, 200

    # # check for a valid password
    # if not user["password"].strip():
    #     return {"warning": "Enter a valid password"}, 200

    # elif len(user['password']) < 6:
    #     return {'warning': 'password requires atlest 6 characters'}, 200
