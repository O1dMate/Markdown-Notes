# Compressing, Decompressing & Archiving

- gzip uses the `DEFLATE` algorithm.
	 - Fast, and Okay compression.
	 - `gz` extension.
- bzip2 uses the `Burrows-Wheeler` algorithm.

	 - Slower, but Moderate compression.
	 - `bz2` extension.
- xz uses the `LZMA2` algorithm.
	 - Much Slower, but Higher compression.
	 - Uses much more RAM.
	 - Linear increase in time for larger compression flags.
	 - `xz` extension.

### Flags Common to All
 - `-k` means `keep the original` file and create a new compressed file.
 - `-t` means perform an `integrity check` on the compressed file.
 - `-d` means `decompress` the file.
 - `-c` means pipe the output.
 	 - Performing compression on a file doesn't actually return any data. If you want pipe the output of the compression/decompression to another command, you need ot use this flag.
 - `-9` means change the compression amount.
 	 - `-1` is the lowest compression but the fastest.
 	 - `-6` is the default.
 	 - `-9` is the highest compression but the slowest.

### gzip

###### Compressing a File
```bash
gzip FILE_NAME
```

###### Display Compressed File Stats
```bash
gzip -l FILE_NAME
```


### bzip2

###### Compressing a File
```bash
bzip2 FILE_NAME
```

### xz

###### Compressing a File
```bash
xz FILE_NAME
```

###### Display Compressed File Stats
```bash
xz -l FILE_NAME
```



### Archiving Using tar

##### Archive a Folder
```bash
tar cvfW OUTPUT_NAME.tar DIRECTORY_TO_ARCHIVE/
```
 - `c` means create a new archive.
 - `v` means verbose mode which prints progress in our case.
 - `f` means specify the archive name.
  - `W` means verify each file (not needed but is safe).

##### Archive & Compress a Folder
```bash
tar cvfz OUTPUT_NAME.tar DIRECTORY_TO_ARCHIVE/
```
 - `z` means compress using `gzip`.
 - `j` instead of `z` means compress using `bzip2`.


##### Extract an Archive
```bash
tar xvf ARCHIVE_NAME.tar
```
 - `x` means extract from an archive.
 - `v` means verbose mode which prints progress in our case.
 - `f` means specify the archive name.

##### View Contents of Archive
```bash
tar tvf ARCHIVE_NAME.tar
```

##### Extract a Single File/Folder from Archive
```bash
tar xvf ARCHIVE_NAME.tar PATH_TO_FILE_IN_ARCHIVE
```
 - Ensure to add a `z` or `j` flag in the archive is encrypted.