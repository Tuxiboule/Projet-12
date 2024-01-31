import os
import platform
from rich.console import Console
from rich.prompt import IntPrompt


class Menu:
    def __init__(self):
        self.console = Console()
        self.blue_console = Console(style="white on blue")

    def main_menu(self):
        """
        Display the main menu and return the user's choice.
        """
        print()
        menu_options = {
            1: "Clients",
            2: "Evènements",
            3: "Contrats",
            4: "Collaborateurs ",
            5: "Fermer",
        }
        self.console.rule("[bold blue]Menu principal")
        print()
        for key in menu_options:
            self.console.print(f"{key}--{menu_options[key]}", style="blue")
            print()

        option = IntPrompt.ask("Entrer votre choix : ", choices=["1", "2", "3", "4", "5"])
        self.clean()
        return option

    def table_name_translation(self, table):
        if table == "client":
            return "Clients"
        elif table == "contract":
            return "Contrats"
        elif table == "event":
            return "Evènements"
        elif table == "staff":
            return "Collaborateurs"

    def submenu(self, table):
        """
        Display the submenu for a specific table and return the user's choice.
        """
        table_in_french = self.table_name_translation(table)
        print()
        self.console.rule(f"[bold blue]Menu {table_in_french}")
        print()
        if table != "staff":
            menu_options = {
                1: "Consulter",
                2: "Créer",
                3: "Modifier",
                4: "Retour au menu principal",
                5: "Fermer",
            }
        elif table == "staff":
            menu_options = {
                1: "Consulter",
                2: "Créer",
                3: "Modifier",
                4: "Supprimer un compte collaborateur",
                5: "Retour au menu principal",
                6: "Fermer",
            }

        for key in menu_options:
            self.console.print(key, "--", menu_options[key], style="blue")
            print()

        if table == "staff":
            option = IntPrompt.ask("Entrer votre choix : ", choices=["1", "2", "3", "4", "5", "6"])
        else:
            option = IntPrompt.ask("Entrer votre choix : ", choices=["1", "2", "3", "4", "5"])
        self.clean()
        return option

    def view_menu_read_only(self, table, staff_user):
        """
        Display the View menu for a specific table and return the user's choice.
        """
        menu_in_french = self.table_name_translation(table)
        print()
        self.console.rule(f"[bold blue]Table {menu_in_french} - Consulter")
        print()
        if table == "client":
            if staff_user.department.name == "COMMERCIAL":
                menu_options = {
                    0: "Afficher tous mes clients",
                    1: "Afficher tous les clients",
                    2: "Trouver un client par son nom",
                    3: "Trouver un client par son numéro (id)",
                    4: "Trouver un client par son email",
                    5: f"Retour au menu {menu_in_french}",
                    6: "Fermer",
                }
            else:
                menu_options = {
                    1: "Afficher tous les clients",
                    2: "Trouver un client par son nom",
                    3: "Trouver un client par son numéro (id)",
                    4: "Trouver un client par son email",
                    5: f"Retour au menu {menu_in_french}",
                    6: "Fermer",
                }
        elif table == "event":
            if staff_user.department.name == "SUPPORT":
                menu_options = {
                    0: "Afficher mes évènements",
                    1: "Afficher tous les évènements",
                    2: "Afficher tous les évènements sans contact Support",
                    3: "Trouver un évènement par son numéro (id)",
                    4: "Afficher tous les évènements d'un client",
                    5: f"Retour au menu {menu_in_french}",
                    6: "Fermer",
                }
            else:
                menu_options = {
                    1: "Afficher tous les évènements",
                    2: "Afficher tous les évènements sans contact Support",
                    3: "Trouver un évènement par son numéro (id)",
                    4: "Afficher tous les évènements d'un client",
                    5: f"Retour au menu {menu_in_french}",
                    6: "Fermer",
                }

        elif table == "contract":
            menu_options = {
                0: "Afficher tous les contrats",
                1: "Afficher tous les contrats qui n'ont pas d'évènement associé",
                2: "Afficher tous les contrats non signés",
                3: "Afficher tous les contrats non soldés",
                4: "Trouver un contrat avec le n° (id) du client",
                5: "Trouver un contrat par son numéro (id)",
                6: "Trouver un contrat avec le n° (id) de l'évènement",
                7: f"Retour au menu {menu_in_french}",
                8: "Fermer",
            }
        elif table == "staff":
            menu_options = {
                1: "Afficher tous les collaborateurs",
                2: "Trouver un colloaborateur avec son n° (id)",
                3: "Trouver un collaborateur avec son nom et prénom",
                4: "Trouver un collaborateur avec son email",
                5: f"Retour au menu {menu_in_french}",
                6: "Fermer",
            }

        for key in menu_options:
            self.console.print(key, "--", menu_options[key], style="blue")
            print()

        if (
            table == "client" and staff_user.department.name == "COMMERCIAL"
        ) or (table == "event" and staff_user.department.name == "SUPPORT"):
            option = IntPrompt.ask("Entrer votre choix : ", choices=["0", "1", "2", "3", "4", "5", "6"],)

        elif table == "contract":
            option = IntPrompt.ask("Entrer votre choix : ", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],)
        else:
            option = IntPrompt.ask("Entrer votre choix : ", choices=["1", "2", "3", "4", "5", "6"])
        self.clean()
        return option

    def choice_column_to_update(self, table):
        """
        Display the selectable fields for update and return the user's choice.
        """
        while True:
            print()
            if table == "client":
                self.console.rule("[bold blue]Modifier un compte client")
                list_of_editable_update_columns = {
                    1: "fullname",
                    2: "email",
                    3: "phone",
                    4: "name_company",
                    5: "Retour",
                    6: "Fermer",
                }

            elif table == "event":
                self.console.rule("[bold blue]Modifier un èvènement")
                list_of_editable_update_columns = {
                    1: "name",
                    2: "support_contact_id",
                    3: "event_date_start",
                    4: "event_date_end",
                    5: "location",
                    6: "attendees",
                    7: "notes",
                    8: "Retour",
                    9: "Fermer",
                }

            elif table == "contract":
                self.console.rule("[bold blue]Modifier un contrat")
                list_of_editable_update_columns = {
                    1: "client_id",
                    2: "total_amount",
                    3: "balance_due",
                    4: "status",
                    5: "Retour",
                    6: "Fermer",
                }

            elif table == "staff":
                self.console.rule("[bold blue]Modifier un collaborateur")
                list_of_editable_update_columns = {
                    1: "name",
                    2: "first_name",
                    3: "email",
                    4: "password",
                    5: "department",
                    6: "Retour",
                    7: "Fermer",
                }
            self.blue_console.print("Liste des champs modifiables : ")
            print()
            for key in list_of_editable_update_columns:
                self.blue_console.print(key, list_of_editable_update_columns[key],)
                print()
            if table == "event":
                number_column_to_update = IntPrompt.ask("Entrer votre choix : ", 
                                                        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9",],
                                                        )
            elif table == "staff":
                number_column_to_update = IntPrompt.ask("Entrer votre choix : ",
                                                        choices=["1", "2", "3", "4", "5", "6", "7"],
                                                        )
            else:
                number_column_to_update = IntPrompt.ask("Entrer votre choix : ",
                                                        choices=["1", "2", "3", "4", "5", "6"],
                                                        )

            self.clean()
            return list_of_editable_update_columns[number_column_to_update]

    def clean(self):
        """Fonction qui efface l'affichage de la console"""
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")
