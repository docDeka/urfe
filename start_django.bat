@echo off
cd /d "%~dp0" || (
    echo Error: Cannot change directory to script location.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat || (
    echo Error: Cannot activate virtual environment. Ensure 'venv' exists in %~dp0.
    pause
    exit /b 1
)

echo Checking and updating dependencies...
if not exist requirements.txt (
    echo requirements.txt not found. Generating from current packages...
    pip freeze > requirements.txt || (
        echo Error: Failed to generate requirements.txt.
        pause
        exit /b 1
    )
)
pip install -r requirements.txt || (
    echo Error: Failed to update dependencies. Check for errors above.
    pause
    exit /b 1
)

echo Starting Django development server...
start /b python manage.py runserver || (
    echo Error: Failed to start Django server. Check for errors above.
    pause
    exit /b 1
)

echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Opening site in Google Chrome...
start chrome "http://127.0.0.1:8000/" || (
    echo Error: Failed to open Google Chrome. Ensure Chrome is installed.
    pause
    exit /b 1
)

echo Server started successfully. Press any key to exit...
pause