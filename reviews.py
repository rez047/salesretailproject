from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Review
from utils import allowed_file

reviews = Blueprint("reviews", __name__)

# --------------------
# ADD REVIEW
# --------------------
@reviews.route("/review/add", methods=["POST"])
@login_required
def add_review():
    data = request.json

    review = Review(
        buyer_id=current_user.id,
        product_id=data["product_id"],
        rating=data["rating"],
        comment=data["comment"]
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "review added"})


# --------------------
# GET REVIEWS FOR PRODUCT
# --------------------
@reviews.route("/review/<int:product_id>")
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()

    return jsonify([
        {
            "rating": r.rating,
            "comment": r.comment
        }
        for r in reviews
    ])