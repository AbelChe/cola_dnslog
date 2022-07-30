from fastapi import APIRouter, Depends
from routers.auth import user_access_token as access_token
from sqlalchemy.orm import sessionmaker
from database import engine
from models import User

router = APIRouter(
    prefix="/dnslog",
    tags=["dnslog"],
    dependencies=[Depends(access_token)]
)

Session_class = sessionmaker(bind=engine)
Session = Session_class()


@router.get("/")
async def read_items(page: int = 1, limit: int = 10, token: str = Depends(access_token)):
    user_obj = Session.query(User).filter_by(token=token).first()
    result = {
        'total': len(user_obj.dnslog_item),
        'items': user_obj.dnslog_item[::-1][(page-1)*limit:limit*page]
    }
    return {'code': 20000, 'page': page, 'limit': limit, 'data': result}
