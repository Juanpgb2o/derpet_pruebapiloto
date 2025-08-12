#!/usr/bin/env python3
"""
Script de prueba para verificar que la función chat_response funcione correctamente
"""

import os
from dotenv import load_dotenv
from ai_analyzer import AIAnalyzer

def test_chat():
    """Prueba la función chat_response"""
    print("🧪 Probando función chat_response...")
    
    # Cargar variables de entorno
    try:
        load_dotenv()
        print("✅ Variables de entorno cargadas")
    except Exception as e:
        print(f"⚠️ Error cargando .env: {e}")
    
    # Verificar API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No se encontró GEMINI_API_KEY")
        return False
    
    print(f"🔑 API Key encontrada: {api_key[:20]}...")
    
    # Crear analizador
    try:
        analyzer = AIAnalyzer(
            api_key=api_key,
            connection_id="f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
        )
        print("✅ AIAnalyzer creado correctamente")
    except Exception as e:
        print(f"❌ Error creando AIAnalyzer: {e}")
        return False
    
    # Contexto de prueba
    contexto_prueba = {
        "analisis": {
            "tipo_documento": "Derecho de Petición",
            "longitud": 1500,
            "confianza": 0.8
        },
        "problemas": [
            {
                "tipo": "FORMAL",
                "descripcion": "Falta número de radicado",
                "severidad": "ALTA"
            }
        ],
        "recomendaciones": [
            {
                "titulo": "Incluir número de radicado",
                "descripcion": "Agregar número de radicado al documento",
                "prioridad": "ALTA"
            }
        ]
    }
    
    # Pregunta de prueba
    pregunta_prueba = "¿Cómo mejorar la contestación del documento?"
    
    print(f"📝 Pregunta de prueba: {pregunta_prueba}")
    print("🔄 Generando respuesta...")
    
    try:
        respuesta = analyzer.chat_response(pregunta_prueba, contexto_prueba)
        
        if respuesta and respuesta.strip():
            print("✅ Respuesta generada exitosamente!")
            print(f"📄 Respuesta: {respuesta[:200]}...")
            return True
        else:
            print("❌ La respuesta está vacía")
            return False
            
    except Exception as e:
        print(f"❌ Error en chat_response: {e}")
        return False

if __name__ == "__main__":
    success = test_chat()
    if success:
        print("\n🎉 ¡La función chat_response funciona correctamente!")
    else:
        print("\n❌ La función chat_response tiene problemas.")

