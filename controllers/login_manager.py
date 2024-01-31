from passlib.hash import argon2
from settings import SECRET, ALGORITHME, SESSION
import jwt
from datetime import datetime, timedelta, timezone
from controllers.menu_manager import MenuManager
from views.menu import Menu
from views.get_datas import GetDatas
from views.messages import Messages
from views.display import Display
from models.models import Staff


class AuthenticationAndPermissions:
    def __init__(self):
        """Initialize AuthenticationAndPermissions class"""
        self.menu = Menu()
        self.messages = Messages()
        self.get_datas = GetDatas()
        self.display = Display()

    def create_token(self, department):
        """Create a JWT token for the specified department.

        Args:
            department (str): The department for which the token is created.

        Returns:
            str: The encoded JWT token.
        """
        encoded_jwt = jwt.encode(
            {
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=1800),
                "department": department,
            },
            SECRET,
            algorithm=ALGORITHME,
        )
        return encoded_jwt

    def staff_user(self, email):
        """Retrieve staff user based on email.

        Args:
            email (str): Email of the staff user.

        Returns:
            Staff: The Staff object corresponding to the provided email.
        """
        return SESSION.query(Staff).filter(Staff.email == email).one_or_none()

    def check_password(self):
        """Check the password entered by the user and manage authentication.

        Returns:
            str: A string representing the result of the authentication attempt.
        """
        get_datas = GetDatas()
        self.display.log()
        email, password = get_datas.get_credentials()
        staff_user = self.staff_user(email)
        if staff_user is not None:
            password_user_hashed = staff_user.password
            if argon2.verify(password, password_user_hashed):
                department = staff_user.department.name
                token = self.create_token(department)
                menu_manager = MenuManager(staff_user, token)
                self.display.hello(staff_user.first_name)
                return menu_manager.choice_main_menu()
            else:
                self.messages.message_error(None, 1)
                return self.check_password()
        else:
            self.messages.message_error(None, 0)
            return self.check_password()
