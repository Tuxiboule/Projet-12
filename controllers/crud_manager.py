from rich.prompt import Confirm
from models import repository
from controllers.permissions import Permissions
from views.menu import Menu
from views.display import Display
from views.get_datas import GetDatas


class CrudManager:
    def __init__(self, staff_user, token):
        """Initialize CrudManager class"""
        self.staff_user = staff_user
        self.token = token
        self.menu = Menu()
        self.display = Display()
        self.permissions = Permissions()
        self.get_datas = GetDatas()
        self.client_repository = repository.ClientRepository()
        self.contract_repository = repository.ContractRepository()
        self.event_repository = repository.EventRepository()
        self.staff_repository = repository.StaffRepository()

    def create(self, table):
        """Creates an entry in the specified table.

        Args:
            table (str): The name of the table where the entry will be created.

        Returns:
            str: A string indicating the outcome of the operation:
                - "creation_ok": If the entry creation was successful.
                - "unknown_client": If the client is unknown (applicable only for client table).
                - "error": If an error occurred during the operation.
                - "not_allowed": If the operation is not allowed based on permissions.
        """
        if self.permissions.permission_create(self.token, table):
            if table == "client":
                datas = self.get_datas.get_create_datas(table)
                try:
                    self.client_repository.create_client(datas, self.staff_user.id)
                    return "creation_ok"
                except:
                    return False

            elif table == "event":
                fullname = self.get_datas.get_fullname()
                client = self.client_repository.find_by_fullname(fullname)
                if client is None:
                    return "unknown_client"
                contract_id = self.get_datas.get_id("contract")
                contract = self.contract_repository.find_by_id(contract_id)
                if contract is None:
                    return "error"
                elif contract.status is False:
                    return "unsigned_contract"

                contracts_without_event = (self.contract_repository.get_all_contracts_without_event())
                if contract not in contracts_without_event:
                    return "existing_event"

                elif self.permissions.is_own_client(self.staff_user.id, client.id):
                    datas = self.get_datas.get_create_datas(table)
                    try:
                        self.event_repository.create_event(datas, client.id, contract.id)
                        return "creation_ok"
                    except:
                        return "error"
                else:
                    return "not_allowed"

            elif table == "contract":
                datas = self.get_datas.get_create_datas(table)
                try:
                    self.contract_repository.create_contract(datas)
                    return "creation_ok"
                except:
                    return "unknown_client"

            elif table == "staff":
                datas = self.get_datas.get_create_datas(table)
                try:
                    self.staff_repository.create_staff(datas)
                    return "creation_ok"
                except:
                    return "error"
        return "not_allowed"

    def read(self, table):
        """Reads data from the specified table.

        Args:
            table (str): The name of the table to read data from.

        Returns:
            str: A string indicating the outcome of the operation:
                - "display_ok": If the data display operation was successful.
                - "back": If the user chooses to go back to the previous menu.
                - "close": If the user chooses to close the current menu.
                - Other specific messages indicating the status of the operation.
        """
        option = self.menu.view_menu_read_only(table, self.staff_user)
        if self.permissions.check_token_validity(self.token):
            if table != "contract" and option == 5:
                return "back"

            elif table != "contract" and option == 6:
                return "close"

            elif table == "contract" and option == 7:
                return "back"

            elif table == "contract" and option == 8:
                return "close"

            elif table == "client":
                if option == 0:
                    clients = self.client_repository.get_all_their_clients(self.staff_user.id)
                    self.display.display_table(clients, table, all=True)
                    return "display_ok"

                if option == 1:
                    client = self.client_repository.get_all()
                    self.display.display_table(client, table, all=True)
                    return "display_ok"

                elif option == 2:
                    fullname = self.get_datas.get_fullname()
                    client = self.client_repository.find_by_fullname(fullname)
                    if client is not None:
                        self.display.display_table(client, table)
                        return "display_ok"

                elif option == 3:
                    id = self.get_datas.get_id(table)
                    client = self.client_repository.find_by_id(id)
                    if client is not None:
                        self.display.display_table(client, table)
                        return "display_ok"

                elif option == 4:
                    client_email = self.get_datas.get_email()
                    client = self.client_repository.find_by_email(client_email)
                    if client is not None:
                        self.display.display_table(client, table)
                        return "display_ok"

            elif table == "event":
                if option == 0:
                    event = self.event_repository.get_all_their_event(self.staff_user.id)
                    self.display.display_table(event, table, all=True)
                    return "display_ok"

                elif option == 1:
                    event = self.event_repository.get_all()
                    self.display.display_table(event, table, all=True)
                    return "display_ok"

                elif option == 2:
                    event = (self.event_repository.get_all_with_support_contact_none())
                    if event is not None:
                        self.display.display_table(event, table, all=True)
                        return "display_ok"

                elif option == 3:
                    id = self.get_datas.get_id(table)
                    event = self.event_repository.find_by_id(id)
                    if event is not None:
                        self.display.display_table(event, table)
                        return "display_ok"

                elif option == 4:
                    fullname_client = self.get_datas.get_fullname()
                    client = self.client_repository.find_by_fullname(fullname_client)
                    if client is not None:
                        event = self.event_repository.find_by_client(client.id)
                        if event is not None:
                            self.display.display_table(event, table, all=True)
                            return "display_ok"

            elif table == "contract":
                if option == 0:
                    contract = self.contract_repository.get_all()
                    self.display.display_table(contract, table, all=True)
                    return "display_ok"

                elif option == 1:
                    contract = (self.contract_repository.get_all_contracts_without_event())
                    self.display.display_table(contract, table, all=True)
                    return "display_ok"

                elif option == 2:
                    contract = self.client_repository.get_all_unsigned()
                    self.display.display_table(contract, table, all=True)
                    return "display_ok"

                elif option == 3:
                    contract = (self.contract_repository.get_all_with_positive_balance_due())
                    self.display.display_table(contract, table, all=True)
                    return "display_ok"

                elif option == 4:
                    client_id = self.get_datas.get_id("client")
                    client = self.client_repository.find_by_id(client_id)
                    if client is not None:
                        contract = self.contract_repository.find_by_client(client.id)
                        if contract is not None:
                            self.display.display_table(contract, table, all=True)
                            return "display_ok"

                elif option == 5:
                    id = self.get_datas.get_id(table)
                    contract = self.contract_repository.find_by_id(id)
                    if contract is not None:
                        self.display.display_table(contract, table)
                        return "display_ok"

                elif option == 6:
                    event_id = self.get_datas.get_id("event")
                    event = self.event_repository.find_by_id(event_id)
                    if event is not None:
                        contract_id = event.contract_id
                        contract = self.contract_repository.find_by_id(contract_id)
                        if contract is not None:
                            self.display.display_table(contract, table)
                            return "display_ok"

            elif table == "staff":
                if option == 1:
                    staff = self.staff_repository.get_all()
                    self.display.display_table(staff, table, all=True)
                    return "display_ok"

                if option == 2:
                    id = self.get_datas.get_id(table)
                    staff_member = self.staff_repository.find_by_id(id)
                    if staff_member is not None:
                        self.display.display_table(staff_member, table)
                        return "display_ok"

                if option == 3:
                    (name, first_name,) = self.get_datas.get_name_and_first_name_staff()
                    staff_member = (self.staff_repository.find_by_name_and_firstname(name, first_name))
                    if staff_member is not None:
                        self.display.display_table(staff_member, table)
                        return "display_ok"

                if option == 4:
                    email = self.get_datas.get_email()
                    staff_member = self.staff_repository.find_by_email(email)
                    if staff_member is not None:
                        self.display.display_table(staff_member, table)
                        return "display_ok"

    def update(self, table):
        """Updates an entry in the specified table.

        Args:
            table (str): The name of the table where the entry will be updated.

        Returns:
            str: A string indicating the outcome of the operation:
                - "update_ok": If the entry update was successful.
                - Various messages indicating reasons for failure or restrictions.
        """
        if table == "client":
            if (self.staff_user.department.name == "SUPPORT"
                or self.staff_user.department.name == "MANAGEMENT"):
                return "not_allowed"
            fullname = self.get_datas.get_fullname()
            client = self.client_repository.find_by_fullname(fullname)
            if client is not None:
                if self.permissions.permission_update(self.staff_user.id, client.id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    if (column_to_update == "Retour" or column_to_update == "Fermer"):
                        return column_to_update
                    else:
                        new_value = self.get_datas.get_new_value(column_to_update)
                        self.client_repository.update_client(client.id, column_to_update, new_value)
                        return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_client"

        elif table == "event":
            if self.staff_user.department.name == "COMMERCIAL":
                return "not_allowed"

            event_id = self.get_datas.get_id(table)
            event = self.event_repository.find_by_id(event_id)
            if event is not None:
                if self.permissions.permission_update(self.staff_user.id, event.id, self.token, table):
                    if self.staff_user.department.name == "SUPPORT":
                        column_to_update = self.menu.choice_column_to_update(table)
                        if (column_to_update == "Retour" or column_to_update == "Fermer"):
                            return column_to_update
                        else:
                            new_value = self.get_datas.get_new_value(column_to_update)
                            self.event_repository.update_event(event_id, column_to_update, new_value)
                            return "update_ok"
                    elif self.staff_user.department.name == "MANAGEMENT":
                        support_contact_id = (self.get_datas.get_support_contact())
                        staff_member_support = (self.staff_repository.find_by_id(support_contact_id))
                        if staff_member_support is None:
                            return "unknown_staff"
                        elif staff_member_support.department.name == "SUPPORT":
                            self.event_repository.update_event(event_id, "support_contact_id", support_contact_id,)
                            return "update_ok"
                        else:
                            return "staff_not_support"
                else:
                    return "not_allowed"
            else:
                return "unknown_event"

        elif table == "contract":
            if self.staff_user.department.name == "SUPPORT":
                return "not_allowed"
            contract_id = self.get_datas.get_id(table)
            contract = self.contract_repository.find_by_id(contract_id)
            client_id = contract.client_id
            if contract is not None:
                if self.permissions.permission_update(self.staff_user.id, client_id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    if (column_to_update == "Retour" or column_to_update == "Fermer"):
                        return column_to_update
                    else:
                        new_value = self.get_datas.get_new_value(column_to_update)
                        self.contract_repository.update_contract(contract.id, column_to_update, new_value)
                        return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_contract"

        elif table == "staff":
            if (self.staff_user.department.name == "COMMERCIAL" or self.staff_user.department.name == "SUPPORT"):
                return "not_allowed"
            name, first_name = self.get_datas.get_name_and_first_name_staff()
            staff_member = self.staff_repository.find_by_name_and_firstname(name, first_name)
            if staff_member is not None:
                if self.permissions.permission_update(self.staff_user.id, staff_member.id, self.token, table):
                    column_to_update = self.menu.choice_column_to_update(table)
                    if (column_to_update == "Retour" or column_to_update == "Fermer"):
                        return column_to_update
                    else:
                        new_value = self.get_datas.get_new_value(column_to_update)
                        print("new_value : ", new_value)
                        print("column_to_update : ", column_to_update)
                        self.staff_repository.update_staff(staff_member.id, column_to_update, new_value)
                        return "update_ok"
                else:
                    return "not_allowed"
            else:
                return "unknown_staff"

    def delete(self, table):
        """Deletes an entry from the specified table.

        Args:
            table (str): The name of the table where the entry will be deleted.

        Returns:
            str: A string indicating the outcome of the operation:
                - "delete_ok": If the entry deletion was successful.
                - "canceled": If the user cancels the deletion operation.
                - Various messages indicating reasons for failure or restrictions.
        """
        if (self.permissions.permission_create(self.token, table) and table == "staff"):
            staff_member_id = self.get_datas.get_id(table)
            staff_member = self.staff_repository.find_by_id(staff_member_id)

            if staff_member is not None:
                if Confirm.ask("Confirmer la suppression"):
                    self.staff_repository.delete_staff(staff_member)
                    return "delete_ok"
                else:
                    return "canceled"
            else:
                return "unknown_staff"
        return "not_allowed"
