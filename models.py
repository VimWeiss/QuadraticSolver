from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class EquationHistory(Base):
    __tablename__ = 'equation_history'
    
    id = Column(Integer, primary_key=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    c = Column(Float, nullable=False)
    discriminant = Column(Float, nullable=False)
    root1 = Column(Float, nullable=True)
    root2 = Column(Float, nullable=True)
    solution_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create database and tables
engine = create_engine('sqlite:///equation_history.db')
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
