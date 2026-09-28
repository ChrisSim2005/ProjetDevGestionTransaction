from datetime import datetime

class Transaction:
    def __init__(self, description, montant):
        self.description = description
        self.montant = montant
        self.date = datetime.now()

    def effet_sur_solde(self):
        raise NotImplementedError("Les sous-classes doivent définir effet_sur_solde()")

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "description": self.description,
            "montant": self.montant,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        pass


class DescriptionVide(Exception):
    pass
