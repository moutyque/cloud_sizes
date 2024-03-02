#!/usr/bin/env python3

from netaddr import IPSet, IPNetwork
from requests import get

def get_and_parse():
    # Google publishes the list in a simple JSON file, and also in an
    # overly complex DNS TXT record, because of course they do
    url = "https://www.gstatic.com/ipranges/cloud.json"
    data = get(url).json()

    # Pull out all of the IPv4 and v6
    v4 = IPSet(IPNetwork(y['ipv4Prefix']) for y in data['prefixes'] if 'ipv4Prefix' in y)
    v6 = IPSet(IPNetwork(y['ipv6Prefix']) for y in data['prefixes'] if 'ipv6Prefix' in y)

    return {
        "name": "google", 
        "pretty": "GCP", 
        "v4": v4, 
        "v6": v6, 
        "show": True, 
        "raw_data": data, 
        "raw_format": "json", 
        "allowed_overlap": {},
    }

def test():
    data = get_and_parse()
    print(f"Results for {data['pretty']}:")
    print(f"  IPv4: {data['v4'].size:,}")
    print(f"  IPv6: {data['v6'].size:,}")

if __name__ == "__main__":
    test()
