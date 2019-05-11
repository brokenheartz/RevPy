from re import compile as regex
from color import *
import requests as rikues
import sys

class reverseIp :

    def __init__(self, url):
        #test connection
        try:
            rikues.get("https://google.com/")
        except Exception:
            print(BOLD + CYAN + "[" + RED + "+" + CYAN + "]" + NORMAL + WHITE + " Make sure you've been connected to the internet!")
            sys.exit(0)

        self.target = url.strip()
        self.agent  = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

    def yougetsignal(self):
        domain   = self.target
        header   = {"user-agent" : self.agent}
        postdata = {"remoteAddress" : domain, "key" : ""}
        requests = rikues.post("https://domains.yougetsignal.com/domains.php", data = postdata, headers = header)
        jsondata = requests.json()

        return jsondata

    def hackertarget(self):
        domain    = self.target
        header    = {"user-agent" : self.agent}
        parameter = {"q" : domain}
        requests  = rikues.get("http://api.hackertarget.com/reverseiplookup/", params = parameter, headers = header)

        if "No DNS" in requests.text or "error" in requests.text:
            domains = []
        else :
            domains = requests.text.split("\n")

        return domains

    def viewdns(self):
        domain    = self.target
        header    = {"user-agent" : self.agent}
        parameter = {"host" : domain, "t" : 1}
        formula   = regex(r'<td>([\d\w-]+\.[\w.-]{2,6})</td>')
        requests  = rikues.get("https://viewdns.info/reverseip/", params = parameter, headers = header)

        # finding domains
        domains = formula.findall(requests.text)
        return domains # returns array

if __name__ == '__main__':
    print("revip-v2.py")
