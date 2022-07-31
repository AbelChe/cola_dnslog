import copy
import os
import tempfile
import re
import datetime

from dnslib import QTYPE, RCODE, RR, TXT
from dnslib.server import BaseResolver, DNSHandler, DNSLogger, DNSServer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import DNS_DOMAIN, NS1_DOMAIN, NS2_DOMAIN, SERVER_IP, DNS_PORT, TEMPLATES_PATH
from database import engine
from models import Dnslog, User

from utils import dingtalk_robot_message_sender, bark_message_sender

# Load dingtalk template
dingtalk_robot_message_template_file = open(os.path.join(TEMPLATES_PATH, 'dingtalk', 'dnslog.md'))
dingtalk_robot_message_template = dingtalk_robot_message_template_file.read()
dingtalk_robot_message_template_file.close()

Session_class = sessionmaker(bind=engine)
Session = Session_class()

class RedisLogger():
    def log_data(self, dnsobj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        domain = request.q.qname.__str__().rstrip('.')
        print('new dnslog : domain--->{} \t type--->{} \t ip--->{}'.format(domain, QTYPE[request.q.qtype], handler.client_address[0]))
        now = datetime.datetime.now()
        try:
            logids = domain.split('.')
            if len(logids) >= 3:
                domain_id = logids[-3]
            else:
                return 1
            user_selectobj = Session.query(User).filter_by(logid=domain_id)
            user_selectdata = user_selectobj.first()
            if user_selectdata:
                sql_obj = Dnslog(record=domain, ip_from=handler.client_address[0], record_time=func.now(), owner_id=user_selectdata.id)
                Session.add(sql_obj)
                Session.commit()
                print('[+ SQL] domain--->{} \t type--->{} \t ip--->{}'.format(domain, QTYPE[request.q.qtype], handler.client_address[0]))
                message_sender(sql_obj)

        except Exception as e:
            Session.rollback()
            print('[SQL ERROR] ' + domain + ' ' + str(e))
            f = open('sqlerror.txt', 'a')
            f.write('domain--->{} \t type--->{} \t ip--->{}'.format(domain, QTYPE[request.q.qtype], handler.client_address[0]))
            f.write('\n')
            f.write(str(e))
            f.write('\n----------------------------------------')
            f.close()
        finally:
            Session.close()


    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass


class ZoneResolver(BaseResolver):
    """
        Simple fixed zone file resolver.
    """

    def __init__(self, zone, glob=False):
        """
            Initialise resolver from zone file.
            Stores RRs as a list of (label,type,rr) tuples
            If 'glob' is True use glob match against zone file
        """
        self.zone = [(rr.rname, QTYPE[rr.rtype], rr)
                     for rr in RR.fromZone(zone)]
        self.glob = glob
        self.eq = 'matchGlob' if glob else '__eq__'

    def resolve(self, request, handler):
        """
            Respond to DNS request - parameters are request packet & handler.
            Method is expected to return DNS response
        """
        reply = request.reply()

        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]
        if qtype == 'TXT':
            txtpath = os.path.join(tempfile.gettempdir(), str(qname).lower())
            if os.path.isfile(txtpath):
                reply.add_answer(
                    RR(qname, QTYPE.TXT, rdata=TXT(open(txtpath).read().strip())))
        for name, rtype, rr in self.zone:
            # Check if label & type match
            if getattr(qname,self.eq)(name) and (qtype == rtype or qtype == 'ANY' or rtype == 'CNAME'):
                # If we have a glob match fix reply label
                if self.glob:
                    a = copy.copy(rr)
                    a.rname = qname
                    reply.add_answer(a)
                else:
                    reply.add_answer(rr)
                # Check for A/AAAA records associated with reply and
                # add in additional section
                if rtype in ['CNAME', 'NS', 'MX', 'PTR']:
                    for a_name, a_rtype, a_rr in self.zone:
                        if a_name == rr.rdata.label and a_rtype in [
                            'A', 'AAAA'
                        ]:
                            reply.add_ar(a_rr)
        if not reply.rr:
            reply.header.rcode = RCODE.NXDOMAIN
        return reply

def message_sender(data: Dnslog):
    userobj = Session.query(User).filter_by(id=data.owner_id).first()
    DingtalkFlag = userobj.dingtalk_flag
    BarkFlag = userobj.bark_flag
    if DingtalkFlag:
        field_list = re.findall(r'\$\{.*?\}\$', dingtalk_robot_message_template)
        message = dingtalk_robot_message_template
        for i in field_list:
            message = message.replace(i, str(getattr(data, i.replace('${', '').replace('}$', ''))))
        dingtalk_robot_message_sender(userobj.dingtalk_robot_token, 'DNS请求 '+data.record, message)
    if BarkFlag:
        bark_message_sender()


def start_server():
    zone = '''
*.{dnsdomain}.       IN      NS      {ns1domain}.
*.{dnsdomain}.       IN      NS      {ns2domain}.
*.{dnsdomain}.       IN      A       {serverip}
{dnsdomain}.       IN      A       {serverip}
'''.format(
        dnsdomain=DNS_DOMAIN,
        ns1domain=NS1_DOMAIN,
        ns2domain=NS2_DOMAIN,
        serverip=SERVER_IP
    )
    resolver = ZoneResolver(zone, True)
    logger = RedisLogger()
    print("[+] DNS server listen on {}:{} [UDP] ServerIP: {}".format('0.0.0.0', str(DNS_PORT), SERVER_IP))

    udp_server = DNSServer(resolver, port=DNS_PORT, address='', logger=logger)
    udp_server.start()


if __name__ == '__main__':
    start_server()
