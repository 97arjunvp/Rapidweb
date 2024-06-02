from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Category, Book, Order
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', categories=categories)

@main_bp.route('/books/<int:categoryid>')
def bookcategory(categoryid):
    books = Book.query.filter(Book.category_id==categoryid)
    return render_template('bookcategory.html', books=books)
@main_bp.route('/books/')

def search():

    search = request.args.get('search')
    search = '%{}%'.format(search)
    books = Book.query.filter(Book.name.like(search)).all()
    return render_template('bookcategory.html', books=books)
# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    book_id = request.values.get('book_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    total_price = 0
    if order is not None:
        for book in order.books:
            total_price = total_price + book.price
    
    # are we adding an item?
    if book_id is not None and order is not None:
        book = Book.query.get(book_id)
        if book not in order.books:
            try:
                order.books.append(book)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('Item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, total_price=total_price)

# Delete specific basket items
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        book_to_delete = Book.query.get(id)
        try:
            order.books.remove(book_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for book in order.books:
                totalcost = totalcost + book.price
            order.totalcost = totalcost
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form)