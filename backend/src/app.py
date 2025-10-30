from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from prometheus_client import Counter, Gauge, Histogram, Info, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
from functools import wraps

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/contacts_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modelagem do Contato ---
class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Contact {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ==========================================
# MÉTRICAS DO PROMETHEUS - VERSÃO MELHORADA
# ==========================================

# Informações da aplicação
APP_INFO = Info('contacts_app', 'Contacts Application Information')
APP_INFO.info({
    'version': 'latest',
    'language': 'python',
    'framework': 'flask',
    'database': 'postgresql'
})

# Contador de requisições HTTP (mantém o seu, mas com nome melhor)
REQUEST_COUNT = Counter(
    'contacts_http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)

# Histograma de duração das requisições
REQUEST_DURATION = Histogram(
    'contacts_http_request_duration_seconds',
    'HTTP Request Duration',
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

# Gauge para o número total de contatos
CONTACTS_TOTAL = Gauge(
    'contacts_total',
    'Total number of contacts in the database'
)

# Contador de operações no banco de dados
DB_OPERATIONS = Counter(
    'contacts_db_operations_total',
    'Total database operations',
    ['operation', 'table', 'status']
)

# Histograma de duração das queries no banco
DB_QUERY_DURATION = Histogram(
    'contacts_db_query_duration_seconds',
    'Database query duration',
    ['operation', 'table']
)

# Contador de erros
ERROR_COUNT = Counter(
    'contacts_errors_total',
    'Total errors',
    ['error_type', 'endpoint']
)

# Gauge de conexões ativas com o banco
DB_CONNECTIONS = Gauge(
    'contacts_db_connections_active',
    'Active database connections'
)

# Middleware para expor as métricas do Prometheus
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# ==========================================
# DECORADORES PARA MÉTRICAS
# ==========================================

def track_request_metrics(f):
    """Decorator para rastrear métricas de requisições"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        endpoint = request.endpoint or 'unknown'
        method = request.method
        
        try:
            response = f(*args, **kwargs)
            status_code = response[1] if isinstance(response, tuple) else 200
            
            # Registra métricas de sucesso
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status_code=status_code
            ).inc()
            
            return response
            
        except Exception as e:
            # Registra métricas de erro
            status_code = 500
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status_code=status_code
            ).inc()
            
            ERROR_COUNT.labels(
                error_type=type(e).__name__,
                endpoint=endpoint
            ).inc()
            
            raise
            
        finally:
            # Registra duração da requisição
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    return decorated_function

def track_db_operation(operation, table='contacts'):
    """Decorator para rastrear operações no banco"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                
                # Registra operação bem-sucedida
                DB_OPERATIONS.labels(
                    operation=operation,
                    table=table,
                    status='success'
                ).inc()
                
                return result
                
            except Exception as e:
                # Registra operação com erro
                DB_OPERATIONS.labels(
                    operation=operation,
                    table=table,
                    status='error'
                ).inc()
                raise
                
            finally:
                # Registra duração da query
                duration = time.time() - start_time
                DB_QUERY_DURATION.labels(
                    operation=operation,
                    table=table
                ).observe(duration)
        
        return decorated_function
    return decorator

# ==========================================
# HEALTH CHECK
# ==========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para healthcheck"""
    try:
        # Testa conexão com o banco
        db.session.execute('SELECT 1')
        db_status = 'healthy'
        status_code = 200
    except Exception as e:
        db_status = 'unhealthy'
        status_code = 503
        ERROR_COUNT.labels(error_type='database_connection', endpoint='/health').inc()
    
    return jsonify({
        'status': 'healthy' if status_code == 200 else 'unhealthy',
        'database': db_status,
        'service': 'contacts-api',
        'version': '1.0.0'
    }), status_code

# ==========================================
# ENDPOINTS DA API RESTful COM MÉTRICAS
# ==========================================

@app.route('/contacts', methods=['GET'])
@track_request_metrics
@track_db_operation('select')
def get_contacts():
    try:
        name_filter = request.args.get('name')
        
        if name_filter:
            contacts = Contact.query.filter(Contact.name.ilike(f'%{name_filter}%')).all()
        else:
            contacts = Contact.query.all()
        
        # Atualiza gauge de total de contatos
        CONTACTS_TOTAL.set(Contact.query.count())
        
        return jsonify([contact.to_dict() for contact in contacts]), 200
        
    except Exception as e:
        ERROR_COUNT.labels(error_type='database_error', endpoint='/contacts').inc()
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/<int:id>', methods=['GET'])
@track_request_metrics
@track_db_operation('select')
def get_contact(id):
    try:
        contact = Contact.query.get_or_404(id)
        return jsonify(contact.to_dict()), 200
    except Exception as e:
        if '404' in str(e):
            ERROR_COUNT.labels(error_type='not_found', endpoint='/contacts/{id}').inc()
            return jsonify({'error': 'Contact not found'}), 404
        ERROR_COUNT.labels(error_type='database_error', endpoint='/contacts/{id}').inc()
        return jsonify({'error': str(e)}), 500

@app.route('/contacts', methods=['POST'])
@track_request_metrics
@track_db_operation('insert')
def create_contact():
    try:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')

        if not name:
            ERROR_COUNT.labels(error_type='validation_error', endpoint='/contacts').inc()
            return jsonify({'error': 'Name is required.'}), 400

        # Validação de email duplicado
        if email:
            existing = Contact.query.filter_by(email=email).first()
            if existing:
                ERROR_COUNT.labels(error_type='duplicate_email', endpoint='/contacts').inc()
                return jsonify({'error': 'Email already exists.'}), 409

        new_contact = Contact(name=name, phone=phone, email=email)
        db.session.add(new_contact)
        db.session.commit()
        
        # Atualiza gauge
        CONTACTS_TOTAL.inc()
        
        return jsonify(new_contact.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        ERROR_COUNT.labels(error_type='database_error', endpoint='/contacts').inc()
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/<int:id>', methods=['PUT'])
@track_request_metrics
@track_db_operation('update')
def update_contact(id):
    try:
        contact = Contact.query.get_or_404(id)
        data = request.get_json()

        name = data.get('name')
        if not name:
            ERROR_COUNT.labels(error_type='validation_error', endpoint='/contacts/{id}').inc()
            return jsonify({'error': 'Name is required.'}), 400

        contact.name = name
        contact.phone = data.get('phone')
        contact.email = data.get('email')

        db.session.commit()
        return jsonify(contact.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            ERROR_COUNT.labels(error_type='not_found', endpoint='/contacts/{id}').inc()
            return jsonify({'error': 'Contact not found'}), 404
        ERROR_COUNT.labels(error_type='database_error', endpoint='/contacts/{id}').inc()
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/<int:id>', methods=['DELETE'])
@track_request_metrics
@track_db_operation('delete')
def delete_contact(id):
    try:
        contact = Contact.query.get_or_404(id)
        db.session.delete(contact)
        db.session.commit()
        
        # Atualiza gauge
        CONTACTS_TOTAL.dec()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        if '404' in str(e):
            ERROR_COUNT.labels(error_type='not_found', endpoint='/contacts/{id}').inc()
            return jsonify({'error': 'Contact not found'}), 404
        ERROR_COUNT.labels(error_type='database_error', endpoint='/contacts/{id}').inc()
        return jsonify({'error': str(e)}), 500

# ==========================================
# ENDPOINT DE ESTATÍSTICAS
# ==========================================

@app.route('/stats', methods=['GET'])
@track_request_metrics
def get_stats():
    """Retorna estatísticas gerais da aplicação"""
    try:
        total_contacts = Contact.query.count()
        
        # Contatos criados nas últimas 24h
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_contacts = Contact.query.filter(Contact.created_at >= yesterday).count()
        
        return jsonify({
            'total_contacts': total_contacts,
            'recent_contacts_24h': recent_contacts,
            'database_status': 'connected'
        }), 200
        
    except Exception as e:
        ERROR_COUNT.labels(error_type='database_error', endpoint='/stats').inc()
        return jsonify({'error': str(e)}), 500

# ==========================================
# INICIALIZAÇÃO
# ==========================================

if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no banco de dados se elas não existirem
        db.create_all()
        
        # Inicializa o gauge de contatos
        try:
            CONTACTS_TOTAL.set(Contact.query.count())
            print("✓ Database tables created")
            print("✓ Prometheus metrics initialized")
            print(f"✓ Total contacts: {Contact.query.count()}")
        except Exception as e:
            print(f"✗ Error initializing metrics: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
