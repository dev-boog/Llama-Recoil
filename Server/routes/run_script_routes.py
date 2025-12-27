from flask import Blueprint, render_template, request, jsonify
from Recoil.recoil import Recoil
from Config.config import Config

run_script_bp = Blueprint('run_script', __name__)

@run_script_bp.route("/run_script/get_state", methods=["GET"])
def get_state():
    return jsonify({
        "recoil_enabled": Recoil.enabled,
        "recoil_mode": Recoil.mode,
        "simple_x": Recoil.simple_mode_x,
        "simple_y": Recoil.simple_mode_y,
        "simple_delay": int(Recoil.simple_mode_delay * 1000),  # Convert back to ms
        "simple_hipfire": Recoil.simple_hipfire,
        "advanced_selected_script": Recoil.advanced_mode_script,
        "advanced_loop_on_complete": Recoil.advanced_loop_when_complete,
        "advanced_hipfire": Recoil.advanced_hipfire
    })

@run_script_bp.route("/run_script/apply_settings", methods=["POST"])
def apply_settings():
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    Recoil.enabled = data.get("recoil_enabled", False)
    Recoil.mode = data.get("recoil_mode", "simple-mode")
    
    simple_x = data.get("simple_x", "0")
    simple_y = data.get("simple_y", "0")
    simple_delay = data.get("simple_delay", "100")
    
    Recoil.simple_mode_x = int(simple_x) if simple_x else 0
    Recoil.simple_mode_y = int(simple_y) if simple_y else 0

    simple_delay_ms = float(simple_delay) if simple_delay else 100
    Recoil.simple_mode_delay = simple_delay_ms / 1000.0
    Recoil.simple_hipfire = data.get("simple_hipfire", False)

    Recoil.advanced_mode_script = data.get("advanced_selected_script", "")
    Recoil.advanced_loop_when_complete = data.get("advanced_loop_on_complete", False)
    Recoil.advanced_hipfire = data.get("advanced_hipfire", False)

    return jsonify({"success": True, "message": "Settings applied"})


@run_script_bp.route("/run_script")
def run_script():
    Config.load_saved_scripts()
    return render_template("run_script.html", saved_scripts=Config.saved_scripts, loaded_script=Config.get_script_by_name(Recoil.advanced_mode_script))
