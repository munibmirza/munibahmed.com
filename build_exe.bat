@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  Building InterAudit-P1.exe
echo ============================================================
echo.

echo [1/3] Installing / updating PyInstaller...
python -m pip install --upgrade pyinstaller || goto :error

echo.
echo [2/3] Cleaning previous build...
if exist build       rmdir /s /q build
if exist dist        rmdir /s /q dist
if exist InterAudit-P1.spec del /q InterAudit-P1.spec

echo.
echo [3/3] Building the .exe (this can take 2-5 minutes)...
python -m PyInstaller ^
  --noconsole ^
  --onefile ^
  --name InterAudit-P1 ^
  --icon "assets\icon.ico" ^
  --add-data "assets\icon.ico;assets" ^
  --add-data "assets\icon.png;assets" ^
  --collect-submodules openpyxl ^
  --collect-submodules pandas ^
  main.py || goto :error

echo.
echo ============================================================
echo  Build complete.
echo.
echo  Your app is here:
echo     %cd%\dist\InterAudit-P1.exe
echo.
echo  Next step: copy the procedures\ folder to sit next to the
echo  .exe (the script does that automatically below).
echo ============================================================

if exist "dist\procedures" rmdir /s /q "dist\procedures"
xcopy /e /i /q "procedures" "dist\procedures" >nul
if not exist "dist\input"  mkdir "dist\input"
if not exist "dist\output" mkdir "dist\output"

echo.
echo Done. Open the dist\ folder and double-click InterAudit-P1.exe
echo.
pause
exit /b 0

:error
echo.
echo *** Build failed. Read the messages above. ***
pause
exit /b 1
