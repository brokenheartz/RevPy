#!/usr/bin/python3

from color import *
from reverseip import reverseIp
from argparse import ArgumentParser
from time import sleep
import os

asci_art = BOLD + YELLOW +"""
  _____            _______     __
 |  __ \          |  __ \ \   / /
 | |__) |_____   _| |__) \ \_/ /
 |  _  // _ \ \ / /  ___/ \   /
 | | \ \  __/\ V /| |      | |
 |_|  \_\___| \_/ |_|      |_|
               """ + GREEN + "[ Version " + WHITE + "1.2" + GREEN + " ]\n"

def banner(): # Banner
    print(asci_art)

# List usable command -----------------------------------------------------------------------------
argument = ArgumentParser( description = "Finding another websites in same server of website." )
grouparg = argument.add_mutually_exclusive_group()

argument.add_argument("-d", "--domain", help = "domain of target") # target's domain
argument.add_argument("-f", "--file", help = "store output into a file")
grouparg.add_argument("-a", "--all", help = "using all", action = "store_true") # using hackertarget, yougetsignal, and viewdns for reverse ip
grouparg.add_argument("-ht", "--hackertarget", help = "using hackertarget", action = "store_true") # using hackertarget for reverse ip
grouparg.add_argument("-yg", "--yougetsignal", help = "using yougetsignal", action = "store_true") # using yougetsignal for reverse ip
grouparg.add_argument("-vd", "--viewdns", help = "using viewdns", action = "store_true") # using viewdns for reverse ip

commands = argument.parse_args()
# -------------------------------------------------------------------------------------------------

# Defined variable that reference user inputted command -------------------------------------------
tdomain = commands.domain # target's domain
alltool = commands.all
viewdns = commands.viewdns
filename     = commands.file # filename that you wanna write the output in
hackertarget = commands.hackertarget
yougetsignal = commands.yougetsignal
# -------------------------------------------------------------------------------------------------

banner()

domains = set() # this set-typed variable's used to store all found domain(s). i chosed set data type bcz for avoiding same domain

if tdomain: # if user input the domain
    revIP = reverseIp(tdomain)

    if yougetsignal:
        ygsdata = revIP.yougetsignal() # yougetsignal json data
        status  = BOLD + RED + "Fail" if ygsdata["status"] == "Fail" else BOLD + GREEN + "Success"

        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "YouGetSignal Status : " + CYAN + status)

        if ygsdata["status"] != "Success":
            if "check limit" in ygsdata["message"]:
                print(RED + "[" + WHITE + "-" + RED + "]" + WHITE + " " + "Change your IP. Your requests has been out of limit.")
            else:
                print(RED + "[" + WHITE + "-" + RED + "]" + WHITE + " " + ygsdata["message"])
        else:
            print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "Target ip           : " + CYAN + ygsdata["remoteIpAddress"])
            print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "Domain count        : " + CYAN + ygsdata["domainCount"])
            print()
            sleep(1)
            for domain, junk in ygsdata["domainArray"]:
                domains.add(domain) # apppending element to variable domains
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(MAGENTA + BOLD + "[YouGetSignal]" + " " + NORMAL + WHITE + domain)
    elif hackertarget:
        htdata = revIP.hackertarget() # HackerTarget domain list
        status = BOLD + GREEN + "Success" if htdata else BOLD + RED + "Fail"

        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "HackerTarget Status : " + CYAN + status)
        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "Domain count        : " + CYAN + str(len(htdata)))
        print()
        sleep(1)

        if not htdata:
            print(RED + "[" + WHITE + "-" + RED + "]" + WHITE + " " + "Nothing domaind found.")
        else :
            for domain in htdata:
                domains.add(domain) # appending element to variable domains
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(CYAN + BOLD + "[HackerTarget]" + " " + NORMAL + WHITE + domain)
    elif viewdns:
        vddata = revIP.viewdns() # ViewDNS domain list
        status = BOLD + GREEN + "Success" if vddata else BOLD + RED + "Fail"

        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "ViewDNS Status : " + CYAN + status)
        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "Domain count   : " + CYAN + str(len(vddata)))
        print()
        sleep(1)

        if not vddata:
            print(RED + "[" + WHITE + "-" + RED + "]" + WHITE + " " + "Nothing domaind found.")
        else:
            for domain in vddata:
                domains.add(domain) # appending element to variable domains
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(BLUE + BOLD + "[ViewDNS]" + " " + NORMAL + WHITE + domain)
    elif alltool:
        # Defining object of 3 different type tools -----------------------------------------
        ygdata = revIP.yougetsignal()
        htdata = revIP.hackertarget()
        vddata = revIP.viewdns()
        # -----------------------------------------------------------------------------------

        # Determining scan status for each tool ---------------------------------------------
        ygstatus = BOLD + RED + "Fail" if ygdata["status"] == "Fail" else BOLD + GREEN + "Success ("+ WHITE + ygdata["domainCount"] + GREEN +")"
        htstatus = BOLD + GREEN + "Success ("+ WHITE + str(len(htdata)) + GREEN +")" if htdata else BOLD + RED + "Fail"
        vdstatus = BOLD + GREEN + "Success ("+ WHITE + str(len(vddata)) + GREEN +")" if vddata else BOLD + RED + "Fail"

        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "YouGetSignal Status : " + CYAN + ygstatus)
        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "HackerTarget Status : " + CYAN + htstatus)
        print(YELLOW + "[" + GREEN + "+" + YELLOW + "] " + WHITE + "ViewDNS Status      : " + CYAN + vdstatus)
        # -----------------------------------------------------------------------------------
        print()
        sleep(1)
        # Making output and appending element to variable domains ---------------------------
        # YouGetSignal
        if ygdata["status"] != "Fail":
            sleep(0.30)
            for domain, junk in ygdata["domainArray"]:
                domains.add(domain)
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(MAGENTA + BOLD + "[YouGetSignal]" + " " + NORMAL + WHITE + domain)
        # HackerTarget
        if len(htdata) != 0:
            sleep(0.30)
            for domain in htdata:
                domains.add(domain)
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(CYAN + BOLD + "[HackerTarget]" + " " + NORMAL + WHITE + domain)
        # ViewDNS
        if len(vddata) != 0:
            sleep(0.30)
            for domain in vddata:
                domains.add(domain)
                print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
                print(BLUE + BOLD + "[ViewDNS]" + " " + NORMAL + WHITE + domain)
        # -----------------------------------------------------------------------------------
    else:
        argument.print_help()

    if filename:
        totaldomain = len(domains)

        try:
            savefile = open(filename, "w")
            savefile.write( "\n".join(domains) )
        except Exception:
            pass
        finally:
            savefile.close()

        if os.path.exists(filename):
            print(YELLOW + "[" + GREEN + BOLD + "*" + YELLOW + NORMAL + "]", end = "")
            print(WHITE + str(totaldomain) + " " + "domain has been saved in %s." % (filename))
        else:
            print(RED + "[" + WHITE + "-" + RED + "]" + WHITE + " " + "Fail to create a file!")
    else:
        pass
else:
    argument.print_help()
