import datetime
import multiprocessing
import pyodbc
import time
import os
import sys
import shutil

DRIVER = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:aeul-test-server.database.windows.net,1433;Database=Aaron_Test_Server;Uid=aeul@aeul-test-server;Pwd={/Raindrop18};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
WORKSPACE = ""#'/Users/Aaron/Desktop/Scripts'
workFolder = "/Users/Aaron/Desktop/Scripts/####_##_##"

dataTable = "Race_Data_35"

PROCESSES = 5

Scripts = []


def scriptFinder():
    exclude = ()
    for root, dirs, files in os.walk(WORKSPACE):

        # If there is a no Script Folder
        # - Created new folder (Scripts)
        scrFd = WORKSPACE + "/scripts"
        if not os.path.exists(scrFd):
            os.mkdir(scrFd)
        else:
            shutil.rmtree(scrFd)
            os.mkdir(scrFd)

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

                # Copy all found .Sql fills into Script folder
                newfile = scrFd + "/" + name
                shutil.copy(subject, newfile)
                print(name, subject)

                global Scripts
                Scripts.append((name, subject))


def worker(num):
    startTime = time.time()

    # workerFolderPath = createWorker(Scripts[num][0])
    #
    # logLocation = workerFolderPath + "/" + ("log.txt")
    errorLogLocation = workFolder + "/" + ("errorlog.txt")

    # log = open(logLocation, 'a')
    errLog = open(errorLogLocation, 'a')

    """worker function"""
    # log.write('Starting ' + Scripts[num][0])

    # time.sleep(randint(1,4))

    con = pyodbc.connect(DRIVER)
    cur = con.cursor()

    # Open and read the file as a single buffer
    fd = open(Scripts[num][1], 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    line = 1
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cur.execute(command)

        except (pyodbc.ProgrammingError) as err:
            pass
            # os.rename(workerFolderPath, workerFolderPath + "[Failed]")
            errLog.write("Command failed: " + command + os.linesep)
            errLog.write("Sql Error Msg: " + str(err) + os.linesep)

            # log.close()
            errLog.close()
            return Scripts[num][0], 0.00, "Failed"


    # log.write('\nExiting ' + Scripts[num][0])

    # log.close()
    errLog.close()

    endTime = time.time()

    return Scripts[num][0], (endTime - startTime), "Successful"


def createWorkspaceFolder():
    time = datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    new_dir = WORKSPACE + "/" + time
    os.mkdir(new_dir)

    global workFolder
    workFolder = new_dir
    print("Work Location : ", workFolder)

def createWorker(fileName):
    new_dir = workFolder + "/" + fileName
    os.mkdir(new_dir)

    return new_dir

def createMasterLog(pool_outputs):
    fileLoc = workFolder + "/" + ("MasterLog.txt")
    log = open(fileLoc, 'a')
    for output in pool_outputs:
        log.write("=========================================" + os.linesep)

        log.write("Script: " + output[0] + " was [" + output[2] + "]" + os.linesep)
        log.write("   Time taken: " + str(output[1]) + os.linesep)

        log.write("=========================================" + os.linesep)

if __name__ == '__main__':
    WORKSPACE = str(sys.argv[1])
    # b = str(sys.argv[2])

    scriptFinder()
    createWorkspaceFolder()

    pool = multiprocessing.Pool(processes=PROCESSES)
    pool_outputs = pool.map(worker, range(5))
    pool.close()
    pool.join()

    createMasterLog(pool_outputs)
