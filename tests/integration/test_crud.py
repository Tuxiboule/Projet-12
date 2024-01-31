from controllers.crud_manager import CrudManager


class TestCrud:
    def test_create_client_ok(
        self,
        mocker,
        get_datas_create_client_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch("views.get_datas.GetDatas.get_create_datas", return_value=get_datas_create_client_fixture,)
        mock_update_contract = mocker.patch("models.repository.ClientRepository.create_client")
        sut = CrudManager(staff_user_commercial_and_token_fixture[0], staff_user_commercial_and_token_fixture[1],)
        assert sut.create("client") == "creation_ok"

    def test_create_event_not_allowed(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_management_and_token_fixture,
    ):
        
        sut = CrudManager(staff_user_management_and_token_fixture[0], staff_user_management_and_token_fixture[1],)
        assert sut.create("event") == "not_allowed"

    def test_create_event_with_unknown_contract(
        self,
        mocker,
        get_datas_create_event_fixture,
        staff_user_commercial_and_token_fixture,
    ):
        mocker.patch("views.get_datas.GetDatas.get_create_datas", return_value=get_datas_create_event_fixture,)
        mock_ask = mocker.patch("views.get_datas.Prompt.ask", side_effect=["Smith", "John"],)
        mock_ask = mocker.patch("views.get_datas.IntPrompt.ask", side_effect=[1999],)

        sut = CrudManager(staff_user_commercial_and_token_fixture[0], staff_user_commercial_and_token_fixture[1],)
        assert sut.create("event") == "error"
