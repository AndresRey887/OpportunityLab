@echo off
setlocal EnableExtensions

rem ============================================================
rem OpportunityLab Review Package Creator
rem
rem Creates a clean ZIP containing source code and documentation.
rem Excludes virtual environments, databases, logs, caches,
rem environment files, API keys, secrets, and Git files.
rem ============================================================

title OpportunityLab Review Package Creator

set "SOURCE=%~dp0"
set "OUTPUT_FOLDER=%SOURCE%OpportunityLab-Review"
set "OUTPUT_ZIP=%SOURCE%OpportunityLab-Review.zip"

echo.
echo ============================================================
echo  OpportunityLab Review Package Creator
echo ============================================================
echo.
echo Source:
echo %SOURCE%
echo.

rem Remove an older review folder.
if exist "%OUTPUT_FOLDER%" (
    echo Removing previous review folder...
    rmdir /S /Q "%OUTPUT_FOLDER%"
)

rem Remove an older ZIP.
if exist "%OUTPUT_ZIP%" (
    echo Removing previous ZIP...
    del /Q "%OUTPUT_ZIP%"
)

mkdir "%OUTPUT_FOLDER%"

echo.
echo Copying project folders...
echo.

rem Copy source and supporting folders.
for %%F in (
    src
    docs
    scripts
    tests
    config
) do (
    if exist "%SOURCE%%%F" (
        echo Copying %%F...

        robocopy "%SOURCE%%%F" "%OUTPUT_FOLDER%\%%F" /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP ^
            /XD ".venv" "venv" "env" "__pycache__" ".pytest_cache" ".mypy_cache" ".ruff_cache" ^
                ".git" ".github" "logs" "log" "data" "database" "databases" "node_modules" ^
            /XF "*.pyc" "*.pyo" "*.db" "*.sqlite" "*.sqlite3" "*.log" ^
                ".env" ".env.*" "*.env" ^
                "*secret*" "*secrets*" "*api_key*" "*apikey*" "*credentials*" ^
                "service-account*.json" "token.json"
    )
)

echo.
echo Copying important project files...
echo.

for %%F in (
    main.py
    requirements.txt
    pyproject.toml
    setup.py
    setup.cfg
    README.md
    AI_HANDOVER.md
    DEVELOPMENT_JOURNAL.md
    Development_Journal.md
    "Development Journal.md"
    .gitignore
) do (
    if exist "%SOURCE%%%~F" (
        copy /Y "%SOURCE%%%~F" "%OUTPUT_FOLDER%\" >nul
        echo Copied %%~F
    )
)

echo.
echo Performing an additional safety cleanup...
echo.

rem Remove sensitive or unnecessary files that may have slipped through.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$root = '%OUTPUT_FOLDER%';" ^
    "$patterns = @(" ^
    "'*.db','*.sqlite','*.sqlite3','*.log','*.pyc','*.pyo'," ^
    "'.env','.env.*','*.env'," ^
    "'*secret*','*secrets*','*api_key*','*apikey*','*credentials*'," ^
    "'service-account*.json','token.json'" ^
    ");" ^
    "foreach ($pattern in $patterns) {" ^
    "  Get-ChildItem -LiteralPath $root -Recurse -Force -File -Filter $pattern -ErrorAction SilentlyContinue |" ^
    "  Remove-Item -Force -ErrorAction SilentlyContinue" ^
    "}"

echo.
echo Creating ZIP file...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Compress-Archive -LiteralPath '%OUTPUT_FOLDER%' -DestinationPath '%OUTPUT_ZIP%' -Force"

if not exist "%OUTPUT_ZIP%" (
    echo.
    echo ERROR: The ZIP file could not be created.
    echo The review folder is still available here:
    echo %OUTPUT_FOLDER%
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Review package created successfully
echo ============================================================
echo.
echo ZIP file:
echo %OUTPUT_ZIP%
echo.
echo This package excludes:
echo   - .venv and other virtual environments
echo   - database files
echo   - logs
echo   - __pycache__
echo   - .env files
echo   - API key and secret files
echo   - Git metadata
echo   - data folders
echo.
echo Please inspect the ZIP before uploading it, especially the
echo config folder, to confirm that no private keys are included.
echo.

explorer /select,"%OUTPUT_ZIP%"

pause
endlocal