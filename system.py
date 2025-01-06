import json
import random
import os

class System:
    def __init__(self):

        self.categorie_hauts = [
            "t-shirt",
            "pull",
            "sweatshirt",
            "débardeur",
            "chemise",
            "veste",
            "manteau",
            "doudoune",
            "robe",
            ]
        self.categorie_bas = [
            "pantalon",
            "jean",
            "jogging",
            "short",
            "jupe"
            ]
        self.categorie_chaussures = [
            "baskets",
            "bottes",
            "sandales"
            ]

    def ajouter_vetement(self, nom, couleur, style, categorie, image):
        
        # Chemin de destination
        image_path = os.path.join('static', 'assets', 'images', image.filename)
        image.save(image_path) # Sauvergarde l'image

        # Récupération des données de vestiaire.json
        try:
            with open('data/vestiaire.json', 'r') as file:
                vestiaire = json.load(file)
        except json.JSONDecodeError:
            vestiaire = []

        # Ajouter l'élément à la liste (ou à une base de données)
        vestiaire.append({
            'name': nom,
            'color': couleur,
            'style': style,
            'categorie': categorie,
            'lien_image' : image_path,
            'id' : len(vestiaire)
        })

        with open('data/vestiaire.json', 'w') as file:
            json.dump(vestiaire, file, indent=4)

    def generer_tenue(self):
        hauts = []
        bas = []
        chaussures = []

        with open('data/vestiaire.json', 'r') as file:
                vestiaire = json.load(file)

        for vetement in vestiaire:
            categorie = vetement['categorie'].lower()
            if categorie in self.categorie_hauts:
                hauts.append(vetement)
            elif categorie in self.categorie_bas:
                bas.append(vetement)
            elif categorie in self.categorie_chaussures:
                chaussures.append(vetement)
        
        # Vérification : s'assurer qu'il y a au moins un élément dans chaque catégorie
        if not hauts or not bas or not chaussures:
            raise ValueError("Une des catégories (haut, bas, chaussures) est vide dans le fichier JSON.")

        # Sélectionner un haut, un bas et des chaussures compatibles
        haut = random.choice(hauts)
        bas = next((b for b in bas if b['style'] == haut['style'] or b['color'] == haut['color']), random.choice(bas))
        chaussure = next((c for c in chaussures if c['style'] == haut['style'] or c['color'] == bas['color']), random.choice(chaussures))
        
        # Retourner la tenue sélectionnée
        return {
            'haut': haut,
            'bas' : bas,
            'chaussures' : chaussure
        }

    def ajouter_tenue(self, tenue):
        # !!! Il faudra faire un system qui trouve 
        # les vetements avec leurs id et les ajouter à la tenue

        try:
            with open('data/tenues.json', 'r') as file:
                tenues = json.load(file)
        except json.JSONDecodeError:
            tenues = []

        tenues.append(tenue)
        with open('data/tenues.json', 'w') as file:
            json.dump(tenues, file, indent=4)
