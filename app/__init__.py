import os
from flask import Flask
from routes.general import rotas_gerais
from .extensions import db
from . import models

def iniciar():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "bos_chave_secreta_atendimento_sus_2026")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(rotas_gerais)
    
    return app
