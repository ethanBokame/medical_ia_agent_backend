import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    # MySQL root sans mot de passe
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        # "mysql+pymysql://root:1234@localhost:3307/medical_ia_agent"
        "mysql+pymysql://avnadmin:AVNS_8AbLwjJlrUModRwnl8E@mysql-136fdcf2-ethaniraqui-3e24.e.aivencloud.com:14567/defaultdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False