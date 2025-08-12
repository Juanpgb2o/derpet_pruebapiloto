@echo off
echo ========================================
echo Configuracion de API Key de Google Gemini
echo ========================================
echo.

echo Para usar la IA en la aplicacion, necesitas una API Key de Google Gemini.
echo.
echo 1. Ve a https://makersuite.google.com/app/apikey
echo 2. Inicia sesion o crea una cuenta
echo 3. Crea una nueva API Key
echo 4. Copia la clave (empieza con bbfe_key_)
echo.

set /p api_key="Ingresa tu API Key de Google Gemini: "

if "%api_key%"=="" (
    echo.
    echo No se ingreso ninguna clave. La aplicacion funcionara en modo simulado.
    echo.
    pause
    exit /b 0
)

echo.
echo Creando archivo .env con tu API Key...
echo GEMINI_API_KEY=%api_key% > .env
echo GEMINI_CONNECTION_ID=f3737a7e-f05f-427b-9591-cdc6feb7c0a4 >> .env
echo STREAMLIT_SERVER_PORT=8501 >> .env
echo STREAMLIT_SERVER_ADDRESS=localhost >> .env
echo LOG_LEVEL=INFO >> .env

echo.
echo ✅ Archivo .env creado exitosamente
echo.
echo IMPORTANTE: Nunca compartas tu API Key con nadie
echo La clave se guarda localmente en el archivo .env
echo.
echo NOTA: Esta es una API Key de Google Gemini, no de OpenAI
echo.
echo Ahora puedes ejecutar la aplicacion con IA completa
echo.
pause 