from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT, telephone TEXT, adresse TEXT, produit TEXT, paiement TEXT, date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/catalogue')
def catalogue():
    return render_template('catalogue.html')

@app.route('/authentique')
def authentique():
    return render_template('authentique.html')

@app.route('/fake')
def fake():
    return render_template('fake.html')

@app.route('/commander', methods=['GET', 'POST'])
def commander():
    if request.method == 'POST':
        nom = request.form['nom']
        telephone = request.form['telephone']
        adresse = request.form['adresse']
        produit = request.form['produit']
        paiement = request.form['paiement']
        date = datetime.now().strftime('%Y-%m-%d %H:%M')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO commandes (nom, telephone, adresse, produit, paiement, date) VALUES (?, ?, ?, ?, ?, ?)', 
                       (nom, telephone, adresse, produit, paiement, date))
        conn.commit()
        conn.close()
        return render_template('merci.html', nom=nom)
    
    return render_template('commander.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM commandes ORDER BY date DESC')
    commandes = cursor.fetchall()
    conn.close()
    return str(commandes)

    init_db()
