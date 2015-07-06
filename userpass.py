#!/usr/bin/env python
#Username passwod generator - Mark Baggett
#Searches for Linkedin.com users of the target company.  
#Then lauches CEWL on each users LinkedIn Profile to build a custom password list per users
#If the user has a photo on linkedin, it will use TinEye to find other accounts or pages used by that individual and use CEWL on them
#If the user list "Their website", facebook, myspace, etc in linkedin we build password lists off of those pages.
#The Default CeWL path assumes your using the Samurai WTF from http://samurai.inguardians.com/. 
#The easiest way to make CeWL run in that environment is to "cd /usr/bin/samurai/cewl" before launching CeWL (or this script)

import re
import urllib
import urllib2 

def TinEyeLinks(imageurl):
    url="http://www.tineye.com/search"
    values = {'url' : imageurl}
    headers = { 'User-Agent' : 'Mozilla/5.0'}
    data = urllib.urlencode(values)
    requestor = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(requestor)
    content = response.read()
    # Title contains number of result  - <title>\n7 results\n - TinEye</title>
    NumTinEyes = re.search('<title>\s+[0-9]',content).group(0).split('\n')[1]
    resultset=[]
    if NumTinEyes:
        TinTargets = re.findall('title="http://[a-zA-Z0-9./_]+',content)
        print "....Adding " + str(len(TinTargets)) + " TinEye.com Pages."
        for target in TinTargets:
            resultset.append(target.split('"')[1])
    return resultset

def cewllinkedinpages(linkedinurl,username):
    print "..Fetching Linkedin Profile ", linkedinurl
    request = urllib2.Request(linkedinurl)
    requestor = urllib2.build_opener()
    request.addheaders = [('User-agent', 'Mozilla/5.0')]
    content = requestor.open(request).read()
    linkedinurls = uniqueurls(re.findall('<li>\s*<a\shref="http://[a-zA-Z0-9]+\.(?!linkedin)[a-zA-Z0-9_./-]+', content))
    if tineyeon:
        #This section of code finds additional pages for the user by using TinEye.   It works fine until TinEye detects you as a bot and throws up a captcha
        photourl= re.search('<img\ssrc=\"http\://media.linkedin.com/[a-zA-Z0-9_/]+.jpg"\sclass="photo"',content)
	if photourl:
            print "..Using TinEye.com on photo " + photourl.group(0).split('"')[1]
            linkedinurls += TinEyeLinks(photourl.group(0).split('"')[1])
    print "..Found "+str(len(linkedinurls))+" Linkedin page references."
    for curltarget in linkedinurls:
       print "..Launching CEWL for "+curltarget
       os.system(PathToCewl +" -m "+ str(wordlength) + " -d " + str(cewldepth) +" "+ curltarget + " >> " + outputdir + "/" +username+"_passwords.txt")

def uniqueurls(notunique):
    keys = {}
    for urls in notunique:
	index=urls.split('"')[1]
        keys[index] = 'ocupodo'
    return keys.keys()

def search(q, start = 0, num = 10):
    url = 'http://www.google.com/m/search?'
    query = urllib.urlencode({'q':q, 'start':start, 'num':num})
    print "Making Google Query ", url+query
    request = urllib2.Request(url + query)
    requestor = urllib2.build_opener()
    request.addheaders = [('User-agent', 'Mozilla/5.0')]
    content = requestor.open(request).read()
    return content

def printhelp():
    print """Usage:   userpass.py "Company Name" [options]
Options:
-g  The number of google pages to parse looking for employees of the Company (default is 2)
-t  Enable TinEye lookup.   (default is Disabled)
-s  additional search options 
-m  minimum word length to give to CeWL  (default is 5)
-d  depth of CeWL crawl (Default is 2)
-o  Absolute path to the output directory ex: /home/samurai (default is .)
-p  Path to CeWL binary (Default is "/usr/bin/samurai/cewl/cewl.rb")

Notes:
If the -t option is specified then the script attempt to locate additional user pages by cross referencing their Linkedin.com photo with TinEye.  Any additional pages are also parse with cewl and appended to the password file.  NOTE:TinEye bot detection will temporarily blacklist your IP address when using this option.  Use the -s to strictly limit your google results and limit the queries to TinEye or stay away from this option. 

If multiple pages are located for the user you should run the resulting password file through "uniq" to eliminate duplicate words found on multiple user pages.
 Ex:  "cat username_passwords.txt | uniq  > targetpasswords.txt"

Examples usage:  
./userpass.py "Company Name" -g 5
  - will run at a google depth of 5 searching for employees of company
./userpass.py "Employee Name" -s "additional search qualifier" -g 1 -o /home/myhome/ -m 10 -t
  - will start with a query of 'site:linkedin.com "Employee Name" additional search qualifiers'  (note the quotes on Employee name, but not on qualifier).  Will do a tineye lookup on the linkedin photo.  Will tell CeWL the minimum password length is 10 and will write the output to /home/myhome.
"""

if __name__ == '__main__':
    import os
    import sys
    import signal
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit())

    googledepth=2
    company=''
    addsearch=''
    wordlength = 5
    outputdir = '.'
    cewldepth=2
    PathToCewl="/usr/bin/samurai/cewl/cewl.rb "
    #PathToCewl="echo "
    tineyeon=False
    
    if '-h' in sys.argv or len(sys.argv)<2:
	printhelp()
	sys.exit(2)
    company=sys.argv[1]
    for i in range(2,len(sys.argv),1):
        if sys.argv[i] == '-g':
	    googledepth=int(sys.argv[i+1])
	elif sys.argv[i] == '-c':
	    company = sys.argv[i+1]
        elif sys.argv[i] == '-d':
	    domain = sys.argv[(i+1)]
	elif sys.argv[i] == '-t':
	    tineyeon=True
	elif sys.argv[i] == '-s':
	    addsearch=sys.argv[i+1]
        elif sys.argv[i] == '-o':
	    outputdir = sys.argv[i+1]
        elif sys.argv[i] == '-m':
	    wordlength = sys.argv[i+1]
        elif sys.argv[i] == '-d':
	    wordlength = sys.argv[i+1]
        elif sys.argv[i] == '-p':
	    PathToCewl = sys.argv[i+1]

    if company=='':
	print " Missing parameters.  You must specify a Company to target.  Try ./userpass.py -h"
	sys.exit(1)
    query = 'site:linkedin.com "'+ company+'" '+addsearch
    names_urls = []
    StartIndex = 0
    while StartIndex < googledepth:
        result=search(query, StartIndex*10,(StartIndex+1)*10)
        names_urls += re.findall(';u=http://\www\.linkedin\.com/pub/(?!dir)[a-zA-Z0-9/-]+.>[ |a-zA-Z0-9,.-]+', result)
	names_urls += re.findall(';u=http://\www\.linkedin\.com/in/[a-zA-Z0-9/-]+.>[ |a-zA-Z0-9,.-]+', result)
        StartIndex = StartIndex + 1
        for token in names_urls:
            token = token.lower()
            names_array=token.split(">")
            url_array=names_array[0].split("=")
            url=url_array[1][:-1]
            name=names_array[1].split(" ")
            fname=name[0]
            lname=name[1]
            print "User Identified - First name: ", fname, " Last name: ", lname 
            cewllinkedinpages(url, fname+lname)
	#If the google page doesn't contain "Next Page" we reached the end of the results
        if not 'Next page' in result:
	    print "End of Google search results reached."
	    break
