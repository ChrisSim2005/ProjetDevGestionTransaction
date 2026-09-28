from fintrack.Depense import Depense
from fintrack.Revenu import Revenu
from tkinter import *
import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
from decorateur import log_action, chronometre
from tkinter import messagebox

Devise = 'FCFA'
Montant_Max = 10000000

class DescriptionVideError(Exception):
    pass


def calcule_solde(transaction):
    total = 0
    for t in transaction:
        total += t.effet_sur_solde()
    return total


@chronometre
@log_action
def ajouter():
    description = entre_description.get()

    try:
        if not description.strip() or description == "Ex: Achat nourriture":
            raise DescriptionVideError("La description ne peut pas être vide.")
        montant = int(entre_montant.get())
    except DescriptionVideError as e:
        label_erreur.config(text=str(e))
        return
    except ValueError:
        label_erreur.config(text="Erreur : le montant doit être un nombre entier.")
        return

    if montant <= 0:
        label_erreur.config(text="Erreur : le montant doit être positif.")
        return
    if montant > Montant_Max:
        label_erreur.config(text="Erreur : le montant dépasse le maximum autorisé.")
        return

    label_erreur.config(text="")

    type_transaction = variable_type.get()
    if type_transaction == "depense":
        transaction.append(Depense(description, montant))
    else:
        transaction.append(Revenu(description, montant))

    rafraichir_affichage()
    entre_description.delete(0, tk.END)
    entre_montant.delete(0, tk.END)
    ajouter_placeholder(entre_description, "Ex: Achat nourriture")
    ajouter_placeholder(entre_montant, "Ex: 15000")
    sauv(transaction)


def rafraichir_affichage():
    for ligne in tableau.get_children():
        tableau.delete(ligne)
    for t in transaction:
        signe = "+" if t.effet_sur_solde() > 0 else "-"
        tableau.insert("", "end", values=(
            t.date.strftime("%d/%m/%Y %H:%M"),
            t.description,
            "Dépense" if t.__class__.__name__ == "Depense" else "Revenu",
            f"{signe}{abs(t.montant):,} {Devise}".replace(",", " ")
        ))
    solde = calcule_solde(transaction)
    couleur = "#2e7d32" if solde >= 0 else "#c62828"
    signe_solde = "+" if solde >= 0 else ""
    label_solde.config(text=f"{signe_solde}{solde:,} {Devise}".replace(",", " "), fg=couleur)


def sauv(transaction, chemin="sauvegarde.json"):
    donnees = [t.to_dict() for t in transaction]
    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, indent=2, ensure_ascii=False)


def charger(chemin="sauvegarde.json"):
    transactions = []
    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)
        for d in donnees:
            if d["type"] == "Depense":
                t = Depense(d["description"], d["montant"])
            else:
                t = Revenu(d["description"], d["montant"])
            if "date" in d:
                t.date = datetime.strptime(d["date"], "%Y-%m-%d %H:%M:%S")
            transactions.append(t)
    except FileNotFoundError:
        pass
    return transactions


def ajouter_placeholder(champ, texte):
    champ.delete(0, tk.END)
    champ.insert(0, texte)
    champ.config(fg="grey")

    def au_focus(event):
        if champ.get() == texte:
            champ.delete(0, tk.END)
            champ.config(fg="black")

    def hors_focus(event):
        if champ.get() == "":
            champ.insert(0, texte)
            champ.config(fg="grey")

    champ.bind("<FocusIn>", au_focus)
    champ.bind("<FocusOut>", hors_focus)


def initialiser():
    confirmation = messagebox.askyesno(
        "Confirmer",
        "Voulez-vous vraiment supprimer toutes les transactions ? Cette action est irréversible."
    )
    if not confirmation:
        return

    transaction.clear()
    sauv(transaction)
    rafraichir_affichage()
    label_erreur.config(text="")


# --- Couleurs et polices ---
COULEUR_FOND = "#FFFFFF"
COULEUR_BOUTON = "#2563EB"
COULEUR_TEXTE_BOUTON = "white"
POLICE_LABEL = ("Segoe UI", 11, "bold")
POLICE_CHAMP = ("Segoe UI", 10)

transaction = charger()

fenetre = tk.Tk()
fenetre.title("Gestion des Transactions")
fenetre.geometry("550x700")
fenetre.minsize(600, 450)
fenetre.configure(bg=COULEUR_FOND)

frame = Frame(fenetre, bg=COULEUR_FOND)
frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
fenetre.grid_rowconfigure(0, weight=1)
fenetre.grid_columnconfigure(0, weight=1)

