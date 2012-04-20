''' PEFTPAccountServiceHandler

    Depends: pexcept (3rd party library)

    Services: AccountHandler
    Actions: Exists, Create, Remove, Passwd

    Copyright GriZella, Corp. 2006
'''

FTPGROUP = 'ftpuser'
FTPMODE = '775'
FTPSHELL = '/bin/false'
FTPDIR = '/home/ftp'

from os import path, system

class AccountHandler:
    '''AccountHandler

        Service: PEFTPAccountServiceHandler
        Actions: Create, Exists, Remove, Passwd
        Parms  : ftpLogin, ftpPass, ftpDir, ftpNewPass
    '''

    def __init__(self, request, content):
        try:
            self.content = _getcontent(content)
        except:
            self.content = ''

        self.default = ['']
        self.user = request.get('ftpLogin', self.default)[0]
        self.pwd = request.get('ftpPass', self.default)[0]
        self.dir = path.join(FTPDIR,self.user)
        self.newPasswd = request.get('ftpNewPass', self.default)[0]

        self.name = 'ResponseVO'
        self.package = {'status':'APPROVED', 'errorCode':'WW3_OK',
                        'technicalMessage':'Success', 'displayMessage':'Success',
                        'action':''}

    def create(self):
        '''Create new user, including ftpDir'''
        try:
            name, package = self.exists()
            
            if not package['action'] == 'EXISTS':
            
                if self.dir == '':
                    self.package['status'] = 'DENIED'
                    self.package['action'] = 'MISSINGINPUT'
                    self.package['technicalMessage'] = 'ftpDir must be populated'
                    self.package['errorCode'] = 'WW3_MI02'
                    
                elif self.pwd == '':
                    self.package['status'] = 'DENIED'
                    self.package['action'] = 'MISSINGINPUT'
                    self.package['technicalMessage'] = 'ftpPass must be populated'
                    self.package['errorCode'] = 'WW3_MI03'
                    
                else:
                    import crypt
                    import random
                    salt = str(random.random())
                    salt = salt[2:]
                    text = self.pwd
                    pwd = crypt.crypt(text,salt)
                    
                    system('sudo -u root useradd -d %s -m -g %s -s %s -p %s %s' % \
                              (self.dir, FTPGROUP, FTPSHELL, pwd, self.user))
                    self.package['action'] = 'CREATED'
            else:
                self.package['status'] = 'DENIED'
                self.package['action'] = 'ALREADYEXISTS'
                self.package['technicalMessage'] = 'ftpUser already exists'
                self.package['errorCode'] = 'WW3_UE01' 

        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['errorCode'] = 'WW3_AC01'
            self.package['displayMessage'] = 'Python Exception'

        return self.name, self.package
            
            

    def exists(self):
        '''Check for existing user'''
        try:
            import pexpect

            child = pexpect.spawn('sudo -u root /usr/sbin/usermod %s' % (self.user))
            index = child.expect(['exist', 'given'], timeout=100)
            if index == 0:
                self.package['action'] = 'NOTEXISTS'
            elif index == 1:
                self.package['action'] = 'EXISTS'

                if not self.pwd == '':
                    try:
                        import ftplib
                        ftp = ftplib.FTP('127.0.0.1')
                        ftp.login(user=self.user,passwd=self.pwd)
                        ftp.quit()
                    except ftplib.error_perm, e:
                        self.package['action'] = 'BADPASSWORD'
                        self.package['displayMessage'] = str(e)
                        
                if not self.dir == '':
                    import re
                    regex = '^%s:.*' % (self.user)
                    p = re.compile(regex)
                    fd = open('/etc/passwd','r')
                    data = fd.readlines()
                    fd.close()

                    for line in data:
                        m = p.match(line)
                        if not m == None:
                            break
                    
                    if m == None:
                        self.package['action'] = 'NOTEXISTS'
                    else:
                        userStr = str(m.group())
                        userStr = userStr.split(':')
                        if self.dir.find(userStr[5]) == -1:
                            self.package['action'] = 'BADHOMEDIR'
                            self.package['errorCode'] = 'WW3_BD01'
                            self.package['technicalMessage'] = 'Oops!'
                            self.package['displayMessage'] = 'Oops!'
                        
                    
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_AE01'

        return self.name, self.package

    
    def remove(self):
        '''Remove a user and ALL folders under that user'''
        try:
            system('sudo -u root userdel -r %s' % (self.user))
            self.package['action'] = 'REMOVED'
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_AR01'

        return self.name, self.package

    def passwd(self):
        '''Change users current password'''
        import pexpect
        
        try:
            if not self.newPasswd == '':
                child = pexpect.spawn('sudo -u root /bin/passwd %s' % (self.user))
                child.expect('assword:',timeout=100)
                child.sendline('%s' % (self.newPasswd))
                child.expect('assword:',timeout=100)
                child.sendline('%s' % (self.newPasswd))
                child.expect('success', timeout=100)
                
                self.package['action'] = 'CHANGED'
            else:
                self.status['status'] = 'DENIED'
                self.package['action'] = 'MISSINGINPUT'
                self.package['technicalMessage'] = 'ftpNewPass must be populated'
                self.package['errorCode'] = 'WW3_MI03'

        except pexpect.EOF:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python EOF'
            self.package['errorCode'] = 'WW3_EO01'
            
        except pexpect.TIMEOUT:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Timeout'
            self.package['errorCode'] = 'WW3_TO01'
            
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_AP01'
            
        return self.name, self.package
