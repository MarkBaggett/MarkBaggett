import time,calendar,sys,glob,sqlite3,dateutil.parser
from optparse import OptionParser

kmlstart = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n' 
kmlend='</Document>\n</kml>\n'

def converttime(timestr):
    gmttime=time.gmtime(float(timestr)+calendar.timegm((2001,1,1,0,0,0,0,0,0)))
    return ('%s/%s/%s %s:%s:%s') % (gmttime[1],gmttime[2],gmttime[0],gmttime[3], gmttime[4], gmttime[5])

parser=OptionParser(usage='%prog [OPTIONS]')
parser.add_option('-o','--output',help='Specify path and filename that you want created.  If not provided it will create a locationmap.kml file in the current directory.',dest='output')
parser.add_option('-p','--path',default="/Users/*/Library/Application Support/MobileSync/Backup/*",help='Search path to look for databases.  By default it will use /Users/*/Library/Application Support/MobileSync/Backup/*',dest='path')
parser.add_option('-s','--start',help='Filter entries extracted from databases to those after or on the given start date.  Startdate is in the form mm/dd/yy or mm/dd/yy hh:mm:ss',dest='start')
parser.add_option('-e','--end',help='Filter entries extracted from databases to those before or on the given end date.  Enddata is in the form mm/dd/yy or mm/dd/yy hh:mm:ss',dest='end')
parser.add_option('-c','--nocell',action='store_true', help='Do not export Cell Tower data')
parser.add_option('-w','--nowifi',action='store_true', help='Do not export Wifi BSSID data')
parser.add_option('-v','--verbose',action='store_true', help='Print verbose output.')

(options,args)=parser.parse_args()

if options.nocell and options.nowifi:
    print "\nNothing to export when both -c and -w are specified.\n"
    sys.exit(2)

filter=""
if options.start:
   try:
       starttimestamp=time.mktime(dateutil.parser.parse(options.start).timetuple())-calendar.timegm((2001,1,1,0,0,0,0,0,0))
   except:
       print "Invalid Start Date/Time format.   Try -s \"mm/dd/yy hh:mm:ss\""
       sys.exit(2)
   filter=" where timestamp >= "+str(starttimestamp)

if options.end:
   try: 
       endtimestamp=time.mktime(dateutil.parser.parse(options.end).timetuple())-calendar.timegm((2001,1,1,0,0,0,0,0,0))
   except:
       print "Invalid End Date/Time format.   Try -e \"mm/dd/yy hh:mm:ss\""
       sys.exit(2)
   if options.start:
        filter=filter+" and timestamp <= "+str(endtimestamp)
   else:
        filter=" where timestamp <= "+str(endtimestamp)

sqlquery=""
if not options.nocell:
    sqlquery="select 'Cell ',timestamp,Longitude,Latitude,timestamp from CellLocation" + filter

if not options.nowifi:
     if not options.nocell:
           sqlquery=sqlquery+" union "
     sqlquery = sqlquery + "select 'Wifi ',MAC,Longitude,Latitude,timestamp from WifiLocation" + filter

sqlquery=sqlquery+" order by 5"

if options.verbose:
    print "\nUsing search path "+options.path
    print "\nFound "+str(len(glob.glob(options.path)))+" potential databases."
    print "\nExecuting query: "+sqlquery +"\n"

for files in glob.glob(options.path):
   answer=raw_input("\nProcess "+files+" ? [Y/N/Q]")
   if answer.lower()=="q":
       print "\nQuitting."
       sys.exit(0)
   if answer.lower()=="n":
       continue
   try:
      dbase=sqlite3.connect(files+"/4096c9ec676f2847dc283405900e284a7c815836")
   except:
      print "\nUnable to Open Database in the directory "+ file
      continue
   try:
      records=dbase.execute(sqlquery)       
   except:
      print "\nUnable to open the tables specified. "
   else:
      savefile="./locationmap.kml"
      if options.output:
            savefile=options.output
      try:
            outfile=open(savefile,"w")
      except:
            print "\n\nCould not create output file. Check path "+str(options.output)+"/locationmap.kml"
            sys.exit(2)
      outfile.write(kmlstart)
      coords=""
      reccount=0
      for rectype,reclabel, long,lat,ts in records:
         reccount=reccount+1
         if options.verbose:
               print ".",
         placemarkname=str(rectype)+str(reclabel)+" "+converttime(ts)
         if rectype=="Cell ":
              placemarkname=str(rectype)+converttime(ts)
         outfile.write( ('<Placemark>\n<name>%s</name>\n<Point>\n<coordinates>%6f,%6f</coordinates>\n</Point>\n</Placemark>\n') %(placemarkname,float(long),float(lat)))
         coords+=('%6f,%6f,1000 ') %(float(long),float(lat))
      print "\n"+str(reccount)+" records found in the database matching your criteria."
      if reccount==0:
           continue
      outfile.write("<Placemark>\n<name>Path with Altitude</name>\n<LineString>\n<extrude>1</extrude>\n<tessellate>1</tessellate>\n<altitudeMode>relative</altitudeMode>")
      outfile.write("<coordinates>"+coords+"</coordinates>\n")
      outfile.write("</LineString>\n</Placemark>")
      outfile.write(kmlend)
      outfile.close()
      print "\n\nUse Google Earth to open the file : "+savefile