from dns.resolver import Resolver
from json import loads
from subprocess import run as sub_run
from time import time as utime

#todo: yaml
resolvers = {
    "CloudFlare": ["1.1.1.1", "1.0.0.1"],
    "Quad9": ["9.9.9.11", "149.112.112.11"],
    "Google": ["8.8.8.8", "8.8.4.4"],
    "OpenDNS": ["208.67.222.222", "208.67.220.220"]
}

resolver_tests = {
    "Akamai": "theia.dl.playstation.net",
    "CloudFront": "cloudfront.debian.net",
    "CloudFlare": "pkg.cloudflare.com"
}

MTR_LOCATION = 'mtr'
if platform == "win32":
    MTR_LOCATION = 'mtr_binary/mtr.exe'

def mtr_report(ip_address):
    try:
        mtr_result = sub_run([MTR_LOCATION, '--show-ips', '--json', '-c', '5', ip_address], capture_output=True)
    except:
        return False

    if mtr_result.returncode != 0:
        return False

    mtr_json = loads(mtr_result.stdout.strip())
    last_hop = mtr_json['report']['hubs'][-1]

    return f"Hops: {last_hop['count']} - Loss: {last_hop['Loss%']}% - Last: {last_hop['Last']} - Avg: {last_hop['Avg']} - Best: {last_hop['Best']} - Worst: {last_hop['Wrst']} - StdDev: {last_hop['StDev']}"

dns_ctx = Resolver(configure=False)
for resolver in resolvers:
    dns_ctx.nameservers = resolvers[resolver]

    print("------------")
    print(f"Testing {resolver}")
    mtr = mtr_report(resolvers[resolver][0])
    if not mtr:
        print("Resolver wasn't reachable by ICMP, skipping")
        continue

    print(mtr)
    print("------------")

    for resolver_test in resolver_tests:
        try:
            #Not sure how accurate this method of measurement is
            #Support v6?
            dns_start = utime()
            query = dns_ctx.query(resolver_tests[resolver_test], 'a')
            dns_end = utime()
            primary_ip = query[0]
            query_response = round(dns_end - dns_start, 4)
        except:
            print(f"Unable to resolve {resolver_tests[resolver_test]}, skipping")

        print(f"{resolver_tests[resolver_test]} ({resolver_test}) resolved to {primary_ip} in {query_response}s")
        mtr = mtr_report(primary_ip.to_text())
        if mtr:
            print(mtr)
        else:
            print("Target wasn't reachable by ICMP")

    print(' ')
