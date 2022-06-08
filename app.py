import base64
import flask
import qrcode

from datetime import datetime
from io import BytesIO
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    qr = None
    if flask.request.method == 'POST':
        friend_code = flask.request.values.get('friend_code')
        """
        Les QR codes pour Shenron contiennent une seule chaîne de caractères, divisée en trois parties :
        
        • Le chiffre '4', aucune idée de pourquoi
        • Le code ami lui-même
        • Un timestamp (https://fr.wikipedia.org/wiki/Heure_Unix) dont les chiffres ont été interchangés avec la lettre de l'alphabet correspondante.
          Le format de timestamp utilisé est le format Unix à 13 chiffres (d'où la multiplication par 1000).
          Donc, 0 = A, 1 = B, 2 = C, ...
          
        Crédit à https://www.reddit.com/r/DragonballLegends/comments/gtzl9t/hey_guys_i_cracked_this_years_qr_code/ pour l'explication initiale.
        """
        transformed_timestamp = ''.join([chr(ord('A') + int(digit)) for digit in str(int(datetime.now().timestamp()*1000))])
        img = qrcode.make(f"4,{friend_code.lower()},{transformed_timestamp}")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return render_template("site.html", qr=qr)

if __name__ == '__main__':
    app.run()
