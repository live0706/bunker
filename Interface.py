"""
Application de tableau de bord bancaire simple
Utilise Tkinter pour l'interface graphique et Matplotlib pour les graphiques.

MODIFICATIONS :
- Augmentation de la taille de toutes les polices (labels, champs, boutons)
  pour une meilleure lisibilité (Accessibilité).
- Ajout de boutons "Retour" sur les fenêtres "Tableau de bord" et 
  "Graphique" pour améliorer la navigation.
"""

# --- Importations ---
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Importations tierces (nécessitent 'pip install matplotlib')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importation de notre module local
try:
    # On suppose que la classe 'account' est définie dans Account_class.py
    from Account_class import account 
except ImportError:
    print("Erreur: Le fichier 'Account_class.py' est introuvable.")
    # Définition d'une classe "mock" pour permettre au script de s'exécuter
    # sans le fichier original, au cas où.
    class account:
        def __init__(self, name, balance, account_number):
            self.holder_name = name
            self.balance = balance
            self.account_number = account_number
        def deposit(self, amount):
            if amount > 0: self.balance += amount
        def withdraw(self, amount):
            if 0 < amount <= self.balance: self.balance -= amount
        def dump(self):
            return f"Mock Account: {self.holder_name}, {self.account_number}"

# --- Définition des Constantes (Thème Sombre & Polices) ---
# Palette de couleurs centralisée pour une maintenance facile du thème
colors = {
    "bg": "#2E2E2E",        # Fond principal (gris foncé)
    "text": "#F5F5F5",      # Texte normal (blanc cassé)
    "accent": "#00AEEF",    # Titres et accents (bleu vif)
    "button_bg": "#007BFF", # Fond des boutons (bleu)
    "button_fg": "#FFFFFF",  # Texte des boutons (blanc)
    "entry_bg": "#4A4A4A",   # Fond des champs de saisie (gris moyen)
    "entry_fg": "#FFFFFF",   # Texte des champs de saisie (blanc)
}

# AJOUTÉ: Définition centralisée des polices pour augmenter la taille
FONT_FAMILY = "Segoe UI"
FONT_BOUTON_RETOUR = (FONT_FAMILY, 12)
FONT_NORMAL = (FONT_FAMILY, 14)
FONT_BOLD = (FONT_FAMILY, 14, "bold")
FONT_LABEL = (FONT_FAMILY, 16) # Pour les labels de champs (login)
FONT_TITRE_SECTION = (FONT_FAMILY, 18, "bold")
FONT_BALANCE = (FONT_FAMILY, 22, "bold")
FONT_TITRE_PAGE = (FONT_FAMILY, 24, "bold")


# --- Initialisation des données (Mock Data) ---
# Création des comptes de démonstration
ross_account = account("Ross", 1350, account_number=9502018482)
rachel_account = account("Rachel", 3450, account_number=1945729572)

print("Comptes créés pour test :")
print(ross_account.dump())
print(rachel_account.dump())

# Structure de données pour retrouver les comptes par leur ID (string)
accounts = {
    str(ross_account.account_number): ross_account,
    str(rachel_account.account_number): rachel_account
}


# --- Définition des Fonctions de l'Application ---

def login():
    """
    Vérifie les identifiants saisis sur l'écran de connexion.
    Ouvre le tableau de bord si la correspondance est trouvée.
    """
    name = username_var.get()
    acc_id = account_id_var.get()

    # Vérification (non sensible à la casse pour le nom)
    if acc_id in accounts and accounts[acc_id].holder_name.lower() == name.lower():
        messagebox.showinfo("Succès", f"Bienvenue {name} !")
        # Ouvre la fenêtre du tableau de bord en passant l'objet compte
        open_dashboard(accounts[acc_id])
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou ID de compte incorrect.")


