from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Chat
from utils import allowed_file

chat = Blueprint("chat", __name__)


# =========================
# SEND MESSAGE (PRODUCT CHAT)
# =========================
@chat.route("/chat/send", methods=["POST"])
@login_required
def send_message():

    data = request.json

    msg = Chat(
        product_id=data["product_id"],
        sender_id=current_user.id,
        message=data["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"message": "sent"})


# =========================
# GET MESSAGES FOR PRODUCT
# =========================
@chat.route("/chat/<int:product_id>", methods=["GET"])
@login_required
def get_chat(product_id):

    messages = Chat.query.filter_by(
        product_id=product_id
    ).order_by(Chat.created_at.asc()).all()

    return jsonify([
        {
            "from": m.sender_id,
            "msg": m.message,
            "time": m.created_at.strftime("%H:%M")
        }
        for m in messages
    ])
