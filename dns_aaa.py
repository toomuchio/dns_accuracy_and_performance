from dns.resolver import Resolver
from json import loads
from subprocess import run as sub_run

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

    return f"Hops: {last_hop['count']} - Loss: {last_hop['Loss%']}% - Last: {last_hop['Last']}ms - Avg: {last_hop['Avg']}ms - Best: {last_hop['Best']}ms - Worst: {last_hop['Wrst']}ms - StdDev: {last_hop['StDev']}ms"

dns_ctx = Resolver(configure=False)
for resolver in resolvers:
    dns_ctx.nameservers = resolvers[resolver]

    print("------------")
    print(f"Testing {resolver}")
    mtr = mtr_report(resolvers[resolver][0])
    if not mtr:
        print(f"Resolver {resolver} is not accepting ICMP, skipping")
        continue

    print(mtr)
    print("------------")

    for resolver_test in resolver_tests:
        try:
            query = dns_ctx.query(resolver_tests[resolver_test], 'a')
            primary_ip = query[0]
            query_response = query.response.time * 1000.0
        except:
            print(f"Unable to resolve {resolver_tests[resolver_test]}, skipping")

        print(f"{resolver_tests[resolver_test]} ({resolver_test}) resolved to {primary_ip} in {query_response:.2f}ms")
        mtr = mtr_report(primary_ip.to_text())
        if mtr:
            print(mtr)
        else:
            print(f"Resolve test {resolver_tests[resolver_test]} is not accepting ICMP, skipping")

    print(' ')
