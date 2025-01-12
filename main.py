from fastapi import FastAPI, HTTPException, Depends
from schemas import Register, Login, StoreTransaction

from database import SessionLocal
from models import User, Transaction
from sqlalchemy.orm import Session
from database import Base, engine
from utils import hash_password, verify_password, get_transaction_id

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

@app.get("/login")
def login_user(user : Login, db : Session = Depends(get_db)):
   try :
      is_existing_user = db.query(User).filter(user.email == User.user_email).first()

      if(is_existing_user):
         if(verify_password(is_existing_user.user_password, user.password)):
            return {
               "status" : "OK", 
               "statusCode" : 200,
               "data" : {
                   "email" : user.email,
                   "password" : user.password,
               },
               "message" : "Login Successful"
            }
         else:
            raise HTTPException(status_code=401, detail="Wrong Password")
      else:   
         raise HTTPException(status_code=401, detail="User not Found")
   except Exception as e:
       return {"status" : "NOT OK", 
               "statusCode" : 401,
               "data" : None,
               "message" : e.detail} 
      

@app.post("/register/")
def register_user(user : Register, db : Session = Depends(get_db)):
    try :
     is_existing_user = db.query(User).filter(user.email == User.user_email).first()
     
     if is_existing_user is None:
        new_user = User(user_name = user.name, user_email  = user.email, user_password = hash_password(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
           "status" : "OK", 
            "statusCode" : 200,
            "data" : {
               "email" : is_existing_user
            },
            "message" : "Sucessfully Registered !!"
        }
     else :
       raise HTTPException(detail="Email already registered")
    except Exception as e : 
         return {
            "status" : "NOT OK", 
            "statusCode" : 200,
            "data" : {},
            "message" : "Email Already Registerd"
         }


@app.post('/dashboard/')
def dashboard(user_data : StoreTransaction, db : Session = Depends(get_db)):
   try :
      is_existing_user = db.query(User).filter(User.user_email == user_data.email).first()

      if(is_existing_user):
        new_transaction = Transaction(transaction_id = get_transaction_id(is_existing_user.user_name[ : 3].upper()), transaction_amount = user_data.amount, transaction_reason = user_data.reason, usr_id = is_existing_user.user_id)
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return {
           "status" : "OK", 
            "statusCode" : 200,
            "data" : {
              "trans_id": new_transaction.transaction_id,
              "trans_amount" : new_transaction.transaction_amount,
              "trans_reason" : new_transaction.transaction_reason
            },
            "message" : "Transaction Successfull"
        }
      else:
         raise HTTPException(status_code=401, detail="User not found")
   except Exception as e:
      return {
            "status" : "NOT OK", 
            "statusCode" : e.status_code,
            "data" : {},
            "message" : e.detail
         }

@app.get('/dashboard/transactions/{email}/')
def getTransactionDetail(email : str, db : Session = Depends(get_db)):
   try : 
      is_existing_user = db.query(User).filter(User.user_email == email).first()
      if is_existing_user: 
         transactions = db.query(Transaction).filter(is_existing_user.user_id == Transaction.usr_id).all()
         print(transactions)
         if transactions:
            return {
            "status" : "OK", 
            "statusCode" : 200,
            "data" : transactions,
            "message" : "Transaction Fetched Successfully"
          }
         else : 
            raise HTTPException(status_code=404, detail="No Transaction Found")
      else:
         raise HTTPException(status_code=404, detail="User not found")
   except Exception as e: 
      return {
            "status" : "NOT OK", 
            "statusCode" : e.status_code,
            "data" : [],
            "message" : e.detail
         }
   
   
   
   
   
   
   


