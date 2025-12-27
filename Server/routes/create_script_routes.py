from flask import Blueprint, render_template, request, jsonify

from Config.config import Config
from Recoil.recoil import Recoil

create_script_bp = Blueprint('create_script', __name__)

@create_script_bp.route("/create_script/create_new", methods=["POST"])
def create_new_script():
    data = request.get_json()
    script_name = data.get('scriptName', '')
    
    if not script_name:
        return jsonify({"success": False, "message": "Script name is required"}), 400
    
    Config.create_new_script_cfg(script_name)
    Config.load_saved_scripts()
    return jsonify({"success": True, "message": f"Script '{script_name}' created successfully"})

@create_script_bp.route("/create_script/get_script/<script_name>", methods=["GET"])
def get_script(script_name):
    script = Config.get_script_by_name(script_name)
    if script:
        return jsonify({"success": True, "script": script})
    return jsonify({"success": False, "message": "Script not found"}), 404

@create_script_bp.route("/create_script/update_script", methods=["POST"])
def update_script():
    data = request.get_json()
    script_name = data.get('scriptName', '')
    delay = data.get('delay', 100)
    steps = data.get('steps', [])
    
    if not script_name:
        return jsonify({"success": False, "message": "Script name is required"}), 400
    
    if Config.update_script(script_name, delay, steps):
        return jsonify({"success": True, "message": f"Script '{script_name}' updated successfully"})
    return jsonify({"success": False, "message": "Failed to update script"}), 500

@create_script_bp.route("/create_script/delete_script", methods=["POST"])
def delete_script():
    data = request.get_json()
    script_name = data.get('scriptName', '')
    
    if not script_name:
        return jsonify({"success": False, "message": "Script name is required"}), 400
    
    if Config.delete_script(script_name):
        return jsonify({"success": True, "message": f"Script '{script_name}' deleted successfully"})
    return jsonify({"success": False, "message": "Failed to delete script"}), 500

@create_script_bp.route("/create_script/set_test_mode", methods=["POST"])
def set_test_mode():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    enabled = data.get('enabled', False)
    delay = data.get('delay', 100)
    steps = data.get('steps', [])
    
    if enabled and steps:
        if not Recoil.test_mode_active:
            Recoil._saved_enabled = Recoil.enabled
            Recoil._saved_mode = Recoil.mode
            Recoil._saved_hipfire = Recoil.advanced_hipfire
        
        Recoil.test_mode_active = True
        Recoil.test_mode_steps = steps
        Recoil.test_mode_delay = delay
        Recoil.mode = "advanced-mode"
        Recoil.shot_count = 0
        Recoil.enabled = True
    else:
        Recoil.test_mode_active = False
        Recoil.enabled = Recoil._saved_enabled
        Recoil.mode = Recoil._saved_mode
        Recoil.advanced_hipfire = Recoil._saved_hipfire
        Recoil.shot_count = 0
    
    return jsonify({"success": True, "message": "Test mode updated"})

@create_script_bp.route("/create_script/set_test_hipfire", methods=["POST"])
def set_test_hipfire():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    hipfire = data.get('hipfire', False)
    Recoil.advanced_hipfire = hipfire
    
    return jsonify({"success": True, "message": "Hipfire mode updated"})

@create_script_bp.route("/create_script/get_test_state", methods=["GET"])
def get_test_state():
    return jsonify({
        "test_enabled": Recoil.test_mode_active and Recoil.enabled,
        "test_hipfire": Recoil.advanced_hipfire
    })

@create_script_bp.route("/create_script/disable_test_mode", methods=["POST"])
def disable_test_mode():
    if Recoil.test_mode_active:
        Recoil.test_mode_active = False

        Recoil.enabled = Recoil._saved_enabled
        Recoil.mode = Recoil._saved_mode
        Recoil.advanced_hipfire = Recoil._saved_hipfire
        Recoil.shot_count = 0
    return jsonify({"success": True, "message": "Test mode disabled"})

@create_script_bp.route("/create_script")
def create_script():
    Config.load_saved_scripts()

    return render_template("create_script.html", saved_scripts=Config.saved_scripts)
