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

    msg = Chat(
        sender_id=current_user.id,
        receiver_id=request.json.get("receiver_id"),
        product_id=request.json.get("product_id"),
        message=request.json["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"msg":"sent"})


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
