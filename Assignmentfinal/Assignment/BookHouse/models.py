from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultcity.jpg')
    books = db.relationship('Book', backref='Category', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.description}"
orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('book_id',db.Integer,db.ForeignKey('books.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'book_id') )

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    author = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def __repr__(self):
        return f"ID: {self.id}\nName: {self.name}\nAuthor: {self.author}\nDescription: {self.description}\nPrice: {self.price}\nCategory: {self.category_id}"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    books = db.relationship("Book", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        return f"ID: {self.id}\nStatus: {self.status}\nFirst Name: {self.first_name}\nSurname: {self.surname}\nEmail: {self.email}\nPhone: {self.phone}\nBooks: {self.books}\nTotal Cost: ${self.totalcost}"
