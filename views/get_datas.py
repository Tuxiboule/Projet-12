import os
import platform
import getpass
import re
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich import print
from passlib.hash import argon2
from views.menu import Menu
from models.models import Department
from rich.console import Console


class GetDatas:
    def __init__(self):
        self.menu = Menu()
        self.console = Console()
        self.blue_console = Console(style="white on blue")

    def get_credentials(self):
        """
        Get user credentials.

        Returns:
            tuple: Email and password entered by the user.
        """
        print()
        self.console.print("Veuillez taper vos identifiants.", style="blue")
        email = Prompt.ask("🆔 Email")
        password = Prompt.ask("🔑 Mot de passe", password=True)
        return email, password

    def get_id(self, table):
        """
        Get the ID of a record.

        Args:
            table (str): The table name.

        Returns:
            int: The ID of the record.
        """
        if table == "client":
            id = IntPrompt.ask("N° (id) du client")
        elif table == "event":
            id = IntPrompt.ask("N° (id) de l'évènement")
        elif table == "contract":
            id = IntPrompt.ask("N° (id) du contrat")
        elif table == "staff":
            id = IntPrompt.ask("N° (id) du collaborateur")
        return id

    def get_fullname(self):
        name = Prompt.ask("Nom du client")
        name = name.capitalize()
        firstname = Prompt.ask("Prénom")
        firstname = firstname.capitalize()
        fullname = firstname + " " + name
        return fullname

    def get_name_event(self):
        self.blue_console.print("Veuillez taper le nom de l'évènement.")
        name_event = input("Nom : ").capitalize()
        return name_event

    def get_name_and_first_name_staff(self):
        name = input("Nom : ").capitalize()
        firstname = input("Prénom : ").capitalize()
        return name, firstname

    def get_email(self):
        email = input("Veuillez taper l'email : ")
        email = self.check_email(email)
        return email

    def hash_password(self, password):
        hash = argon2.hash(f"{password}")
        return hash

    def get_password(self):
        password = getpass.getpass(prompt="Veuillez créer un mot de passe : ")
        while (re.fullmatch(r"^(?=.{8,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$", password,) is None):
            print(
                "Le mot de passe doit être formé d'un minimum de 8 caractères, "
                "au moins une lettre majuscule, "
                "au moins une lettre minuscule, "
                "au moins un chiffre, "
                "au moins un caractère spécial."
            )
            password = getpass.getpass("Mot de passe : ")
        password_hashed = self.hash_password(password)
        return password_hashed

    def get_create_datas(self, table):
        """
        Get the data required to create a record.

        Args:
            table (str): The table name.

        Returns:
            dict: The data required to create the record.
        """
        if table == "client":
            self.blue_console.print("Veuillez taper les données suivantes.")
            fullname = self.get_fullname()
            email_input = input("Email : ")
            email = self.check_email(email_input)
            phone = IntPrompt.ask("Téléphone")
            name_company = input("Nom de l'entreprise : ")
            datas = {
                "fullname": fullname,
                "email": email,
                "phone": phone,
                "name_company": name_company,
            }
            return datas
        elif table == "event":
            self.blue_console.print("Veuillez taper les données suivantes.")
            name = input("Nom de l'évènement : ").capitalize()
            self.blue_console.print("Indiquer la date et l'heure du début de l'évènement :")
            event_date_start = self.get_datetime()
            self.blue_console.print("Indiquer la date et l'heure de la fin de l'évènement :")
            event_date_end = self.get_datetime()
            location = input("lieu : ")
            attendees = input("Nombre de personnes estimé : ")
            notes = input("Notes : ")
            datas = {
                "name": name,
                "event_date_start": event_date_start,
                "event_date_end": event_date_end,
                "location": location,
                "attendees": attendees,
                "notes": notes,
            }
            return datas

        elif table == "contract":
            self.blue_console.print("Veuillez taper les données suivantes.")
            client_id = input("N° (id) du client : ")
            total_amount = IntPrompt.ask("Montant total")
            balance_due = IntPrompt.ask("Montant restant à payer")
            status = self.get_status_contract()
            datas = {
                "client_id": client_id,
                "total_amount": total_amount,
                "balance_due": balance_due,
                "status": status,
            }
            return datas

        elif table == "staff":
            self.blue_console.print("Veuillez taper les données suivantes.")
            name, first_name = self.get_name_and_first_name_staff()
            email = self.get_email()
            password_hashed = self.get_password()
            department = self.get_department()
            datas = {
                "name": name,
                "first_name": first_name,
                "email": email,
                "password": password_hashed,
                "department": department,
            }
            return datas

    def get_datetime(self):
        year = Prompt.ask("année (ex : 2023) ")
        while re.fullmatch(r"\d{4}", year) is None:
            self.blue_console.print("Veuillez taper un nombre à 4 chiffres. Exemple : 2024")
            year = Prompt.ask("année")
        month = Prompt.ask("mois (ex : 01) ")
        while re.fullmatch(r"\d{2}", month) is None:
            self.blue_console.print("Veuillez taper un nombre à 2 chiffres. Exemple : 02")
            month = Prompt.ask("mois")
        day = Prompt.ask("jour (ex : 04) ")
        while re.fullmatch(r"\d{2}", day) is None:
            self.blue_console.print("Veuillez taper un nombre à 2 chiffres. Exemple : 25")
            day = Prompt.ask("jour")
        hour = Prompt.ask("heure (ex : 14) ")
        while re.fullmatch(r"\d{2}", hour) is None:
            self.blue_console.print("Veuillez taper un nombre à 2 chiffres. Exemple : 15")
            hour = Prompt.ask("heure")
        date_time = f"{year}-{month}-{day} {hour}:00"
        return date_time

    def check_email(self, email):
        while (re.fullmatch(r"[a-z0-9._-]+@[a-z0-9._-]+\.[a-z0-9._-]+", email) is None):
            self.blue_console.print("Veuillez taper un email valide. Exemple : alice@gmail.com")
            email = input("Email : ")
        return email

    def get_status_contract(self):
        option = Prompt.ask("Le contrat est-il signé?", choices=["y", "n"],)
        if option == "y":
            return True
        elif option == "n":
            return False

    def get_new_value(self, column):
        if column == "fullname":
            return self.get_fullname()
        elif column == "status":
            return self.get_status_contract()
        elif column == "password":
            return self.get_password()
        elif column == "phone":
            return IntPrompt.ask("N° de téléphone")
        elif column == "total_amount" or column == "balance_due":
            return IntPrompt.ask("Nouveau montant")
        elif column == "department":
            return self.get_department()
        else:
            new_value = input("Veuillez entrer la nouvelle valeur : ")
            if column == "email":
                email = self.check_email(new_value)
                return email
            else:
                return new_value

    def get_support_contact(self):
        support_contact = IntPrompt.ask("Veuillez taper l'id du collaborateur support de l'évènement")
        return support_contact

    def get_department(self):
        self.blue_console.print("Liste des départements : ")
        for department in Department:
            self.blue_console.print(f"{department.name} : {department.value}")
        department_number = IntPrompt.ask("Veuillez entrer le n° du département", choices=["1", "2", "3"])
        department = Department(department_number)
        return department.name

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
