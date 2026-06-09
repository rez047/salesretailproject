from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Chat
from utils import allowed_file

chat = Blueprint("chat", __name__)

# --------------------
# SEND MESSAGE
# --------------------
@chat.route("/chat/send", methods=["POST"])
@login_required
def send_message():
    data = request.json

    msg = Chat(
        sender_id=current_user.id,
        receiver_id=data["receiver_id"],
        message=data["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"message": "sent"})


# --------------------
# GET MESSAGES
# --------------------
@chat.route("/chat/<int:user_id>", methods=["GET"])
@login_required
def get_chat(user_id):
    messages = Chat.query.filter(
        ((Chat.sender_id == current_user.id) & (Chat.receiver_id == user_id)) |
        ((Chat.sender_id == user_id) & (Chat.receiver_id == current_user.id))
    ).all()

    return jsonify([
        {"from": m.sender_id, "to": m.receiver_id, "msg": m.message}
        for m in messages
    ])