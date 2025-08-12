@echo off
echo ========================================
echo Optimizando Sistema de Derechos de Peticion
echo ========================================
echo.

echo Limpiando cache de Python...
python -m pip cache purge
if errorlevel 1 (
    echo ⚠️ No se pudo limpiar cache de pip
) else (
    echo ✅ Cache de pip limpiado
)

echo.
echo Limpiando archivos temporales...
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ Cache de Python limpiado
)

if exist ".streamlit" (
    echo ✅ Configuración de Streamlit encontrada
) else (
    echo ⚠️ Configuración de Streamlit no encontrada
)

echo.
echo Verificando dependencias...
python -c "import streamlit, pandas, numpy, google.generativeai, dotenv, PyPDF2, docx2txt; print('✅ Todas las dependencias están disponibles')"
if errorlevel 1 (
    echo ⚠️ Algunas dependencias pueden tener problemas
    echo Ejecuta install.bat para reinstalar
)

echo.
echo ========================================
echo ✅ Optimización completada
echo ========================================
echo.
echo La aplicación está optimizada para mejor rendimiento
echo.
pause 