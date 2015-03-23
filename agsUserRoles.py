Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> # This script creates a bank of users and roles given a comma-separated text file
#  They should be listed in the following format and saved in a file with a .txt extension:
#
#  User,Role,RoleType,Password,EMail,FullName,Description
#  John,Admins,ADMINISTER,changeme,johndoe@esri.com,John Doe,Server admin
#  Jane,Publishers,PUBLISH,changeme,janedoe@esri.com,Jane Doe,Server publisher
#  Etc.

import json, urllib,httplib

# For system tools
import sys

# For reading passwords without echoing
import getpass


def main(argv=None):
    # Ask for admin/publisher user name and password
    username = raw_input("arcgis: ")
    password = getpass.getpass("9ball1: ")

    # Ask for server name & port
    serverName = raw_input("67.227.0.42: ")
    serverPort = 6080

    # Input File with the Role and user information
    inFile = raw_input("C:\testing\agsUsersRoles.txt:")

    # InFile = r"C:\testing\agsUsersRoles.txt"
    opnFile = open(inFile,'r')

    # Dictionaries to store user and role information
    roles = {}
    users = {}   
    addUserRole = {}

    # Read the next line 
    ln = opnFile.readline()

    # Counter to get through the column header of the input file
    num = 0
    while ln:
        if num == 0:
            pass # File header
        else:
            # Split the current line into list
            lnSplt = ln.split(",")
            
            # Build the Dictionary to add the roles
            roles[lnSplt[1]] = {lnSplt[2]:lnSplt[len(lnSplt) -1].rstrip()}
           
            # Add the user information to a dictionary
            users["user" + str(num)] = {"username":lnSplt[0],"password":lnSplt[3],"fullname":lnSplt[5],"email":lnSplt[4],"description":lnSplt[-1].rstrip()}

            # Store the user and role type in a dictionary
            if addUserRole.has_key(lnSplt[1]):
                addUserRole[lnSplt[1]] =  addUserRole[lnSplt[1]] + "," + lnSplt[0]
            else:
                addUserRole[lnSplt[1]] = lnSplt[0]

        # Prepare to move to the next line        
        ln = opnFile.readline()
        num +=1

    # Get a token and connect
    token = getToken(username, password,serverName,serverPort)
    if token == "":
            sys.exit(1)

    # Call helper functions to add users and roles
    addRoles(roles, token,serverName,serverPort)
    addUsers(users,token,serverName,serverPort)
    addUserToRoles(addUserRole,token,serverName,serverPort)


def addRoles(roleDict, token, serverName, serverPort):
    
    for item in roleDict.keys():
        # Build the dictionary with the role name and description
        roleToAdd = {"rolename":item}

        # Load the response
        jsRole = json.dumps(roleToAdd)
        
        # URL for adding a role
        addroleURL = "/arcgis/admin/security/roles/add"
        params = urllib.urlencode({'token':token,'f':'json','Role':jsRole})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        # Build the connection to add the roles to the server
        httpRoleConn = httplib.HTTPConnection(serverName, serverPort)
        httpRoleConn.request("POST",addroleURL,params,headers)

        response = httpRoleConn.getresponse()
        if (response.status != 200):
            httpRoleConn.close()
            print "Could not add role."
            return
        else:
            data = response.read()
            
            # Check that data returned is not an error object
            if not assertJsonSuccess(data):          
                print "Error when adding role. " + str(data)
                return
            else:
                print "Added role successfully"

        httpRoleConn.close()

        # Assign a privilege to the recently added role 
        assignAdminUrl = "/arcgis/admin/security/roles/assignPrivilege"
        params = urllib.urlencode({'token':token,'f':'json',"rolename":item, "privilege":roleDict[item].keys()[0]})
            
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        # Build the connection to assign the privilege
        httpRoleAdminConn = httplib.HTTPConnection(serverName, serverPort)
        httpRoleAdminConn.request("POST",assignAdminUrl,params,headers)

        response = httpRoleAdminConn.getresponse()
        if (response.status != 200):
            httpRoleAdminConn.close()
            print "Could not assign privilege to role."
            return
        else:
            data = response.read()
            
            # Check that data returned is not an error object
            if not assertJsonSuccess(data):          
                print "Error when assigning privileges to role. " + str(data)
                return
            else:
                print "Assigned privileges to role successfully"

        httpRoleAdminConn.close()


def addUsers(userDict,token, serverName, serverPort):

    for userAdd in userDict:
        jsUser = json.dumps(userDict[userAdd])
        
        # URL for adding a user
        addUserURL = "/arcgis/admin/security/users/add"
        params = urllib.urlencode({'token':token,'f':'json','user':jsUser})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        # Build the connection to add the users
        httpRoleConn = httplib.HTTPConnection(serverName, serverPort)
        httpRoleConn.request("POST",addUserURL,params,headers)


        httpRoleConn.close()
       

def addUserToRoles(userRoleDict,token, serverName, serverPort):
    for userRole in userRoleDict.keys():

        # Using the current role build the URL to assign the right users to the role
        addUserURL = "/arcgis/admin/security/roles/addUsersToRole"
        params = urllib.urlencode({'token':token,'f':'json',"rolename":userRole,"users":userRoleDict[userRole]})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
        # Build the connection
        httpRoleConn = httplib.HTTPConnection(serverName, serverPort)
        httpRoleConn.request("POST",addUserURL,params,headers)

        response = httpRoleConn.getresponse()
        if (response.status != 200):
            httpRoleConn.close()
            print "Could not add user to role."
            return
        else:
            data = response.read()
            
            # Check that data returned is not an error object
            if not assertJsonSuccess(data):          
                print "Error when adding user to role. " + str(data)
                return
            else:
                print "Added user to role successfully"
                    
        httpRoleConn.close()
        

def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"
    
    params = urllib.urlencode({'username': username, 'password': password,'client': 'requestip', 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        data = response.read()
        httpConn.close()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):            
            return
        
        # Extract the token from it
        token = json.loads(data)        
        return token['token']            
        

# A function that checks that the input JSON object 
#  is not an error object.   
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True

# Script start 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
