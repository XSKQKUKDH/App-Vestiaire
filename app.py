from flask import Flask, render_template, url_for, request, redirect, flash
from system import System
import json
import ast
import webbrowser
from threading import Timer

app = Flask(__name__)
app_systeme = System()

app.secret_key = 'super_secret_key'

@app.route('/')
def acceuil():
    return render_template('acceuil.html')

@app.route('/connection', methods=['GET', 'POST'])
def connection():
    if request.method == 'POST':
        # Récupération des données du formulaire
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Vérification des données
        if username in app_systeme.usernames:
            for utilisateur in app_systeme.utilisateurs:
                if utilisateur['username'] == username:
                    if utilisateur['password'] == password:
                        app_systeme.connecter_utilisateur(username)
                        return redirect(url_for('home'))
                    else:
                        flash('Mot de passe incorrect', 'error')
                        return redirect(url_for('connection'))
        else:
            flash("Ce nom d'utilisateur n'existe pas", 'error')
            return redirect(url_for('connection'))
    return render_template('connection.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name')
        username = request.form.get('username').lower()
        password = request.form.get('password')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')

        # Vérification des données
        if password != password2:
            flash('Les mots de passe ne correspondent pas', 'error')
            return redirect(url_for('inscription'))
        elif username in app_systeme.usernames:
            flash("Ce nom d'utilisateur est déjà pris", 'error')
            return redirect(url_for('inscription'))
        else:
            app_systeme.inscrire_utilisateur(name, username, password, gender)
            return redirect(url_for('home'))
    
    return render_template('inscription.html')

@app.route('/home')
def home():
    with open(app_systeme.utilisateur_connecte['chemin_tenues'], 'r') as file:
        tenues = json.load(file)
    return render_template('home.html', tenues=tenues, name=app_systeme.utilisateur_connecte['name'])   

@app.route('/vestiaire')
def vestiaire():
    with open(app_systeme.utilisateur_connecte['chemin_vestiaire'], 'r') as file:
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
        if tenue != None:
            return render_template('generer.html', tenue=tenue)
        elif tenue == None:
            flash("Il n'y a pas assez de vêtements pour générer une tenue", 'error')
            return render_template('generer.html')
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

@app.route('/profile')
def profile():
    return render_template('profile.html', utilisateur=app_systeme.utilisateur_connecte)

if __name__ == '__main__':
    app.run(debug=True)
