import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PWD_AIVEN = os.environ.get('PWD_AIVEN')
    # MySQL root sans mot de passe
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        # "mysql+pymysql://root:1234@localhost:3307/medical_ia_agent"
        "mysql+pymysql://avnadmin:{PWD_AIVEN}@mysql-136fdcf2-ethaniraqui-3e24.e.aivencloud.com:14567/defaultdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False