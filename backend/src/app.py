from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from prometheus_client import generate_latest, Counter, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/contacts_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelagem do Contato ---
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

# --- Métricas do Prometheus ---
# Contador para requisições da API
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)

# Gauge para o número total de contatos
CONTACTS_TOTAL = Gauge(
    'contacts_total',
    'Total number of contacts in the database'
)

# Middleware para expor as métricas do Prometheus
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Hook para atualizar o gauge de contatos após cada requisição que modifica dados
@app.after_request
def update_contacts_gauge(response):
    if request.method in ['POST', 'PUT', 'DELETE']:
        with app.app_context():
            CONTACTS_TOTAL.set(Contact.query.count())
    return response

# Inicializa o gauge no início
with app.app_context():
    db.create_all() # Garante que as tabelas existam
    CONTACTS_TOTAL.set(Contact.query.count())

# --- Endpoints da API RESTful ---

@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        name_filter = request.args.get('name')
        if name_filter:
            contacts = Contact.query.filter(Contact.name.ilike(f'%{name_filter}%')).all()
        else:
            contacts = Contact.query.all()
        REQUEST_COUNT.labels(method='GET', endpoint='/contacts', status_code=200).inc()
        return jsonify([contact.to_dict() for contact in contacts])
    except Exception as e:
        REQUEST_COUNT.labels(method='GET', endpoint='/contacts', status_code=500).inc()
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    REQUEST_COUNT.labels(method='GET', endpoint='/contacts/{id}', status_code=200).inc()
    return jsonify(contact.to_dict())

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    if not name:
        REQUEST_COUNT.labels(method='POST', endpoint='/contacts', status_code=400).inc()
        return jsonify({'error': 'Name is required.'}), 400

    new_contact = Contact(name=name, phone=phone, email=email)
    db.session.add(new_contact)
    db.session.commit()
    REQUEST_COUNT.labels(method='POST', endpoint='/contacts', status_code=201).inc()
    return jsonify(new_contact.to_dict()), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()

    name = data.get('name')
    if not name:
        REQUEST_COUNT.labels(method='PUT', endpoint='/contacts/{id}', status_code=400).inc()
        return jsonify({'error': 'Name is required.'}), 400

    contact.name = name
    contact.phone = data.get('phone')
    contact.email = data.get('email')

    db.session.commit()
    REQUEST_COUNT.labels(method='PUT', endpoint='/contacts/{id}', status_code=200).inc()
    return jsonify(contact.to_dict())

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    REQUEST_COUNT.labels(method='DELETE', endpoint='/contacts/{id}', status_code=204).inc()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas no banco de dados se elas não existirem
    app.run(host='0.0.0.0', port=5000, debug=True)
