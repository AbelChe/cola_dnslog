from config import DNS_DOMAIN, HTTP_PORT, LDAP_PORT, RMI_PORT, SERVER_IP
from database import engine
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libs.auth import new_token, password_hash
from models import User
from pydantic import BaseModel
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
        if len(userinfo.logid.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')) < 3:
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

class passwordData(BaseModel):
    password: str
    new_password: str

@router.post('/info/change_password')
async def change_password(passworddata: passwordData, user: dict = Depends(get_current_user_info)):
    if len(passworddata.new_password) < 6:
        return {'code': 50001, 'message': 'The password length should be at least 6 digits!', 'data': {}}
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    if user_obj.first().hashed_password != password_hash(passworddata.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    try:
        user_obj.update({'hashed_password': password_hash(passworddata.new_password)})
        Session.commit()
        return {'code': 20000, 'message': 'Update success!', 'data': {}}
    except Exception as e:
        Session.rollback()
        print('[SQL ERROR] ' + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error..."
        )

@router.post('/new_token')
async def genter_new_token(user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    for i in range(3):
        newtoken = new_token()
        if not Session.query(User).filter_by(token=newtoken).first():
            try:
                user_obj.update({'token': newtoken})
                Session.commit()
                return {'code': 20000, 'message': 'Update success!', 'data': {}}
            except Exception as e:
                Session.rollback()
                print('[SQL ERROR] ' + str(e))
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Server Error..."
                )
    raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Please try again......"
            )

@router.get('/get_my_server_info')
async def get_my_server_domain(user: dict = Depends(get_current_user_info)):
    data = {}
    data['logid'] = user.get('logid')
    data['domain'] = '{}.{}'.format(user.get('logid'), DNS_DOMAIN)
    data['http'] = '{}:{}'.format(SERVER_IP, HTTP_PORT) if HTTP_PORT != 80 else '{}'.format(SERVER_IP)
    data['ldap'] = '{}:{}'.format(SERVER_IP, LDAP_PORT) if LDAP_PORT != 80 else '{}'.format(SERVER_IP)
    data['rmi'] = '{}:{}'.format(SERVER_IP, RMI_PORT) if RMI_PORT != 80 else '{}'.format(SERVER_IP)
    return {'code': 20000, 'message': 'success', 'data': data}

@router.get('/get_dingtalk_switch_status')
async def get_dingtalk_switch_status(user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    return {'code': 20000, 'message': 'success', 'data': {'status': user_obj.first().dingtalk_flag}}

@router.get('/change_dingtalk_switch_status')
async def set_dingtalk_switch_status(user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    try:
        status = (not user_obj.first().dingtalk_flag)
        user_obj.update({'dingtalk_flag': status})
        Session.commit()
        return {'code': 20000, 'message': 'success', 'data': {'status': status}}
    except Exception as e:
        Session.rollback()
        print('[SQL ERROR] ' + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error..."
        )

@router.get('/get_bark_switch_status')
async def get_bark_switch_status(user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    return {'code': 20000, 'message': 'success', 'data': {'status': user_obj.first().bark_flag}}

@router.get('/change_bark_switch_status')
async def set_bark_switch_status(user: dict = Depends(get_current_user_info)):
    user_obj = Session.query(User).filter_by(token=user.get('token'))
    try:
        status = (not user_obj.first().bark_flag)
        user_obj.update({'bark_flag': status})
        Session.commit()
        return {'code': 20000, 'message': 'success', 'data': {'status': status}}
    except Exception as e:
        Session.rollback()
        print('[SQL ERROR] ' + str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server Error..."
        )