frame_1 = Frame(frame, bg=COULEUR_FOND)
frame_1.grid(row=0, column=0, sticky=W)

# Description
titre_1 = Label(frame_1, text="Description :", font=POLICE_LABEL, bg=COULEUR_FOND)
entre_description = Entry(frame_1, font=POLICE_CHAMP, width=35)
titre_1.grid(row=0, column=0, sticky=W, pady=5)
entre_description.grid(row=0, column=1, columnspan=2, sticky=W, padx=10)
ajouter_placeholder(entre_description, "Ex: Achat nourriture")

# Montant
titre_2 = Label(frame_1, text="Montant :", font=POLICE_LABEL, bg=COULEUR_FOND)
entre_montant = Entry(frame_1, font=POLICE_CHAMP, width=15)
titre_2.grid(row=1, column=0, sticky=W, pady=5)
entre_montant.grid(row=1, column=1, sticky=W, padx=10)
ajouter_placeholder(entre_montant, "Ex: 15000")

# Type
variable_type = tk.StringVar(value="depense")
titre_3 = Label(frame_1, text="Type :", font=POLICE_LABEL, bg=COULEUR_FOND)
titre_3.grid(row=2, column=0, sticky=W, pady=5)
tk.Radiobutton(frame_1, text="Dépense", variable=variable_type, value="depense", bg=COULEUR_FOND, font=POLICE_CHAMP).grid(row=2, column=1, sticky=W)
tk.Radiobutton(frame_1, text="Revenu", variable=variable_type, value="revenu", bg=COULEUR_FOND, font=POLICE_CHAMP).grid(row=2, column=2, sticky=W)

# Bouton Ajouter
bouton_ajouter = tk.Button(
    frame_1, text="Ajouter", command=ajouter,
    bg=COULEUR_BOUTON, fg=COULEUR_TEXTE_BOUTON,
    font=("Segoe UI", 11, "bold"),
    relief="flat", padx=25, pady=8, cursor="hand2"
)
bouton_ajouter.grid(row=3, column=0, columnspan=3, pady=15)

# Message d'erreur
label_erreur = Label(frame_1, text="", font=("Segoe UI", 10), bg=COULEUR_FOND, fg="red")
label_erreur.grid(row=4, column=0, columnspan=3, sticky=W)

# --- Tableau ---
# --- Tableau avec scrollbar ---
cadre_tableau = Frame(frame, bg=COULEUR_FOND)
cadre_tableau.grid(row=1, column=0, sticky="nsew", pady=15)

style = ttk.Style()
style.configure("Treeview", font=POLICE_CHAMP, rowheight=28)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

colonnes = ("date", "description", "type", "montant")
tableau = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings", height=8)
tableau.heading("date", text="Date")
tableau.heading("description", text="Description")
tableau.heading("type", text="Type")
tableau.heading("montant", text="Montant")
tableau.column("date", width=130)
tableau.column("description", width=180)
tableau.column("type", width=80, anchor="center")
tableau.column("montant", width=110, anchor="e")

barre_defilement = ttk.Scrollbar(cadre_tableau, orient="vertical", command=tableau.yview)
tableau.configure(yscrollcommand=barre_defilement.set)

tableau.pack(side="left", fill="both", expand=True)
barre_defilement.pack(side="right", fill="y")

# --- Solde ---
cadre_solde = Frame(frame, bg=COULEUR_FOND, highlightbackground="#CCCCCC", highlightthickness=1)
cadre_solde.grid(row=2, column=0, sticky="ew", pady=10, ipady=10)

label_solde_titre = Label(cadre_solde, text="Solde :", font=("Segoe UI", 14, "bold"), bg=COULEUR_FOND, fg="black")
label_solde_titre.pack(side="left", padx=(15, 5))

label_solde = Label(cadre_solde, text="+0 FCFA", font=("Segoe UI", 14, "bold"), bg=COULEUR_FOND)
label_solde.pack(side="left")

#boutton initialiser

cadre_init = Frame(frame, bg=COULEUR_FOND, highlightbackground="#CCCCCC")
cadre_init.grid(row=3, column=0, sticky="ew", pady=5)
bouton_init = tk.Button(
    cadre_init, text="Initialiser", command=initialiser,
    bg=COULEUR_BOUTON, fg=COULEUR_TEXTE_BOUTON,
    font=("Segoe UI", 11, "bold"),
    relief="flat", padx=25, pady=8, cursor="hand2"
)
bouton_init.grid(row=3, column=0, columnspan=3, pady=15)

rafraichir_affichage()

fenetre.mainloop()