# Using Screen

### View Current Screen Processes
```bash
screen -ls
```

### Create a new Screen
```bash
screen -S SCREEN_NAME
```

###### Example:
```bash
screen -S webserver
```



### Start a Process in a new Screen
```bash
screen -d -m COMMAND_NAME
```
 - `-d -m` means start a new screen in detached mode.


### Reattached to a Detached Screen
```bash
screen -r -d SESSION_ID
```
 - `-r -d` means resume a detached screen session and if needed detach it first.


### Detact From Current Screen
- Press `Ctrl + A + D`


### Kill a Detached Screen
```bash
screen -X -S SESSION_ID quit
```
 - `-X` means send a command to a running screen (the `quit` command in our case).
 - `-S` means specify a screen session ID (SESSION_ID).

 - Alternatively you can kill a screen by reattaching and then: Ctrl + C