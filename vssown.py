import win32com.client
from optparse import OptionParser

#Define and parse all the command line options
parser=OptionParser(usage='%prog <option>')
parser.add_option('-l','--list',action="store_true", help='List Volume Shadow Copies')
parser.add_option('-c','--create', action="store_true", help='Create a Volume Shadow Copy')

(options,args)=parser.parse_args()


def vss_list():
    wcd=win32com.client.Dispatch("WbemScripting.SWbemLocator")
    wmi=wcd.ConnectServer(".","root\cimv2")
    obj=wmi.ExecQuery("SELECT * FROM Win32_ShadowCopy")
    return [x.DeviceObject for x in obj]

def vss_create():
    wmi=win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2:Win32_ShadowCopy")
    createmethod = wmi.Methods_("Create")
    createparams = createmethod.InParameters
    createparams.Properties_[1].value="c:\\"
    results = wmi.ExecMethod_("Create", createparams)
    return results.Properties_[1].value

def main():
    if not (options.list or options.create):
        print "\n\nPlease specify at least one option.\n"
        parser.print_help()
    if options.list: print vss_list()
    if options.create: print vss_create()

if __name__ == "__main__":
    main()
