from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime
from abc import ABC, abstractmethod

# --- OOP IMPLEMENTATION ---

# Abstraction: Abstract base class for entities
class Entity(ABC):
    _data = []

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    def find_by_id(cls, entity_id):
        return next((item for item in cls._data if item['id'] == entity_id), None)

    @classmethod
    def search(cls, query, fields):
        if not query:
            return cls._data
        return [item for item in cls._data if any(query.lower() in str(item.get(field, '')).lower() for field in fields)]

# Encapsulation: User class with private attributes
class User(Entity):
    _data = [
        {'username': 'admin', 'password': 'admin', 'role': 'admin'},
        {'username': 'cashier', 'password': 'cashier', 'role': 'cashier'}
    ]

    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role

    # Encapsulation: Getters
    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def role(self):
        return self.__role

    @classmethod
    def authenticate(cls, username, password):
        user = next((u for u in cls._data if u['username'] == username and u['password'] == password), None)
        return user

# Inheritance: Customer inherits from Entity
class Customer(Entity):
    _data = []

    def __init__(self, customer_id, name, contact, address):
        self.__id = customer_id
        self.__name = name
        self.__contact = contact
        self.__address = address

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def contact(self):
        return self.__contact

    @property
    def address(self):
        return self.__address

    def save(self):
        existing = self.find_by_id(self.__id)
        if existing:
            existing.update({'name': self.__name, 'contact': self.__contact, 'address': self.__address})
        else:
            self._data.append({'id': self.__id, 'name': self.__name, 'contact': self.__contact, 'address': self.__address, 'status': 'Active'})

    def delete(self):
        self._data[:] = [c for c in self._data if c['id'] != self.__id]

# Inheritance: Product inherits from Entity
class Product(Entity):
    _data = []

    def __init__(self, product_id, name, category, price, stock):
        self.__id = product_id
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def category(self):
        return self.__category

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def save(self):
        existing = self.find_by_id(self.__id)
        if existing:
            existing.update({'name': self.__name, 'category': self.__category, 'price': self.__price, 'stock': self.__stock})
        else:
            self._data.append({'id': self.__id, 'name': self.__name, 'category': self.__category, 'price': self.__price, 'stock': self.__stock, 'status': 'active'})

    def delete(self):
        self._data[:] = [p for p in self._data if p['id'] != self.__id]

# Inheritance: Sale inherits from Entity
class Sale(Entity):
    _data = []

    def __init__(self, customer_id, product, quantity, total, date, customer, payment_type):
        self.__customer_id = customer_id
        self.__product = product
        self.__quantity = quantity
        self.__total = total
        self.__date = date
        self.__customer = customer
        self.__payment_type = payment_type

    def save(self):
        sale_id = len(self._data) + 1
        self._data.append({
            'id': sale_id,
            'customer_id': self.__customer_id,
            'product': self.__product,
            'customer': self.__customer,
            'quantity': self.__quantity,
            'total': self.__total,
            'date': self.__date,
            'payment_type': self.__payment_type
        })

# Inheritance: Bill inherits from Entity
class Bill(Entity):
    _data = []

    def __init__(self, customer_id, customer, amount, date, status, description, bill_type):
        self.__customer_id = customer_id
        self.__customer = customer
        self.__amount = amount
        self.__date = date
        self.__status = status
        self.__description = description
        self.__type = bill_type

    def save(self):
        bill_id = max([b['id'] for b in self._data], default=0) + 1
        self._data.append({
            'id': bill_id,
            'customer_id': self.__customer_id,
            'customer': self.__customer,
            'amount': self.__amount,
            'date': self.__date,
            'status': self.__status,
            'description': self.__description,
            'type': self.__type
        })

# Inheritance: Activity inherits from Entity
class Activity(Entity):
    _data = []

    def __init__(self, activity_type, description, user):
        self.__type = activity_type
        self.__description = description
        self.__user = user
        self.__timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        self._data.append({
            'type': self.__type,
            'description': self.__description,
            'user': self.__user,
            'timestamp': self.__timestamp
        })

    def delete(self):
        # Activity logs don't need deletion, but required by abstract base class
        pass

