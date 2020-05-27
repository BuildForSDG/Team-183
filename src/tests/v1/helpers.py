import json
# from flask_bcrypt import Bcrypt


def register_user(self):
    """helper function for registering a user."""
    return self.client.post(
        'api/v1/users/signup',
        data=json.dumps(dict(
            email='kamardaniel@gmail.com',
            username='kamar',
            password='password123',
            confirm='password123'
        )),
        content_type='application/json'
    )


def register_admin(self):
    """helper function for registering an admin user."""
    # username = 'admin'
    # email = 'kamardaniel1@gmail.com'
    # password = b'password123'
    # hash_password = Bcrypt().generate_password_hash(password).decode()
    # admin = True
