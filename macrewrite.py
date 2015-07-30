import os, json

own_mac = open('/sys/class/net/%s/address' % "eth0").read().strip()

def handleMac(mac, ips):
    commands = []
    commands.append("ebtables -t nat -A POSTROUTING -s %s -j snat --to-src %s --snat-arp --snat-target ACCEPT" % (mac, own_mac))
    if "ip4" in ips:
        for ip in ips["ip4"]:
            commands.append("ebtables -t nat -A PREROUTING -p IPv4 --ip-dst %s -j dnat --to-dst %s --dnat-target ACCEPT" % (ip, mac))
            commands.append("ebtables -t nat -A PREROUTING -p ARP --arp-ip-dst %s -j dnat --to-dst %s --dnat-target ACCEPT" % (ip, mac))
    if "ip6" in ips:
        for ip in ips["ip6"]:
            commands.append("ebtables -t nat -A PREROUTING -p IPv6 --ip6-dst %s -j dnat --to-dst %s --dnat-target ACCEPT" % (ip, mac))
    return commands

dirname, filename = os.path.split(os.path.abspath(__file__))
config = json.loads(file(dirname + "/config.json").read())

for mac in config:
    for cmd in handleMac(mac, config[mac]):
        print cmd

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
