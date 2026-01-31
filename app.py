from flask import Flask, request, redirect, send_file, abort, jsonify

import os

app = Flask(__name__)

STAFF_PASSWORD = 'EERIE'

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/staff_login")
def staff_sign():
    return send_file("staff_login.html")

@app.route("/orders", methods=['GET'])
def pull_page():
    token = request.args.get("key")

    if token != STAFF_PASSWORD:
        abort(403)
    return send_file("assign_pulls.html")

@app.route("/load_employees", methods=["GET"])
def fetch_orders():
    from Pull_Automator.employees import GathingSkills
    employees = GathingSkills()  # this is your dictionary

    employees_dict = employees.employees
    return jsonify({
        "employees": employees_dict
    })

@app.route("/assign_pulls", methods=["POST"])
def assign_pulls():
    data = request.get_json()

    from Pull_Automator.orders import OrderSheet
    from Pull_Automator.automator import assign_pulls
    orders = OrderSheet().orders
    ass = assign_pulls(data, orders)
    print(ass.unassigned_items)
    return jsonify({
        "columns": ass.assignments.columns.tolist(),
        "assignments": ass.assignments.to_dict(orient="records"),
        "unassigned_items": ass.unassigned_items,
        "unrecognized_items": ass.unrecognized_items
    })

@app.route("/login", methods=["POST"])
def login():
    entered = request.form.get("password")

    if entered == STAFF_PASSWORD:
        return redirect(f"https://pursersbank-production.up.railway.app/orders?key={STAFF_PASSWORD}")
    else:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)