# Using Git CLI

##### Check & Set Config
```bash
git config --list
git config --global user.email "name@email.com"
```


##### Clone a repo
Once you have the address of the repo:
```bash
git clone repo_address
```


##### Check status of git
```bash
git status
```

This tells you what branch you are on and the differences between your local branch and the HEAD commit.


##### (Un)Tracked files
 - If a file/dir is untracked, then git won't commit these to the remote branch when you push your files.

Start tracking a file:
```bash
git add filename
```

Start tracking all files:
```bash
git add .
```

##### Create Branch
To change the branch your currently on:
```bash
git checkout -b branch_name
```

##### Change Branches
To change the branch your currently on:
```bash
git checkout branch_name
```

##### Commit changes
To commit all of your changes to your local branch:
```bash
git commit -m "Commit Message"
```

Your commit message is the little message next to a file/folder on git just before it says when it was uploaded


##### Push to remote branch
Push your files to the remote branch:

```bash
git push
```

```bash
git push --set-upstream origin branch_name
```

##### Pull changes from the server
```bash
git pull
```


##### Certificate Error
If you get certificate or SSL errors, try the following for clone, push & pull commands:
```bash
git -c http.sslVerify=false clone repo_address
git -c http.sslVerify=false push --set-upstream origin branch_name
git -c http.sslVerify=false pull
```