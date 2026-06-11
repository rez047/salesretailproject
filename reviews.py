from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Review, Order

reviews = Blueprint("reviews", __name__)


# =========================
# ADD REVIEW (VERIFIED BUYER ONLY)
# =========================
@reviews.route("/review/product/<int:product_id>")
@login_required
def review_page(product_id):

    return render_template(
        "review_product.html",
        product_id=product_id
    )
    

@reviews.route("/review/add", methods=["POST"])
@login_required
def add_review():

    data = request.json

    product_id = data["product_id"]

    # 🔒 CHECK IF USER BOUGHT PRODUCT
    order = Order.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
        status="delivered"
    ).first()

    if not order:
        return jsonify({"error": "Only verified buyers can review"}), 403

    # prevent duplicate review
    existing = Review.query.filter_by(
        buyer_id=current_user.id,
        product_id=product_id
    ).first()

    if existing:
        existing.rating = data["rating"]
        existing.comment = data["comment"]
    else:
        review = Review(
            buyer_id=current_user.id,
            product_id=product_id,
            rating=data["rating"],
            comment=data["comment"]
        )
        db.session.add(review)

    db.session.commit()

    return jsonify({"message": "review saved"})


# =========================
# GET REVIEWS + STATS
# =========================
@reviews.route("/review/<int:product_id>")
def get_reviews(product_id):

    reviews = Review.query.filter_by(product_id=product_id).all()

    if not reviews:
        return jsonify({
            "average": 0,
            "count": 0,
            "ratings": [],
            "reviews": []
        })

    total = sum(r.rating for r in reviews)
    avg = round(total / len(reviews), 1)

    return jsonify({
        "average": avg,
        "count": len(reviews),
        "ratings": [r.rating for r in reviews],
        "reviews": [
            {
                "rating": r.rating,
                "comment": r.comment
            }
            for r in reviews
        ]
    })
