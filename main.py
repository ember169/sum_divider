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
        <h3>Imposable</h3>
        <table>
            <tr>
                <td>Cash</td>
                <td>{{ result['cash'] }}</td>
            </tr>
            <tr>
                <td>PEA</td>
                <td>{{ result['pea'] }}</td>
            </tr>
            <tr>
                <td>LA (épargne)</td>
                <td>{{ result['epargne'] }}</td>
            </tr>
            <tr>
                <td>LLDS (impôts)</td>
                <td>{{ result['impots'] }}</td>
            </tr>
        </table>
        <h3>Non imposable</h3>
        <table>
            <tr>
                <td>Crypto</td>
                <td>{{ result['crypto'] }}</td>
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
            
            # Calcul de la crypto (20 % du montant total)
            crypto = round(montant * 1 / 10, 2)  # 20% de l'ensemble du montant total

            # Calcul du montant restant sans la crypto pour les impôts et autres enveloppes
            montant_sans_crypto = montant - crypto  # On retire la part Crypto du montant total

            impots = math.ceil(montant_sans_crypto * 0.30)  # 30% du montant restant après avoir retiré la crypto
            reste = montant_sans_crypto - impots  # On calcule le montant restant après le prélèvement des impôts
            cash = round(reste * 1 / 10, 2)  # 10% du montant restant après impôt
            pea = round(reste * 4 / 10, 2)  # 40% du montant restant après impôt
            epargne = round(reste * 2 / 10, 2)  # 20% du montant restant après impôt

            # Résultat final
            result = {
                "cash": cash,
                "pea": pea,
                "epargne": epargne,
                "impots": impots,
                "crypto": crypto,
            }
        except ValueError:
            result = None
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
