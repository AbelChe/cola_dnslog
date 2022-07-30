from database import engine
from pydantic import BaseModel
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libs.auth import password_hash
from models import User
from sqlalchemy.orm import sessionmaker

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

Session_class = sessionmaker(bind=engine)
Session = Session_class()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/auth')


@router.post("/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user_obj = Session.query(User).filter_by(name=username).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password error..."
        )

    if not password_hash(password) == user_obj.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password error..."
        )

    return {'code': 20000, 'message': 'Success', 'data': {'token': user_obj.token, 'token_type': 'Bearer'}}


async def get_current_user_info(token: str = Depends(oauth2_scheme)) -> dict:
    user_obj = Session.query(User).filter_by(token=token).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid User"
        )
    user = {
        'id': user_obj.id,
        'name': user_obj.name,
        'roles': user_obj.roles,
        'token': user_obj.token,
        'logid': user_obj.logid,
        'dingtalk_robot_token': user_obj.dingtalk_robot_token,
        'bark_url': user_obj.bark_url,
        'register_time': user_obj.register_time,
        'last_logintime': user_obj.last_logintime,
    }
    return user


async def user_access_token(user: dict = Depends(get_current_user_info)) -> str:
    token = user.get('token')
    return token


@router.get('/info')
async def user_info(user: str = Depends(get_current_user_info)):
    return {'code': 20000, 'message': 'Success', 'data': user}


class userInfo(BaseModel):
    dingtalk_robot_token: str
    bark_url: str
    logid: str

@router.post('/info/update')
async def user_info_update(userinfo: userInfo, user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    try:
        userinfo.login = userinfo.logid.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        if len(userinfo.logid) < 3:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server Error..."
            )
        user_obj.update({'dingtalk_robot_token': userinfo.dingtalk_robot_token, 'bark_url':userinfo.bark_url, 'logid':userinfo.logid})
        Session.commit()
    except Exception as e:
        Session.rollback()
        print('[SQL ERROR] ' + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error..."
        )
    return {'code': 20000, 'message': 'Success', 'data': {}}
