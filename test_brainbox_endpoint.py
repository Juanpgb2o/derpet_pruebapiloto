#!/usr/bin/env python3
"""
Script para probar el endpoint específico de BrainBox: /api/public/v1/check
"""

import requests
import json

def test_brainbox_endpoint():
    """Prueba el endpoint específico de BrainBox"""
    print("🧠 Probando endpoint específico de BrainBox...")
    
    # API Key de BrainBox
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    connection_id = "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
    base_url = "https://app.brainbox.com.co"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🔗 Connection ID: {connection_id}")
    print(f"🌐 Base URL: {base_url}")
    
    # Probar endpoint de verificación
    endpoint = "/api/public/v1/check"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Probar con GET primero
    print(f"\n1️⃣ Probando GET en: {endpoint}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Respuesta exitosa: {json.dumps(result, indent=2)}")
            except:
                print(f"✅ Respuesta exitosa (texto): {response.text}")
        else:
            print(f"❌ Error HTTP: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en GET: {e}")
    
    # Probar con POST
    print(f"\n2️⃣ Probando POST en: {endpoint}")
    try:
        data = {
            "connection_id": connection_id,
            "test": True
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Respuesta exitosa: {json.dumps(result, indent=2)}")
            except:
                print(f"✅ Respuesta exitosa (texto): {response.text}")
        else:
            print(f"❌ Error HTTP: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en POST: {e}")
    
    # Probar otros endpoints posibles
    print(f"\n3️⃣ Probando otros endpoints posibles...")
    
    possible_endpoints = [
        "/api/public/v1/chat",
        "/api/public/v1/generate",
        "/api/public/v1/search",
        "/api/public/v1/rag",
        "/api/public/v1/connections",
        "/api/public/v1/connections/" + connection_id,
        "/api/public/v1/connections/" + connection_id + "/search",
        "/api/public/v1/connections/" + connection_id + "/generate"
    ]
    
    for ep in possible_endpoints:
        try:
            test_url = f"{base_url}{ep}"
            print(f"\n🔍 Probando: {ep}")
            
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Endpoint válido encontrado!")
                try:
                    result = response.json()
                    print(f"   Respuesta: {json.dumps(result, indent=2)[:200]}...")
                except:
                    print(f"   Respuesta: {response.text[:200]}...")
                    
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")

if __name__ == "__main__":
    print("🧠 PRUEBA DE ENDPOINTS DE BRAINBOX")
    print("=" * 60)
    test_brainbox_endpoint()

