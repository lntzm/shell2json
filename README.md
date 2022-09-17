# shell2json
**A very LIMITED script, just for using on my own.**

A demo which tramsforms args in a deep learning shell script to launch.json of vscode for debugging.

## Introduction
Some deep learning projects contain many args to parse for training and testing in different conditions, and they are usually writen in shell scripts.
When I debug my deep learning projects in VSCode, it is a boring job to copy content of `*.sh` to `./.vscode/launch.json` due to many quotation marks.
So this demo is to solve this issue, automatically generating shell content to json format, which fits VSCode debugging.

## Usage
class Configuration is used to generate a config. 
1. Intiialize it with file_name and path of the bash file.
2. Run the method `read()` to read the bash file.
3. Run the method `exportJson()` to return the content in json format.
4. Copy and Complete VScode launch.json
```java
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        // Paste the content generated by this demo here.
    ]
}
```
