:: the following command must be run first:
:: Set-ExecutionPolicy RemoteSigned

:: @echo off
REM Navigate to the directory containing the virtual environment
cd /d "PupInvoiceGenerator"

REM Activate the virtual environment
call .\venv\Scripts\activate
call pip3 install -r requirements.txt


REM Run the Python script
python main.py

REM Deactivate the virtual environment
deactivate
exit
