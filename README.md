# Logitech G Hub App Disabler

This script was made to work around the lack of basic functionality that should have been included in logitech g hub.

## What does this script do

In short, this script disables all applications inside logitech g hub.

The longer explaination of this is that this scripts reads the sqlite db file at 'C:\Users\Username\AppData\Local\LGHUB\settings.db', extracts the json configuration and disables all applications.

## Why

Running this script essentially making your desktop profile the "global" profile. This by extention then allows you to re-enable an application to override your global profile.

It's simple, but if you're like me and have over 400 applications detected by logitech g hub, you don't want to go through these one by one.

## Requirements

The only requirements for this script is Python, no additional libraries/packages required (Note: This script has only been validated against python 3.11 64bit, and i cannot see a reason why this script would fail on newer versions of python, but i cannot say without full certainty that this script will work).

This tool only supports Windows (Sorry MacOS Users, but providing the json configuration is the same, it should be trivial to port)

## Running

Note this tool will create a backup of your configuration for you, but it still recommended that your backup your config yourself before attempting to run this script.
your config file can be found in ```C:\Users\%USERNAME%\AppData\Local\LGHUB``` called settings.db

- Download the Main.py file
- Open Powershell, Terminal or CMD within the same folder as the script
- Quit logitech G Hub
- run ```Python Main.exe```

If all went well, you will see something like the below

```
Found settings db at: C:\Users\HDBSD\AppData\Local\LGHUB\settings.db
attempting to read db file...
Found 1 configs within database.
Found 3 Applications within config
App 0: Example app1 Installed: True Disabled: True
App 1: Example App2 Installed: True Disabled: True
App 3: APPLICATION_NAME_DESKTOP        Installed: False        Disabled: False
```

If the command completes with a line starting with `Exception: ...` something has gone wrong and usuall the error will be able to advise on what went wrong, if not please log an issue.

providing no error has occurred, reopen logitech g hub

## Recovery

Should something go wrong, you will be able to recover your old config by doing the following.
- closing logitech g hub
- navigating to ```C:\Users\%USERNAME%\AppData\Local\LGHUB```
- check for the existance of ```settings.backup.db``` (this might be called ```settings.backup``` if you do not have show file extensions enabled)
- delete settings.db
- rename settings.backup.db to settings.db
- re-open logitech g hub
