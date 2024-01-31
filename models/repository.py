import logging
from settings import SESSION
from .models import Client, Event, Contract, Staff


class ClientRepository:
    """
    Repository class for handling operations related to clients in the database.
    """
    def find_by_fullname(self, fullname):
        return (SESSION.query(Client).filter(Client.fullname == fullname).one_or_none())

    def find_by_id(self, id):
        return SESSION.query(Client).filter(Client.id == id).one_or_none()

    def find_by_email(self, email):
        return SESSION.query(Client).filter_by(email=email).one_or_none()

    def get_all(self):
        return SESSION.query(Client).all()
    
    def get_all_their_clients(self, staff_member_id):
        return SESSION.query(Client).filter_by(commercial_contact_id=staff_member_id)

    def create_client(self, datas, staff_id):
        client = Client(
            fullname=datas["fullname"],
            email=datas["email"],
            phone=datas["phone"],
            name_company=datas["name_company"],
            commercial_contact_id=staff_id,
        )
        SESSION.add(client)
        SESSION.commit()

    def update_client(self, client_id, column, new_value):
        client = SESSION.query(Client).filter_by(id=client_id).one_or_none()
        if column == "fullname":
            client.fullname = new_value
        if column == "email":
            client.email = new_value
        if column == "phone":
            client.phone = new_value
        if column == "name_company":
            client.name_company = new_value
        SESSION.commit()


class EventRepository:
    """
    Repository class for handling operations related to events in the database.
    """
    def find_by_name(self, name):
        return SESSION.query(Event).filter(Event.name == name).one_or_none()

    def find_by_id(self, id):
        return SESSION.query(Event).filter(Event.id == id).one_or_none()

    def find_by_client(self, client_id):
        return SESSION.query(Event).filter_by(client_id=client_id).all()

    def get_all(self):
        return SESSION.query(Event).all()

    def get_all_with_support_contact_none(self):
        return SESSION.query(Event).filter_by(support_contact_id=None)

    def get_all_their_event(self, staff_member_id):
        return SESSION.query(Event).filter_by(
            support_contact_id=staff_member_id
        )

    def create_event(self, datas, client_id, contract_id):
        event = Event(
            name=datas["name"],
            contract_id=contract_id,
            client_id=client_id,
            event_date_start=datas["event_date_start"],
            event_date_end=datas["event_date_end"],
            location=datas["location"],
            attendees=datas["attendees"],
            notes=datas["notes"],
        )
        SESSION.add(event)
        SESSION.commit()

    def update_event(self, event_id, column, new_value):
        event = SESSION.query(Event).filter_by(id=event_id).one_or_none()
        if column == "name":
            event.name = new_value
        elif column == "contract_id":
            event.contract_id = new_value
        elif column == "client_id":
            event.client_id = new_value
        elif column == "support_contact_id":
            event.support_contact_id = new_value
        elif column == "event_date_start":
            event.event_date_start = new_value
        elif column == "event_date_end":
            event.event_date_end = new_value
        elif column == "location":
            event.location = new_value
        elif column == "attendees":
            event.attendees = new_value
        elif column == "notes":
            event.notes = new_value

        SESSION.commit()


class ContractRepository:
    """
    Repository class for handling operations related to contracts in the database.
    """
    def find_by_id(self, id):
        return SESSION.query(Contract).filter(Contract.id == id).one_or_none()

    def find_by_client(self, client_id):
        return SESSION.query(Contract).filter_by(client_id=client_id).all()

    def get_all(self):
        return SESSION.query(Contract).all()

    def get_all_unsigned(self):
        return SESSION.query(Contract).filter_by(status=False)

    def get_all_contracts_without_event(self):
        return SESSION.query(Contract).filter_by(event=None).all()

    def get_all_with_positive_balance_due(self):
        return SESSION.query(Contract).filter(Contract.balance_due > 0)

    def create_contract(self, datas):
        client = ClientRepository().find_by_id(datas["client_id"])
        commercial_contact_id = client.commercial_contact_id
        contract = Contract(
            client_id=datas["client_id"],
            commercial_contact_id=commercial_contact_id,
            total_amount=datas["total_amount"],
            balance_due=datas["balance_due"],
            status=datas["status"],
        )
        SESSION.add(contract)
        SESSION.commit()

    def update_contract(self, contract_id, column, new_value):
        contract = SESSION.query(Contract).filter_by(id=contract_id).one_or_none()
        if column == "client_id":
            client = ClientRepository().find_by_id(int(new_value))
            contract.client_id = new_value
            contract.commercial_contact_id = client.commercial_contact_id
        elif column == "total_amount":
            contract.total_amount = new_value
        elif column == "balance_due":
            contract.balance_due = new_value
        elif column == "status":
            contract.status = new_value
        SESSION.commit()
        if column == "status" and new_value == True:
            logging.info(f"Le contrat n°{contract_id} du client : {contract.client.fullname} a été signé.")


class StaffRepository:
    """
    Repository class for handling operations related to staff in the database.
    """
    def get_all(self):
        return SESSION.query(Staff).all()

    def find_by_id(self, id):
        return SESSION.query(Staff).filter(Staff.id == id).one_or_none()

    def find_by_name_and_firstname(self, name, first_name):
        return (
            SESSION.query(Staff)
            .filter((Staff.name == name) & (Staff.first_name == first_name))
            .one_or_none()
        )

    def find_by_email(self, email):
        return SESSION.query(Staff).filter_by(email=email).one_or_none()

    def create_staff(self, datas):
        staff = Staff(
            name=datas["name"],
            first_name=datas["first_name"],
            email=datas["email"],
            password=datas["password"],
            department=datas["department"],
        )
        SESSION.add(staff)
        SESSION.commit()
        logging.info(f"Le collaborateur {datas['first_name']} {datas['name']} a été créé.")

    def update_staff(self, staff_id, column, new_value):
        staff_member = SESSION.query(Staff).filter_by(id=staff_id).one_or_none()
        if column == "name":
            staff_member.name = new_value
        elif column == "first_name":
            staff_member.first_name = new_value
        elif column == "email":
            staff_member.email = new_value
        elif column == "password":
            staff_member.password = new_value
        elif column == "department":
            staff_member.department = new_value
        SESSION.commit()
        logging.info(f"Le {column} du collaborateur {staff_member.first_name} {staff_member.name} a été modifié.")

    def delete_staff(self, staff_member):
        SESSION.delete(staff_member)
        SESSION.commit()
        logging.info(f"Le collaborateur {staff_member.first_name} {staff_member.name} a été modifié.")
