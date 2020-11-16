# Using MSOnline (MsolService) Powershell


#### Install MSOnline
```bash
Install-Module MSOnline
```

##### Connect
```bash
Connect-MsolService
```

##### Get the first 100 users in the database
```bash
Get-MsolUser -MaxResult 100
```

##### Return all users that have "John" in their name
```bash
Get-MsolUser -SearchString "John"
```

##### Return the user that has 'john@gmail.com' as their email
```bash
Get-MsolUser -UserPrincipalName "john@gmail.com"
```

##### Write the output of a command to a file
```bash
Get-MsolUser -SearchString "John" | Export-CSV C:\Users\Public\outFile1.csv
```

##### Return a list of help commands
```bash
Get-Help Get-MsolUser
```