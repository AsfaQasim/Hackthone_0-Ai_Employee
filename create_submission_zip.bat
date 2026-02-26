@echo off
echo ========================================
echo    Bronze Tier Submission ZIP Creator
echo ========================================
echo.

echo Creating clean submission package...
echo.

REM Create temp directory for clean files
mkdir temp_submission 2>nul

echo Copying project files (excluding sensitive data)...

REM Copy main files
xcopy /Y Dashboard.md temp_submission\
xcopy /Y Company_Handbook.md temp_submission\
xcopy /Y README.md temp_submission\
xcopy /Y requirements.txt temp_submission\
xcopy /Y .env.example temp_submission\
xcopy /Y .gitignore temp_submission\
xcopy /Y package.json temp_submission\

REM Copy documentation
xcopy /Y BRONZE_*.md temp_submission\
xcopy /Y "Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md" temp_submission\

REM Copy folders (excluding sensitive data)
xcopy /E /I Skills temp_submission\Skills
xcopy /E /I Specs temp_submission\Specs
xcopy /E /I src temp_submission\src
xcopy /E /I ui temp_submission\ui

REM Create empty folders
mkdir temp_submission\Inbox
mkdir temp_submission\Needs_Action
mkdir temp_submission\Done
mkdir temp_submission\Plans
mkdir temp_submission\Pending_Approval
mkdir temp_submission\config
mkdir temp_submission\Logs

REM Copy .gitkeep files
copy Inbox\.gitkeep temp_submission\Inbox\ 2>nul
copy Needs_Action\.gitkeep temp_submission\Needs_Action\ 2>nul
copy Done\.gitkeep temp_submission\Done\ 2>nul

REM Create README for submission
echo # Bronze Tier Submission > temp_submission\SUBMISSION_README.md
echo. >> temp_submission\SUBMISSION_README.md
echo **Student**: Asfa Qasim >> temp_submission\SUBMISSION_README.md
echo **Email**: asfaqasim145@gmail.com >> temp_submission\SUBMISSION_README.md
echo **Date**: %date% >> temp_submission\SUBMISSION_README.md
echo. >> temp_submission\SUBMISSION_README.md
echo ## Bronze Tier Status: COMPLETE >> temp_submission\SUBMISSION_README.md
echo. >> temp_submission\SUBMISSION_README.md
echo All requirements met: >> temp_submission\SUBMISSION_README.md
echo - Obsidian vault structure >> temp_submission\SUBMISSION_README.md
echo - Dashboard.md and Company_Handbook.md >> temp_submission\SUBMISSION_README.md
echo - Gmail Watcher implementation >> temp_submission\SUBMISSION_README.md
echo - Claude Code integration >> temp_submission\SUBMISSION_README.md
echo - Agent Skills framework >> temp_submission\SUBMISSION_README.md
echo. >> temp_submission\SUBMISSION_README.md
echo See BRONZE_TIER_COMPLETION_REPORT.md for details. >> temp_submission\SUBMISSION_README.md

echo.
echo Creating ZIP file...
powershell Compress-Archive -Path temp_submission\* -DestinationPath Bronze-Tier-Submission.zip -Force

echo.
echo Cleaning up...
rmdir /s /q temp_submission

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo ZIP file created: Bronze-Tier-Submission.zip
echo.
echo Next steps:
echo 1. Upload to Google Drive
echo 2. Get shareable link
echo 3. Submit in hackathon form
echo.
echo OR
echo.
echo Submit directly via form:
echo https://forms.gle/JR9T1SJq5rmQyGkGA
echo ========================================
echo.

pause
