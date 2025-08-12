#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Google Gemini
"""

import os
import sys
from dotenv import load_dotenv

def test_gemini_connection():
    """Prueba la conexión con Google Gemini"""
    print("🔍 Probando conexión con Google Gemini...")
    
    # Cargar variables de entorno
    try:
        load_dotenv()
        print("✅ Variables de entorno cargadas")
    except Exception as e:
        print(f"⚠️ Error cargando .env: {e}")
    
    # Obtener API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No se encontró GEMINI_API_KEY en las variables de entorno")
        return False
    
    print(f"🔑 API Key encontrada: {api_key[:20]}...")
    
    # Validar formato
    if not api_key.startswith("bbfe_key_"):
        print("❌ API Key inválida. Debe empezar con 'bbfe_key_'")
        return False
    
    print("✅ Formato de API Key válido")
    
    # Probar importación de Google Gemini
    try:
        import google.generativeai as genai
        print("✅ Google Gemini disponible")
    except ImportError as e:
        print(f"❌ Error importando Google Gemini: {e}")
        print("💡 Ejecuta: pip install google-generativeai")
        return False
    
    # Probar configuración
    try:
        genai.configure(api_key=api_key)
        print("✅ API Key configurada en Gemini")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return False
    
    # Probar modelo
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        print("✅ Modelo Gemini 2.0 Flash Exp disponible")
    except Exception as e:
        print(f"❌ Error con modelo: {e}")
        return False
    
    print("\n🎉 ¡Conexión exitosa con Google Gemini!")
    return True

if __name__ == "__main__":
    success = test_gemini_connection()
    if not success:
        print("\n❌ La conexión falló. Verifica tu API Key y dependencias.")
        sys.exit(1)
    else:
        print("\n✅ Todo listo para usar la aplicación con IA completa!") 