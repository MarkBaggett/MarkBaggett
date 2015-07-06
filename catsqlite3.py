import sqlite3,glob,re
from optparse import OptionParser

parser=OptionParser(usage='%prog [OUTPUT OPTIONS]')
parser.add_option('-e','--emails',action='store_true', help='Only display email addresses')
#parser.add_option('-u','--urls',action='store_true', help='Only display urls')
parser.add_option('-p','--phone',action='store_true', help='Only display phone numbers')
parser.add_option('-v','--verbose',action='store_true', help='Be Verbose')
parser.add_option('-l','--limit',help='Limit the number of records queried to the number specified.')

(options,args)=parser.parse_args()

for file in glob.glob("*/*"):
    try:
        dbcon= sqlite3.connect(file)
        records=dbcon.execute("select sql,name from sqlite_master where type = 'table';")
    except:
        continue 
    for schema,row in records:
        sql="select * from "+str(row)
        if options.limit:
            sql+=" limit "+options.limit
        if options.verbose:
            print "\n\nsqlite3 "+file+' "'+str(sql)+'"'
            print "SCHEMA: " + str(schema)
        try: 
            tabdump=dbcon.execute(sql)
        except:
            continue
        if options.emails:  
            allrows= str(tabdump.fetchall())
            emails=re.findall(r"[\w\+\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*\.[a-zA-Z]+",allrows)
            for email in emails:
                print email
            continue
        if options.phone:
            allrows= str(tabdump.fetchall())
            result=re.findall(r'(?:1|1[-( +])?\(?[2-9][0-8][0-9][-)/ +]?[2-9][0-9]{2}[-/ +]?[0-9]{4}',allrows)
            for item in result:
                print item
            continue
        for row in tabdump:
             print row
