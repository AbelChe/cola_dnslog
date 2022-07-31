from database import engine, Base, INSTALL
from models import User, Dnslog, Httplog
from sqlalchemy.orm import sessionmaker


domain = 'xxx.yiu.l00l.co'

logid = domain.split('.')[-3]
Session_class = sessionmaker(bind=engine)
Session = Session_class()
user_selectobj = Session.query(User).filter_by(logid=logid)
user_selectdata = user_selectobj.first()
if user_selectdata:
    sql_obj = Dnslog(record=domain, ip_from='1.1.1.1', owner_id=user_selectdata.id)
    Session.add(sql_obj)
    Session.commit()
    print('[+ SQL] domain--->{} \t ip--->{}'.format(domain, '1.1.1.1'))