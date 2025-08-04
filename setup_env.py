#!/usr/bin/env python3
"""
Script para configurar el archivo .env de forma segura
"""

import os
import getpass

def create_env_file():
    """Crea o actualiza el archivo .env"""
    print("🔧 Configurando archivo .env...")
    
    # Contenido del archivo .env
    env_content = """# Configuración de Google Gemini
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
    
    # Solicitar API Key
    print("\n🔑 Configuración de Google Gemini API Key")
    print("💡 Obtén tu API Key en: https://makersuite.google.com/app/apikey")
    print("💡 Si no tienes una, presiona Enter para usar modo simulado")
    
    api_key = getpass.getpass("Ingresa tu API Key (se ocultará): ").strip()
    
    if not api_key:
        print("✅ Modo simulado activado")
        api_key = "gemini-simulated-mode"
    elif not api_key.startswith("AI"):
        print("⚠️  La API Key de Gemini debe empezar con 'AI'")
        api_key = "gemini-simulated-mode"
    else:
        print("✅ API Key configurada")
    
    # Crear archivo .env
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content.format(api_key=api_key))
        
        print("✅ Archivo .env creado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 CONFIGURADOR DE ENVIRONMENT")
    print("=" * 50)
    
    success = create_env_file()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Configuración completada")
        print("💡 Ahora puedes ejecutar la aplicación")
    else:
        print("❌ Error en la configuración")
    print("=" * 50) 