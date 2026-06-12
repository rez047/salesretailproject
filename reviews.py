from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Review, Order, Product

reviews_bp = Blueprint("reviews", __name__)


# =========================
# REVIEW PAGE
# =========================
@reviews_bp.route("/review/product/<int:product_id>")
@login_required
def review_page(product_id):
    return render_template("review_product.html", product_id=product_id)


# =========================
# ADD / UPDATE REVIEW
# =========================
@reviews_bp.route("/review/add", methods=["POST"])
@login_required
def add_review():

    data = request.json
    product_id = data["product_id"]

    order = Order.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
        status="delivered"
    ).first()

    if not order:
        return jsonify({"error": "Only delivered buyers can review"}), 403

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

    update_product_rating(product_id)

    return jsonify({"message": "saved"})


# =========================
# GET REVIEWS
# =========================
@reviews_bp.route("/review/<int:product_id>")
def get_reviews(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    if not reviews:
        return jsonify({"average": 0, "count": 0, "reviews": []})

    return jsonify({
        "average": round(sum(r.rating for r in reviews) / len(reviews), 1),
        "count": len(reviews),
        "reviews": [
            {"rating": r.rating, "comment": r.comment}
            for r in reviews
        ]
    })


# =========================
# UPDATE PRODUCT RATING (AUTO)
# =========================
def update_product_rating(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    product = Product.query.get(product_id)

    if reviews:
        product.avg_rating = sum(r.rating for r in reviews) / len(reviews)
        product.rating_count = len(reviews)
    else:
        product.avg_rating = 0
        product.rating_count = 0

    db.session.commit()
