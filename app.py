cat > app.py << 'EOF'
from flask import Flask
from routes.employees import employees_bp
from routes.departments import departments_bp
from routes.salaries import salaries_bp

app = Flask(__name__)

app.register_blueprint(employees_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(salaries_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
EOF