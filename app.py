from flask import Flask
from db import db
from config import Config
from users.models import User
from users.routes import bp as users_bp
from flask_cors import CORS
app = Flask(__name__)


CORS(app,origins=["http://localhost:8080,http://localhost:5173,*"],  # 前端地址
    supports_credentials=True  )
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    print("✅ All tables already exist:", db.metadata.tables.keys())

app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True,port=32222)
