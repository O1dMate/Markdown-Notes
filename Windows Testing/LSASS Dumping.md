# LSASS Dumping

<br>

## 1. Using Task Manager
 - Open Task Manager
 - Right click on `lsass.exe` or `Local Security Authority Process` and click `Create dump file`
 - If you are unable to access the link provided to the file, Go to Task Manager, click `File` then `New Task` then `Browse`. Enter the link in this new window and copy the dump file to a location you have access to.

<br>

## 2. Using ProcDump

#### Download Sysinternals Suite from Microsoft
 - Search `Sysinternals Suite` and download the tools.
 - Get them from the Microsoft website to ensure they're legit.


#### Dump LSASS Data Using Sysinternals Suite
 - Open the folder of tools you just downloaded.

Run the command:
```bash
procdump64.exe -ma lsass.exe lsass
```