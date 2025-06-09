from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Configuration ---
COST_CONFIG = {
    "vm": {
        "small": {"cpu": 2, "ram": 4, "costPerMonth": 50},
        "medium": {"cpu": 4, "ram": 8, "costPerMonth": 100},
        "large": {"cpu": 8, "ram": 16, "costPerMonth": 200},
    },
    "database": {
        "standard": {"storageGB": 100, "costPerMonth": 80},
        "performant": {"storageGB": 500, "costPerMonth": 300},
    },
    "storage": {
        "standard": 0.02,  # Cost per GB per month
        "ssd": 0.10,       # Cost per GB per month
    },
    "bandwidth": {
        "costPerGB": 0.09,  # Cost per GB egress per month
    },
}

@app.route('/api/calculate', methods=['POST'])
def calculate_cost():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    vm_type = data.get("vmType", "medium")
    vm_count = data.get("vmCount", 0)

    db_type = data.get("dbType", "standard")
    db_count = data.get("dbCount", 0)

    storage_type = data.get("storageType", "standard")
    storage_gb = data.get("storageGB", 0)

    bandwidth_gb = data.get("bandwidthGB", 0)

    total_cost = 0
    breakdown = {}

    # VM Costs
    if vm_count > 0 and vm_type in COST_CONFIG["vm"]:
        selected_vm = COST_CONFIG["vm"][vm_type]
        vm_cost = selected_vm["costPerMonth"] * vm_count
        breakdown["vms"] = {
            "label": f"VMs ({vm_count} x {vm_type})",
            "cost": vm_cost,
            "details": f"{selected_vm['cpu']} vCPU, {selected_vm['ram']} GB RAM each"
        }
        total_cost += vm_cost

    # Database Costs
    if db_count > 0 and db_type in COST_CONFIG["database"]:
        selected_db = COST_CONFIG["database"][db_type]
        db_cost = selected_db["costPerMonth"] * db_count
        breakdown["databases"] = {
            "label": f"Databases ({db_count} x {db_type})",
            "cost": db_cost,
            "details": f"~{selected_db['storageGB']} GB Storage each"
        }
        total_cost += db_cost

    # Storage Costs
    if storage_gb > 0 and storage_type in COST_CONFIG["storage"]:
        storage_cost = COST_CONFIG["storage"][storage_type] * storage_gb
        breakdown["storage"] = {
            "label": f"Storage ({storage_gb} GB {storage_type})",
            "cost": storage_cost,
            "details": f"${COST_CONFIG['storage'][storage_type]:.2f}/GB/Month"
        }
        total_cost += storage_cost

    # Bandwidth Costs
    if bandwidth_gb > 0:
        bandwidth_cost = COST_CONFIG["bandwidth"]["costPerGB"] * bandwidth_gb
        breakdown["bandwidth"] = {
            "label": f"Bandwidth ({bandwidth_gb} GB Egress)",
            "cost": bandwidth_cost,
            "details": f"${COST_CONFIG['bandwidth']['costPerGB']:.2f}/GB/Month"
        }
        total_cost += bandwidth_cost

    return jsonify({
        "totalCost": total_cost,
        "breakdown": breakdown
    })

if __name__ == '__main__':
    app.run(debug=True)