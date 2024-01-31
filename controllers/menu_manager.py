from views.menu import Menu
from views.get_datas import GetDatas
from views.messages import Messages
from views.display import Display
from settings import SESSION
from controllers.permissions import Permissions
from controllers.crud_manager import CrudManager


class MenuManager:
    """Manages the main menu and submenus of the application"""
    def __init__(self, staff_user, token):
        """Initialize MenuManager"""
        self.token = token
        self.menu = Menu()
        self.messages = Messages()
        self.display = Display()
        self.get_datas = GetDatas()
        self.permissions = Permissions()
        self.crud = CrudManager(staff_user, token)
        self.staff_user = staff_user

    def choice_main_menu(self):
        """Displays the main menu and handles user choices"""
        option = self.menu.main_menu()
        if option == 1:
            self.choice_submenu("client")
        elif option == 2:
            self.choice_submenu("event")
        elif option == 3:
            self.choice_submenu("contract")
        elif option == 4:
            self.choice_submenu("staff")
        elif option == 5:
            SESSION.close()
            exit()

    def choice_submenu(self, table):
        """Displays the submenu for the specified table and handles user choices.

        Args:
            table (str): The table for which the submenu is displayed.
        """
        option = self.menu.submenu(table)

        if option == 1:
            # Read operation
            return_of_order = self.crud.read(table)
            if return_of_order == "display_ok" or return_of_order == "back":
                return self.choice_submenu(table)
            elif return_of_order == "close":
                SESSION.close()
                exit()

            else:
                self.messages.message_error(table, 3)
                return self.choice_main_menu()

        elif option == 2 or option == 3:
            # Create or update operation
            if option == 2:
                return_of_order = self.crud.create(table)
            elif option == 3:
                return_of_order = self.crud.update(table)

            if return_of_order == "creation_ok":
                self.messages.messages_ok(table, 1)
                return self.choice_main_menu()
            elif return_of_order == "update_ok":
                self.messages.messages_ok(table, 2)
                return self.choice_main_menu()
            elif return_of_order == "error":
                self.messages.message_error(table, 3)
                return self.choice_main_menu()
            elif return_of_order == "unknown_client":
                self.messages.message_error("client", 4)
                return self.choice_main_menu()
            elif return_of_order == "unknown_contract":
                self.messages.message_error("contract", 4)
                return self.choice_main_menu()
            elif return_of_order == "unknown_event":
                self.messages.message_error("event", 4)
                return self.choice_main_menu()
            elif return_of_order == "unknown_staff":
                self.messages.message_error("staff", 4)
                return self.choice_main_menu()
            elif return_of_order == "staff_not_support":
                self.messages.message_error("staff", 8)
                return self.choice_main_menu()
            elif return_of_order == "not_allowed":
                self.messages.message_error(table, 5)
                return self.choice_main_menu()
            elif return_of_order == "unsigned_contract":
                self.messages.message_error(table, 6)
                return self.choice_main_menu()
            elif return_of_order == "existing_event":
                self.messages.message_error(table, 7)
                return self.choice_main_menu()
            elif return_of_order == "Retour":
                return self.choice_submenu(table)
            elif return_of_order == "Fermer":
                SESSION.close()
                exit()

        elif option == 4 and table != "staff":
            # Delete operation
            return self.choice_main_menu()

        elif option == 4 and table == "staff":
            return_of_order = self.crud.delete(table)
            if return_of_order == "delete_ok":
                self.messages.messages_ok(table, 3)
                return self.choice_main_menu()
            elif return_of_order == "canceled":
                return self.choice_main_menu()

            elif return_of_order == "not_allowed":
                self.messages.message_error(table, 5)
                return self.choice_main_menu()
            elif return_of_order == "unknown_staff":
                self.messages.message_error("staff", 4)
                return self.choice_main_menu()
            else:
                self.messages.message_error(table, 3)
                return self.choice_main_menu()

        elif option == 5 and table != "staff":
            # Exit submenu or application
            SESSION.close()
            exit()

        elif option == 5 and table == "staff":
            return self.choice_main_menu()

        elif option == 6 and table == "staff":
            # Exit application
            SESSION.close()
            exit()
