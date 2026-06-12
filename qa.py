from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models import db, ProductQuestion, Product


qa = Blueprint(
    "qa",
    __name__
)



# ==========================
# ASK PRODUCT QUESTION
# ==========================

@qa.route(
    "/product/<int:product_id>/question",
    methods=["POST"]
)
@market.route("/product/<int:product_id>/question", methods=["POST"])
@login_required
def ask_question(product_id):
    q = Question(
        product_id=product_id,
        user_id=current_user.id,
        question=request.json["question"]
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({"msg":"sent"})





# ==========================
# VIEW QUESTIONS
# ==========================

@qa.route(
    "/product/<int:product_id>/questions"
)
def questions(product_id):

    qs=ProductQuestion.query.filter_by(
        product_id=product_id
    ).all()


    return jsonify([

        {
        "id":q.id,
        "question":q.question,
        "answer":q.answer
        }

        for q in qs

    ])





# ==========================
# ANSWER QUESTION
# ADMIN OR RETAILER
# ==========================

@qa.route(
    "/question/<int:id>/answer",
    methods=["POST"]
)
@login_required
def answer(id):


    if current_user.role not in [
        "admin",
        "retailer"
    ]:
        return jsonify(
            {"error":"Unauthorized"}
        ),403


    q=ProductQuestion.query.get(id)


    q.answer=request.json["answer"]
    q.answered_by=current_user.id


    db.session.commit()


    return jsonify(
        {"message":"answered"}
    )
