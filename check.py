import ssl,socket
host='www.7sportsacademy.com'
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
print(neededinfo)