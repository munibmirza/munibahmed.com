@echo off
cd /d "%~dp0"
echo Building protected obfuscated deploy copy into web folder...
if not exist node_modules\javascript-obfuscator (
  echo Installing obfuscator, first time only...
  call npm install --no-save javascript-obfuscator
)
node build_protected.js
echo.
echo Done. Now deploy the web folder to Netlify.
pause
