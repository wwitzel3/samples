''' PEFTPDirectoryServiceHandler

    Services: DirectoryHandler
    Actions: Exists, Create, Remove, List

    Copyright GriZella, Corp 2006.
'''

FTPGROUP = "ftpuser"
FTPMODE = '775'
FTPDIR = '/home/ftp'

from AccountHandler import AccountHandler

from os import path, system

class DirectoryHandler:
    '''DirectoryHandler

        Service: PEFTPDirectoryServiceHandler
        Actions: Create, Exists, Remove, List
        Parms  : ftpLogin, ftpPass, ftpAddr, ftpPort, userHomeDir
        Data   : DirectoryListVO
    '''
    
    def __init__(self, request, content):
        try:
            self.content = _getcontent(content)
        except:
            self.content = ''

        self.account = AccountHandler(request,content)
        
        self.default = ['']
        self.user = request.get('ftpLogin', self.default)[0]
        self.passwd = request.get('ftpPass', self.default)[0]
        self.dir = path.join(FTPDIR,self.user)
        self.otherDir = request.get('ftpDir', self.default)[0]

        self.name = 'ResponseVO'
        self.package = {'status':'APPROVED', 'errorCode':'WW3_OK',
                        'technicalMessage':'Success', 'displayMessage':'Success',
                        'action':''}

    def create(self):
        '''Create the new folders for the user. If parent folders do not exist
        create them as needed'''
        try:
            acctName, acctPackage = self.account.exists()
            folderName, folderPackage = self.exists()
            
            if not acctPackage['action'] == 'EXISTS':
                self.package = acctPackage
                if self.package['action'] == 'NOTEXISTS':
                    self.package['action'] = 'USERNOTEXISTS'
                self.package['status'] = 'DENIED'
                self.package['errorCode'] = 'WW3_BU01'
                self.package['technicalMessage'] = 'Oops!'
                self.package['displayMessage'] = 'Oops!'
                
            elif not folderPackage['action'] == 'EXISTS':
                self.package = folderPackage
                self.package['action'] = 'DIRNOTEXISTS'
                self.package['errorCode'] = 'WW3_BUD03'
                self.package['status'] = 'DENIED'
                self.package['technicalMessage'] = 'Oops!'
                self.package['displayMessage'] = 'Oops!'
            else:
                if path.isdir(self.dir):
                    for newDir in self.content:
                        crPath = path.join(self.dir,newDir.lstrip('/'))
                        system("sudo -u root mkdir -p %s" % (crPath))
                    system("sudo -u root chown -R %s:%s %s" % (self.user, FTPGROUP, self.dir))
                    system("sudo -u root chmod -R %s %s" % (FTPMODE, self.dir))
                    self.package['action'] = 'CREATED'
                else:
                    self.package['status'] = 'DENIED'
                    self.package['action'] = 'MISSINGINPUT'
                    self.package['technicalMessage'] = 'ftpDir must be populated'
                    self.package['errorCode'] = 'WW3_MI01'
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_DC01'

        return self.name, self.package

    def exists(self):
        '''Check if a path exists'''
        try:
            acctName, acctPackage = self.account.exists()
            
            if not acctPackage['action'] == 'EXISTS':
                self.package = acctPackage
                if self.package['action'] == 'NOTEXISTS':
                    self.package['action'] = 'USERNOTEXISTS'
                self.package['status'] = 'DENIED'
                self.package['errorCode'] = 'WW3_BU02'
                self.package['technicalMessage'] = 'Oops!'
                self.package['displayMessage'] = 'Oops!'
            else:
                if path.isdir(path.join(self.dir,self.otherDir.lstrip('/'))):
                    self.package['action'] = 'EXISTS'
                else:
                    self.package['action'] = 'NOTEXISTS'
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_DE01'
            
        return self.name, self.package

    def remove(self):
        '''Remove a folder and all its subfolders (rm -rf)'''
        try:
            acctName, acctPackage = self.account.exists()
            folderName, folderPackage = self.exists()
            
            if not acctPackage['action'] == 'EXISTS':
                self.package = acctPackage
                if self.package['action'] == 'NOTEXISTS':
                    self.package['action'] = 'USERNOTEXISTS'
                self.package['status'] = 'DENIED'
                self.package['errorCode'] = 'WW3_DR03'
                self.package['technicalMessage'] = 'Oops!'
                self.package['displayMessage'] = 'Oops!'
            elif not folderPackage['action'] == 'EXISTS':
                self.package = folderPackage
                self.package['action'] = 'DIRNOTEXISTS'
                self.package['errorCode'] = 'WW3_DR04'
                self.package['status'] = 'DENIED'
                self.package['technicalMessage'] = 'Oops!'
                self.package['displayMessage'] = 'Oops!'
            else:
                if path.isdir(self.dir):
                    for newDir in self.content:
                        rmPath = path.join(self.dir,newDir.lstrip('/'))
                        if not rmPath.rstrip('/') == self.dir.rstrip('/'):
                            system("sudo -u root rm -rf %s" % (rmPath))
                            self.package['action'] = 'REMOVED'
                        else:
                            self.package['status'] = 'DENIED'
                            self.package['action'] = 'CANNOTREMHOME'
                            self.package['displayMessage'] = 'Error, some files may have not been deleted'
                            self.package['technicalMessage'] = 'You cannot delete your home directory, please see Account Remove'
                            self.package['errorCode'] = 'WW3_DR02'
                            break
                else:
                    self.package['status'] = 'DENIED'
                    self.package['action'] = 'MISSINGINPUT'
                    self.package['technicalMessage'] = 'ftpDir must be populated'
                    self.package['errorCode'] = 'WW3_MI01'
            
        except:
            import sys
            self.package['status'] = 'ERROR'
            self.package['action'] = 'SHOWMESSAGE'
            self.package['technicalMessage'] = str(sys.exc_info()[0])
            self.package['displayMessage'] = 'Python Exception'
            self.package['errorCode'] = 'WW3_DR01'

        return self.name, self.package
    
    def listing(self):
        '''Grab folder and subfolder listing from userHomeDir'''
        acctName, acctPackage = self.account.exists()
        folderName, folderPackage = self.exists()
        
        if not acctPackage['action'] == 'EXISTS':
            self.package = acctPackage
            if self.package['action'] == 'NOTEXISTS':
                self.package['action'] = 'USERNOTEXISTS'
            self.package['status'] = 'DENIED'
            self.package['errorCode'] = 'WW3_DL01'
            self.package['technicalMessage'] = 'Oops!'
            self.package['displayMessage'] = 'Oops!'
        elif not folderPackage['action'] == 'EXISTS':
            self.package = folderPackage
            self.package['errorCode'] = 'WW3_DL02'
            self.package['action'] = 'DIRNOTEXISTS'
            self.package['status'] = 'DENIED'
            self.package['technicalMessage'] = 'Oops!'
            self.package['displayMessage'] = 'Oops!'
        else:
            import os
            _dirstore = []
            [_dirstore.append(root.lstrip(self.dir)) for root, dirs, files in os.walk(path.join(self.dir,self.otherDir))]
            
            self.name = 'DirectoryListVO'
            self.package = {'dirName':'\n'.join(_dirstore)}
        return self.name, self.package
        

def _getcontent(data):
    data = data.split('\n')
    data = data[2:(len(data)-1)]
    return data
