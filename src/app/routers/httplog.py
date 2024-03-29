from database import engine
from fastapi import APIRouter, Depends
from models import User, Httplog
from sqlalchemy.orm import sessionmaker

from routers.auth import user_access_token as access_token

router = APIRouter(
    prefix="/httplog",
    tags=["httplog"],
    dependencies=[Depends(access_token)]
)

Session_class = sessionmaker(bind=engine)
Session = Session_class()


@router.get("/")
async def read_items(page: int = 1, limit: int = 10, sort: str = '-id', token: str = Depends(access_token)):
    user_obj = Session.query(User).filter_by(token=token).first()
    sort_id = 1 if sort == '+id' else -1
    result = {
        'total': len(user_obj.httplog_item),
        'items': user_obj.httplog_item[::sort_id][(page-1)*limit:limit*page]
    }
    return {'code': 20000, 'page': page, 'limit': limit, 'data': result}

@router.get("/delete")
async def delete_items(size: int = 10, token: str = Depends(access_token)):
    try:
        user_obj = Session.query(User).filter_by(token=token).first()
        sort_id = -1
        for i in user_obj.httplog_item[::sort_id][:size]:
            Session.delete(i)
        Session.commit()
        return {'code': 20000}
    except Exception as e:
        print(e)
        Session.rollback()
    finally:
        Session.close()

@router.get("/delete/all")
async def delete_all_items(token: str = Depends(access_token)):
    try:
        user_obj = Session.query(User).filter_by(token=token).first()
        Session.query(Httplog).filter_by(owner_id=user_obj.id).delete()
        Session.commit()
        return {'code': 20000}
    except Exception as e:
        print(e)
        Session.rollback()
    finally:
        Session.close()
