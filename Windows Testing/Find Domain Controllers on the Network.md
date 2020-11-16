# Find Domain Controllers on the Network:

### Open cmd and run the following
```bash
nslookup
set type=all
_ldap._tcp.dc._msdcs.DOMAIN_NAME
```