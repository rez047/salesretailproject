from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Review

reviews = Blueprint("reviews", __name__)


# =====================
# ADD REVIEW (5 STAR FIX)
# =====================
@reviews.route("/review/add", methods=["POST"])
@login_required
def add_review():

    data = request.json

    rating = int(data["rating"])

    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be 1-5"}), 400

    review = Review(
        buyer_id=current_user.id,
        product_id=data["product_id"],
        rating=rating,
        comment=data.get("comment", "")
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "review added"})


# =====================
# GET REVIEWS
# =====================
@reviews.route("/review/<int:product_id>")
def get_reviews(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    avg = 0
    if reviews:
        avg = sum([r.rating for r in reviews]) / len(reviews)

    return jsonify({
        "average": round(avg, 1),
        "reviews": [
            {
                "rating": r.rating,
                "comment": r.comment
            }
            for r in reviews
        ]
    })
