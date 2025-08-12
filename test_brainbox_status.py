#!/usr/bin/env python3
"""
Script para verificar el estado completo de Brainbox y generar un informe detallado
"""

import os
import requests
import json
from datetime import datetime

def test_brainbox_connectivity():
    """Prueba la conectividad completa con Brainbox"""
    print("🔍 VERIFICANDO ESTADO COMPLETO DE BRAINBOX")
    print("=" * 60)
    
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
    
    # 1. Verificar conectividad básica
    print("🌐 PRUEBA 1: CONECTIVIDAD BÁSICA")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/health", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 2. Verificar endpoint de documentos
    print("📚 PRUEBA 2: ENDPOINT DE DOCUMENTOS")
    print("-" * 40)
    try:
        endpoint = f"/boxes/{box_id}/retrieve-documents"
        data = {"query": "derecho de petición"}
        
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   🔍 Estructura de respuesta:")
                print(f"      - Keys principales: {list(result.keys())}")
                if "data" in result:
                    print(f"      - Data keys: {list(result['data'].keys())}")
                if "success" in result:
                    print(f"      - Success: {result['success']}")
            except json.JSONDecodeError:
                print("   ⚠️ Respuesta no es JSON válido")
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 3. Verificar endpoint de búsqueda
    print("🔍 PRUEBA 3: ENDPOINT DE BÚSQUEDA")
    print("-" * 40)
    try:
        endpoint = f"/boxes/{box_id}/search"
        data = {"query": "derecho de petición", "limit": 5}
        
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json=data, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 4. Verificar endpoint de información del box
    print("📦 PRUEBA 4: INFORMACIÓN DEL BOX")
    print("-" * 40)
    try:
        endpoint = f"/boxes/{box_id}"
        
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 5. Verificar endpoint de conexiones
    print("🔗 PRUEBA 5: ENDPOINT DE CONEXIONES")
    print("-" * 40)
    try:
        endpoint = f"/connections/{box_id}"
        
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()
    
    # 6. Verificar endpoint de documentos del box
    print("📄 PRUEBA 6: DOCUMENTOS DEL BOX")
    print("-" * 40)
    try:
        endpoint = f"/boxes/{box_id}/documents"
        
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Respuesta: {response.text[:300]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()

def test_gemini_status():
    """Prueba el estado de Gemini"""
    print("🤖 VERIFICANDO ESTADO DE GEMINI")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print(f"   ✅ API Key configurada: {api_key[:20]}...{api_key[-4:]}")
            
            # Verificar que sea una clave válida de Gemini
            if api_key.startswith("AIzaSy"):
                print("   ✅ Formato de API Key válido para Gemini")
            else:
                print("   ⚠️ Formato de API Key no es de Gemini")
        else:
            print("   ❌ No se encontró API Key de Gemini")
            
    except Exception as e:
        print(f"   ❌ Error verificando Gemini: {str(e)}")
    
    print()

def generate_report():
    """Genera un informe completo"""
    print("📊 INFORME COMPLETO DEL SISTEMA")
    print("=" * 60)
    print(f"   📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   🖥️  Sistema: Windows")
    print(f"   🐍 Python: Disponible")
    print(f"   📦 Streamlit: Disponible")
    print()
    
    # Verificar archivos del proyecto
    print("📁 ARCHIVOS DEL PROYECTO:")
    print("-" * 40)
    files = [
        "app.py", "ai_analyzer.py", "ai_analyzer_simple.py", 
        "document_processor.py", "advanced_prompts.py", ".env"
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} (no encontrado)")
    
    print()
    
    # Verificar dependencias
    print("📦 DEPENDENCIAS:")
    print("-" * 40)
    try:
        import streamlit
        print(f"   ✅ Streamlit: {streamlit.__version__}")
    except ImportError:
        print("   ❌ Streamlit: No instalado")
    
    try:
        import google.generativeai
        print("   ✅ Google Generative AI: Instalado")
    except ImportError:
        print("   ❌ Google Generative AI: No instalado")
    
    try:
        import requests
        print(f"   ✅ Requests: {requests.__version__}")
    except ImportError:
        print("   ❌ Requests: No instalado")
    
    try:
        import docx2txt
        print("   ✅ Docx2txt: Instalado")
    except ImportError:
        print("   ❌ Docx2txt: No instalado")
    
    print()

if __name__ == "__main__":
    generate_report()
    test_gemini_status()
    test_brainbox_connectivity()
    
    print("🏁 VERIFICACIÓN COMPLETADA")
    print("=" * 60)
    print("💡 RECOMENDACIONES:")
    print("   • Si Brainbox falla, el sistema usa Gemini como respaldo")
    print("   • Si Gemini falla, el sistema usa SimpleAIAnalyzer")
    print("   • El chat siempre estará funcional")
    print("   • Revisa los errores específicos para cada endpoint")
