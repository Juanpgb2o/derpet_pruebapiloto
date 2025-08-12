#!/usr/bin/env python3
"""
Script para configurar una nueva API Key de Google Gemini
"""

import os

def setup_new_api_key():
    """Guía para configurar una nueva API Key"""
    print("🔑 CONFIGURACIÓN DE NUEVA API KEY DE GOOGLE GEMINI")
    print("=" * 60)
    
    print("\n❌ PROBLEMA DETECTADO:")
    print("La API Key actual no es válida o ha expirado.")
    print("Error: 'API key not valid. Please pass a valid API key'")
    
    print("\n🔧 SOLUCIÓN:")
    print("1. Ve a Google AI Studio: https://makersuite.google.com/app/apikey")
    print("2. Inicia sesión con tu cuenta de Google")
    print("3. Haz clic en 'Create API Key'")
    print("4. Copia la nueva API Key (debe empezar con 'AI')")
    
    print("\n📝 NOTA IMPORTANTE:")
    print("- Las API Keys de Gemini empiezan con 'AI', no con 'bbfe_key_'")
    print("- La API Key anterior parece ser de un servicio diferente")
    print("- Gemini tiene cuota gratuita generosa")
    
    print("\n💡 PASOS PARA CONFIGURAR:")
    print("1. Obtén tu nueva API Key de Google AI Studio")
    print("2. Ejecuta este comando en PowerShell:")
    print("   Set-Content -Path .env -Value 'GEMINI_API_KEY=tu_nueva_api_key_aqui' -Encoding UTF8")
    print("3. Reemplaza 'tu_nueva_api_key_aqui' con tu API Key real")
    print("4. Reinicia la aplicación")
    
    print("\n🔍 VERIFICACIÓN:")
    print("Después de configurar, ejecuta: py debug_chat.py")
    print("Deberías ver '✅ Todas las pruebas pasaron exitosamente!'")
    
    print("\n" + "=" * 60)
    print("💡 Si necesitas ayuda, consulta la documentación de Google AI Studio")

if __name__ == "__main__":
    setup_new_api_key()

