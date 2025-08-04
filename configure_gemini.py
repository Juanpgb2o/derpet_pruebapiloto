#!/usr/bin/env python3
"""
Script simple para configurar la API Key de Google Gemini
"""

def create_env_file():
    """Crea el archivo .env con la API Key de Gemini"""
    
    # API Key proporcionada por el usuario
    api_key = "AIzaSyB34CAmzxI14VNCldBPAEG6xtTK_0W-dB4"
    
    # Contenido del archivo .env
    env_content = f"""# Configuración de Google Gemini
# Obtén tu API Key en: https://makersuite.google.com/app/apikey
GEMINI_API_KEY={api_key}

# Configuración del servidor Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# Configuración de logging
LOG_LEVEL=INFO

# NOTAS IMPORTANTES:
# 1. Si obtienes error de cuota excedida, verifica:
#    - Tu saldo en: https://makersuite.google.com/app/apikey
#    - Gemini tiene cuota gratuita generosa
# 2. La aplicación funcionará en modo simulado sin API Key
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado exitosamente")
        print("✅ API Key de Google Gemini configurada")
        print("💡 Ahora puedes usar la aplicación con IA completa")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 CONFIGURANDO GOOGLE GEMINI")
    print("=" * 50)
    
    success = create_env_file()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Configuración completada")
        print("💡 Reinicia la aplicación para aplicar los cambios")
    else:
        print("❌ Error en la configuración")
    print("=" * 50) 