def open_dashboard(current_account: account):
    """
    Crée et affiche la fenêtre principale du tableau de bord pour le compte connecté.
    """
    dashboard = tk.Toplevel(root)
    dashboard.title("Tableau de bord bancaire")
    dashboard.state('zoomed') # Affiche la fenêtre en plein écran
    dashboard.configure(bg=colors["bg"])

    # Initialise un historique des transactions pour cette session GUI.
    # 'history_tk' est ajouté dynamiquement à l'objet 'account'
    # uniquement pour la durée de vie de l'application.
    if not hasattr(current_account, "history_tk"):
        current_account.history_tk = [(datetime.now(), current_account.balance)]

    
    # --- AJOUTÉ: Bouton Retour (Déconnexion) ---
    def go_back_to_login():
        """Ferme le tableau de bord pour revenir à l'écran de connexion."""
        dashboard.destroy()

    tk.Button(dashboard, text="< Retour (Déconnexion)", 
              command=go_back_to_login, 
              fg=colors["accent"], 
              bg=colors["bg"], 
              font=FONT_BOUTON_RETOUR, # Police plus petite pour un lien
              relief="flat", # Style "lien" sans bordure
              activeforeground=colors["text"]
    ).pack(anchor="nw", padx=10, pady=5) # "nw" = Nord-Ouest (Haut-Gauche)


    # --- Widgets du Tableau de Bord ---

    # Titre (Nom + ID)
    tk.Label(dashboard, 
             text=f" {current_account.holder_name} | ID: {current_account.account_number}",
             font=FONT_TITRE_SECTION, # MODIFIÉ: Police
             fg=colors["accent"], 
             bg=colors["bg"]
    ).pack(pady=10)

    # Affichage du solde (ce label sera mis à jour)
    balance_label = tk.Label(dashboard, 
                             text=f" Solde actuel : {current_account.balance} €",
                             font=FONT_BALANCE, # MODIFIÉ: Police
                             fg=colors["accent"], 
                             bg=colors["bg"])
    balance_label.pack(pady=20)

    # --- Frame pour les opérations (Dépôt / Retrait) ---
    ops_frame = tk.Frame(dashboard, bg=colors["bg"])
    ops_frame.pack(pady=10)

    # Variables pour les champs de saisie
    deposit_var = tk.DoubleVar()
    withdraw_var = tk.DoubleVar()

    # --- Section Dépôt ---
    tk.Label(ops_frame, text="Montant à déposer :", fg=colors["text"], bg=colors["bg"],
             font=FONT_NORMAL # MODIFIÉ: Police
    ).grid(row=0, column=0, padx=10, pady=5)
    
    tk.Entry(ops_frame, textvariable=deposit_var, bg=colors["entry_bg"], fg=colors["entry_fg"], 
             insertbackground=colors["text"], # Couleur du curseur
             font=FONT_NORMAL # MODIFIÉ: Police
    ).grid(row=0, column=1, padx=10, pady=5)

    def do_deposit():
        """Callback pour le bouton 'Déposer'."""
        try:
            amount = deposit_var.get()
            current_account.deposit(amount) # Logique métier (via la classe)
            
            # Mise à jour de l'interface
            balance_label.config(text=f"Solde actuel : {current_account.balance} €")
            # Ajout à l'historique de session
            current_account.history_tk.append((datetime.now(), current_account.balance))
            deposit_var.set(0.0) # Réinitialise le champ
        except Exception as e:
            messagebox.showwarning("Erreur", f"Montant invalide : {e}")

    tk.Button(ops_frame, text="Déposer", command=do_deposit, 
              bg=colors["button_bg"], fg=colors["button_fg"], 
              font=FONT_BOLD # MODIFIÉ: Police
    ).grid(row=0, column=2, padx=10, pady=5)

    # --- Section Retrait ---
    tk.Label(ops_frame, text="Montant à retirer :", fg=colors["text"], bg=colors["bg"],
             font=FONT_NORMAL # MODIFIÉ: Police
    ).grid(row=1, column=0, padx=10, pady=5)
    
    tk.Entry(ops_frame, textvariable=withdraw_var, bg=colors["entry_bg"], fg=colors["entry_fg"], 
             insertbackground=colors["text"],
             font=FONT_NORMAL # MODIFIÉ: Police
    ).grid(row=1, column=1, padx=10, pady=5)

    def do_withdraw():
        """Callback pour le bouton 'Retirer'."""
        try:
            amount = withdraw_var.get()
            # On pourrait ajouter une vérification ici avant d'appeler withdraw
            # (ex: si le solde est suffisant)
            current_account.withdraw(amount) # Logique métier (via la classe)
            
            # Mise à jour de l'interface
            balance_label.config(text=f" Solde actuel : {current_account.balance} €")
            # Ajout à l'historique de session
            current_account.history_tk.append((datetime.now(), current_account.balance))
            withdraw_var.set(0.0) # Réinitialise le champ
        except Exception as e:
            messagebox.showwarning("Erreur", f"Montant invalide : {e}")

    tk.Button(ops_frame, text="Retirer", command=do_withdraw, 
              bg=colors["button_bg"], fg=colors["button_fg"], 
              font=FONT_BOLD # MODIFIÉ: Police
    ).grid(row=1, column=2, padx=10, pady=5)

    # --- Section Graphique (lancée dans une nouvelle fenêtre) ---
    def show_graph():
        """
        Ouvre une nouvelle fenêtre Toplevel pour afficher le graphique
        de l'évolution du solde (basé sur 'history_tk').
        """
        graph_window = tk.Toplevel(dashboard)
        graph_window.title("Évolution du solde")
        graph_window.state('zoomed')
        graph_window.configure(bg=colors["bg"])

        # --- AJOUTÉ: Bouton Retour ---
        def go_back_to_dashboard():
            """Ferme la fenêtre du graphique."""
            graph_window.destroy()

        tk.Button(graph_window, text="< Retour au tableau de bord", 
                  command=go_back_to_dashboard, 
                  fg=colors["accent"], 
                  bg=colors["bg"], 
                  font=FONT_BOUTON_RETOUR, # Police plus petite
                  relief="flat", # Style "lien"
                  activeforeground=colors["text"]
        ).pack(anchor="nw", padx=10, pady=5) # "nw" = Nord-Ouest (Haut-Gauche)

        tk.Label(graph_window, text=f"Évolution du compte de {current_account.holder_name}",
                 font=FONT_TITRE_SECTION, # MODIFIÉ: Police
                 fg=colors["accent"], 
                 bg=colors["bg"]
        ).pack(pady=20)

        # Préparation des données pour le graphique
        # Utilise l'historique de session
        dates = [entry[0].strftime("%H:%M:%S") for entry in current_account.history_tk]
        balances = [entry[1] for entry in current_account.history_tk]

        # --- Configuration du style sombre pour Matplotlib ---
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(colors["bg"]) # Fond de la figure globale
        ax.set_facecolor(colors["bg"])        # Fond de la zone de traçage

        # Tracé de la ligne
        ax.plot(dates, balances, marker="o", color=colors["accent"], linewidth=2, markersize=8)
        
        # Style des textes (titre, labels) - MODIFIÉ: Tailles de police
        ax.set_title("Évolution du solde", fontsize=FONT_TITRE_SECTION[1], fontweight="bold", color=colors["text"])
        ax.set_xlabel("Heure de l'opération", fontsize=FONT_NORMAL[1], color=colors["text"])
        ax.set_ylabel("Solde (€)", fontsize=FONT_NORMAL[1], color=colors["text"])
        
        # Style des axes (graduations) - MODIFIÉ: Tailles de police
        ax.tick_params(axis='x', colors=colors["text"], labelsize=FONT_BOUTON_RETOUR[1])
        ax.tick_params(axis='y', colors=colors["text"], labelsize=FONT_BOUTON_RETOUR[1])
        
        # Style du cadre (bordures)
        for spine in ax.spines.values():
            spine.set_edgecolor(colors["text"])
        # --- Fin de la configuration Matplotlib ---

        plt.xticks(rotation=45) # Rotation des labels de l'axe X
        plt.tight_layout()     # Ajuste le graphique pour éviter les superpositions

        # Intégration du graphique Matplotlib dans la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

    # Bouton sur le tableau de bord pour ouvrir le graphique
    tk.Button(dashboard, text=" Afficher l'évolution du solde", command=show_graph, 
              bg=colors["button_bg"], fg=colors["button_fg"], 
              font=FONT_BOLD 
    ).pack(pady=30)


