#!/usr/bin/env python3
"""
Integración con Brainbox API para Retrieval Augmented Generation (RAG)
"""

import requests
import json
from typing import Dict, List, Any, Optional
import streamlit as st

class BrainboxAnalyzer:
    """Analizador que usa Brainbox API con RAG para documentos"""
    
    def __init__(self, api_key: str, connection_id: str):
        self.api_key = api_key
        self.connection_id = connection_id
        self.base_url = "https://api.brainbox.com"  # Ajustar según la URL real de Brainbox
        
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Realiza petición a la API de Brainbox"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en petición a Brainbox: {str(e)}")
    
    def search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca documentos relevantes usando RAG"""
        endpoint = f"/connections/{self.connection_id}/search"
        data = {
            "query": query,
            "limit": limit,
            "include_metadata": True
        }
        
        try:
            result = self._make_request(endpoint, method="POST", data=data)
            return result.get("documents", [])
        except Exception as e:
            st.error(f"Error buscando documentos: {str(e)}")
            return []
    
    def analyze_document_with_rag(self, texto: str, query: str = None) -> Dict[str, Any]:
        """Análisis de documento usando RAG de Brainbox"""
        if not query:
            query = "Analiza este documento legal y proporciona un análisis detallado"
        
        # Buscar documentos relevantes
        relevant_docs = self.search_documents(query)
        
        # Construir prompt con contexto de documentos
        context = self._build_context_from_docs(relevant_docs)
        
        # Prompt para análisis legal
        system_prompt = """Eres un abogado experto en derecho administrativo colombiano con más de 15 años de experiencia. 
        Analiza el documento proporcionado utilizando el contexto legal disponible y proporciona un análisis detallado."""
        
        user_prompt = f"""
DOCUMENTO A ANALIZAR:
{texto[:3000]}

CONTEXTO LEGAL DISPONIBLE:
{context}

INSTRUCCIONES:
- Proporciona un análisis integral del documento
- Identifica el tipo de documento y su propósito
- Analiza la estructura formal y legal
- Evalúa la fundamentación jurídica
- Identifica fortalezas y áreas de mejora
- Utiliza el contexto legal disponible para enriquecer tu análisis

