from fastapi import HTTPException
from passlib.context import CryptContext
from app.repositories import users as u
from jose import jwt
from datetime import datetime,timedelta
import logging
logger=logging.getLogger(__name__)
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRET_KEY='SECRET_KEY'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=60

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
def signup(new_user):
    user=u.get_email(new_user.email)
    if user:
        logger.warning(f"invalid credential use another {new_user.email}")
        raise HTTPException(status_code=403,detail='already user')
    hashed=hash_password(new_user.password)
    result= u.create_user(hashed,new_user)
    logger.info("user signup success")
    return result

def login(email:str,password:str):
    user=u.get_email(email)
    if not user:
        logger.info(f"invalid credential, put corrct credential {email}")
        raise HTTPException(status_code=403,detail='invalid credential')
    if not verify_password(password,user['hashed_password']):
        logger.info("wrong password")
        raise HTTPException(status_code=403,detail='invalid credential')
    token=create_access_token({"sub":user['email']})
    logger.info("login successfully")
    return{"token" : token, "token_type": "bearer"}

    