from settings import Base, ENGINE
from models.repository import StaffRepository
from views.get_datas import GetDatas


get_datas = GetDatas()
staff_repository = StaffRepository()


def create_tables():
    Base.metadata.create_all(ENGINE)
    print("Les tables ont bien été créées")
    datas = get_datas.get_create_datas("staff")
    staff_repository.create_staff(datas)
    print(f"L'utilisateur {datas['name']} a bien été créé.")
    print(f"Son identifiant de connexion est : {datas['email']}")


if __name__ == "__main__":
    create_tables()