# Polymorphism: Dashboard class with static method
class Dashboard:
    @staticmethod
    def get_metrics():
        total_sales = sum(s['total'] for s in Sale._data)
        total_customers = len(Customer._data)
        total_products = len(Product._data)
        total_bills = len(Bill._data)
        paid_bills = len([b for b in Bill._data if b['status'] == 'Paid'])
        unpaid_bills = total_bills - paid_bills
        total_revenue = sum(b['amount'] for b in Bill._data if b['status'] == 'Paid')
        pending_bills = len([b for b in Bill._data if b['status'] == 'Pending'])

        return {
            'total_sales': total_sales,
            'total_customers': total_customers,
            'total_products': total_products,
            'total_bills': total_bills,
            'paid_bills': paid_bills,
            'unpaid_bills': unpaid_bills,
            'total_revenue': total_revenue,
            'pending_bills': pending_bills
        }

# Encapsulation: POSApp class with private app instance
class POSApp:
    def __init__(self):
        self.__app = Flask(__name__, template_folder='templates', static_folder='Static')
        self.__app.secret_key = 'your_secret_key_here'
        self.setup_routes()

    @property
    def app(self):
        return self.__app

    def setup_routes(self):
        @self.__app.route('/')
        def index():
            return render_template('index.html')

        @self.__app.route('/login', methods=['POST', 'GET'])
        def login():
            error = None
            if request.method == "POST":
                username = request.form.get('username', '').strip().lower()
                password = request.form.get('password', '').strip()

                user = User.authenticate(username, password)
                if user:
                    Activity('login', f'User {username} logged in', username).save()
                    session['username'] = username
                    session['role'] = user['role']
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    elif user['role'] == 'cashier':
                        return redirect(url_for('cashier_dashboard'))
                else:
                    error = "Invalid username or password!"
            return render_template('login.html', error=error)

        @self.__app.route('/admin')
        def admin_dashboard():
            return render_template('admin/dashboard.html', **Dashboard.get_metrics(), recent_bills=Bill._data[-5:], recent_activities=Activity._data[-5:])

        @self.__app.route('/cashier')
        def cashier_dashboard():
            return render_template('cashier/dashboard.html', **Dashboard.get_metrics(), recent_bills=Bill._data[-5:], recent_activities=Activity._data[-5:])

        @self.__app.route('/customer_management', methods=['POST', 'GET'])
        def customer_management():
            error = None
            search_query = ''
            if request.method == 'POST':
                if 'save_customer' in request.form:
                    c_id = request.form.get('customerId', '').strip()
                    c_name = request.form.get('customerName', '').strip()
                    contact = request.form.get('contactNo', '').strip()
                    address = request.form.get('address', '').strip()
                    if not c_id or not c_name or not contact:
                        error = "Customer ID, Name, and Contact are required!"
                    else:
                        if Customer.find_by_id(c_id):
                            error = "Customer ID already exists!"
                        else:
                            customer = Customer(c_id, c_name, contact, address)
                            customer.save()
                            Activity('customer', f'Added: {c_name}', 'admin').save()
                            return redirect(url_for('customer_management'))
                elif 'search_customer' in request.form:
                    search_query = request.form.get('searchInput', '').strip().lower()

            filtered = Customer.search(search_query, ['id', 'name'])
            return render_template('admin/customer.html', customers=filtered, error=error, search_query=search_query)

        @self.__app.route('/cashier/customer_management', methods=['POST', 'GET'])
        def cashier_customer_management():
            error = None
            search_query = ''
            if request.method == 'POST':
                if 'save_customer' in request.form:
                    c_id = request.form.get('customerId', '').strip()
                    c_name = request.form.get('customerName', '').strip()
                    contact = request.form.get('contactNo', '').strip()
                    address = request.form.get('address', '').strip()
                    if not c_id or not c_name or not contact:
                        error = "Customer ID, Name, and Contact are required!"
                    else:
                        if Customer.find_by_id(c_id):
                            error = "Customer ID already exists!"
                        else:
                            customer = Customer(c_id, c_name, contact, address)
                            customer.save()
                            Activity('customer', f'Added: {c_name}', 'cashier').save()
                            return redirect(url_for('cashier_customer_management'))
                elif 'search_customer' in request.form:
                    search_query = request.form.get('searchInput', '').strip().lower()

            filtered = Customer.search(search_query, ['id', 'name'])
            return render_template('cashier/customer.html', customers=filtered, error=error, search_query=search_query)

        @self.__app.route('/delete_customer/<customer_id>')
        def delete_customer(customer_id):
            customer = Customer.find_by_id(customer_id)
            if customer:
                Customer(customer_id, '', '', '').delete()
                Activity('customer', f'Deleted ID: {customer_id}', 'admin').save()
            return redirect(url_for('customer_management'))

        @self.__app.route('/products', methods=['POST', 'GET'])
        def products_management():
            error = None
            search_query = ''
            if request.method == 'POST':
                if 'save_product' in request.form:
                    p_id = request.form.get('productId', '').strip()
                    p_name = request.form.get('productName', '').strip()
                    cat = request.form.get('category', '').strip()
                    prc = request.form.get('price', '').strip()
                    stk = request.form.get('stock', '').strip()
                    if not p_id or not p_name or not cat or not prc or not stk:
                        error = "All fields are required!"
                    else:
                        try:
                            if Product.find_by_id(p_id):
                                error = "Product ID already exists!"
                            else:
                                product = Product(p_id, p_name, cat, float(prc), stk)
                                product.save()
                                Activity('product', f'Added: {p_name}', 'admin').save()
                                return redirect(url_for('products_management'))
                        except ValueError:
                            error = "Invalid Price format!"
                elif 'search_product' in request.form:
                    search_query = request.form.get('searchInput', '').strip().lower()

            filtered = Product.search(search_query, ['id', 'name'])
            return render_template('admin/Products.html', products=filtered, error=error, search_query=search_query)

        @self.__app.route('/cashier/products', methods=['POST', 'GET'])
        def cashier_products_management():
            error = None
            search_query = ''
            if request.method == 'POST':
                if 'save_product' in request.form:
                    p_id = request.form.get('productId', '').strip()
                    p_name = request.form.get('productName', '').strip()
                    cat = request.form.get('category', '').strip()
                    prc = request.form.get('price', '').strip()
                    stk = request.form.get('stock', '').strip()
                    if not p_id or not p_name or not cat or not prc or not stk:
                        error = "All fields are required!"
                    else:
                        try:
                            if Product.find_by_id(p_id):
                                error = "Product ID already exists!"
                            else:
                                product = Product(p_id, p_name, cat, float(prc), stk)
                                product.save()
                                Activity('product', f'Added: {p_name}', 'cashier').save()
                                return redirect(url_for('cashier_products_management'))
                        except ValueError:
                            error = "Invalid Price format!"
                elif 'search_product' in request.form:
                    search_query = request.form.get('searchInput', '').strip().lower()
            filtered = Product.search(search_query, ['id', 'name'])
            return render_template('cashier/Products.html', products=filtered, error=error, search_query=search_query)

        @self.__app.route('/cashier/edit_product/<product_id>', methods=['GET', 'POST'])
        def cashier_edit_product(product_id):
            product = Product.find_by_id(product_id)
            if request.method == 'POST' and product:
                product['name'] = request.form.get('productName')
                product['price'] = float(request.form.get('price'))
                product['category'] = request.form.get('category')
                product['stock'] = request.form.get('stock')
                return redirect(url_for('cashier_products_management'))
            return render_template('cashier/Products.html', products=Product._data, edit_product=product)

        @self.__app.route('/cashier/delete_product/<product_id>')
        def cashier_delete_product(product_id):
            product = Product.find_by_id(product_id)
            if product:
                Product(product_id, '', '', 0, '').delete()
            return redirect(url_for('cashier_products_management'))

        @self.__app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
        def edit_product(product_id):
            product = Product.find_by_id(product_id)
            if request.method == 'POST' and product:
                product['name'] = request.form.get('productName')
                product['price'] = float(request.form.get('price'))
                product['category'] = request.form.get('category')
                product['stock'] = request.form.get('stock')
                return redirect(url_for('products_management'))
            return render_template('admin/Products.html', products=Product._data, edit_product=product)

        @self.__app.route('/delete_product/<product_id>')
        def delete_product(product_id):
            product = Product.find_by_id(product_id)
            if product:
                Product(product_id, '', '', 0, '').delete()
            return redirect(url_for('products_management'))

        @self.__app.route('/sales', methods=['GET', 'POST'])
        def sales_management():
            search_query = ''
            if request.method == 'POST':
                if 'add_sale' in request.form:
                    prod_name = request.form.get('product')
                    cust_name = request.form.get('customer')
                    qty = int(request.form.get('quantity'))
                    pay_type = request.form.get('payment_type')
                    date = request.form.get('date')

                    matched_prod = next((p for p in Product._data if p['name'] == prod_name), None)
                    if matched_prod:
                        customer = next((c for c in Customer._data if c['name'] == cust_name), None)
                        customer_id = customer['id'] if customer else ''
                        total_p = matched_prod['price'] * qty
                        sale = Sale(customer_id, prod_name, qty, total_p, date, cust_name, pay_type)
                        sale.save()

                        if pay_type == 'cash':
                            bill = Bill(customer_id, cust_name, total_p, date, 'Paid', f'Full payment {prod_name}', 'Full Payment')
                            bill.save()

                        return redirect(url_for('sales_management'))
                elif 'search_sale' in request.form:
                    search_query = request.form.get('searchInput', '').lower()

            filtered = Sale.search(search_query, ['customer'])
            return render_template('admin/Sales.html', sales=filtered, products=Product._data, search_query=search_query)

        @self.__app.route('/cashier/sales', methods=['GET', 'POST'])
        def cashier_sales_management():
            search_query = ''
            if request.method == 'POST':
                if 'add_sale' in request.form:
                    prod_name = request.form.get('product')
                    cust_name = request.form.get('customer')
                    qty = int(request.form.get('quantity'))
                    pay_type = request.form.get('payment_type')
                    date = request.form.get('date')

                    matched_prod = next((p for p in Product._data if p['name'] == prod_name), None)
                    if matched_prod:
                        customer = next((c for c in Customer._data if c['name'] == cust_name), None)
                        customer_id = customer['id'] if customer else ''
                        total_p = matched_prod['price'] * qty
                        sale = Sale(customer_id, prod_name, qty, total_p, date, cust_name, pay_type)
                        sale.save()

                        if pay_type == 'cash':
                            bill = Bill(customer_id, cust_name, total_p, date, 'Paid', f'Full payment {prod_name}', 'Full Payment')
                            bill.save()

                        return redirect(url_for('cashier_sales_management'))
                elif 'search_sale' in request.form:
                    search_query = request.form.get('searchInput', '').lower()

            filtered = Sale.search(search_query, ['customer'])
            return render_template('cashier/Sales.html', sales=filtered, products=Product._data, search_query=search_query)

        @self.__app.route('/cashier/payment')
        def cashier_payment():
            return render_template('cashier/payment.html')

        @self.__app.route('/billing', methods=['GET', 'POST'])
        def billing_management():
            if 'username' not in session:
                return redirect(url_for('login'))
            error = None
            if request.method == 'POST':
                if 'add_bill' in request.form:
                    customer = request.form.get('customer', '').strip()
                    amount = request.form.get('amount', '').strip()
                    date = request.form.get('date', '').strip()
                    status = request.form.get('status', 'Unpaid')
                    bill_type = request.form.get('type', 'Manual')
                    description = request.form.get('description', '').strip()

                    if not customer or not amount or not date:
                        error = "All fields are required!"
                    else:
                        try:
                            amount = float(amount)
                            customer_id = ''
                            for c in Customer._data:
                                if c['name'] == customer:
                                    customer_id = c['id']
                                    break
                            bill = Bill(customer_id, customer, amount, date, status, description, bill_type)
                            bill.save()
                            Activity('billing', f'Bill added for {customer}', session.get('username', 'Unknown')).save()
                        except ValueError:
                            error = "Invalid amount!"
                search_query = request.form.get('searchInput', '').lower()
            else:
                search_query = ''

            filtered_bills = Bill.search(search_query, ['customer'])

            metrics = Dashboard.get_metrics()
            template = 'cashier/billing.html' if session.get('role') == 'cashier' else 'admin/billing.html'
            return render_template(template, bills=filtered_bills,
                                   total_bills=metrics['total_bills'], paid_bills=metrics['paid_bills'],
                                   unpaid_bills=metrics['unpaid_bills'], total_collected=metrics['total_revenue'],
                                   outstanding_amount=sum(b['amount'] for b in Bill._data if b['status'] != 'Paid'),
                                   bills_json=json.dumps(filtered_bills), pending_bills=metrics['pending_bills'],
                                   search_query=search_query, error=error)

        @self.__app.route('/update_bill_status/<int:bill_id>/<status>')
        def update_bill_status(bill_id, status):
            bill = next((b for b in Bill._data if b['id'] == bill_id), None)
            if bill:
                bill['status'] = status
            return redirect(url_for('billing_management'))

        @self.__app.route('/delete_bill/<int:bill_id>')
        def delete_bill(bill_id):
            bill = next((b for b in Bill._data if b['id'] == bill_id), None)
            if bill:
                Bill._data = [b for b in Bill._data if b['id'] != bill_id]
            return redirect(url_for('billing_management'))

        @self.__app.route('/payment')
        def payment():
            return render_template('admin/payment.html')

        @self.__app.route('/reports')
        def reports():
            if 'username' not in session:
                return redirect(url_for('login'))
            search_query = request.args.get('searchInput', '').lower()
            overdue_bills = [b for b in Bill._data if b['status'] != 'Paid']
            if search_query:
                overdue_bills = [b for b in overdue_bills if search_query in b['customer'].lower()]
            total_overdue = len(overdue_bills)
            overdue_amount = sum(b['amount'] for b in overdue_bills)
            reminder_list = [f"Reminder for {b['customer']}: ₱{b['amount']} due on {b.get('due_date', b['date'])}" for b in overdue_bills]
            template = 'cashier/report.html' if session.get('role') == 'cashier' else 'admin/Report.html'
            return render_template(template, overdue_bills=overdue_bills, reminder_list=reminder_list, search_query=search_query, total_overdue=total_overdue, overdue_amount=overdue_amount)

        @self.__app.route('/users', methods=['GET', 'POST'])
        def users():
            if 'username' not in session:
                return redirect(url_for('login'))
            error = None
            search_query = request.args.get('searchInput', '').strip().lower()
            if request.method == 'POST':
                if 'save_user' in request.form:
                    username = request.form.get('username', '').strip()
                    password = request.form.get('password', '').strip()
                    role = request.form.get('role', '').strip()
                    
                    if not username or not password or not role:
                        error = "All fields are required!"
                    elif any(u['username'] == username for u in User._data):
                        error = "Username already exists!"
                    else:
                        User._data.append({'username': username, 'password': password, 'role': role})
                        Activity('user', f'Added user: {username}', session.get('username', 'Unknown')).save()
                        return redirect(url_for('users'))
            
            user_list = User._data.copy()
            if search_query:
                user_list = [u for u in user_list if search_query in u['username'].lower() or search_query in u['role'].lower()]
            
            return render_template('admin/User.html', users=user_list, error=error, search_query=search_query)

        @self.__app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('index'))

    def run(self):
        Activity('system', 'System Start', 'System').save()
        self.__app.run(debug=True)

# --- MAIN ---
if __name__ == '__main__':
    pos_app = POSApp()
    pos_app.run()