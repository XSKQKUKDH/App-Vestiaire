import json
import random
import os

class System:
    def __init__(self):

        # Catégories de vêtements
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
        try:
            with open('data/utilisateurs.json', 'r') as file:
                self.utilisateurs = json.load(file)
        except json.JSONDecodeError:
            self.utilisateurs = []

        self.usernames = [utilisateur['username'] for utilisateur in self.utilisateurs]
        self.utilisateur_connecte = None

    def inscrire_utilisateur(self, nom, username, password, genre):
        # Créer un dossier pour l'utilisateur
        os.makedirs(f'data/{username}', exist_ok=True)
        fichiers_json = ['vestiaire.json', 'tenues.json']

        chemin_vestiaire = os.path.join('data', username, 'vestiaire.json')
        chemin_tenues = os.path.join('data', username, 'tenues.json')

        # Créer un dictionnaire pour l'utilisateur
        self.utilisateur = {
            'name': nom,
            'username': username,
            'password': password,
            'gender' : genre,
            'chemin_vestiaire' : chemin_vestiaire,
            'chemin_tenues' : chemin_tenues,
            'id' : len(self.utilisateurs)
        }

        # Ajouter l'utilisateur à la liste des utilisateurs
        self.utilisateurs.append(self.utilisateur)
        with open('data/utilisateurs.json', 'w') as file:
            json.dump(self.utilisateurs, file, indent=4)
        
        # Parcourt les noms de fichiers et crée chaque fichier avec une liste vide
        for nom_fichier in fichiers_json:
            chemin_complet = os.path.join('data', username, nom_fichier)
            
            # Écrit une liste vide dans chaque fichier JSON
            with open(chemin_complet, "w") as fichier:
                json.dump([], fichier)
            self.vestiaire = []
            self.tenues = []
        
        # Connecter l'utilisateur
        self.utilisateur_connecte = self.utilisateur

    def connecter_utilisateur(self, username):
        # Charger les données de l'utilisateur
        for utilisateur in self.utilisateurs:
            if utilisateur['username'].lower() == username.lower():
                self.utilisateur_connecte = utilisateur
        
        # Charger le vestiaire de l'utilisateur
        with open(self.utilisateur_connecte['chemin_vestiaire'], 'r') as file:
            self.vestiaire = json.load(file)
        
        # Charger les tenues de l'utilisateur
        with open(self.utilisateur_connecte['chemin_tenues'], 'r') as file:
            self.tenues = json.load(file)

    def ajouter_vetement(self, nom, couleur, style, categorie, image):
        
        # Chemin de destination
        image_path = os.path.join('static', 'assets', 'images', image.filename)
        image.save(image_path) # Sauvergarde l'image

        # Ajouter l'élément à la liste (ou à une base de données)
        self.vestiaire.append({
            'name': nom,
            'color': couleur,
            'style': style,
            'categorie': categorie,
            'lien_image' : image_path,
            'id' : len(self.vestiaire)
        })

        with open(self.utilisateur_connecte['chemin_vestiaire'], 'w') as file:
            json.dump(self.vestiaire, file, indent=4)

    def generer_tenue(self):
        hauts = []
        bas = []
        chaussures = []

        # with open(self.utilisateur_connecte['chemin_tenues'], 'r') as file:
        #         vestiaire = json.load(file)

        for vetement in self.vestiaire:
            categorie = vetement['categorie'].lower()
            if categorie in self.categorie_hauts:
                hauts.append(vetement)
            elif categorie in self.categorie_bas:
                bas.append(vetement)
            elif categorie in self.categorie_chaussures:
                chaussures.append(vetement)
        
        # Vérification : s'assurer qu'il y a au moins un élément dans chaque catégorie
        if not hauts or not bas or not chaussures:
            return None

        # Sélectionner un haut, un bas et des chaussures compatibles
        haut = random.choice(hauts)
        bas = next((b for b in bas if b['style'] == haut['style'] or b['color'] == haut['color']), random.choice(bas))
        chaussure = next((c for c in chaussures if c['style'] == haut['style'] or c['color'] == bas['color']), random.choice(chaussures))
        
        print(f"Haut: {haut}")
        print(f"Bas: {bas}")
        print(f"Chaussures: {chaussure}")

        # Retourner la tenue sélectionnée
        return {
            'haut': haut,
            'bas' : bas,
            'chaussures' : chaussure
        }

    def ajouter_tenue(self, tenue):

        self.tenues.append(tenue)
        with open(self.utilisateur_connecte['chemin_tenues'], 'w') as file:
            json.dump(self.tenues, file, indent=4)
