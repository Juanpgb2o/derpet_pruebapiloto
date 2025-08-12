#!/usr/bin/env python3
"""
Script de prueba para verificar que la función chat_response funcione correctamente
"""

import os
from ai_analyzer import AIAnalyzer

def test_chat():
    """Prueba la función chat_response"""
    print("🧪 Probando función chat_response...")
    
    # Configurar API key directamente
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    os.environ['GEMINI_API_KEY'] = api_key
    
    print(f"🔑 API Key configurada: {api_key[:20]}...")
    
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

