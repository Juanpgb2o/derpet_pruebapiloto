#!/usr/bin/env python3
"""
Script para verificar Brainbox usando los endpoints oficiales de la documentación
"""

import os
import requests
import json
from datetime import datetime

def test_brainbox_official_endpoints():
    """Prueba los endpoints oficiales de BrainBox según la documentación"""
    print("🔍 VERIFICANDO BRAINBOX CON ENDPOINTS OFICIALES")
    print("=" * 70)
    
    # Configuración de Brainbox
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    box_id = "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
    base_url = "https://app.brainbox.com.co/api/public/v1"
    
    print(f"📋 CONFIGURACIÓN ACTUAL:")
    print(f"   • API Key: {api_key[:20]}...{api_key[-4:]}")
    print(f"   • Box ID: {box_id}")
    print(f"   • Base URL: {base_url}")
    print()
    
    # Headers para las peticiones
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 1. Health Check (endpoint oficial)
    print("🌐 PRUEBA 1: HEALTH CHECK OFICIAL")
    print("-" * 50)
    try:
        endpoint = "/check"
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   🔍 Estructura: {list(result.keys())}")
                print(f"   ✅ Health Check: Exitoso")
            except json.JSONDecodeError:
                print("   ⚠️ Respuesta no es JSON válido")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 2. Retrieve Documents (endpoint oficial)
    print("📚 PRUEBA 2: RETRIEVE DOCUMENTS OFICIAL")
    print("-" * 50)
    try:
        endpoint = f"/boxes/{box_id}/retrieve-documents"
        data = {"query": "derecho de petición"}
        
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:400]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   🔍 Estructura de respuesta:")
                print(f"      - Keys principales: {list(result.keys())}")
                if "data" in result:
                    print(f"      - Data keys: {list(result['data'].keys())}")
                    if "documents" in result["data"]:
                        docs = result["data"]["documents"]
                        print(f"      - Documentos encontrados: {len(docs)}")
                        if docs and len(docs) > 0:
                            first_doc = docs[0]
                            print(f"      - Primer documento keys: {list(first_doc.keys())}")
                if "success" in result:
                    print(f"      - Success: {result['success']}")
            except json.JSONDecodeError:
                print("   ⚠️ Respuesta no es JSON válido")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 3. List Box Files (endpoint oficial)
    print("📁 PRUEBA 3: LIST BOX FILES OFICIAL")
    print("-" * 50)
    try:
        endpoint = f"/boxes/{box_id}/files"
        
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:400]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   🔍 Estructura de respuesta:")
                print(f"      - Keys principales: {list(result.keys())}")
                if "data" in result:
                    print(f"      - Data keys: {list(result['data'].keys())}")
                    if "files" in result["data"]:
                        files = result["data"]["files"]
                        print(f"      - Archivos encontrados: {len(files)}")
                        if files and len(files) > 0:
                            first_file = files[0]
                            print(f"      - Primer archivo keys: {list(first_file.keys())}")
            except json.JSONDecodeError:
                print("   ⚠️ Respuesta no es JSON válido")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 4. Retrieve Full Documents (endpoint oficial)
    print("📄 PRUEBA 4: RETRIEVE FULL DOCUMENTS OFICIAL")
    print("-" * 50)
    try:
        endpoint = f"/boxes/{box_id}/retrieve-full-documents"
        # Necesitamos file IDs para este endpoint
        data = {"sources": ["sample_file_id"]}  # Placeholder
        
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:400]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   🔍 Estructura de respuesta:")
                print(f"      - Keys principales: {list(result.keys())}")
            except json.JSONDecodeError:
                print("   ⚠️ Respuesta no es JSON válido")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 5. Verificar estructura de respuesta completa
    print("🔍 PRUEBA 5: ANÁLISIS DETALLADO DE RESPUESTA")
    print("-" * 50)
    try:
        endpoint = f"/boxes/{box_id}/retrieve-documents"
        data = {"query": "derecho de petición"}
        
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   📊 ANÁLISIS COMPLETO:")
            print(f"      - Success: {result.get('success')}")
            print(f"      - Data keys: {list(result.get('data', {}).keys())}")
            
            if "data" in result and "documents" in result["data"]:
                documents = result["data"]["documents"]
                print(f"      - Total de grupos de documentos: {len(documents)}")
                
                for i, doc_group in enumerate(documents):
                    print(f"      - Grupo {i+1}: {list(doc_group.keys())}")
                    if "documents" in doc_group:
                        sub_docs = doc_group["documents"]
                        print(f"        - Sub-documentos: {len(sub_docs)}")
                        if sub_docs and len(sub_docs) > 0:
                            first_sub_doc = sub_docs[0]
                            print(f"        - Primer sub-documento: {list(first_sub_doc.keys())}")
            
            if "usage" in result.get("data", {}):
                usage = result["data"]["usage"]
                print(f"      - Usage: {usage}")
                
    except Exception as e:
        print(f"   ❌ Error en análisis: {str(e)}")
    print()

def generate_official_report():
    """Genera un informe basado en la documentación oficial"""
    print("📊 INFORME OFICIAL DE BRAINBOX")
    print("=" * 70)
    print(f"   📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   📚 Documentación: https://app.brainbox.com.co/en/reference/api")
    print()
    
    print("🔗 ENDPOINTS OFICIALES:")
    print("-" * 50)
    print("   ✅ /api/public/v1/check - Health Check (GET)")
    print("   ✅ /api/public/v1/boxes/:box_id/retrieve-documents - Búsqueda semántica (POST)")
    print("   ✅ /api/public/v1/boxes/:box_id/retrieve-full-documents - Documentos completos (POST)")
    print("   ✅ /api/public/v1/boxes/:box_id/files - Lista de archivos (GET)")
    print("   ✅ /api/public/v1/files/:id/signed-url - URL firmada (GET)")
    print()
    
    print("💡 CARACTERÍSTICAS OFICIALES:")
    print("-" * 50)
    print("   • Autenticación: Bearer Token (bbfe_[prefix]_[secret_key])")
    print("   • Unidades de Inteligencia: /retrieve-documents consume 1 unidad")
    print("   • /retrieve-full-documents: GRATIS (0 unidades)")
    print("   • Timeout: 500 segundos para retrieve-documents")
    print("   • Máximo: 50 resultados vectoriales antes del reranking")
    print("   • Score mínimo: 0.1")
    print()
    
    print("⚠️ ENDPOINTS INCORRECTOS QUE ESTABA USANDO:")
    print("-" * 50)
    print("   ❌ /health (debería ser /check)")
    print("   ❌ /boxes/{box_id} (no existe)")
    print("   ❌ /connections/{box_id} (no existe)")
    print("   ❌ /boxes/{box_id}/documents (debería ser /files)")
    print("   ❌ /boxes/{box_id}/search (debería ser /retrieve-documents)")
    print()

if __name__ == "__main__":
    generate_official_report()
    test_brainbox_official_endpoints()
    
    print("🏁 VERIFICACIÓN OFICIAL COMPLETADA")
    print("=" * 70)
    print("💡 RECOMENDACIONES:")
    print("   • Usar solo los endpoints oficiales de la documentación")
    print("   • /check para health check")
    print("   • /retrieve-documents para búsqueda semántica")
    print("   • /files para listar archivos del box")
    print("   • Verificar estructura de respuesta según documentación")

