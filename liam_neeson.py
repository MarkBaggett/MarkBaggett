#Liam Neeson is the single most protection that any organization can take to protect their Linux passwords hashes.
#Once Liam Neeson is protecting your shadow file all your hashes are invisible to terrorist tools like cat, less and others that process bash escape sequences
#Are you seriously thinking about using this in production?  Back up your files and test it first.
#Author @MarkBaggett

import re
import argparse
import os
import sys

def moveup(lines):
    return "\x1b[%sA" % (lines)

def movedown(lines):
    return "\x1b[%sB" % (lines)

def moveright(lines):
    return "\x1b[%sC" % (lines)

def moveleft(lines):
    return "\x1b[%sD" % (lines)


liam = "I don't know who you are. I don't know what you want. If you are looking for ransom, I can tell you I don't have money. But what I do have are a very particular set of skills, skills I have acquired over a very long career. Skills that make me a nightmare for people like you. If you leave my system alone now, that'll be the end of it. I will not look for you, I will not pursue you. But if you don't, I will look for you, I will find you, and I will kill you."


parser=argparse.ArgumentParser()
parser.add_argument('-p','--protect', action="store_true", help="Have Liam Neeson protect your /etc/shadow file")
parser.add_argument('-u','--unprotect', action="store_true", help="I am friggin Chuck Norris.  I don't need Liam Neeson")
parser.add_argument('-a','--alt_path', default = '/etc/shadow', help="I am afraid of Liam Neeson touching my shadow file. Protect this file instead.")
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(0)

if not os.path.exists(args.alt_path):
   print "File %s not found. If that file has been Taken, you've  obviously asked for Liam's protection after the fact." % (args.alt_path)
   sys.exit(1)

with open(args.alt_path) as fh:
     shadow_list = fh.readlines()
     fh.close()

if not all("\x1b[" not in x for x in shadow_list) and not args.unprotect:
     print "File %s is already protected.  One Liam Neeson is more than enough protection for anything." % (args.alt_path)
     sys.exit(1)

liam_list = []
for i in re.split(r"[,.]",liam):
   liam_list.append("{0: ^100}".format(i))

file_length = len(shadow_list)
line_spacing = file_length/len(liam_list)
header = (file_length % len(liam_list)) / 2
footer = (file_length % len(liam_list)) - header

cover = moveup(file_length)+moveright(15)
cover = cover + (((" "*100)+"\n"+moveright(15)) * header)
for i in liam_list:
     cover = cover + i + "\n"+moveright(15)
     if line_spacing > 1:
         cover = cover + ((" "*100)+"\n"+moveright(15)) * (line_spacing-1)
cover = cover + (((" "*100)+"\n"+moveright(15)) * footer) + "\n"

if args.protect:
    with open(args.alt_path,"a") as fh:
        fh.write(cover)
        fh.close()
    print "File %s is now protected by Liam Neeson" % (args.alt_path)

if args.unprotect:
   clean_shadow = [ x for x in shadow_list if "\x1b[" not in x]
   with open(args.alt_path,"w") as fh:
       fh.write("".join(clean_shadow))
       fh.close()
   



