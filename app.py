from flask import Flask, render_template, url_for, request, redirect
from system import System
import requests
import json
import ast

# Juste un petit test pour voir si ça marche

# Un autre test pour essayer la git pull commande

app = Flask(__name__)
app_systeme = System()

@app.route('/')
def acceuil():
    return render_template('acceuil.html')

@app.route('/home')
def home():
    with open('data/tenues.json', 'r') as file:
        tenues = json.load(file)
    return render_template('home.html', tenues=tenues)

@app.route('/vestiaire')
def vestiaire():
    with open('data/vestiaire.json', 'r') as file:
        vetements = json.load(file)
    return render_template('vestiaire.html', vetements=vetements)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name')
        color = request.form.get('color')
        style = request.form.get('style')
        categorie = request.form.get('categorie')
        image = request.files['image']

        # Ajout du vetement au vestiaire
        app_systeme.ajouter_vetement(name, color, style, categorie, image)

        # Redirection pour éviter une soumission multiple en rechargeant la page
        return redirect(url_for('confirmation'))
    
    return render_template('ajouter.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/generer', methods=['GET', 'POST'])
def generer():
    if request.method == 'POST':
        tenue = app_systeme.generer_tenue()
        return render_template('generer.html', tenue=tenue)
    return render_template('generer.html')

@app.route('/enregistrer_tenue', methods=['POST'])
def ajouter_tenue():
    tenue = request.form.get('tenue')
    print(tenue)
    tenue_dict = ast.literal_eval(tenue)
    print(tenue_dict)

    if tenue:
        app_systeme.ajouter_tenue(tenue_dict) # Ajouter la tenue à la liste des tenues
        return render_template('generer.html')
    else:
        return render_template('generer.html')

if __name__ == '__main__':
    app.run(debug=True)
