@echo off
REM Wrapper para Windows
REM Uso: traduzir.bat arquivo.pdf [opcoes]

setlocal

set SCRIPT_DIR=%~dp0

REM Carregar .env se existir
if exist "%SCRIPT_DIR%.env" (
    for /f "tokens=1,2 delims==" %%a in (%SCRIPT_DIR%.env) do (
        if not "%%a"=="" set %%a=%%b
    )
)

REM Ativar venv se existir
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
)

python "%SCRIPT_DIR%translate.py" %*
