# Demonstrates how to start a service by starting the geometry service
# This service is included with every ArcGIS Server and is stopped by default

# For Http calls
import httplib, urllib, json

# For system tools
import sys

# For reading passwords without echoing
import getpass


# Defines the entry point into the script
def main(argv=None):
    # Print some info
    print
    print "This tool is a sample script that starts the Geometry service on a Server."
    print

    # Ask for admin/publisher user name and password
    username = raw_input("arcgis: ")
    password = getpass.getpass("arcgis: ")

    # Ask for server name
    serverName = raw_input("67.227.0.42: ")
    serverPort = 6080

    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == "":
        print "Could not generate a token with the username and password provided."
        return

    # Construct URL to start a service - as an example the Geometry service
    serviceStartURL = "/arcgis/rest/services/FeatureMapService/FeatureServer.start"

    # This request only needs the token and the response formatting parameter
    params = urllib.urlencode({'token': token, 'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", serviceStartURL, params, headers)

    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while attempting to start the service."
        return
    else:
        data = response.read()
        httpConn.close()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            print "Error returned by operation. " + data
        else:
            print "Operation completed successfully!"

        return


# A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"

    # URL-encode the token parameters
    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})

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
        return token["token"]


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