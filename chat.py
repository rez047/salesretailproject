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
        sender_id=current_user.id,
        receiver_id=data.get("receiver_id", 1),
        product_id=data["product_id"],
        message=data["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"message": "sent"})


# =========================
# LOAD PRODUCT CHAT
# =========================
@chat.route("/chat/product/<int:product_id>")
@login_required
def get_chat(product_id):

    messages = Chat.query.filter_by(product_id=product_id).all()

    return jsonify([
        {
            "from": m.sender_id,
            "msg": m.message
        }
        for m in messages
    ])
