from datetime import datetime
import time

def log_action(fonction):
    def enveloppe(*args, **kwargs):
        resultat = fonction(*args, **kwargs)
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{maintenant}] Action exécutée : {fonction.__name__}")
        return resultat
    return enveloppe

def chronometre(fonction):
    def enveloppe(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        duree = time.time() - debut
        print(f"{fonction.__name__} a pris {duree:.4f} secondes")
        return resultat
    return enveloppe