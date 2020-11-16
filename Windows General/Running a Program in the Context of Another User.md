# Executing an Application in the Context of a Domain User

### Open CMD and Run the Following
```bash
runas /netonly /user:DOMAIN_NAME\USERNAME "PROGRAM_TO_EXECUTE"
```

### Examples:
```bash
runas /netonly /user:mydomain.net\johnsmith "cmd.exe"
runas /netonly /user:pirates.local\captainjack "mmc"
```