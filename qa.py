from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Question, Product

qa = Blueprint("qa", __name__)


@qa.route("/product/<int:product_id>/questions")
def get_questions(product_id):

    qs = Question.query.filter_by(product_id=product_id).all()

    return jsonify([
        {
            "id": q.id,
            "question": q.question,
            "answer": q.answer
        }
        for q in qs
    ])


@qa.route("/product/<int:product_id>/question", methods=["POST"])
@login_required
def ask_question(product_id):

    data = request.json

    q = Question(
        product_id=product_id,
        user_id=current_user.id,
        question=data["question"]
    )

    db.session.add(q)
    db.session.commit()

    return jsonify({"msg": "sent"})


@qa.route("/question/<int:id>/answer", methods=["POST"])
@login_required
def answer_question(id):

    q = Question.query.get(id)
    q.answer = request.json["answer"]

    db.session.commit()

    return jsonify({"msg": "answered"})
