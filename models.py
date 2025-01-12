from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'tbl_user'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(255),  index=True)
    user_email = Column(String(255), index=True, unique=True)
    user_password = Column(String(255), index=True, unique=True)

    transaction = relationship("Transaction", back_populates='user')

class Transaction(Base):
    __tablename__ = 'tbl_transaction'
    transaction_id = Column(String(255), primary_key=True, index=True, unique=True)
    transaction_amount = Column(Float)
    transaction_reason = Column(String(255), index=True)
    usr_id = Column(Integer, ForeignKey("tbl_user.user_id"))

    user = relationship("User", back_populates= "transaction")



