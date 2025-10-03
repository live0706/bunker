import tkinter as tk
from tkinter import messagebox
from Account_class import account
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


# Création des comptes Ross et Rachel 
ross_account = account("Ross", 1350, account_number=9502018482)
rachel_account = account("Rachel", 3450, account_number=1945729572)

print("Comptes disponibles pour test :")
print(ross_account.dump())
print(rachel_account.dump())

accounts = {
    str(ross_account.account_number): ross_account,
    str(rachel_account.account_number): rachel_account
}

# Fenêtre principale (Login)
root = tk.Tk()
root.title("Banque - Login")
root.geometry("400x250")
root.configure(bg="white")

username_var = tk.StringVar()
account_id_var = tk.StringVar()

def login():
    name = username_var.get()
    acc_id = account_id_var.get()

    if acc_id in accounts and accounts[acc_id].holder_name.lower() == name.lower():
        messagebox.showinfo("Succès", f"Bienvenue {name} !")
        open_dashboard(accounts[acc_id])
    else:
        messagebox.showerror("Erreur", "Nom ou ID incorrect")

# Dashboard
def open_dashboard(account: account):
    dashboard = tk.Toplevel(root)
    dashboard.title("Tableau de bord bancaire")
    dashboard.geometry("500x400")
    dashboard.configure(bg="white")

    # Ajout historique si inexistant
    if not hasattr(account, "history_tk"):
        account.history_tk = [(datetime.now(), account.balance)]

 # Nom + ID
    tk.Label(dashboard, text=f" {account.holder_name} | ID: {account.account_number}",
             font=("Segoe UI", 12, "bold"), fg="blue", bg="white").pack(pady=5)

    balance_label = tk.Label(dashboard, text=f" Solde actuel : {account.balance} €",
                             font=("Segoe UI", 14, "bold"), fg="blue", bg="white")
    balance_label.pack(pady=10)

    # Dépôt
    tk.Label(dashboard, text="Montant à déposer :", fg="blue", bg="white").pack()
    deposit_var = tk.DoubleVar()
    tk.Entry(dashboard, textvariable=deposit_var).pack()

    def do_deposit():
        account.deposit(deposit_var.get())
        balance_label.config(text=f"Solde actuel : {account.balance} €")
        account.history_tk.append((datetime.now(), account.balance))

    tk.Button(dashboard, text="Déposer", command=do_deposit, bg="blue", fg="white").pack(pady=5)

    # Retrait
    tk.Label(dashboard, text="Montant à retirer :", fg="blue", bg="white").pack()
    withdraw_var = tk.DoubleVar()
    tk.Entry(dashboard, textvariable=withdraw_var).pack()

    def do_withdraw():
        account.withdraw(withdraw_var.get())
        balance_label.config(text=f" Solde actuel : {account.balance} €")
        account.history_tk.append((datetime.now(), account.balance))

    tk.Button(dashboard, text="Retirer", command=do_withdraw, bg="blue", fg="white").pack(pady=5)

     # Plus d'infos -> Graphique
    def show_graph():
        graph_window = tk.Toplevel(dashboard)
        graph_window.title("Évolution du solde")
        graph_window.geometry("700x500")
        graph_window.configure(bg="black")

        tk.Label(graph_window, text=f"Compte de {account.holder_name}",
                 font=("Segoe UI", 14, "bold"), fg="blue", bg="black").pack(pady=10)

        dates = [entry[0].strftime("%H:%M:%S") for entry in account.history_tk]
        balances = [entry[1] for entry in account.history_tk]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, balances, marker="o", color="blue", linewidth=2)
        ax.set_title("Évolution du solde", fontsize=14, fontweight="bold")
        ax.set_xlabel("Heure de l'opération")
        ax.set_ylabel("Solde (€)")
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    tk.Button(dashboard, text=" Plus d'infos", command=show_graph, bg="blue", fg="white").pack(pady=15)

    # Interface Login
frame_login = tk.Frame(root, bg="white")
frame_login.pack(expand=True)

tk.Label(frame_login, text=" Connexion", font=("Segoe UI", 16, "bold"), fg="black", bg="white").pack(pady=10)

tk.Label(frame_login, text="Nom :", fg="black", bg="white").pack()
tk.Entry(frame_login, textvariable=username_var).pack()

tk.Label(frame_login, text="ID du compte :", fg="black", bg="white").pack()
tk.Entry(frame_login, textvariable=account_id_var).pack()

tk.Button(frame_login, text="Se connecter", command=login, bg="blue", fg="white").pack(pady=20)

root.mainloop()


