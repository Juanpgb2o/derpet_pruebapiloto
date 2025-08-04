@echo off
echo ========================================
echo Iniciando Sistema de Derechos de Peticion
echo ========================================
echo.

echo Verificando instalacion...
if not exist "app.py" (
    echo ERROR: app.py no encontrado
    echo Ejecuta install.bat primero
    pause
    exit /b 1
)

echo ✅ Aplicacion encontrada
echo.
echo Iniciando Streamlit...
echo.
echo La aplicacion se abrira en tu navegador
echo Si no se abre automaticamente, ve a: http://localhost:8501
echo.
echo Para detener la aplicacion: Ctrl+C
echo.

streamlit run app.py --server.port 8501

pause 