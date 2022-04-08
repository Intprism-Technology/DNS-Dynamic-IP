import importorinstall
import configuration

importorinstall.package('CloudFlare')

import CloudFlare

cf = CloudFlare.CloudFlare(email=configuration.cf_email, token=configuration.cf_token)

def do_dns_update(zone_name, zone_id, ip_address, ip_address_type):
    """Cloudflare API DNS Update"""

    try:
        params = {'match':'all', 'type':ip_address_type}
        dns_records = cf.zones.dns_records.get(zone_id, params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records %s - %d %s - api call failed' % ('dns_name', e, e))

    updated = False

    # update the record - unless it's already correct
    for dns_record in dns_records:
        if(dns_record['name'] not in configuration.cf_exceptListDnsUpdate):
            print(dns_record['name'])
            old_ip_address = dns_record['content']
            old_ip_address_type = dns_record['type']

            if ip_address_type not in ['A', 'AAAA']:
                # we only deal with A / AAAA records
                continue

            if ip_address_type != old_ip_address_type:
                # only update the correct address type (A or AAAA)
                # we don't see this becuase of the search params above
                print('IGNORED: %s %s ; wrong address family' % (dns_record['name'], old_ip_address))
                continue

            if ip_address == old_ip_address:
                print('UNCHANGED: %s %s' % (dns_record['name'], ip_address))
                updated = True
                continue

            proxied_state = dns_record['proxied']
    
            # Yes, we need to update this record - we know it's the same address type

            dns_record_id = dns_record['id']
            dns_record = {
                'name':dns_record['name'],
                'type':ip_address_type,
                'content':ip_address,
                'proxied':proxied_state
            }
            try:
                dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                exit('/zones.dns_records.put %s - %d %s - api call failed' % (dns_record['name'], e, e))
            print('UPDATED: %s %s -> %s' % (dns_record['name'], old_ip_address, ip_address))
            updated = True

    if updated:
        return

def dns_update(ip_address):
    zones = cf.zones.get()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        # print("zone_id=%s zone_name=%s" % (zone_id, zone_name))
        if(len(configuration.cf_onlyDomain) > 0 and zone_name in configuration.cf_onlyDomain):
            do_dns_update(zone_name, zone_id, ip_address, configuration.cf_ipType)
        elif(len(configuration.cf_onlyDomain) == 0):
            do_dns_update(zone_name, zone_id, ip_address, configuration.cf_ipType)