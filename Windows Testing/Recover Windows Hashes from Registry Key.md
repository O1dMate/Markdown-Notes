# Recovering Windows Hashes from Registry Keys

### Get Registry Keys
 - A SAM & SYSTEM file from the target machine. The SECURITY file is optional.

### Recover Hashes
 - Open Kali linux.
 - Run the following command in the terminal:
```bash
samdump2 system.sav sam.sav
```