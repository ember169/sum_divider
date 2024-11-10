from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Répartition des gains</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@700&family=Roboto:wght@500&display=swap" rel="stylesheet">
    <style>
        /* Styles CSS */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        h3 {
            text-align: center;
        }
        form {
            background-color: #1f1f1f;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            max-width: 400px;
            width: 90%;
        }
        label, input, button {
            width: 100%;
            margin-bottom: 15px;
        }
        input {
            background-color: #333;
            border: none;
            padding: 10px;
            color: #e0e0e0;
            border-radius: 5px;
            font-size: 16px;
            text-align: center;
        }
        button {
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .results {
            max-width: 400px;
            width: 90%;
            background-color: #1f1f1f;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Roboto Mono', monospace;
        }
        th, td {
            padding: 12px;
            text-align: right;
            border: 1px solid #333;
        }
        th {
            background-color: #333;
            color: #e0e0e0;
        }
    </style>
</head>
<body>
    <form method="post">
        <h3>Montant total en USDC</h3>
        <input type="text" name="montant_usdc" placeholder="Entrez le montant en USDC" required pattern="\\d+(\\.\\d{1,2})?" title="Entrez un montant valide" value="{{ montant_usdc }}">
        
        {% if montant_placeholder %}
            <h3>Montant restant en EUR (hors crypto)</h3>
            <input type="text" name="montant_eur" placeholder="Suggestion : {{ montant_placeholder }}" required pattern="\\d+(\\.\\d{1,2})?" title="Entrez un montant valide" value="{{ montant_eur }}">
            <button type="submit" formaction="/calculer">Valider les montants</button>
        {% else %}
            <button type="submit" formaction="/calcul_placeholder">Calculer le montant EUR suggéré</button>
        {% endif %}
    </form>
    
    {% if result %}
    <div class="results">
        <table>
            <tr class="total-row">
                <td>Montant total</td>
                <td>{{ result['montant_usdc'] }}</td>
            </tr>
            <tr>
                <td>Crypto</td>
                <td>{{ result['crypto'] }}</td>
            </tr>
            <tr class="total-row">
                <td>Montant imposable</td>
                <td>{{ result['montant_eur'] }}</td>
            </tr>
            <tr class="taxable-row">
                <td>PEA</td>
                <td>{{ result['pea'] }}</td>
            </tr>
            <tr class="taxable-row">
                <td>LA</td>
                <td>{{ result['epargne'] }}</td>
            </tr>
            <tr class="taxable-row">
                <td>LDDS (impôts)</td>
                <td>{{ result['impots'] }}</td>
            </tr>
            <tr class="taxable-row">
                <td>Cash</td>
                <td>{{ result['cash'] }}</td>
            </tr>
        </table>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template_string(html_template, montant_placeholder=None, result=None)

@app.route("/calcul_placeholder", methods=["POST"])
def calcul_placeholder():
    try:
        montant_usdc = float(request.form["montant_usdc"])
        crypto = round(montant_usdc * 0.10, 2)
        montant_placeholder = round(montant_usdc - crypto, 2)
        return render_template_string(html_template, montant_usdc=montant_usdc, montant_placeholder=montant_placeholder, result=None)
    except ValueError:
        return render_template_string(html_template, montant_placeholder=None, result=None)

@app.route("/calculer", methods=["POST"])
def repartir_gains():
    try:
        montant_usdc = float(request.form["montant_usdc"])
        montant_eur = float(request.form["montant_eur"])

        # Calcul de la part crypto (10 % du montant total en USDC)
        crypto = round(montant_usdc * 0.10, 2)

        # Calcul du montant imposable (le montant EUR entré manuellement)
        impots = math.ceil(montant_eur * 0.30)
        reste = montant_eur - impots
        cash = round(reste * 0.10, 2)
        pea = round(reste * 0.40, 2)
        epargne = round(reste * 0.20, 2)

        # Formattage des montants
        def format_number(value):
            return "{:,.2f}".format(value).replace(",", " ").replace(".", ",")

        result = {
            "montant_usdc": format_number(montant_usdc),
            "crypto": format_number(crypto),
            "montant_eur": format_number(montant_eur),
            "cash": format_number(cash),
            "pea": format_number(pea),
            "epargne": format_number(epargne),
            "impots": format_number(impots),
        }
        return render_template_string(html_template, montant_placeholder=None, result=result)
    except ValueError:
        return render_template_string(html_template, montant_placeholder=None, result=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)