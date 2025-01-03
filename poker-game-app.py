from flask import Flask, request, jsonify, send_from_directory
import os

print("Goodbye, World!")
app = Flask(__name__, static_folder="Public")


# Algorithm to calculate transactions
def minimize_transactions(players):
    creditors = [player for player in players if player['balance'] > 0]
    debtors = [player for player in players if player['balance'] < 0]

    transactions = []

    while creditors and debtors:
        creditor = creditors[0]
        debtor = debtors[0]

        payment = min(creditor['balance'], -debtor['balance'])
        transactions.append({
            "from": debtor['name'],
            "to": creditor['name'],
            "amount": payment,
        })

        creditor['balance'] -= payment
        debtor['balance'] += payment

        if creditor['balance'] == 0:
            creditors.pop(0)
        if debtor['balance'] == 0:
            debtors.pop(0)

    return transactions

# API route for calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    players = data.get('players')

    if not players or not isinstance(players, list):
        return jsonify({"error": "Invalid input. 'players' must be a list."}), 400

    try:
        transactions = minimize_transactions(players)
        return jsonify({"transactions": transactions})
    except Exception as e:
        return jsonify({"error": "Internal server error."}), 500

# Serve static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
