from flask import Flask, jsonify, send_file
from flask_cors import CORS  # <--- added
import os

app = Flask(__name__)
CORS(app)  # <--- added

@app.route("/orders", methods=["GET"])
def fetch_orders():
    from Pull_Automator.employees import GathingSkills
    from Pull_Automator.orders import OrderSheet
    from Pull_Automator.automator import assign_pulls
    orders = OrderSheet().orders
    employees = GathingSkills()
    ass = assign_pulls(employees, orders)
    return jsonify({
        "columns": ass.assignments.columns.tolist(),
        "assignments": ass.assignments.to_dict(orient="records"),
        "unassigned_items": ass.unassigned_items,
        "unrecognized_items": ass.unrecognized_items
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
