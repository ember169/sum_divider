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
            text-align: right;
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
    {% if show_table %}
    <form method="post" action="/calculer">
        <div class="results">
            <table>
                <tr class="total-row">
                    <td>Montant total</td>
                    <td><input type="text" name="montant_usdc" value="{{ montant_usdc }}" readonly></td>
                </tr>
                <tr>
                    <td>Crypto</td>
                    <td><input type="text" name="crypto" value="{{ result['crypto'] }}" readonly></td>
                </tr>
                <tr class="total-row">
                    <td>Montant imposable</td>
                    <td><input type="text" name="montant_eur" placeholder="Suggestion : {{ result['montant_eur'] }}" required></td>
                </tr>
                <tr class="taxable-row">
                    <td>PEA</td>
                    <td><input type="text" name="pea" placeholder="{{ result['pea'] }}"></td>
                </tr>
                <tr class="taxable-row">
                    <td>LA</td>
                    <td><input type="text" name="epargne" placeholder="{{ result['epargne'] }}"></td>
                </tr>
                <tr class="taxable-row">
                    <td>LDDS (impôts)</td>
                    <td><input type="text" name="impots" placeholder="{{ result['impots'] }}"></td>
                </tr>
                <tr class="taxable-row">
                    <td>Cash</td>
                    <td><input type="text" name="cash" placeholder="{{ result['cash'] }}"></td>
                </tr>
            </table>
        </div>
        <button type="submit">Valider les montants</button>
    </form>
    {% else %}
    <form method="post" action="/calcul_placeholder">
        <h3>Montant total en USDC</h3>
        <input type="text" name="montant_usdc" placeholder="Entrez le montant en USDC" required pattern="\\d+(\\.\\d{1,2})?" title="Entrez un montant valide">
        <button type="submit">Calculer le montant EUR suggéré</button>
    </form>
    {% endif %}

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

@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template, show_table=False, result=None)

@app.route("/calcul_placeholder", methods=["POST"])
def calcul_placeholder():
    try:
        montant_usdc = float(request.form["montant_usdc"])
        crypto = round(montant_usdc * 0.10, 2)
        montant_eur = round(montant_usdc - crypto, 2)
        impots = math.ceil(montant_eur * 0.30)
        reste = montant_eur - impots
        cash = round(reste * 0.10, 2)
        pea = round(reste * 0.40, 2)
        epargne = round(reste * 0.20, 2)

        result = {
            "montant_usdc": montant_usdc,
            "crypto": crypto,
            "montant_eur": montant_eur,
            "cash": cash,
            "pea": pea,
            "epargne": epargne,
            "impots": impots,
        }
        return render_template_string(html_template, show_table=True, result=result)
    except ValueError:
        return render_template_string(html_template, show_table=False, result=None)

@app.route("/calculer", methods=["POST"])
def repartir_gains():
    try:
        montant_usdc = float(request.form["montant_usdc"])
        montant_eur = float(request.form["montant_eur"])
        crypto = float(request.form["crypto"])
        pea = float(request.form["pea"])
        epargne = float(request.form["epargne"])
        impots = float(request.form["impots"])
        cash = float(request.form["cash"])

        result = {
            "montant_usdc": "{:,.2f}".format(montant_usdc).replace(",", " ").replace(".", ","),
            "crypto": "{:,.2f}".format(crypto).replace(",", " ").replace(".", ","),
            "montant_eur": "{:,.2f}".format(montant_eur).replace(",", " ").replace(".", ","),
            "cash": "{:,.2f}".format(cash).replace(",", " ").replace(".", ","),
            "pea": "{:,.2f}".format(pea).replace(",", " ").replace(".", ","),
            "epargne": "{:,.2f}".format(epargne).replace(",", " ").replace(".", ","),
            "impots": "{:,.2f}".format(impots).replace(",", " ").replace(".", ","),
        }
        return render_template_string(html_template, show_table=False, result=result)
    except ValueError:
        return render_template_string(html_template, show_table=False, result=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)