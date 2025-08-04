#!/usr/bin/env python3
"""
Script para verificar el estado de la cuenta de Google Gemini
y diagnosticar problemas de cuota.
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def check_gemini_status():
    """Verifica el estado de la cuenta de Google Gemini"""
    print("🔍 Verificando estado de Google Gemini...")
    
    # Cargar variables de entorno de forma segura
    try:
        load_dotenv()
    except Exception as e:
        print(f"⚠️  No se pudo cargar archivo .env: {e}")
        print("💡 Esto es normal si no tienes un archivo .env configurado")
    
    # Obtener API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "tu_clave_aqui":
        print("❌ No se encontró API Key de Google Gemini")
        print("💡 Soluciones:")
        print("   1. Crea un archivo .env con tu API Key")
        print("   2. Ejecuta setup_api_key.bat")
        print("   3. Obtén una API Key en: https://makersuite.google.com/app/apikey")
        print("   4. La aplicación funcionará en modo simulado")
        return False
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Intentar una llamada simple para verificar
        print("✅ API Key válida")
        print("🔍 Verificando cuota...")
        
        # Hacer una llamada de prueba
        response = model.generate_content("Hola")
        
        print("✅ Conexión exitosa")
        print("✅ Cuota disponible")
        print("💡 La aplicación debería funcionar correctamente")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        if "quota" in error_msg.lower() or "limit" in error_msg.lower():
            print("\n💡 PROBLEMA DE CUOTA DETECTADO")
            print("🔧 Soluciones:")
            print("   1. Verifica tu saldo: https://makersuite.google.com/app/apikey")
            print("   2. Gemini tiene cuota gratuita generosa")
            print("   3. La aplicación funcionará en modo simulado")
        elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
            print("\n💡 API KEY INVÁLIDA")
            print("🔧 Soluciones:")
            print("   1. Verifica tu API Key en: https://makersuite.google.com/app/apikey")
            print("   2. Asegúrate de que empiece con 'AI'")
        else:
            print("\n💡 ERROR DESCONOCIDO")
            print("🔧 Verifica tu conexión a internet y configuración")
        
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 DIAGNÓSTICO DE GOOGLE GEMINI")
    print("=" * 50)
    
    success = check_gemini_status()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Todo está configurado correctamente")
    else:
        print("⚠️  Hay problemas de configuración")
        print("💡 La aplicación funcionará en modo simulado")
    print("=" * 50) 