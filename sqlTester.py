import datetime
import multiprocessing
import pyodbc
import time
import os
import sys
import shutil

DRIVER = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:aeul-test-server.database.windows.net,1433;Database=Aaron_Test_Server;Uid=aeul@aeul-test-server;Pwd={/Raindrop18};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
WORKSPACE = "" #'/Users/Aaron/Desktop/Scripts'
workFolder = "/Users/Aaron/Desktop/Scripts/####_##_##"

PROCESSES = 5

Scripts = []

def logErr(message):
        curTime = datetime.datetime.now().strftime('%H:%M:%S')
        errorLogLocation = workFolder + "/" + ("errorlog.txt")
        errLog = open(errorLogLocation, 'a')
        errLog.write("[" + curTime + "]" + message + os.linesep)
        errLog.close()

def log(message):
        LogLocation = workFolder + "/" + ("log.txt")
        errLog = open(LogLocation, 'a')
        errLog.write("[" + curTime + "]" + message + os.linesep)
        errLog.close()

def findScripts():
    numScripts = 0
    exclude = ()
    for root, dirs, files in os.walk(WORKSPACE):
        # If there is a no Script Folder
        # - Created new folder (Scripts)
        scriptsFd = WORKSPACE + "/scripts"
        if not os.path.exists(scrFd):
            os.mkdir(scriptsFd)
        else:
            shutil.rmtree(scriptsFd) #If it does, delete current and remake
            os.mkdir(scriptsFd)

        for name in files:
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
                print("Moved ==> " + name)

                numScripts += 1

                # Append found script name and path to Scripts Array
                global Scripts
                Scripts.append((name, newfile))

            return numScripts


def node(num):
    startTime = time.time()
    log("Node " + num + ": is starting...")
    # time.sleep(randint(1,4))

    con = pyodbc.connect(DRIVER)
    log("Node " + num + ": connected to Sql Server")
    cur = con.cursor()

    # Open and read the file as a single buffer
    fd = open(Scripts[num][1], 'r')
    sqlFile = fd.read()
    fd.close()
    log("Node " + num + ": read Sql Script :" + Scripts[num][0])

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    line = 1
    for command in sqlCommands:
        try:
            log("Node " + num + ": executing :" + command)
            cur.execute(command) #Run Sql Command
        except (pyodbc.ProgrammingError) as err:
            pass
            log("Node : " + num + ": Command = " + command + "failed")
            log("Node : " + num + "Sql Error Msg: " + str(err))

            errlog("Node : " + num + ": Command = " + command + "failed")
            errlog("Node : " + num + "Sql Error Msg: " + str(err))
            return Scripts[num][0], 0.00, "Failed"

    endTime = time.time()
    log("Node " + num + "completed ")
    return Scripts[num][0], (endTime - startTime), "Successful"

#Builds folder which will contain logs
def createWorkspaceFolder():
    time = datetime.datetime.now().strftime('%Y_%M_%D__%H_%M_%S')
    new_dir = WORKSPACE + "/" + time
    os.mkdir(new_dir)

    global workFolder
    workFolder = new_dir
    print("Work Location : ", workFolder)

# def createNode(fileName):
#     new_dir = workFolder + "/" + fileName
#     os.mkdir(new_dir)
#
#     return new_dir

def createReport(pool_outputs):
    fileLoc = workFolder + "/" + ("MasterLog.txt")
    log = open(fileLoc, 'a')
    for output in pool_outputs:
        log.write("=========================================" + os.linesep + os.linesep)

        log.write("Script: " + output[0] + " was [" + output[2] + "]" + os.linesep)
        log.write("   Time taken: " + str(output[1]) + os.linesep + os.linesep)

        log.write("=========================================" + os.linesep)

if __name__ == '__main__':
    WORKSPACE = str(sys.argv[1])

    numScripts = findScripts()
    createWorkspaceFolder()

    pool = multiprocessing.Pool(processes=PROCESSES)
    pool_outputs = pool.map(node, range(numScripts))
    pool.close()
    pool.join()

    createReport(pool_outputs)
