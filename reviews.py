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

    product = Product.query.get(product_id)

    if not product:
        return "Product not found", 404


    return render_template(
        "review_product.html",
        product=product
    )



# =========================
# ADD REVIEW
# =========================
@reviews_bp.route("/review/add", methods=["POST"])
@login_required
def add_review():


    product_id = request.form.get("product_id")
    rating = request.form.get("rating")
    comment = request.form.get("comment")



    if not product_id or not rating:
        return "Missing review data",400



    product_id = int(product_id)



    # buyer must have received product
    order = Order.query.filter(
        Order.user_id == current_user.id,
        Order.product_id == product_id,
        Order.status.in_(
            ["delivered","Delivered"]
        )
    ).first()



    if not order:

        return """
        You can only review products after delivery.
        """,403




    review = Review.query.filter_by(
        buyer_id=current_user.id,
        product_id=product_id
    ).first()



    if review:

        review.rating = int(rating)
        review.comment = comment


    else:

        review = Review(
            buyer_id=current_user.id,
            product_id=product_id,
            rating=int(rating),
            comment=comment
        )

        db.session.add(review)




    db.session.commit()


    update_product_rating(product_id)



    return """
    Review saved successfully.
    <br>
    <a href='/buyer'>Back</a>
    """





# =========================
# SHOW REVIEWS
# =========================
@reviews_bp.route("/review/<int:product_id>")
def get_reviews(product_id):


    reviews = Review.query.filter_by(
        product_id=product_id
    ).all()



    if not reviews:

        return jsonify({
            "average":0,
            "count":0,
            "reviews":[]
        })



    return jsonify({

        "average":
        round(
            sum(r.rating for r in reviews)
            /
            len(reviews),
            1
        ),


        "count":len(reviews),


        "reviews":[

            {
            "rating":r.rating,
            "comment":r.comment
            }

            for r in reviews

        ]

    })





# =========================
# UPDATE PRODUCT RATING
# =========================
def update_product_rating(product_id):


    reviews = Review.query.filter_by(
        product_id=product_id
    ).all()


    product = Product.query.get(product_id)



    if not product:
        return



    if reviews:

        product.avg_rating = (
            sum(r.rating for r in reviews)
            /
            len(reviews)
        )

        product.rating_count=len(reviews)


    else:

        product.avg_rating=0
        product.rating_count=0



    db.session.commit()
