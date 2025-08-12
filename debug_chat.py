#!/usr/bin/env python3
"""
Script de depuración para identificar problemas en el chat
"""

import os
import google.generativeai as genai
from ai_analyzer import AIAnalyzer

def debug_chat():
    """Depura el problema del chat paso a paso"""
    print("🔍 Depurando problema del chat...")
    
    # API Key hardcodeada
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Paso 1: Probar configuración básica de Gemini
    print("\n1️⃣ Probando configuración básica de Gemini...")
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return False
    
    # Paso 2: Probar modelo
    print("\n2️⃣ Probando modelo Gemini...")
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        print("✅ Modelo Gemini creado correctamente")
    except Exception as e:
        print(f"❌ Error creando modelo: {e}")
        return False
    
    # Paso 3: Probar llamada simple
    print("\n3️⃣ Probando llamada simple a Gemini...")
    try:
        response = model.generate_content("Hola, responde solo 'OK'")
        if response and response.text:
            print(f"✅ Respuesta simple exitosa: {response.text}")
        else:
            print("❌ Respuesta vacía de Gemini")
            return False
    except Exception as e:
        print(f"❌ Error en llamada simple: {e}")
        return False
    
    # Paso 4: Probar AIAnalyzer
    print("\n4️⃣ Probando AIAnalyzer...")
    try:
        analyzer = AIAnalyzer(
            api_key=api_key,
            connection_id="f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
        )
        print("✅ AIAnalyzer creado correctamente")
    except Exception as e:
        print(f"❌ Error creando AIAnalyzer: {e}")
        return False
    
    # Paso 5: Probar chat_response
    print("\n5️⃣ Probando chat_response...")
    try:
        contexto_prueba = {
            "analisis": {"tipo": "test"},
            "problemas": [],
            "recomendaciones": []
        }
        
        respuesta = analyzer.chat_response("Hola", contexto_prueba)
        print(f"✅ chat_response exitoso: {respuesta[:100]}...")
        
    except Exception as e:
        print(f"❌ Error en chat_response: {e}")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    return True

if __name__ == "__main__":
    success = debug_chat()
    if not success:
        print("\n❌ Se encontraron problemas durante la depuración.")

