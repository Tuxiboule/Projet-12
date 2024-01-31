from rich.console import Console
from rich.style import Style


class Messages:
    def __init__(self):
        self.console = Console()
        self.error_style = Style(color="red", bold=True)
        self.ok_style = Style(color="green", bold=True)

    def messages_ok(self, table, message_number):
        if message_number == 1:
            if table == "client":
                self.console.print("Le client a bien été enregistré.", style=self.ok_style)
            elif table == "event":
                self.console.print("L'évènement a bien été enregistré.", style=self.ok_style)
            elif table == "contract":
                self.console.print("Le contrat a bien été enregistré.", style=self.ok_style)
            elif table == "staff":
                self.console.print("Le collaborateur a bien été enregistré.", style=self.ok_style,)

        elif message_number == 2:
            if table == "client":
                self.console.print("Le client a bien été modifié.", style=self.ok_style)
            elif table == "event":
                self.console.print("L'évènement a bien été modifié.", style=self.ok_style)
            elif table == "contract":
                self.console.print("Le contrat a bien été modifié.", style=self.ok_style)
            elif table == "staff":
                self.console.print("Le collaborateur a bien été modifié.", style=self.ok_style)

        elif message_number == 3 and table == "staff":
            self.console.print("Le collaborateur a bien été supprimé de la base de données.", style=self.ok_style,)

    def message_error(self, table, message_number):
        if message_number == 0:
            self.console.print("Email inconnu", style=self.error_style)
        elif message_number == 1:
            self.console.print("Mot de passe invalide", style=self.error_style)
        elif message_number == 2:
            self.console.print(
                "Votre session a expiré. L'application va se fermer. Veuillez vous authentifier de nouveau.",
                style=self.error_style,
            )
        elif message_number == 3:
            self.console.print("Une erreur s'est produite : id ou nom inconnu. Veuillez recommencer.",
                               style=self.error_style,)

        elif message_number == 4:
            if table == "client":
                self.console.print("Ce client est inconnu.", style=self.error_style)
            if table == "event":
                self.console.print("Cet évènement est inconnu.", style=self.error_style)
            if table == "contract":
                self.console.print("Ce contrat est inexistant.", style=self.error_style)
            if table == "staff":
                self.console.print("Ce collaborateur est inconnu.", style=self.error_style)

        elif message_number == 5:
            self.console.print("Vous n'êtes pas autorisé à effectuer cette action.",style=self.error_style,)
        elif message_number == 6:
            self.console.print("Ce contrat n'est pas signé.", style=self.error_style)
        elif message_number == 7:
            self.console.print("Un évènement associé à ce contrat existe déjà dans la base de données.",
                               style=self.error_style,
                               )
        elif message_number == 8:
            self.console.print("Le collaborateur doit faire parti du service Support.", style=self.error_style,)
