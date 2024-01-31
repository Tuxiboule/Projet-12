import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.models import Staff, Client, Event, Contract, Department


config = configparser.ConfigParser()
config.read("config.ini")
config_root = config["admin"]
password = config_root["password"]

engine = create_engine(f"postgresql+psycopg2://admin:{password}@localhost/epic_events")
Session = sessionmaker(bind=engine)
session = Session()


# STAFF
staff_data = [
    {'name': 'Ercial', 'first_name': 'Com', 'email': 'commercial@example.com', 'password': 'password123', 'department': Department.COMMERCIAL},
    {'name': 'Ager', 'first_name': 'Man', 'email': 'management@example.com', 'password': 'password123', 'department': Department.MANAGEMENT},
    {'name': 'John', 'first_name': 'Doe', 'email': 'john.doe@example.com', 'password': 'password123', 'department': Department.COMMERCIAL},
    {'name': 'Henry', 'first_name': 'Thierry', 'email': 'henry.thierry@example.com', 'password': 'abc123', 'department': Department.SUPPORT},
    {'name': 'Bob', 'first_name': 'Johnson', 'email': 'bob.johnson@example.com', 'password': 'xyz789', 'department': Department.MANAGEMENT}
]

for data in staff_data:
    staff = Staff(**data)
    session.add(staff)

# CLIENT
client_data = [
    {'fullname': 'Martin Durand', 'email': 'durand_martin@example.com', 'phone': '123456789', 'name_company': 'Company Y', 'date_creation': datetime.now(), 'date_update': datetime.now(), 'commercial_contact_id': 1},
    {'fullname': 'John Smith', 'email': 'smith_john@example.com', 'phone': '123456789', 'name_company': 'Company X', 'date_creation': datetime.now(), 'date_update': datetime.now(), 'commercial_contact_id': 1},
    {'fullname': 'Client1', 'email': 'client1@example.com', 'phone': '123456789', 'name_company': 'Company A', 'date_creation': datetime.now(), 'date_update': datetime.now(), 'commercial_contact_id': 1},
    {'fullname': 'Client2', 'email': 'client2@example.com', 'phone': '987654321', 'name_company': 'Company B', 'date_creation': datetime.now(), 'date_update': datetime.now(), 'commercial_contact_id': 3},
    {'fullname': 'Client3', 'email': 'client3@example.com', 'phone': '555555555', 'name_company': 'Company C', 'date_creation': datetime.now(), 'date_update': datetime.now(), 'commercial_contact_id': 3}
]

for data in client_data:
    client = Client(**data)
    session.add(client)



# CONTRACT
contract_data = [
    {'client_id': 3, 'commercial_contact_id': 1, 'total_amount': 5000, 'balance_due': 2500, 'date_creation': datetime.now(), 'status': True},
    {'client_id': 4, 'commercial_contact_id': 2, 'total_amount': 8000, 'balance_due': 4000, 'date_creation': datetime.now(), 'status': True},
    {'client_id': 5, 'commercial_contact_id': 3, 'total_amount': 10000, 'balance_due': 7500, 'date_creation': datetime.now(), 'status': False},
    {'client_id': 2, 'commercial_contact_id': 1, 'total_amount': 5000, 'balance_due': 2500, 'date_creation': datetime.now(), 'status': True},

]

for data in contract_data:
    contract = Contract(**data)
    session.add(contract)


# EVENT
event_data = [
    {
        "name": "Evenement test",
        "contract_id": 1,
        "event_date_start": "2024-02-25 20:00:00",
        "event_date_end": "2024-02-26 20:00:00",
        "location": "Bordeaux",
        "attendees": 350,
        "notes": "ras",
    },
    {'name': 'Event1', 'contract_id': 2, 'client_id': 1, 'event_date_start': datetime.now(), 'event_date_end': datetime.now(), 'support_contact_id': 4, 'location': 'Location1', 'attendees': 50, 'notes': 'Notes for Event1'},
    {'name': 'Event2', 'contract_id': 3, 'client_id': 2, 'event_date_start': datetime.now(), 'event_date_end': datetime.now(), 'support_contact_id': 3, 'location': 'Location2', 'attendees': 100, 'notes': 'Notes for Event2'}
]

for data in event_data:
    event = Event(**data)
    session.add(event)

session.commit()

print("Données de test insérées avec succès.")
