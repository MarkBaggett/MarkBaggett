#The following code will reassemble fragmented packets using the BSD, BSD-Right, First, Last and Linux so that an analyst gets a better understanding of how an attack would affect each of his different hosts.
#This program was written by @MarkBaggett and is available for download at http://baggett-scripts.googlecode.com/svn/trunk/reassembler.py
#If you have questions about the script you can read the associated SANS Gold paper called "IP Fragment Reassembly with Scapy" by Mark Baggett

from scapy.all import *
import StringIO
from optparse import OptionParser
import os
import sys

def rfc791(fragmentsin):
    buffer=StringIO.StringIO()
    for pkt in fragmentsin:
         buffer.seek(pkt[IP].frag*8)
         buffer.write(pkt[IP].payload)
    return buffer.getvalue()

def first(fragmentsin):
    buffer=StringIO.StringIO()
    for pkt in fragmentsin[::-1]:
         buffer.seek(pkt[IP].frag*8)
         buffer.write(pkt[IP].payload)
    return buffer.getvalue()

def bsdright(fragmentsin):
    buffer=StringIO.StringIO()
    for pkt in sorted(fragmentsin, key= lambda x:x[IP].frag):
         buffer.seek(pkt[IP].frag*8)
         buffer.write(pkt[IP].payload)
    return buffer.getvalue()

def bsd(fragmentsin):
    buffer=StringIO.StringIO()
    for pkt in sorted(fragmentsin, key=lambda x:x[IP].frag)[::-1]:
         buffer.seek(pkt[IP].frag*8)
         buffer.write(pkt[IP].payload)
    return buffer.getvalue()


def linux(fragmentsin):
    buffer=StringIO.StringIO()
    for pkt in sorted(fragmentsin, key= lambda x:x[IP].frag, reverse=True):
         buffer.seek(pkt[IP].frag*8)
         buffer.write(pkt[IP].payload)
    return buffer.getvalue()

def genjudyfrags():
    pkts=scapy.plist.PacketList()
    pkts.append(IP(flags="MF",frag=0)/("1"*24))
    pkts.append(IP(flags="MF",frag=4)/("2"*16))
    pkts.append(IP(flags="MF",frag=6)/("3"*24))
    pkts.append(IP(flags="MF",frag=1)/("4"*32))
    pkts.append(IP(flags="MF",frag=6)/("5"*24))
    pkts.append(IP(frag=9)/("6"*24))
    return pkts

def processfrags(fragmenttrain): 
    print "Reassembled using policy: First (Windows, SUN, MacOS, HPUX)"
    print first(fragmenttrain)
    print "Reassembled using policy: Last/RFC791 (Cisco)"
    print rfc791(fragmenttrain)
    print "Reassembled using policy: Linux (Umm.. Linux)"
    print linux(fragmenttrain)
    print "Reassembled using policy: BSD (AIX, FreeBSD, HPUX, VMS"
    print bsd(fragmenttrain)
    print "Reassembled using policy: BSD-Right (HP Jet Direct)"
    print bsdright(fragmenttrain)
    
    
def writefrags(fragmenttrain): 
    fileobj=open(options.prefix+"-first","w")
    fileobj.write(first(fragmenttrain))
    fileobj.close()
    fileobj=open(options.prefix+"-rfc791","w")
    fileobj.write(rfc791(fragmenttrain))
    fileobj.close()
    fileobj=open(options.prefix+"-bsd","w")
    fileobj.write(bsd(fragmenttrain))
    fileobj.close()
    fileobj=open(options.prefix+"-bsdright","w")
    fileobj.write(bsdright(fragmenttrain))
    fileobj.close()
    fileobj=open(options.prefix+"-linux","w")
    fileobj.write(linux(fragmenttrain))
    fileobj.close()
    
    
    
def main():
    parser=OptionParser(usage='%prog [OPTIONS]')
    parser.add_option('-r','--read',default="",help='Read the specified packet capture',dest='pcap')
    parser.add_option('-d','--demo',action='store_true', help='Generate classic fragment test pattern and reassemble it.')
    parser.add_option('-w','--write',action='store_true', help='Write 5 files to disk with the payloads.')
    parser.add_option('-p','--prefix',default='reassembled', help='Specify the prefix for file names')

    if (len(sys.argv)==1):
       parser.print_help()
       sys.exit()

    global options, args
    (options,args)=parser.parse_args()

    if options.demo:
        processfrags(genjudyfrags())

    if not os.path.exists(options.pcap):
        print "Packet capture file not found."
        sys.exit(2)

    print "Reading fragmented packets from disk."
    packets=rdpcap(options.pcap)
    ippackets=[a for a in packets if a.haslayer("IP")]
    fragmentedpackets=[a for a in ippackets if a[IP].flags==1 or a[IP].frag > 0]
    
    if len(fragmentedpackets)==0:
        print "No fragments in packet capture."
        sys.exit(2)

    uniqipids={}
    for a in fragmentedpackets:
         uniqipids[a[IP].id]='we are here'

    for ipid in uniqipids.keys():
        print "Packet fragments found.  Collecting fragments now."
        fragmenttrain = [ a for a in fragmentedpackets if a[IP].id == ipid ] 
        processit = raw_input("Reassemble packets between hosts "+str(a[0][IP].src)+" and "+str(a[0][IP].dst)+"? [Y/N]")
        if str(processit).lower()=="y":
            if options.write:
                writefrags(fragmenttrain)
            else:
                processfrags(fragmenttrain)

if __name__ == '__main__':
    main()
