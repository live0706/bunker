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