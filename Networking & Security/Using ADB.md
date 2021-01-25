# Using ADB

### View Connected Devices
```text
adb devices
```

### Installs the package located at C:\package.apk on your computer on your device.
```text
adb install C:\package.apk
```

### Uninstall a package from your Device
```text
adb uninstall package.name
```

 - For example, you'd use the name com.rovio.angrybirds to uninstall the Angry Birds app.

### Push a file from your Computer to your Device
```text
adb push C:\file /sdcard/file
```

 - For example, the command here pushes the file located at C:\file on your computer to /sdcard/file on your device

### Pull a file from your Device to your Computer
```text
adb pull /sdcard/file C:\file
```

 - Works like adb push, but in reverse.

### View your Android Device’s log
```text
adb logcat
```

 - Can be useful for debugging apps.

### Spawn interactive Linux command-line shell on your Device
```text
adb shell
```

### Runs a specified shell command on your Device
```text
adb shell command
```