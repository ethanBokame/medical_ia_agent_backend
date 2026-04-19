import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    # MySQL root sans mot de passe
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        # "mysql+pymysql://root:1234@localhost:3307/medical_ia_agent"
        "postgresql://root:n5z94zvKXiPEzSIumBPiqlelxGexnAfz@dpg-d7ifghnaqgkc739snsig-a.virginia-postgres.render.com/medical_ia_agent_backend"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False