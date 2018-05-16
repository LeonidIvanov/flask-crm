import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_crm.db import get_db
from flask_crm.auth import login_required

app = Flask(__name__)
bp = Blueprint('orders', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    orders = db.execute(
        "SELECT 'order'.id, lead.first_name as lead_name, lead.phone,"
        "product.name as product_name, product.price, 'order'.product_qty,"
        "order_status.name as status "
        "FROM 'order' "
        "JOIN lead ON 'order'.lead_id = lead.id "
        "JOIN product ON 'order'.product_id = product.id "
        "JOIN order_status ON 'order'.status_id = order_status.id "
        "ORDER BY 'order'.id DESC "
    ).fetchall()
    return render_template('orders/index.html', orders=orders)


def new_orders_count_tag():
    db = get_db()
    new_orders_count = db.execute(
        "SELECT COUNT(*) FROM 'order' "
        "WHERE 'order'.status_id = 1 "
    ).fetchall()
    return dict(new_orders_count=new_orders_count[0][0])
