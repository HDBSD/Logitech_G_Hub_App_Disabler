import sqlite3
import os
import json
import subprocess

def main():

    # if script is not running on windows just throw an exception
    
    if os.name != 'nt':
        raise Exception('This script is only designed to work on windows')
    
    # check if logitech g hub is running (ignoring the updater)

    if process_exists('lghub.exe') or process_exists('lghub_agent.exe') or process_exists('lghub_system_tray.exe'):
        raise Exception('Logitech G hub is running, this probably won\'t cause any issues, but this isn\'t a tested senario.')

    # create path to logitech g hub's sqlite3 config database
    
    settingsPath = os.environ['localappdata'] + '\\LGHUB\\settings.db'
    backupPath = os.environ['localappdata'] + '\\LGHUB\\settings.bakup.db'

    # if the expected db doesn't exist throw an exception

    if not os.path.isfile(settingsPath):
        raise Exception('Settings db could not be found in expected location')
    
    print('Found settings db at: ' + settingsPath)
    print('attempting to read db file...')
    
    # create a connection to the db and another to new backup db

    conn = sqlite3.connect(settingsPath)
    
    bakconn = sqlite3.connect(backupPath)

    # make a backup

    conn.backup(bakconn)
    bakconn.close()

    # read configs

    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    
    rows = cur.fetchall()

    print('Found ' +  str(len(rows)) + ' configs within database.' )

    if len(rows) != 1:
        raise Exception('This script cannot handle multiple configs within a database')
    
    conf = json.loads(rows[0][2])

    print('Found ' + str(len(conf['applications']['applications'])) + ' Applications within config')

    # loop through all applications and disable all applications other than the desktop app

    for x in range(0, len(conf['applications']['applications'])):
        appname = conf['applications']['applications'][x].get('name', None)
        if appname is None:
            raise Exception('Application name doesn\'t exist')
        
        isInstalled = conf['applications']['applications'][x].get('isInstalled', False)
        isDisabled = conf['applications']['applications'][x].get('isDisabled', False)

        if appname != 'APPLICATION_NAME_DESKTOP' and isDisabled == False:
            print('App ' + str(x) + ': ' + appname + '\tInstalled: ' + str(isInstalled) + '\tDisabled: ' + str(isDisabled) + '\t\t\t-> Setting to Disabled to True')
            conf['applications']['applications'][x]['isDisabled'] = True
        else:
            print('App ' + str(x) + ': ' + appname + '\tInstalled: ' + str(isInstalled) + '\tDisabled: ' + str(isDisabled))
            

    # commit the changes to the db and close it

    cur.execute("UPDATE data SET file = ? where _id = ?", (json.dumps(conf), rows[0][0]))
    conn.commit()
    conn.close()
    
# thanks to Eric Werner - goodsoul.de for the below snippet

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())



if __name__ == '__main__':
    main()