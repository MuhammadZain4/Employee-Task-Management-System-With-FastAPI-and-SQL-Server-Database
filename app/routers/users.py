from app.services import users as u
from fastapi import FastAPI,APIRouter,Depends
from app.schemas.emp import requesteduser,LoginRequest

router=APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/signup')
def sign_up(new:requesteduser):
    return u.signup(new)

@router.post('/login')
def login_user(log:LoginRequest):
    return u.login(log.email,log.password)