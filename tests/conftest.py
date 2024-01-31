import pytest
from settings import SESSION
from controllers.login_manager import AuthenticationAndPermissions
from models.models import Staff


@pytest.fixture
def staff_user_commercial_and_token_fixture():
    staff_user = (
        SESSION.query(Staff).filter(Staff.email == "commercial@example.com").one_or_none()
    )
    token = AuthenticationAndPermissions().create_token(
        department=staff_user.department.name
    )
    return staff_user, token


@pytest.fixture
def staff_user_management_and_token_fixture():
    staff_user = (
        SESSION.query(Staff).filter(Staff.email == "management@example.com").one_or_none()
    )
    token = AuthenticationAndPermissions().create_token(
        department=staff_user.department.name
    )
    return staff_user, token


@pytest.fixture
def get_datas_create_client_fixture():
    datas = {
        "fullname": "Cyril Dupont",
        "email": "dupont@orange.fr",
        "phone": 234344565,
        "name_company": "Tintin Cie",
    }
    return datas


@pytest.fixture
def get_datas_create_contract_fixture():
    datas = {
        "client_id": 1,
        "total_amount": 500,
        "balance_due": 250,
        "status": True,
    }
    return datas


@pytest.fixture
def get_datas_create_event_fixture():
    datas = {
        "name": "Evenement test",
        "contract_id": 1,
        "event_date_start": "2024-02-25 20:00:00",
        "event_date_end": "2024-02-26 20:00:00",
        "location": "Bordeaux",
        "attendees": 350,
        "notes": "ras",
    }
    return datas


@pytest.fixture
def get_datas_create_staff_fixture():
    datas = {
        "name": "Gandriau",
        "first_name": "Paul",
        "email": "paul@gmail.com",
        "password": "$argon2id$v=19$m=65536,t=3,p=4$NSYEgHCOce4dY6xV6j3nHA$Kjfk2mLmPQ/MUXgT3BdQ6gP0ZjCpntp0GsCpNaRLCuA",
        "department": "SUPPORT",
    }
    return datas
