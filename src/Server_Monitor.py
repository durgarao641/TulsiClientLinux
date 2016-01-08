import smtplib
import time
from os import path
import ConfigParser

class Server_Monitor(object):
    def __init__(self):
        self.this_failed_services={}
	self.conf = ConfigParser.ConfigParser()
    def correct_services(self,fail_services):
        fs={}
        for node in fail_services:
            if node not in self.this_failed_services:
                fs[node]=fail_services[node]
            else:
                for ser in fail_services[node]:
                    if ser not in self.this_failed_services[node]:
                        if node in fs:
                            fs[node].append(ser)
                        else:
                            fs[node]=[ser]
        us={}
        for node in self.this_failed_services:
            if node not in fail_services:
                us[node]=self.this_failed_services[node]
            else:
                for ser in self.this_failed_services[node]:
                    if ser not in fail_services[node]:
                        if node in us:
                            us[node].append(ser)
                        else:
                            us[node]=[ser]
        self.this_failed_services=fail_services
        return fs,us

    def send_mail(self,fail_services,up_services):
	self.conf.read('tulsiclient.conf')
        print fail_services,"failed"
        print up_services,"up"
        msg=""
        if fail_services:
            msg = msg + "Failed Services:\n"
            for ser in fail_services:
                for f in fail_services[ser]:
                    msg = msg + f + "   "
                msg = msg + " failed in " + ser + "\n\n"
        if up_services:
            msg = msg + "UP Services:\n"
            for ser in up_services:
                for f in up_services[ser]:
                    msg = msg + f + "   "
                msg = msg + " up in " + ser + "\n\n"
	try:
	    domain_mail = self.conf.get('mailid','domain_mail').lower()
	    smtp_server = self.conf.get('mailid','smtp_server')
	    smtp_port = int(self.conf.get('mailid','smtp_port'))
            fromaddr = self.conf.get('mailid','from')
	    toaddrs = self.conf.get('mailid','to').split(',')
	    username = fromaddr
	    password = self.conf.get('mailid','password')
	except:
	    domain_mail = 'gmail'
	    smtp_server = 'smtp.gmail.com'
	    smtp_port = 465
	    fromaddr = 'jagathasureshbabu@gmail.com'
            toaddrs  =['ramanagak@vedams.com','rekhapriyankac@vedams.com']
	    username = 'jagathasureshbabu@gmail.com'
	    password = 'suresh111'
        subject = 'ALERT'
        text = ' %s ' %(msg)
        text=text+"\n\nplease do not reply to this mail.This is an automated mail sent by Tulsi"
        msg='subject:%s\n\n%s'%(subject,text)
	if domain_mail is 'yahoo':
	    server = smtplib.SMTP(smtp_server,smtp_port)
	    server.starttls()
	else:
            server = smtplib.SMTP_SSL(smtp_server,smtp_port)
            server.ehlo()
        server.login(username,password)
        for i in toaddrs:
            server.sendmail(fromaddr, i, msg)

    def alert_module(self):
        while(True):
            file_path=path.relpath("clusterStatus.txt")
	    with open(file_path) as fo:
	    	statusdata=fo.read() 
            fo.close()
            fail_services={}
            status_lines = statusdata.split('\n')
            for line in status_lines:
                n=line.find('Names')
                if(n!=-1):
                    disk_names=line[n+7:].split(',')
                else:
                    line_=line.find(':')
                    host_name=line[:line_]
                    if line[line_+1:line_+2]!='s':
                        if line[line.find(',')+1:]!='g':
                            if host_name!='':
                                fail_services[host_name]=['swift-proxy/Tulsi']
                    else:
                        health=[line[line.find('[')+1:line.find(']')]]
                        health=health+line[line.find(']')+2:].split(',')
                        i=1
                        while(i<len(health)):
                            if health[i]!='g':
                                if host_name not in fail_services:
                                    fail_services[host_name]=[]
                                if i==1:
                                    h=health[0].split(',')
                                    for j in h:
                                        fail_services[host_name].append(j[2:j.find(':')])
                                else:
                                    fail_services[host_name].append(disk_names[i-2])
                            i=i+1
            fail_services,up_services=self.correct_services(fail_services)
            if fail_services or up_services:
                self.send_mail(fail_services,up_services)
            time.sleep(10)
if __name__=='__main__':
    alert_monitor=Server_Monitor()
    alert_monitor.alert_module()
