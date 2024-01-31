from views import menu, get_datas


class TestMenu:
    def test_main_menu(self, mocker):
        mock_ask = mocker.patch(
            "views.menu.IntPrompt.ask",
            side_effect=[1],
        )
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.main_menu() == 1

    def test_submenu(self, mocker):
        mock_ask = mocker.patch(
            "views.menu.IntPrompt.ask",
            side_effect=[1],
        )
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.submenu("staff") == 1

    def test_view_menu_read_only(
        self, mocker, staff_user_commercial_and_token_fixture
    ):
        mock_ask = mocker.patch(
            "views.menu.IntPrompt.ask",
            side_effect=[2],
        )
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert (
            sut.view_menu_read_only(
                "event", staff_user_commercial_and_token_fixture[0]
            )
            == 2
        )

    def test_choice_column_to_update(self, mocker):
        mock_ask = mocker.patch(
            "views.menu.IntPrompt.ask",
            side_effect=[2],
        )
        mocker.patch("views.menu.Menu.clean")
        sut = menu.Menu()
        assert sut.choice_column_to_update("contract") == "total_amount"


class TestGetDatas:
    def test_get_credentials(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["me@example.com", "mon mot de passe"],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_credentials() == (
            "me@example.com",
            "mon mot de passe",
        )

    def test_get_id_client(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[2],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_id("client") == 2

    def test_get_id_staff(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[4],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_id("staff") == 4

    def test_get_fullname(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["Dupond", "dupont"],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_fullname() == "Dupont Dupond"

    def test_get_name_event(self, mocker):
        mocker.patch("builtins.input", return_value="noël FFF")
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_name_event() == "Noël fff"

    def test_check_email(self):
        email = "essai@gmail.com"
        email_checked = get_datas.GetDatas()
        assert email_checked.check_email(email) == email

    def test_check_status_true(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["y"],
        )
        status_checked = get_datas.GetDatas()
        assert status_checked.get_status_contract() is True

    def test_check_status_false(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.Prompt.ask",
            side_effect=["n"],
        )
        status_checked = get_datas.GetDatas()
        assert status_checked.get_status_contract() is False

    def test_get_new_value(self, mocker):
        mocker.patch("builtins.input", return_value=3)
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_new_value("client_id") == 3

    def test_get_new_value_phone(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[202020202],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_new_value("phone") == 202020202

    def test_get_support_contact(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[2],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_support_contact() == 2

    def test_get_department(self, mocker):
        mock_ask = mocker.patch(
            "views.get_datas.IntPrompt.ask",
            side_effect=[2],
        )
        get_datas_test = get_datas.GetDatas()
        assert get_datas_test.get_department() == "SUPPORT"

    @classmethod
    def teardown_class(cls):
        # This method is being called after each test case, and it will revert input back to original function
        get_datas_test = get_datas.GetDatas()
        get_datas_test.input = input
