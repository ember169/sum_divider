from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def repartir_gains():
    result = None
    if request.method == "POST":
        try:
            montant = float(request.form.get("montant", 0))
            imposition = float(request.form.get("imposition", 0))

            # Calcul des montants imposables
            montant_imposable = montant * ((100 - imposition) / 100)
            impots = montant - montant_imposable

            # Récupération des enveloppes dynamiques
            enveloppes = []
            i = 1
            while f"enveloppe-nom-{i}" in request.form:
                nom = request.form.get(f"enveloppe-nom-{i}")
                pourcentage = float(request.form.get(f"enveloppe-pourcentage-{i}", 0))
                montant_enveloppe = round(montant_imposable * (pourcentage / 100), 2)
                enveloppes.append({
                    "nom": nom,
                    "montant": "{:,.2f}".format(montant_enveloppe).replace(",", " ").replace(".", ",")
                })
                i += 1

            def format_number(value):
                return "{:,.2f}".format(value).replace(",", " ").replace(".", ",")

            result = {
                "montant_total": format_number(montant),
                "montant_imposable": format_number(montant_imposable),
                "impots": format_number(impots),
                "enveloppes": enveloppes
            }
        except ValueError:
            result = None  # Gérer les entrées invalides de manière appropriée

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
