from flask import Blueprint, jsonify, request
from ..auth import is_token_valid

bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@bp.get("/<int:order_id>")
def get_order(order_id):
    return jsonify({"id": order_id, "status": "pending", "total": 0})

@bp.post("")
def create_order():
    return jsonify({"id": 1, "total": sum(i["price"] for i in request.json["items"])}), 201

@bp.post("/<int:order_id>/confirm")
def confirm(order_id):
    return jsonify({"id": order_id, "status": "paid"})

@bp.post("/<int:order_id>/cancel")
def cancel(order_id):
    return jsonify({"id": order_id, "status": "cancelled"})
