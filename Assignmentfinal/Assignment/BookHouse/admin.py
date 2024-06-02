from flask import Blueprint
from . import db
from .models import Category, Book, Order
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
