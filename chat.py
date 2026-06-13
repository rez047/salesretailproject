from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user

from extensions import db
from models import Chat, User


chat = Blueprint("chat", __name__, url_prefix="/chat")


# =====================================
# PRODUCT CHAT (BUYER ↔ RETAILER)
# =====================================

@chat.route("/product/<int:product_id>")
@login_required
def product_chat(product_id):

    messages = Chat.query.filter_by(
        product_id=product_id
    ).order_by(Chat.id.asc()).all()


    return jsonify([
        {
            "from": m.sender_id,
            "to": m.receiver_id,
            "msg": m.message
        }
        for m in messages
    ])



# =====================================
# SEND MESSAGE
# =====================================

@chat.route("/send", methods=["POST"])
@login_required
def send_message():

    data = request.json


    message = Chat(
        product_id=data.get("product_id"),

        sender_id=current_user.id,

        receiver_id=data.get("receiver_id"),

        message=data.get("message")
    )


    db.session.add(message)

    db.session.commit()


    return jsonify({
        "status":"sent"
    })



# =====================================
# ADMIN / USER CHAT INBOX
# =====================================

@chat.route("/inbox")
@login_required
def inbox():

    messages = Chat.query.filter(
        (Chat.sender_id == current_user.id) |
        (Chat.receiver_id == current_user.id)
    ).order_by(
        Chat.id.desc()
    ).all()


    return render_template(
        "chat_inbox.html",
        messages=messages
    )
