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
        /* Applique l'overlay sombre par-dessus le GIF en fond */
        body {
            font-family: 'Roboto', sans-serif;
            background-image: 
                linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* Overlay sombre */
                url('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3BnZGg4OGpjM2JueWE4c2F1Mm50MWgyNWUwNnkzN2ljbHdjOGU5biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YnkMcHgNIMW4Yfmjxr/giphy.gif'); /* GIF en fond */
            background-size: cover;
            background-position: center;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        h2 {
            font-family: 'Roboto', sans-serif;
            font-weight: 500;
            color: #ffffff;
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 400px;
            width: 90%;
            background-color: #1f1f1f;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            text-align: center;
        }
        label, input, button {
            font-family: 'Roboto', sans-serif;
            width: 100%;
            color: #e0e0e0;
            font-weight: 500;
            margin-bottom: 15px;
            max-width: 300px;
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
            font-weight: 500;
            text-align: center;
            max-width: 300px;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            max-width: 400px;
            width: 90%;
            background-color: #1f1f1f;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
            text-align: center;
            margin-bottom: 20px;
        }
        .total-row {
            font-weight: 700;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Roboto Mono', monospace;
            font-weight: 500;
        }
        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #333;
        }
        th {
            background-color: #333;
            color: #e0e0e0;
        }
        td {
            color: #ffffff;
        }
    </style>
</head>
<body>
    <form method="post">
        <h3>Montant à répartir</h3>
        <input type="text" name="montant" placeholder="Entrez le montant" required pattern="\\d+" title="Entrez un nombre entier">
        <button type="submit">Calculer</button>
    </form>
    {% if result %}
    <div class="results">
        <table>
            <tr class="total-row">
                <td>Montant total</td>
                <td>{{ result['montant_total'] }}</td>
            </tr>
            <tr>
                <td>Crypto</td>
                <td>{{ result['crypto'] }}</td>
            </tr>
            <tr class="total-row">
                <td>Montant imposable</td>
                <td>{{ result['imposable'] }}</td>
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
                <td>LLDS (impôts)</td>
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
def repartir_gains():
    result = None
    if request.method == "POST":
        try:
            montant = float(request.form["montant"])
            
            # Calculs pour chaque enveloppe
            crypto = round(montant * 1 / 10, 2)
            montant_sans_crypto = montant - crypto
            impots = math.ceil(montant_sans_crypto * 0.30)
            reste = montant_sans_crypto - impots
            cash = round(reste * 1 / 10, 2)
            pea = round(reste * 4 / 10, 2)
            epargne = round(reste * 2 / 10, 2)

            result = {
                "montant_total": montant,
                "cash": cash,
                "pea": pea,
                "epargne": epargne,
                "impots": impots,
                "crypto": crypto,
                "imposable": montant_sans_crypto,
            }
        except ValueError:
            result = None
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
