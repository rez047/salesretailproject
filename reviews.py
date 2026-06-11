from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Review, Order

reviews = Blueprint("reviews", __name__)


# =========================
# REVIEW PAGE (optional UI route)
# =========================
@reviews.route("/buyer/review/product/<int:product_id>")
@login_required
def review_page(product_id):
    return render_template("review_product.html", product_id=product_id)


# =========================
# ADD / UPDATE REVIEW (DELIVERED ONLY)
# =========================
@reviews.route("/review/add", methods=["POST"])
@login_required
def add_review():

    data = request.json
    product_id = data["product_id"]

    # verify delivered purchase
    order = Order.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
        status="delivered"
    ).first()

    if not order:
        return jsonify({"error": "Only delivered buyers can review"}), 403

    # one review per user per product (update allowed)
    review = Review.query.filter_by(
        buyer_id=current_user.id,
        product_id=product_id
    ).first()

    if review:
        review.rating = int(data["rating"])
        review.comment = data["comment"]
    else:
        review = Review(
            buyer_id=current_user.id,
            product_id=product_id,
            rating=int(data["rating"]),
            comment=data["comment"]
        )
        db.session.add(review)

    db.session.commit()

    return jsonify({"message": "saved"})


# =========================
# GET REVIEWS + AVERAGE
# =========================
@reviews.route("/review/<int:product_id>")
def get_reviews(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    if not reviews:
        return jsonify({
            "average": 0,
            "count": 0,
            "reviews": []
        })

    avg = sum(r.rating for r in reviews) / len(reviews)

    return jsonify({
        "average": round(avg, 1),
        "count": len(reviews),
        "reviews": [
            {"rating": r.rating, "comment": r.comment}
            for r in reviews
        ]
    })
