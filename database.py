import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt

DATABASE_URL = "sqlite:///parkinsons_app.db"
engine = db.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    hashed_password = db.Column(db.String, nullable=False)

class Prediction(Base):
    __tablename__ = "predictions"
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.String)
    probability = db.Column(db.Float)
    result_text = db.Column(db.String)
Base.metadata.create_all(bind=engine)


def get_db():
    """Generator to get a new database session."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def create_user(db_session, name, email, age, gender, password):
    """Creates a new user and adds them to the database."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(
        name=name,
        email=email,
        age=age,
        gender=gender,
        hashed_password=hashed_password.decode('utf-8')
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

def get_user_by_email(db_session, email):
    """Retrieves a user by their email address."""
    return db_session.query(User).filter(User.email == email).first()

def check_password(email, password):
    """Verifies a user's password."""
    db_session = next(get_db())
    user = get_user_by_email(db_session, email)
    db_session.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return True
    return False

def add_prediction(db_session, user_id, date, probability, result_text):
    """Saves a new prediction record to the database."""
    new_prediction = Prediction(
        user_id=user_id,
        date=date,
        probability=probability,
        result_text=result_text
    )
    db_session.add(new_prediction)
    db_session.commit()
    db_session.refresh(new_prediction)
    return new_prediction

def get_predictions_by_user_id(db_session, user_id):
    """Retrieves all prediction records for a specific user, newest first."""
    return db_session.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.date.desc()).all()
def get_user_details_by_email(db_session, email):
    """Retrieves a full user object by their email address."""
    return db_session.query(User).filter(User.email == email).first()

def get_user_stats(db_session, user_id):
    """Retrieves statistics for a user's dashboard."""
    stats = {
        "total_analyses": 0,
        "last_analysis_date": "N/A"
    }
    stats["total_analyses"] = db_session.query(Prediction).filter(Prediction.user_id == user_id).count()
    last_prediction = db_session.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.date.desc()).first()
    if last_prediction:
        stats["last_analysis_date"] = last_prediction.date.split(" ")[0] 
        
    return stats