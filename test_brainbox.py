#!/usr/bin/env python3
"""
Script de prueba para verificar la integración con Brainbox API
"""

import os
import requests
from ai_analyzer import AIAnalyzer

def test_brainbox_connection():
    """Prueba la conexión con Brainbox API"""
    print("🧠 Probando conexión con Brainbox API...")
    
    # API Key de Brainbox
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    connection_id = "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🔗 Connection ID: {connection_id}")
    
    # Paso 1: Probar AIAnalyzer
    print("\n1️⃣ Probando AIAnalyzer...")
    try:
        analyzer = AIAnalyzer(
            api_key=api_key,
            connection_id=connection_id
        )
        print("✅ AIAnalyzer creado correctamente")
    except Exception as e:
        print(f"❌ Error creando AIAnalyzer: {e}")
        return False
    
    # Paso 2: Probar búsqueda de documentos
    print("\n2️⃣ Probando búsqueda de documentos...")
    try:
        docs = analyzer._search_documents("derecho de petición")
        print(f"✅ Búsqueda exitosa. Documentos encontrados: {len(docs)}")
        if docs:
            print(f"📄 Primer documento: {docs[0].get('content', '')[:100]}...")
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return False
    
    # Paso 3: Probar chat_response
    print("\n3️⃣ Probando chat_response...")
    try:
        contexto_prueba = {
            "analisis": {"tipo": "test"},
            "problemas": [],
            "recomendaciones": []
        }
        
        respuesta = analyzer.chat_response("¿Cómo mejorar la fundamentación legal?", contexto_prueba)
        
        if respuesta and respuesta.strip():
            print("✅ chat_response exitoso!")
            print(f"📄 Respuesta: {respuesta[:200]}...")
        else:
            print("❌ Respuesta vacía")
            return False
            
    except Exception as e:
        print(f"❌ Error en chat_response: {e}")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    print("🚀 La integración con Brainbox está funcionando correctamente")
    return True

def test_brainbox_api_directly():
    """Prueba la API de Brainbox directamente"""
    print("\n🔍 Probando API de Brainbox directamente...")
    
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    connection_id = "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
    
    # Probar endpoint de búsqueda
    url = f"https://app.brainbox.com.co/connections/{connection_id}/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": "derecho de petición",
        "limit": 3,
        "include_metadata": True
    }
    
    try:
        print(f"🌐 Probando endpoint: {url}")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta exitosa: {result}")
        else:
            print(f"❌ Error HTTP: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🧠 PRUEBA DE INTEGRACIÓN CON BRAINBOX")
    print("=" * 50)
    
    # Probar API directamente primero
    test_brainbox_api_directly()
    
    print("\n" + "=" * 50)
    
    # Probar integración completa
    success = test_brainbox_connection()
    
    if success:
        print("\n🎉 ¡La integración con Brainbox está funcionando!")
    else:
        print("\n❌ Hay problemas con la integración de Brainbox")
