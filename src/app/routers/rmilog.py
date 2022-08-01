from database import engine
from fastapi import APIRouter, Depends
from models import User
from sqlalchemy.orm import sessionmaker

from routers.auth import user_access_token as access_token

router = APIRouter(
    prefix="/rmilog",
    tags=["rmilog"],
    dependencies=[Depends(access_token)]
)

Session_class = sessionmaker(bind=engine)
Session = Session_class()


@router.get("/")
async def read_items(page: int = 1, limit: int = 10, sort: str = '-id', token: str = Depends(access_token)):
    user_obj = Session.query(User).filter_by(token=token).first()
    sort_id = 1 if sort == '+id' else -1
    result = {
        'total': len(user_obj.rmilog_item),
        'items': user_obj.rmilog_item[::sort_id][(page-1)*limit:limit*page]
    }
    return {'code': 20000, 'page': page, 'limit': limit, 'data': result}

