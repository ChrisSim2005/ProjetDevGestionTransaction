from fintrack.Transaction import Transaction

class Depense(Transaction):

    def __init__(self,description, montant):
        super().__init__(description,montant)

    def effet_sur_solde(self):
            return -self.montant

    def __str__(self):
        return f"Depense: {self.description}  -{self.montant}"