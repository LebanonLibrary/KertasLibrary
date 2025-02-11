from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '298c12920446cb7f9f562851e172334d'  # For using session

# Setup MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MahdiMortada_2009",
    database="book_store"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/english_books')
def english_books():
    books = [
        {"name": "English book 1", "price": "$10", "image": "ac altair.jpg", "id": 1},
        {"name": "English Book 2", "price": "$15", "image": "ac malyon.jpg", "id": 2},
    ]
    return render_template('english_books.html', books=books)

@app.route('/arabic_books')
def arabic_books():
    books = [
        {"name": "انسان", "price": "$12", "image": "arabic1.jpg", "id": 1},
        {"name": "Arabic Book 2", "price": "$18", "image": "arabic2.jpg", "id": 2},
    ]
    return render_template('arabic_books.html', books=books)

@app.route('/book_detail/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    books = [
        {"name": "English Book 1", "price": "$10", "image": "ac altair.jpg", "id": 1},
        {"name": "English Book 2", "price": "$15", "image": "book2.jpg", "id": 2},
        {"name": "Arabic Book 1", "price": "$12", "image": "arabic1.jpg", "id": 3},
        {"name": "Arabic Book 2", "price": "$18", "image": "arabic2.jpg", "id": 4},
    ]
    book = next(book for book in books if book['id'] == int(book_id))

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        book['quantity'] = quantity
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(book)
        session.modified = True
        return redirect(url_for('cart'))

    return render_template('book_detail.html', book=book)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)  # Clear the cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        
        cursor = db.cursor()
        for item in session.get('cart', []):
            cursor.execute("INSERT INTO orders (name, phone, book_name, order_date) VALUES (%s, %s, %s, NOW())", 
                           (name, phone, item['name']))
        db.commit()

        session.pop('cart', None)  # Clear cart
        return render_template('thank_you.html')

    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)

