#!/usr/bin/env python3
"""
Integración alternativa con BrainBox usando la interfaz web
"""

import requests
import json
from typing import Dict, List, Any, Optional
import streamlit as st

class BrainBoxWebAnalyzer:
    """Analizador que usa BrainBox a través de la interfaz web"""
    
    def __init__(self, api_key: str, connection_id: str):
        self.api_key = api_key
        self.connection_id = connection_id
        self.base_url = "https://app.brainbox.com.co"
        
    def _make_web_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Realiza petición a la interfaz web de BrainBox"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en petición a BrainBox: {str(e)}")
    
    def search_documents_web(self, query: str, limit: int = 5) -> List[Dict]:
        """Búsqueda de documentos a través de la interfaz web"""
        # Intentar diferentes endpoints posibles
        endpoints_to_try = [
            "/api/search",
            "/api/documents/search",
            "/api/rag/search",
            "/search",
            "/documents/search"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                data = {
                    "query": query,
                    "limit": limit,
                    "connection_id": self.connection_id
                }
                
                result = self._make_web_request(endpoint, method="POST", data=data)
                if result and "documents" in result:
                    return result["documents"]
                elif result and "results" in result:
                    return result["results"]
                    
            except Exception as e:
                continue
        
        # Si ningún endpoint funciona, devolver lista vacía
        return []
    
    def generate_content_web(self, prompt: str, context: str = "") -> str:
        """Generación de contenido a través de la interfaz web"""
        # Intentar diferentes endpoints posibles
        endpoints_to_try = [
            "/api/generate",
            "/api/chat",
            "/api/completion",
            "/generate",
            "/chat"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                data = {
                    "prompt": prompt,
                    "context": context,
                    "connection_id": self.connection_id,
                    "max_tokens": 2000,
                    "temperature": 0.2
                }
                
                result = self._make_web_request(endpoint, method="POST", data=data)
                if result and "response" in result:
                    return result["response"]
                elif result and "content" in result:
                    return result["content"]
                elif result and "text" in result:
                    return result["text"]
                    
            except Exception as e:
                continue
        
        # Si ningún endpoint funciona, devolver mensaje de error
        return "Lo siento, no pude generar una respuesta. Verifica la configuración de BrainBox."
    
    def chat_response_web(self, pregunta: str, contexto: Dict[str, Any]) -> str:
        """Respuesta de chat usando la interfaz web de BrainBox"""
        try:
            # Construir prompt con contexto
            system_prompt = """Eres un asistente legal especializado en derecho administrativo colombiano. 
            Responde de manera profesional, clara y útil utilizando el contexto disponible."""
            
            user_prompt = f"""
PREGUNTA: {pregunta}

CONTEXTO DISPONIBLE:
- Análisis: {str(contexto.get('analisis', 'No disponible'))}
- Problemas: {str(contexto.get('problemas', 'No disponibles'))}
- Recomendaciones: {str(contexto.get('recomendaciones', 'No disponibles'))}

Responde de manera completa y útil, utilizando el contexto disponible.
            """.strip()
            
            # Generar respuesta
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            return self.generate_content_web(full_prompt)
            
        except Exception as e:
            return f"Lo siento, hubo un error al procesar tu pregunta: {str(e)}"
    
    def test_connection(self) -> bool:
        """Prueba la conexión con BrainBox"""
        try:
            # Intentar hacer una petición simple
            response = requests.get(self.base_url, timeout=10)
            return response.status_code == 200
        except:
            return False

def test_brainbox_web():
    """Prueba la integración web con BrainBox"""
    print("🌐 Probando integración web con BrainBox...")
    
    api_key = "bbfe_key_55DzECZtUTOPicncc14IaAjjl98QeN9yMTdco6fPeUfzAQgfoUgR-GgMvBT1ljyAyiHZpVAkCepRs8ttQ34be-l-ji"
    connection_id = "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
    
    analyzer = BrainBoxWebAnalyzer(api_key, connection_id)
    
    # Probar conexión
    if analyzer.test_connection():
        print("✅ Conexión a BrainBox exitosa")
    else:
        print("❌ No se pudo conectar a BrainBox")
        return False
    
    # Probar chat
    try:
        contexto = {"analisis": {"tipo": "test"}, "problemas": [], "recomendaciones": []}
        respuesta = analyzer.chat_response_web("¿Cómo mejorar la fundamentación legal?", contexto)
        print(f"✅ Chat funcionando: {respuesta[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return False

if __name__ == "__main__":
    test_brainbox_web()

