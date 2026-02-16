from flask import Flask, render_template, request, jsonify, session
import os
import requests

app = Flask(__name__)
app.secret_key = 'legobricks_secret_key_2026'

# ========== TELEGRAM ==========
TELEGRAM_TOKEN = '7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw'  # ЗАМЕНИ!
TELEGRAM_CHAT_ID = '123456789'  # ЗАМЕНИ!

# Товары
bricks = [
    {'id': 4, 'name': 'Бежевый Крым', 'color': 'beige_crimea', 'price': 3300, 'image': 'beige_crimea.png'},
    {'id': 3, 'name': 'Коричневый Манхэттен', 'color': 'brown_manhattan', 'price': 3200, 'image': 'brown_manhattan.png'},
    {'id': 5, 'name': 'Чёрный Кварц (двухцветный)', 'color': 'black_quartz', 'price': 3400, 'image': 'black_quartz.png'},
    {'id': 7, 'name': 'Бежевый микс (двухцветный)', 'color': 'beige_mix', 'price': 3400, 'image': 'beige_mix.png'},
    {'id': 8, 'name': 'Красный гранат (двухцветный)', 'color': 'red_garnet', 'price': 3300, 'image': 'red_garnet.png'},
    {'id': 9, 'name': 'Темно-серый Чикаго', 'color': 'dark_gray_chicago', 'price': 3100, 'image': 'dark_gray_chicago.png'},
    {'id': 10, 'name': 'Желтый песок', 'color': 'yellow_sand', 'price': 3400, 'image': 'yellow_sand.png'},
    {'id': 11, 'name': 'Коричнево-белый Мрамор', 'color': 'brown_white_marble', 'price': 3400, 'image': 'brown_white_marble.png'},
    {'id': 13, 'name': 'Бежевый кварц (двухцветный)', 'color': 'beige_quartz', 'price': 3300, 'image': 'beige_quartz.png'},
    {'id': 6, 'name': 'Серый Лондон', 'color': 'gray_london', 'price': 3000, 'image': 'gray_london.png'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', bricks=bricks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product/<int:product_id>')
def product(product_id):
    brick = next((b for b in bricks if b['id'] == product_id), None)
    return render_template('product.html', brick=brick)

# ========== КОРЗИНА ==========

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_details = []
    total = 0
    
    for item in cart_items:
        brick = next((b for b in bricks if b['id'] == item['id']), None)
        if brick:
            item_total = brick['price'] * item['quantity']
            total += item_total
            cart_details.append({
                'id': brick['id'],
                'name': brick['name'],
                'price': brick['price'],
                'quantity': item['quantity'],
                'image': brick['image'],
                'total': item_total
            })
    
    return render_template('cart.html', cart=cart_details, total=total)

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        cart.append({'id': product_id, 'quantity': quantity})
    
    session['cart'] = cart
    total_items = sum(item['quantity'] for item in cart)
    
    return jsonify({'success': True, 'cart_count': total_items})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.json
    product_id = data.get('id')
    quantity = data.get('quantity')
    
    cart = session.get('cart', [])
    
    for item in cart:
        if item['id'] == product_id:
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    
    session['cart'] = cart
    
    total_items = sum(item['quantity'] for item in cart)
    total_sum = 0
    for item in cart:
        brick = next((b for b in bricks if b['id'] == item['id']), None)
        if brick:
            total_sum += brick['price'] * item['quantity']
    
    return jsonify({
        'success': True,
        'cart_count': total_items,
        'total': total_sum
    })

@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return jsonify({'success': True})

@app.route('/api/cart/count', methods=['GET'])
def cart_count():
    cart = session.get('cart', [])
    total_items = sum(item['quantity'] for item in cart)
    return jsonify({'count': total_items})

# ========== ЗАКАЗ ==========

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    try:
        requests.post(url, data=data)
    except:
        pass

@app.route('/api/order/submit', methods=['POST'])
def submit_order():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    comment = data.get('comment', '')
    cart = data.get('cart', [])
    
    message = f"<b>🛍 НОВЫЙ ЗАКАЗ!</b>\n\n"
    message += f"<b>👤 Имя:</b> {name}\n"
    message += f"<b>📞 Телефон:</b> {phone}\n"
    if comment:
        message += f"<b>💬:</b> {comment}\n\n"
    message += f"<b>🛒 ТОВАРЫ:</b>\n"
    
    total = 0
    for item in cart:
        brick = next((b for b in bricks if b['id'] == item['id']), None)
        if brick:
            item_total = brick['price'] * item['quantity']
            total += item_total
            message += f"• {brick['name']} x {item['quantity']} = {item_total} сум\n"
    
    message += f"\n<b>💰 ИТОГО:</b> {total} сум"
    
    send_telegram_message(message)
    session['cart'] = []
    
    return jsonify({'success': True})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
