import datetime
import multiprocessing
import pyodbc
import time
import os
import sys
import shutil

DRIVER = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:aeul-test-server.database.windows.net,1433;Database=Aaron_Test_Server;Uid=aeul@aeul-test-server;Pwd={/Raindrop18};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

PROCESSES = 5

Scripts = []

def logErr(message):
        curTime = datetime.datetime.now().strftime('%H:%M:%S')
        errorLogLocation = build_folder + "/" + ("errorlog.txt")
        print(message)
        errLog = open(errorLogLocation, 'a')
        errLog.write("[" + curTime + "]" + message + os.linesep)
        errLog.close()

def log(message):
        curTime = datetime.datetime.now().strftime('%H:%M:%S')
        LogLocation = build_folder + "/" + ("log.txt")
        print(message)
        errLog = open(LogLocation, 'a')
        errLog.write("[" + curTime + "]" + message + os.linesep)
        errLog.close()

def findScripts():
    print(WORKSPACE)
    numScripts = 0
    exclude = ()
    for root, dirs, files in os.walk(SCRIPTS):
        # If there is a no Script Folder
        # - Created new folder (Scripts)
        scriptsFd = WORKSPACE + "scripts"
        if not os.path.exists(scriptsFd):
            os.mkdir(scriptsFd)
        else:
            shutil.rmtree(scriptsFd) #If it does, delete current and remake
            os.mkdir(scriptsFd)

        for name in files:
            print("Found: " + name)
            subject = root + "/" + name
            #Filter out:
            # - Hidden Files
            # - Without_extension Files
            if name.startswith("."):
                extension = ".hidden_files"
            elif not "." in name:
                extension = ".without_extension"
            else:
                extension = name[name.rfind("."):]

            # Filter out:
            # -None .Sql Files
            if extension == ".sql":
                # Copy found .Sql file into Script folder
                newfile = scriptsFd + "/" + name
                shutil.copy(subject, newfile)
                print("Copied ==> " + name + "Path = " + scriptsFd)

                numScripts += 1

                # Append found script name and path to Scripts Array
                global Scripts
                Scripts.append((name, newfile))

        return numScripts


def node(num):
    startTime = time.time()
    log("Node " + str(num) + ": is starting...")
    # time.sleep(randint(1,4))

    con = pyodbc.connect(DRIVER)
    log("Node " + str(num) + ": connected to Sql Server")
    cur = con.cursor()

    # Open and read the file as a single buffer
    fd = open(Scripts[num][1], 'r')
    sqlFile = fd.read()
    fd.close()
    log("Node " + str(num) + ": read Sql Script :" + Scripts[num][0])

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    line = 1
    for command in sqlCommands:
        try:
            log("Node " + str(num) + ": executing :" + command)
            cur.execute(command) #Run Sql Command
        except (pyodbc.ProgrammingError) as err:
            pass
            log("Node " + str(num) + ": Command = " + command + "failed")
            log("Node " + str(num) + ": Sql Error Msg: " + str(err))

            logErr("Node " + str(num) + ": Command = " + command + "failed")
            logErr("Node " + str(num) + ": Sql Error Msg: " + str(err))
            return Scripts[num][0], 0.00, "Failed"

    endTime = time.time()
    log("Node " + str(num) + " completed ")
    return Scripts[num][0], (endTime - startTime), "Successful"

#Builds folder which will contain logs
def createWorkspaceFolder():
    builds_folder = WORKSPACE + "/Builds"
    if not os.path.exists(builds_folder):
        os.mkdir(builds_folder)


    time = datetime.datetime.now().strftime('%y_%m_%d_%S')
    new_dir = builds_folder + "/" + time
    os.mkdir(new_dir)

    global build_folder
    build_folder = new_dir
    print("Work Location : ", build_folder)

def createReport(pool_outputs):
    fileLoc = build_folder + "/" + ("MasterLog.txt")
    log = open(fileLoc, 'a')
    for output in pool_outputs:
        log.write("=========================================" + os.linesep + os.linesep)

        log.write("Script: " + output[0] + " was [" + output[2] + "]" + os.linesep)
        log.write("   Time taken: " + str(output[1]) + os.linesep + os.linesep)

        log.write("=========================================" + os.linesep)

if __name__ == '__main__':
    global WORKSPACE
    global SCRIPTS

    try:
        WORKSPACE = sys.argv[1]
        SCRIPTS = sys.argv[2]
    except:
        WORKSPACE = "/Users/e174285/Documents/GitHub/Jenkins_Test/"
        SCRIPTS = "/Users/e174285/Desktop/Scripts/"

    num_scripts = findScripts()

    if num_scripts > 0:
        createWorkspaceFolder()

        pool = multiprocessing.Pool(processes=PROCESSES)
        pool_outputs = pool.map(node, range(num_scripts))
        pool.close()
        pool.join()

        createReport(pool_outputs)
    else:
        print("No scripts found in repo")
