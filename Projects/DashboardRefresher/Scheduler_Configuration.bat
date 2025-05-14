rem This file acts as a configuration for the Windows Scheduler
rem which triggers the dashboard refresh using the miniconda python distribution
rem You would have a conda environment created before running this bat file

@echo OFF
rem activate the conda environment
call "C:\Program Files\miniconda3\Scripts\activate.bat" "C:\Users\xyz\.conda\envs\dev"

rem Run a python script in that environment
python "C:\Users\xyz\Scripts\DashboardRefresher.py"

rem Deactivate the environment
call conda deactivate