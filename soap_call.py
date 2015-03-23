import string, os, sys
import httplib


server_addr = httplib. HTTPConnection('67.227.0.42:6080')
service_action = "/arcgis/services/FeatureMapService/MapServer?wsdl"



body = """
<soap:Envelope xmlns:soapenv="http://www.esri.com/schemas/ArcGIS/10.1" xmlns:ns="http://schemas.xmlsoap.org/wsdl/">
<soap:Header/>
<soap:Body>
<ns:GetServiceDescriptions>
</ns:GetServiceDescriptions>
</soap:Body>
</soap:Envelope>"""

request = httplib.HTTPConnection('67.227.0.42:6080')
request.putrequest("POST", service_action)
request.putheader("Accept", "application/soap+xml, application/dime, multipart/related, text/*")
request.putheader("Content-Type", "text/xml; charset=utf-8")
request.putheader("Cache-Control", "no-cache")
request.putheader("Pragma", "no-cache")
request.putheader("SOAPAction", "http://" + '67.227.0.42:6080' + service_action)
request.putheader("Content-Length", str(len(body)))
request.endheaders()
request.send(body)
response = request.getresponse().read()

print response
