# NPM (Node Package Manager)

## What is package.json?
The `package.json` file contains information about all the node modules you currently have installed and their versions. This file is useful so that you don't have to save and backup your `node_modules` folder as they can all re-downloaded easily with the information stored in the `package.json` file.



## Installing from Package.json
 - This command reads the `package.json` file in the current directory and will download all the modules and save them in the `node_modules` folder.
 - The `node_modules` folder should be added to the `.gitignore` file as it can be hundreds of megabytes.
```bash
npm i
```



## Installing Node Modules

#### Install Module
```bash
npm install PACKAGE_NAME1 PACKAGE_NAME2 PACKAGE_NAME3
```

 - The `--save` flag saves the package name and version to the `package.json` file. You may need to included it if you are using an older version of NPM. Newer version of NPM do this automatically.

#### Install Module Globally to your system
```bash
npm install -g PACKAGE_NAME
```



## Un-installing a Node Module
```bash
npm uninstall PACKAGE_NAME
```