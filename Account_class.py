import random
# Classe représentant un compte bancaire
class account:
    def __init__(self, holder_name, balance, account_number=None):
        self.holder_name = holder_name
        # Si aucun numéro fourni -> on génère automatiquement
        self.account_number = account_number if account_number else random.randint(1000000000, 9999999999)
        self.balance = balance
        self.history = [(self.balance, "Création du compte courant ")]
