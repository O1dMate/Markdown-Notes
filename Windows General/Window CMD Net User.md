# Net User

### View Users
```bash
net user
```

### View User Info
```bash
net user USERNAME
```

### Create/Delete User
```bash
net user USERNAME PASSWORD /add
net user USERNAME /delete
```

### View Local Groups:
```bash
net localgroup
```

### View Local Group Info:
```bash
net localgroup GROUPNAME
```

### Add/Remove User from Local Group:
```bash
net localgroup GROUPNAME USERNAME /add
net localgroup GROUPNAME USERNAME /delete
```

### Enable/Disable Account
```bash
net user USERNAME /active:yes
net user USERNAME /active:no
```