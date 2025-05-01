@echo off
REM Nos aseguramos de estar en la carpeta del .bat
cd /d "%~dp0"
REM Instalamos Flask (solo la primera vez; después puedes comentar esta línea poniendo REM al inicio)
pip install flask
REM Ejecutamos la app
python app.py
REM Mantenemos la ventana abierta para ver errores o la URL
pause