Responde en formato JSON estructurado.
        """.strip()
        
        # Llamada a Brainbox para análisis
        return self._generate_analysis(system_prompt, user_prompt)
    
    def detect_problems_with_rag(self, texto: str, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detección de problemas usando RAG"""
        query = "Identifica problemas legales y formales en este documento"
        relevant_docs = self.search_documents(query)
        context = self._build_context_from_docs(relevant_docs)
        
        system_prompt = """Eres un abogado revisor especializado en derecho administrativo colombiano. 
        Identifica problemas legales, formales y de procedimiento en el documento."""
        
        user_prompt = f"""
DOCUMENTO:
{texto[:3000]}

CONTEXTO LEGAL:
{context}

ANÁLISIS PREVIO:
{json.dumps(contexto, indent=2, ensure_ascii=False)}

INSTRUCCIONES:
Identifica problemas específicos en formato JSON con:
- tipo: FORMAL, LEGAL, PROCEDIMENTAL
- descripcion: Descripción detallada del problema
- severidad: ALTA, MEDIA, BAJA
- fundamento_legal: Base legal del problema
- recomendacion: Cómo solucionarlo
        """.strip()
        
        return self._generate_problems_analysis(system_prompt, user_prompt)
    
    def generate_recommendations_with_rag(self, texto: str, problemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generación de recomendaciones usando RAG"""
        query = "Genera recomendaciones para mejorar este documento legal"
        relevant_docs = self.search_documents(query)
        context = self._build_context_from_docs(relevant_docs)
        
        system_prompt = """Eres un abogado redactor especializado en derecho administrativo colombiano. 
        Genera recomendaciones específicas y accionables para mejorar el documento."""
        
        user_prompt = f"""
DOCUMENTO:
{texto[:2000]}

PROBLEMAS IDENTIFICADOS:
{json.dumps(problemas, indent=2, ensure_ascii=False)}

CONTEXTO LEGAL:
{context}

INSTRUCCIONES:
Genera recomendaciones en formato JSON con:
- titulo: Título de la recomendación
- descripcion: Descripción detallada
- prioridad: ALTA, MEDIA, BAJA
- accion: Acción específica a realizar
- fundamento_legal: Base legal
- tiempo_estimado: Tiempo para implementar
- recursos_necesarios: Recursos requeridos
- impacto_esperado: Beneficio esperado
        """.strip()
        
        return self._generate_recommendations_analysis(system_prompt, user_prompt)
    
    def chat_response_with_rag(self, pregunta: str, contexto: Dict[str, Any]) -> str:
        """Respuesta de chat usando RAG de Brainbox"""
        # Buscar documentos relevantes a la pregunta
        relevant_docs = self.search_documents(pregunta)
        context = self._build_context_from_docs(relevant_docs)
        
        system_prompt = """Eres un asistente legal especializado en derecho administrativo colombiano. 
        Responde de manera profesional, clara y útil utilizando el contexto legal disponible."""
        
        user_prompt = f"""
PREGUNTA: {pregunta}

CONTEXTO DISPONIBLE:
- Análisis: {str(contexto.get('analisis', 'No disponible'))}
- Problemas: {str(contexto.get('problemas', 'No disponibles'))}
- Recomendaciones: {str(contexto.get('recomendaciones', 'No disponibles'))}

CONTEXTO LEGAL RELEVANTE:
{context}

Responde de manera completa y útil, utilizando tanto el contexto del análisis como el contexto legal disponible.
        """.strip()
        
        return self._generate_chat_response(system_prompt, user_prompt)
    
    def _build_context_from_docs(self, documents: List[Dict]) -> str:
        """Construye contexto a partir de documentos recuperados"""
        if not documents:
            return "No hay documentos relevantes disponibles."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "Documento")
            
            context_parts.append(f"Documento {i} ({source}):\n{content[:500]}...")
        
        return "\n\n".join(context_parts)
    
    def _generate_analysis(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Genera análisis usando Brainbox"""
        endpoint = f"/connections/{self.connection_id}/generate"
        data = {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "model": "brainbox-legal",  # Ajustar según el modelo disponible
            "max_tokens": 4000,
            "temperature": 0.2
        }
        
        try:
            result = self._make_request(endpoint, method="POST", data=data)
            response_text = result.get("response", "")
            
            # Intentar parsear JSON
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Si no es JSON válido, crear estructura básica
                return {
                    "tipo_documento": "Análisis generado",
                    "resumen": response_text[:500],
                    "analisis_detallado": response_text,
                    "confianza": 0.8
                }
                
        except Exception as e:
            st.error(f"Error generando análisis: {str(e)}")
            return {"error": str(e)}
    
    def _generate_problems_analysis(self, system_prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
        """Genera análisis de problemas"""
        result = self._generate_analysis(system_prompt, user_prompt)
        
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and "error" not in result:
            # Intentar extraer problemas del análisis
            return [{"descripcion": "Problema identificado", "tipo": "ANALISIS", "severidad": "MEDIA"}]
        else:
            return []
    
    def _generate_recommendations_analysis(self, system_prompt: str, user_prompt: str) -> List[Dict[str, Any]]:
        """Genera análisis de recomendaciones"""
        result = self._generate_analysis(system_prompt, user_prompt)
        
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and "error" not in result:
            # Intentar extraer recomendaciones del análisis
            return [{"titulo": "Recomendación general", "descripcion": "Mejorar documento", "prioridad": "MEDIA"}]
        else:
            return []
    
    def _generate_chat_response(self, system_prompt: str, user_prompt: str) -> str:
        """Genera respuesta de chat"""
        result = self._generate_analysis(system_prompt, user_prompt)
        
        if isinstance(result, dict) and "error" in result:
            return f"Lo siento, hubo un error: {result['error']}"
        elif isinstance(result, str):
            return result
        else:
            return str(result)

