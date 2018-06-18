Xenotix-xBOT
============
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


xBOT COMMANDS
============
* xSYSINFO : Get System Information
* EXECUTE <command> : Execute a passive system command
* xDOWNLOAD <url> : Download a file from an URL
* xUPLOAD <filepath> : Upload a file
* xNETWORK : Get network information
* xPORTSCAN <ip> : Run a Portscan
* xSCREENSHOT : Grab a Screenshot
* xKILL : Kill and Remove the xBOT.

