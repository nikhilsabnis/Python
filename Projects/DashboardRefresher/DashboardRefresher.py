import traceback
from pathlib import Path
import sys, logging, datetime

# Check if the tableauserverclient library is installed.
# if not installed then exit the program
try:
    import tableauserverclient as TSC
except:
    print('tableauserverclient library is not installed on this system')
    exit(1)

### Declarations

# The List of dashboard names that are hosted on the respective Tableau Server
# for which you want to trigger the data refresh
dashboardList = ['Dashboard1', 'Dashboard2', 'Dashboard3']

# The list of folders in which the dashbaords are hosted on the Tableau Server.
projectList = ['Folder1', 'Folder2']

# Credentials for logging in to the Tableau Server
credID = 'userid' # The userid of the person who has access to the folders and the dashboards on the Tableau server
credToken = 'PAT' # The Personal Access Token (PAT) you generated on the Tableau server for credID
credSite = 'SiteName' # The name of the site which is hosting the dashboards
credServerAddr = 'https://tableauSiteAddress' # The URL of the Tableau server

# File name and path used as a trigger the dashboard refresh
triggerFile = Path('\\\path\filename.extension')

# Path to store the log file
logPath = Path('\\\path\foldername')

# List will hold the date formats & the timestamp for logging & log file name
fmtList = [datetime.datetime.now().strftime("%Y-%m-%d%H%M%S"), '%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S']

# Create the log file and start logging the actions taken
logfilename = f"{logPath}{fmtList[0]}.log"

# Create a file logger with custom format
logger = logging.getLogger('')
logging.basicConfig(filename=logfilename,
                    level=logging.DEBUG,
                    format=fmtList[1],
                    datefmt=fmtList[2])

# Create a custom formatter for displaying text on the standard stream
formatter = logging.Formatter(fmt=fmtList[1],datefmt=fmtList[2])

# Add standard stream handler that will print the log to the screen
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
logger.addHandler(sh)

# Function to trigger the dashboard refresh
# If there is any error while requesting the dashboard refresh an error is thrown and
# next dashboard refresh is requested for the same queue
def triggerDashboardRefresh(loginid, token, site, address, projects_list, dashboards_list):
    # Set Tableau server access parameter values
    tableau_auth = TSC.PersonalAccessTokenAuth(loginid, token, site)
    server = TSC.Server(address)
    server.add_http_options({'verify':False})
    server.use_server_version()

    # Login to the Tableau server
    try:
        server.auth.sign_in(tableau_auth)
    except:
        logger.error('Encountered error, mentioned below, while logging on to the server:')
        logger.error(traceback.format_exc())
        logger.info('Logging completed')
        logging.shutdown()
        exit(1)

    # Get the dashboard and its resource id from the Tableau server
    try:
        dashboards = ((wb.id, wb.name) for wb in TSC.Pager(server.workbooks) if wb.project_name in projects_list and wb.name in dashboards_list)
    except:
        logger.error('Encountered error, mentioned below, while retrieving the list of workbooks from the server:')
        logger.error(traceback.format_exc())
        logger.info('Logging completed')
        logging.shutdown()
        exit(1)

    # Trigger dashboard refresh for each dashboard in the requested list
    for id, name in dashboards_list:
        try:
            with server.auth.sign_in(tableau_auth):
                jobID = server.workbooks.refresh(id)

                logger.info(f'Refresh requested for: {name}')
                logger.info(f'Resource ID: {id}')
                logger.info(f'Job ID: {jobID.id}')

                jobID = server.jobs.wait_for_job(jobID)

                logger.info(f'Refresh completed for: {name}')
        except:
            logger.error(f'Refresh failed for: {name}, due to error mentioned below:')
            logger.error(traceback.format_exc())
            logger.info('Will continue with the next dashboard in the queue')

def main():
    logger.info('Logging started')

    # Check if the trigger file is received and start the dashbaord refresh
    if triggerFile.exists():
        logger.info('Trigger file received')

        try:
            triggerFile.unlink(missing_ok=True)
            logger.info('Trigger file deleted')
        except PermissionError as e:
            logger.error('Trigger file cannot be deleted as it is used by someone/another process')
            logger.error('Please close the trigger file and try again')
            logger.info('Logging completed')
            logging.shutdown()
            exit(1)

        # Trigger dashboard refresh
        triggerDashboardRefresh(credID, credToken, credSite, credServerAddr, projectList, dashboardList)
        logger.info('Logging completed')
        logging.shutdown()
        exit(0)
    else:
        logger.info('Trigger file not received yet')
        logger.info('Logging completed')
        logging.shutdown()
        exit(0)

if __name__ == '__main__':
    main()