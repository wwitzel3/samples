#!/usr/bin/python

'''PEFTP.py
Handles requests for creating Accounts and Directories on the local system.
This script needs to be a member of a user that has password-less access to
the sudo command.

Depends on AccountHandler.py and DirectoryHandler.py

Internal Note:
PEFTP and associated libraries use TABs not spaces.
Python is whitespace dependant, if you edit this file make
sure your editor is set to use TAB and not replace tabs with
spaces.

Copyright GriZella, Corp. 2006'''

import sys

from AccountHandler import AccountHandler
from DirectoryHandler import DirectoryHandler

def index():
    '''Main action handler for PEFTP service calls
    Dispatches the requests to the proper handler using a dictionary map.

    req: Apache request data
    data: the params and request data sent by the caller'''

    sys.stdout.write('Content-type: text/plain \n\n')
    
    try:
        import cgi
        import cgitb; cgitb.enable()
    except ImportError:
        package = _except(errorCode="WW3_EX01", technicalMessage=str(sys.exc_info()[0]))
        output = _generateVO('ResponseVO', package)

        _write(output)
        return
 
    try:
        data = cgi.parse() # reads params
        content = sys.stdin.read() # reads VO/stream data
                
        handler = None
        definedAction = None

        # Break out the service and the action
        service = data['Service'][0]
        action = data['Action'][0]

        if service == 'PEFTPAccountServiceHandler':
            handler = AccountHandler(data, content)
            definedAction = {'passwd':handler.passwd}
            
        elif service == 'PEFTPDirectoryServiceHandler':
            handler = DirectoryHandler(data, content)
            definedAction = {'listing':handler.listing}

        genericAction = {'create':handler.create,
                         'remove':handler.remove,
                         'exists':handler.exists}

        # Action to method map (like a switch)
        # Combine the definedAction and genericAction maps
        name, package = dict(genericAction, **definedAction).get(action, _default)()
        actionOutput = _generateVO(name, package)

        # Did the object return a response VO?
        # If not, generate and write a generic success
        if not name == 'ResponseVO':
            response = _generateVO('ResponseVO', _default(status="APPROVED", errorCode="WW3_OK",
                                                          technicalMessage="Success",
                                                          displayMessage="Success", action="OK"))
            _write(response)
        _write(actionOutput)

        return

    except:
        package = _except(errorCode="WW3_EX02", technicalMessage=str(sys.exc_info()[0]))
        output = _generateVO('ResponseVO',package)

        _write(output)
        return

'''Local methods
Prepending mod_python method with an '_' prevents them from being called remotely.
All methods for internal script use should be prepended with a '_' '''

def _default(status='DENIED', errorCode='WW3_DEF1',
             technicalMessage='Action Not Found',
             displayMessage='Action Not Found',
             action='SHOWMESSAGE'):
    '''Default action if no matching actions are found for in the
    handler for the callers request. Returns an Denied, Action Not Found package
    for use in a ReponseVO'''
    
    return {'status':status,
            'errorCode':errorCode,
            'technicalMessage':technicalMessage,
            'displayMessage':displayMessage,
            'action':action}

def _except(errorCode="WW3_EX00", technicalMessage="Python Exception"):
    '''Uses _default to implement an exception default package creator'''
    return _default(status="ERROR", errorCode=errorCode,
                    technicalMessage=technicalMessage,
                    displayMessage="Python Exception")

def _generateVO(name, package):
    '''Takes a name and a package (Python dictionary), and generates the proper VO.
    It uses the values for content and keys to generate the header

    name: VO Name, e.g. ResponseVO
    package: dictionary, contains header (as keys) and content (as values)'''

    btag = "<%s>" % (name)
    etag = "</%s>" % (name)

    header = '\t'.join(package.keys())
    content = '\t'.join(package.values())

    return '\n'.join([btag, header, content, etag])

def _write(w):
    sys.stdout.write(w)
    sys.stdout.write('\n')
    return


'''assure that if being ran for the first time as a new instance
that our entry point is always index()'''
if __name__ == '__main__':
    index()
