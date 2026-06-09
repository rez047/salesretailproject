from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from models import db, Order, Product

retailer_bp = Blueprint("retailer", __name__)
