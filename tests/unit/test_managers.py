from unittest.mock import MagicMock
from models.models import Client, Staff, Contract
from models.repository import ClientRepository
from controllers.crud_manager import CrudManager
from settings import SESSION
from controllers import login_manager, menu_manager, permissions

FAKE_PASSWORD = "12345"
FAKE_HASHED_PASSWORD = (
    "$argon2id$v=19$m=65536,t=3,p=4$AcB4D8GYc27tnRPinNM6hw$2PfVv4W"
    "H1CoD0/TWmyDw2z0iBTj++WAVt/G9IJRnvtg"
)


class TestLogin:
    def test_check_password(self, mocker):
        mocker.patch("controllers.login_manager.Menu")
        mocker.patch("controllers.login_manager.Messages")
        MockGetDatas = mocker.patch("controllers.login_manager.GetDatas")
        MockGetDatas.return_value.get_credentials.return_value = (
            "me@example.com",
            FAKE_PASSWORD,
        )

        mock_session = mocker.patch("controllers.login_manager.SESSION")
        mock_staff_user = (
            mock_session.query.return_value.filter.return_value.one_or_none.return_value
        )
        mock_staff_user.password = FAKE_HASHED_PASSWORD
        mock_staff_user.department.name = "COMMERCIAL"
        mock_create_token = mocker.patch(
            "controllers.login_manager.AuthenticationAndPermissions.create_token"
        )
        MockMenuManager = mocker.patch("controllers.login_manager.MenuManager")
        mock_choice_main_menu = MockMenuManager.return_value.choice_main_menu

        auth_and_perms = login_manager.AuthenticationAndPermissions()
        auth_and_perms.check_password()
        mock_create_token.assert_called_once_with("COMMERCIAL")
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()


