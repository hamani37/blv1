import random

class IA_Pro:
    def __init__(self):
        self.compteur = 0
        self.liste_signaux = []

    def apprentissage_en_cours(self):
        return self.compteur < 50

    def entrainer(self, signal, prix):
        self.liste_signaux.append({"signal": signal, "prix": prix})
        self.compteur += 1

    def get_compteur(self):
        return self.compteur

    def analyser(self, signal, prix):
        decision = random.choice(["bon", "mauvais"])
        if decision == "bon":
            commentaire = f"Ce signal {signal['type']} pue la réussite, mec. Ça sent la moulaga !"
        else:
            commentaire = f"Ce signal {signal['type']} est plus moisi qu’un sandwich oublié dans le frigo. Laisse tomber."
        return decision, commentaire