# --- Configuration de la Fenêtre Principale (Login) ---
root = tk.Tk()
root.title("Banque - Connexion")
root.state('zoomed') # Affiche la fenêtre en plein écran
root.configure(bg=colors["bg"])

# Variables Tkinter pour les champs de saisie (Portée globale)
username_var = tk.StringVar()
account_id_var = tk.StringVar()

# --- Widgets de l'Interface de Connexion ---

# Frame pour centrer les éléments de connexion
frame_login = tk.Frame(root, bg=colors["bg"])
# 'expand=True' centre le frame dans la fenêtre (même maximisée)
frame_login.pack(expand=True) 

tk.Label(frame_login, text=" Connexion", 
         font=FONT_TITRE_PAGE, 
         fg=colors["accent"], bg=colors["bg"]
).pack(pady=20)

# Champ Nom
tk.Label(frame_login, text="Nom :", 
         font=FONT_LABEL,
         fg=colors["text"], bg=colors["bg"]
).pack(pady=(10,0))

tk.Entry(frame_login, textvariable=username_var, 
         font=FONT_LABEL,
         bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["text"]
).pack(pady=5, padx=20)

# Champ ID
tk.Label(frame_login, text="ID du compte :", 
         font=FONT_LABEL, 
         fg=colors["text"], bg=colors["bg"]
).pack(pady=(10,0))

tk.Entry(frame_login, textvariable=account_id_var, 
         font=FONT_LABEL, 
         bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["text"]
).pack(pady=5, padx=20)

# Bouton de Connexion
tk.Button(frame_login, text="Se connecter", command=login, 
          font=FONT_BOLD,
          bg=colors["button_bg"], fg=colors["button_fg"]
).pack(pady=30)


# --- Lancement de l'application ---
if __name__ == "__main__":
    root.mainloop()