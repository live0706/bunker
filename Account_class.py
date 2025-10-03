import random
# Classe représentant un compte bancaire
class account:
    def __init__(self, holder_name, balance, account_number=None):
        self.holder_name = holder_name
        # Si aucun numéro fourni -> on génère automatiquement
        self.account_number = account_number if account_number else random.randint(1000000000, 9999999999)
        self.balance = balance
        self.history = [(self.balance, "Création du compte courant ")]
# Méthode pour déposer de l'argent
    def deposit(self, amount):
        self.balance += amount
        self.history.append((self.balance, f"Dépôt de {amount} €"))

# Méthode pour retirer de l'argent  
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.history.append((self.balance, f"Retrait de {amount} €"))
        else:
            print("Fonds insuffisants")