class TestCrud:
    def test_create_client_ok(
        self,
        mocker,
        get_datas_create_client_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_client_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_update_contract = mocker.patch(
            "models.repository.ClientRepository.create_client"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("client") == "creation_ok"

    def test_create_client_false(
        self,
        mocker,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value="bad_datas",
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("client") is False

    def test_create_contract_ok(
        self,
        mocker,
        get_datas_create_contract_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_contract_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_update_contract = mocker.patch(
            "models.repository.ContractRepository.create_contract"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("contract") == "creation_ok"

    def test_create_event_ok(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_event_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["Smith", "John"],
        )
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[4],
        )
        mocker.patch(
            "controllers.permissions.Permissions.is_own_client",
            return_value=True,
        )

        mock_update_event = mocker.patch(
            "models.repository.EventRepository.create_event"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("event") == 'creation_ok'

    def test_create_event_with_unknown_client(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_event_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["Client", "unknown"],
        )

        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("event") == 'unknown_client'

    def test_create_event_with_unsigned_contract(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_event_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["Smith", "John"],
        )
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[3],
        )

        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("event") == "unsigned_contract"

    def test_create_event_not_ok_existing(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_event_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["Smith", "John"],
        )
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[1],
        )
        mocker.patch(
            "controllers.permissions.Permissions.is_own_client",
            return_value=True,
        )

        mock_update_event = mocker.patch(
            "models.repository.EventRepository.create_event"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("event") == 'existing_event'

    def test_create_contract_with_unknown_client(
        self,
        mocker,
        get_datas_create_contract_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        get_datas_create_contract_fixture["client_id"] = 999
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_contract_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("contract") == "unknown_client"

    def test_create_staff_ok(
        self,
        mocker,
        get_datas_create_staff_fixture,
        staff_user_management_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_staff_fixture,
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mock_update_contract = mocker.patch(
            "models.repository.StaffRepository.create_staff"
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.create("staff") == "creation_ok"

    def test_create_staff_not_allowed(
        self,
        mocker,
        get_datas_create_staff_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_create_datas",
            return_value=get_datas_create_staff_fixture,
        )

        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.create("staff") == "not_allowed"

    def test_read_client_fullname(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=2)
        mocker.patch("views.get_datas.GetDatas.get_fullname", return_value="John Smith")
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("client") == "display_ok"

    def test_read_client_id(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("client") == "display_ok"

    def test_read_contract_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=2)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") == "display_ok"

    def test_read_contract_with_unknown_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_id",
            return_value=1999,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") is None

    def test_read_contract_with_unknown_event(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=6)
        mocker.patch(
            "views.get_datas.GetDatas.get_id",
            return_value=1999,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("contract") is None

    def test_read_event_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=2)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") == "display_ok"

    def test_read_event_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch(
            "views.get_datas.GetDatas.get_id",
            return_value=1999,
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") is None

    def test_read_event_with_no_unknown_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_fullname",
            return_value="client that doesn't exist",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("event") is None

    def test_read_staff_ok(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=2)
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") == "display_ok"

    def test_read_staff_with_name_and_first_name_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=3)
        mocker.patch(
            "views.get_datas.GetDatas.get_name_and_first_name_staff",
            return_value=(
                "name that doesn't exist",
                "first name that doesn't exist",
            ),
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") is None

    def test_read_staff_with_email_not_exist(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.view_menu_read_only", return_value=4)
        mocker.patch(
            "views.get_datas.GetDatas.get_email",
            return_value="unknown@email.com",
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.read("staff") is None

    def test_update_client(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_fullname",
            return_value="Martin Durand",
        )
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        mocker.patch(
            "views.menu.Menu.choice_column_to_update", return_value="fullname"
        )
        mocker.patch(
            "views.get_datas.GetDatas.get_new_value",
            return_value="Martin Dupond",
        )
        mock_update_client = mocker.patch(
            "models.repository.ClientRepository.update_client"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.update("client") == "update_ok"

    def test_update_contract(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=2)
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        mocker.patch(
            "views.menu.Menu.choice_column_to_update", return_value="client_id"
        )
        mocker.patch("views.get_datas.GetDatas.get_new_value", return_value=3)
        mock_update_contract = mocker.patch(
            "models.repository.ContractRepository.update_contract"
        )
        sut = CrudManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        assert sut.update("contract") == "update_ok"

    def test_update_event(
        self, mocker, staff_user_management_and_token_fixture
    ):
        mocker.patch("views.get_datas.GetDatas.get_id", return_value=1)
        mocker.patch(
            "controllers.permissions.Permissions.permission_update",
            return_value=True,
        )
        mocker.patch(
            "views.get_datas.GetDatas.get_support_contact", return_value=4
        )
        mock_update_contract = mocker.patch(
            "models.repository.EventRepository.update_event"
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.update("event") == "update_ok"

    def test_update_staff(
        self, mocker, staff_user_management_and_token_fixture
    ):
        mocker.patch(
            "views.get_datas.GetDatas.get_name_and_first_name_staff",
            return_value=("Henry", "Thierry"),
        )
        mocker.patch(
            "views.menu.Menu.choice_column_to_update", return_value="email"
        )
        mocker.patch(
            "views.get_datas.GetDatas.get_new_value",
            return_value="nouvel_email@gmail.com",
        )
        mock_update_contract = mocker.patch(
            "models.repository.StaffRepository.update_staff"
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.update("staff") == "update_ok"

    def test_delete_staff(
        self, mocker, staff_user_management_and_token_fixture
    ):
        mocker.patch(
            "controllers.permissions.Permissions.permission_create",
            return_value=True,
        )
        mocker.patch(
            "views.get_datas.GetDatas.get_id",
            return_value=5,
        )
        mock_update_contract = mocker.patch(
            "models.repository.StaffRepository.delete_staff"
        )
        mock_ask = mocker.patch(
            "controllers.crud_manager.Confirm.ask",
            side_effect=["y"],
        )
        sut = CrudManager(
            staff_user_management_and_token_fixture[0],
            staff_user_management_and_token_fixture[1],
        )
        assert sut.delete("staff") == "delete_ok"


class TestMenuManager:
    def test_main_menu(self, mocker, staff_user_commercial_and_token_fixture):
        mocker.patch("views.menu.Menu.main_menu", return_value=1)
        mock_choice_submenu = mocker.patch(
            "controllers.menu_manager.MenuManager.choice_submenu"
        )
        choice_submenu = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_submenu.choice_main_menu()
        mock_choice_submenu.assert_called_once()
        mock_choice_submenu.assert_called_once_with("client")

    def test_choice_submenu(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.submenu", return_value=2)
        mocker.patch(
            "controllers.crud_manager.CrudManager.create",
            return_value="creation_ok",
        )
        mock_message_ok = mocker.patch("views.messages.Messages.messages_ok")
        mock_message_ok.return_value = "Le client a bien été enregistré."
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_create = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_create.choice_submenu("client")
        mock_message_ok.assert_called_once_with("client", 1)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()

    def test_choice_submenu_with_message_error(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.submenu", return_value=3)
        mocker.patch(
            "controllers.crud_manager.CrudManager.update",
            return_value="error",
        )
        mock_message_error = mocker.patch(
            "views.messages.Messages.message_error"
        )
        mock_message_error.return_value = (
            "Une erreur s'est produite. Veuillez recommencer."
        )
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_update = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_update.choice_submenu("client")
        mock_message_error.assert_called_once_with("client", 3)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()

    def test_choice_submenu_with_message_erro_not_allowed(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mocker.patch("views.menu.Menu.submenu", return_value=3)
        mocker.patch(
            "controllers.crud_manager.CrudManager.update",
            return_value="not_allowed",
        )
        mock_message_error = mocker.patch(
            "views.messages.Messages.message_error"
        )
        mock_message_error.return_value = (
            "Vous n'êtes pas autorisé(e) à effectuer cette action."
        )
        mock_choice_main_menu = mocker.patch(
            "controllers.login_manager.MenuManager.choice_main_menu"
        )
        choice_crud_update = menu_manager.MenuManager(
            staff_user_commercial_and_token_fixture[0],
            staff_user_commercial_and_token_fixture[1],
        )
        choice_crud_update.choice_submenu("client")
        mock_message_error.assert_called_once_with("client", 5)
        mock_choice_main_menu.assert_called_once()
        mock_choice_main_menu.assert_called_once_with()


class TestPermissions:
    def test_permission_create_client(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "COMMERCIAL"},
        )
        perm_create = permissions.Permissions()
        assert perm_create.permission_create("token", "client") is True

    def test_permission_create_staff(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "MANAGEMENT"},
        )
        perm_create = permissions.Permissions()
        assert perm_create.permission_create("token", "staff") is True

    def test_permission_update_client(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "COMMERCIAL"},
        )
        perm_update = permissions.Permissions()
        assert perm_update.permission_update(1, 1, "token", "client") is True

    def test_permission_update_event_with_staff_support(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "SUPPORT"},
        )
        mock_is_their_event = mocker.patch(
            "controllers.permissions.Permissions.is_their_event"
        )
        perm_update = permissions.Permissions()
        perm_update.permission_update(3, 4, "token", "event")
        mock_is_their_event.assert_called_once()

    def test_permission_update_event_with_staff_management(self, mocker):
        mocker.patch(
            "controllers.permissions.Permissions.check_token_validity",
            return_value={"exp": 1701208489, "department": "MANAGEMENT"},
        )
        perm_update = permissions.Permissions()
        assert perm_update.permission_update(3, 4, "token", "event") is True

    def test_is_own_client(self, mocker):
        own_client = permissions.Permissions()
        assert own_client.is_own_client(1, 1) is True

    def test_is_their_event(self):
        their_event = permissions.Permissions()
        assert their_event.is_their_event(4, 2) is True
