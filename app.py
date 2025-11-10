# app.py
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file, render_template_string
from models import db, Contact
from config import Config
from datetime import datetime
from pathlib import Path
import csv
from io import StringIO

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure DB path
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database ready → instance/app.db")

    # --------------------------------------------------
    # LOGIN REQUIRED DECORATOR
    # --------------------------------------------------
    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated

    # --------------------------------------------------
    # LOGIN ROUTE
    # --------------------------------------------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if (username == app.config['ADMIN_USERNAME'] and
                password == app.config['ADMIN_PASSWORD']):
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Invalid credentials.', 'error')
        return render_template('login.html')

    # --------------------------------------------------
    # LOGOUT
    # --------------------------------------------------
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('Logged out.', 'info')
        return redirect(url_for('home'))

    # --------------------------------------------------
    # HOME + CONTACT FORM
    # --------------------------------------------------
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()

            if not all([name, email, message]):
                flash('Please fill all fields.', 'danger')
            else:
                try:
                    contact = Contact(name=name, email=email, message=message)
                    db.session.add(contact)
                    db.session.commit()
                    flash('Thank you! Your message has been saved.', 'success')
                except Exception as e:
                    flash('Error saving message.', 'danger')
                    print(f"DB Error: {e}")
                return redirect(url_for('home') + '#contact')
        return render_template('index.html')

    # --------------------------------------------------
    # ADMIN DASHBOARD
    # --------------------------------------------------
    @app.route('/admin')
    @login_required
    def admin():
        contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8"><title>Admin Dashboard</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
          <style>body{padding:2rem;}</style>
        </head>
        <body>
          <div class="container">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h2>Contact Messages ({{ contacts|length }})</h2>
              <div>
                <a href="{{ url_for('export_csv') }}" class="btn btn-success">Export CSV</a>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-danger">Logout</a>
              </div>
            </div>
            <div class="row">
              {% for c in contacts %}
              <div class="col-md-6 mb-3">
                <div class="card">
                  <div class="card-body">
                    <h5 class="card-title">{{ c.name }} <small class="text-muted">({{ c.email }})</small></h5>
                    <p class="card-text"><small>{{ c.timestamp.strftime('%d %b %Y, %I:%M %p') }}</small></p>
                    <p>{{ c.message }}</p>
                  </div>
                </div>
              </div>
              {% endfor %}
            </div>
          </div>
        </body>
        </html>
        ''', contacts=contacts)

    # --------------------------------------------------
    # EXPORT TO CSV
    # --------------------------------------------------
    @app.route('/admin/export')
    @login_required
    def export_csv():
        contacts = Contact.query.order_by(Contact.timestamp.asc()).all()
        from io import StringIO, BytesIO
        import csv

        # Use StringIO for writing strings
        si = StringIO()
        writer = csv.writer(si, quoting=csv.QUOTE_ALL)

        # Header
        writer.writerow(['ID', 'Name', 'Email', 'Message', 'Timestamp'])

        # Data
        for c in contacts:
            writer.writerow([
                c.id,
                c.name,
                c.email,
                c.message,
                c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        # Convert to bytes
        output = BytesIO()
        output.write(si.getvalue().encode('utf-8'))
        output.seek(0)

        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
    return app
if __name__ == '__main__':
    # Debug mode: True for development
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)