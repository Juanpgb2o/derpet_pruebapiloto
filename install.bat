@echo off
echo ========================================
echo Instalando Sistema de Derechos de Peticion
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: No se pudo actualizar pip
    pause
    exit /b 1
)

echo ✅ Pip actualizado
echo.

echo Instalando dependencias...
python -m pip install -r requirements.txt --no-cache-dir
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Verifica que tienes conexión a internet
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas
echo.

echo Verificando instalación...
python -c "import streamlit, pandas, numpy, google.generativeai, dotenv, PyPDF2, docx2txt; print('✅ Todas las dependencias están instaladas')"
if errorlevel 1 (
    echo ERROR: Algunas dependencias no se instalaron correctamente
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Instalación completada exitosamente
echo ========================================
echo.
echo Para ejecutar la aplicación:
echo   run_app.bat
echo.
echo O manualmente:
echo   py -m streamlit run app.py --server.port 8501
echo.
pause 