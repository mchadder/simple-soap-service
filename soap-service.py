import http.server

PORT = 9999

def wp(self, rq):
  self.server_version = "ChaddersSOAPServer/1.0"
#  self.sys_version = ""

  # enumerate the request headers
  #for hdr in self.headers:
  #  print(hdr,self.headers[hdr])

  # get the submitted data
  # Note, it would generally not be a good idea to do the below in a generic sense, since Content-Length could be enormous (if specified) and then "data" would be massive.
  # It'd be better to loop around a given offset at a time, it all depends on the context. In this case (i.e.a SOAP service), you usually need to validate that the submitted data
  # is a valid SOAP message and hence (if using DOM) you would need to construct the whole message. SAX would be better for "larger" messages, but
  # of course, you need to code that completely differently.

  # length = int(self.headers['Content-Length'])

  # print("length : " + str(length))
  # Note, need to include the encoding when converting to a string
  #data = str(self.rfile.read(length), 'utf8')
  #print(data)

# set the return time here (in time.time() format or None if current time required), this is included in send_response() as the "Date" HTTP header
  self.date_time_string(None)

  # Set the HTTP response code 200 ("OK")
  self.send_response(200)

  # Can include headers directly by the send_header() method
  if rq == "GET":
    self.send_header("Content-Type", "text/html")
    resp = "<html>"
    resp += "<body>"
    resp += "<h1>Chadders Test SOAP Service</h1>"
    resp += "You issued a GET request, you need to submit the SOAP XML as a POST request to receive the correct response"
    resp += "</body>"
    resp += "</html>"
  elif rq == "POST":
    # application/soap+xml is valid for SOAP1.2 only, SOAP 1.1 should use text/xml
    # http://www.ietf.org/rfc/rfc3902.txt
    # self.send_header("Content-Type", "application/soap+xml")
    self.send_header("Content-Type", "text/xml; charset=utf-8")
#    self.send_header("Content-Length", "123")
    # encoding="UTF-8"
    resp = "<?xml version=\"1.0\"?>"

    # SOAP 1.2 xmlns should be http://www.w3.org/2003/05/soap-envelope
    # SOAP 1.1 xmlns should be http://schemas.xmlsoap.org/soap/envelope/
    resp += "<soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">"
    # resp += "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\">"
    resp += "<soap:Body>"
    # resp += "<Chadders><![CDATA[<x/>]]></Chadders>"
    resp += "<GetSMSReplyResponse xmlns=\"http://www.textapp.net/\"><GetSMSReplyResult><![CDATA[<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    resp += "<GetSMSReplyResponse><Transaction><Code>3</Code><Description>Transaction returns no result</Description></Transaction></GetSMSReplyResponse>]]>"
    resp += "</GetSMSReplyResult></GetSMSReplyResponse>"

    resp += "</soap:Body></soap:Envelope>"

  self.send_header("Content-Length", str(len(resp)))

  self.end_headers()

  self.wfile.write(bytes(resp, 'utf8'))
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
       wp(self, 'GET')
    def do_POST(self):
       wp(self, 'POST')
try:
# can specify the address specifically, and it will only serve with addresses exactly that
#    server = http.server.HTTPServer(('10.100.4.221', PORT), MyHandler)
    server = http.server.HTTPServer(("", PORT), MyHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
