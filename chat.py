from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Chat

chat = Blueprint("chat", __name__)


# =========================
# PRODUCT CHAT PAGE
# =========================
@chat.route("/chat/product/<int:product_id>")
@login_required
def product_chat_page(product_id):
    return render_template("chat_product.html", product_id=product_id)


# =========================
# LOAD CHAT MESSAGES
# =========================
@chat.route("/chat/messages/<int:product_id>")
@login_required
def get_messages(product_id):

    messages = Chat.query.filter_by(product_id=product_id).all()

    return jsonify([
        {
            "from": m.sender_id,
            "to": m.receiver_id,
            "msg": m.message
        }
        for m in messages
    ])


# =========================
# SEND MESSAGE
# =========================
@chat.route("/chat/send", methods=["POST"])
@login_required
def send_message():

    data = request.json

    msg = Chat(
        product_id=data.get("product_id"),
        sender_id=current_user.id,
        receiver_id=data.get("receiver_id"),
        message=data["message"]
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"status": "sent"})

@chat.route("/chat/inbox")
@login_required
def chat_inbox():

    # optional: admin/retailer view of all chats
    messages = Chat.query.all()

    return render_template(
        "chat_inbox.html",
        messages=messages
    )
