import smtplib
import json
import time
import math
import fileinput
import sys
class HeartBeat:
    def replaceAll(self,file,searchExp,replaceExp):
        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)
    def send_mail(self,msg,host_name):
        fromaddr = 'jagathasureshbabu@gmail.com'
        toaddrs  = ['rekhapriyankac@vedams.com']#,'ramanagak@vedams.com','sureshbabuj@vedams.com','chaithanyak@vedams.com','alekhyam@vedams.com','srinivasd@vedams.com']
        subject = 'ALERT'
        text = ' %s %s ' %(msg,host_name)
        text=text+"\n\nplease do not reply to this mail.This is an automated mail sent by Tulsi"
        msg='subject:%s\n\n%s'%(subject,text)
        username = 'jagathasureshbabu@gmail.com'
        password = 'suresh111'
        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.ehlo()
        server.login(username,password)
        for i in toaddrs:
            server.sendmail(fromaddr, toaddrs, msg)
    def heartmodule(self,data):
        data_string=json.loads(data)
        key=data_string["hostname"]
        print key
        f=open("status1.txt","a+")
        text=f.read()
        if key not in text:
            now=math.ceil(time.time())
            f.write('\n'+key+": "+str(now)+" ,True")
            print "a write to file"
        f.close()
        f1=open("status1.txt","r+")
        for line in f1:
            if key in line:
                now=math.ceil(time.time())
                print now
                replaceExp=key+": "+str(now)+" ,True"
                self.replaceAll("status1.txt",line,replaceExp)
        f1.close()
        f1=open("status1.txt","r+")
        for line in f1:
            now=math.ceil(time.time())
            if key in line:
                var=line[line.find(" "):line.find(",")]
                print var
                var=float(var)
                if now-var>5 and line.find(",True")!=-1:
                    replaceExp=key+": "+str(now)+",False"
                    self.replaceAll("status1.txt",line,replaceExp)
                    msg="Tulsi service down in :"
                    self.send_mail(msg,key)
                    print msg
        f1.close()
        '''text1=f1.read()
        text1.rstrip('\n')
        pos=text1.find(data_string["hostname"])
        now=time.time()
        now=math.round(now)
        space=text1.find(" ",pos)
        text1=text1[:space+1]+str(now)+
        if key in self.ip_arry_time:
            now=time.time()
            self.ip_arry_time[key][0]=now
            print self.ip_arry_time
            if self.ip_arry_time[key][1] is False:
                text2=""
                self.ip_arry_time[key][1]=True
                self.send_mail("Tulsi service is up in :",key)
                f=open("status3.txt","r+")
                text=f.read()
                text.rstrip('\n')
                print text
                f.seek(0,0)
                host_pos=text.find(key)
                text=text[:host_pos+len(key)+2]+" True"
                text=text.rstrip('\n')
                f.write(text)
                print text
                f.close()
            self.ip_arry_time[key][2]=True
        now=time.time()
        for i in self.ip_arry_time:
            if (now - self.ip_arry_time[i][0]) > 10:
                self.ip_arry_time[i][1]=False
                if self.ip_arry_time[i][2]:
                    self.send_mail("Tulsi service down in:",i)
                    f=open("status.txt","r+")
                    text=f.read()
                    text.rstrip('\n')
                    print text
                    init_pos=text.find(i)
                    f.seek(0,0)
                    text=text[:init_pos+len(i)+2]+"False"
                    self.ip_arry_time[i][2]=False
                    text=text.rstrip('\n')
                    f.write(text)
                    print text
                    f.close()'''
