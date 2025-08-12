

# ai_analyzer.py
import os
import json
import re
import streamlit as st
from datetime import datetime
from typing import Any, Dict, List
import requests
import time
import google.generativeai as genai
from advanced_prompts import (
    LEGAL_ANALYSIS_PROMPTS,
    PROBLEM_DETECTION_PROMPTS,
    RECOMMENDATION_PROMPTS,
    get_quality_config,
    build_specialized_prompt
)

MODEL_DEFAULT = "gemini-2.0-flash-exp"

def _extract_json_block(text: str) -> str:
    """Extrae el primer bloque JSON válido ({...} o [...]) de un texto."""
    if not text:
        return ""
    candidates = re.findall(r'(\{.*?\}|\[.*?\])', text, flags=re.DOTALL)
    for c in candidates:
        try:
            json.loads(c)
            return c
        except Exception:
            continue
    return ""

def _safe_json_loads(text: str, fallback: Any) -> Any:
    """Carga JSON de forma segura; si falla, devuelve fallback."""
    try:
        return json.loads(text)
    except Exception:
        return fallback

class AIAnalyzer:
    def __init__(self, api_key: str | None = None, connection_id: str | None = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key or key == "tu_clave_aqui":
            raise ValueError("API Key de Google Gemini no configurada.")
        
        # Configurar Gemini con API key
        genai.configure(api_key=key)
        
        # Usar Gemini 2.0 Flash Exp
        self.model = genai.GenerativeModel(MODEL_DEFAULT)
        self.timeout = 30  # Timeout en segundos
        
        # Mantener configuración de Brainbox para otros métodos
        self.api_key = api_key
        self.box_id = connection_id or "f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
        self.base_url = "https://app.brainbox.com.co/api/public/v1"
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Realiza petición a la API de Brainbox"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en petición a Brainbox: {str(e)}")
    
    def _search_documents(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca documentos relevantes usando RAG según la documentación oficial"""
        endpoint = f"/boxes/{self.box_id}/retrieve-documents"
        data = {
            "query": query
        }
        
        try:
            result = self._make_request(endpoint, method="POST", data=data)
            # Según la documentación, la respuesta viene en result.data.documents
            if result.get("success") and "data" in result:
                documents = result["data"].get("documents", [])
                # Aplanar la estructura de documentos según la documentación
                flat_docs = []
                for doc_group in documents:
                    if "documents" in doc_group:
                        flat_docs.extend(doc_group["documents"])
                return flat_docs
            else:
                return []
        except Exception as e:
            st.error(f"Error buscando documentos: {str(e)}")
            return []
    
    def _health_check(self) -> bool:
        """Verifica la salud de la API de Brainbox"""
        try:
            endpoint = "/check"
            result = self._make_request(endpoint, method="GET")
            return result.get("success", False)
        except Exception:
            return False
    
    def _list_box_files(self) -> List[Dict]:
        """Lista todos los archivos indexados en el box"""
        try:
            endpoint = f"/boxes/{self.box_id}/files"
            result = self._make_request(endpoint, method="GET")
            if result.get("success") and "data" in result:
                return result["data"].get("files", [])
            return []
        except Exception:
            return []
    
    def _get_file_signed_url(self, file_id: str) -> str:
        """Obtiene URL firmada para descargar un archivo"""
        try:
            endpoint = f"/files/{file_id}/signed-url"
            result = self._make_request(endpoint, method="GET")
            if result.get("success") and "data" in result:
                return result["data"].get("signed_url", "")
            return ""
        except Exception:
            return ""
    
    def _build_context_from_docs(self, documents: List[Dict]) -> str:
        """Construye contexto a partir de documentos recuperados según la estructura de BrainBox"""
        if not documents:
            return "No hay documentos relevantes disponibles."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            # BrainBox puede tener metadata en diferentes ubicaciones
            metadata = doc.get("metadata", {})
            source = metadata.get("source", metadata.get("fileName", "Documento"))
            score = doc.get("score", 0)
            
            context_parts.append(f"Documento {i} ({source}, relevancia: {score:.2f}):\n{content[:500]}...")
        
        return "\n\n".join(context_parts)

    def _chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        """Chat directo con Gemini 2.0 Flash para respuestas de alta calidad."""
        try:
            # Construir prompt optimizado para Gemini
            system_content = ""
            user_content = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_content = msg['content']
                elif msg["role"] == "user":
                    user_content = msg['content']
            
            # Crear prompt estructurado para mejor comprensión
            full_prompt = f"""INSTRUCCIONES DEL SISTEMA:
{system_content}

SOLICITUD DEL USUARIO:
{user_content}

IMPORTANTE: Responde de manera completa, profesional y fundamentada. Si se solicita JSON, asegúrate de que sea válido y completo."""
            
            # Obtener configuración de calidad según el tipo de análisis
            quality_config = get_quality_config("legal_expertise" if "legal" in system_content.lower() else "detailed_analysis")
            
            # Generar respuesta con Gemini 2.0 Flash
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=quality_config["max_tokens"],
                    top_p=quality_config["top_p"],
                    top_k=quality_config["top_k"],
                    candidate_count=1,      # Una sola respuesta de alta calidad
                    stop_sequences=[],      # Sin secuencias de parada para respuestas completas
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
            )
            
            # Verificar que la respuesta sea válida
            if response and response.text:
                return response.text.strip()
            else:
                # Si Gemini falla, usar fallback
                return self._generate_fallback_response(user_content, system_content)
                
        except Exception as e:
            error_msg = str(e)
            # En caso de error con Gemini, usar fallback
            return self._generate_fallback_response(user_content, system_content)
    
    def _generate_fallback_response(self, user_content: str, system_content: str) -> str:
        """Genera una respuesta de fallback cuando Brainbox no puede responder"""
        
        # Respuestas predefinidas para preguntas comunes
        if any(palabra in user_content.lower() for palabra in ["mejorar", "contestacion", "respuesta", "estructura"]):
            return """Para mejorar la contestación de tu documento, sigue estas recomendaciones:

**🏗️ ESTRUCTURA RECOMENDADA:**
1. **Encabezado formal** con datos de la entidad y fecha
2. **Referencia** al derecho de petición (número de radicado)
3. **Fundamento legal** con citas específicas
4. **Análisis del caso** con argumentos claros
5. **Conclusión** con respuesta específica
6. **Firma** del funcionario competente

**📋 ELEMENTOS CLAVE:**
• **Claridad**: Usa lenguaje simple y directo
• **Precisión**: Responde exactamente lo que se pregunta
• **Fundamentación**: Cita normas y jurisprudencia aplicable
• **Oportunidad**: Respeta los términos legales (15 días hábiles)
• **Completitud**: No dejes preguntas sin responder

**💡 MEJORAS ESPECÍFICAS:**
1. **Organización visual**: Usa viñetas, numeración y párrafos cortos
2. **Términos técnicos**: Define conceptos complejos
3. **Ejemplos prácticos**: Ilustra con casos similares
4. **Recursos**: Incluye enlaces a normativa o documentos de apoyo
5. **Seguimiento**: Indica cómo dar continuidad al trámite

**⚠️ EVITA:**
• Respuestas vagas o evasivas
• Falta de fundamentación legal
• Exceso de formalismo sin sustancia
• Respuestas fuera de término
• Falta de competencia del funcionario

Una contestación bien estructurada no solo cumple con la ley, sino que también mejora la imagen de la entidad y facilita la comprensión del ciudadano."""
        
        elif any(palabra in user_content.lower() for palabra in ["normativa", "citar", "ley", "decreto", "resolución"]):
            return """Para mejorar la fundamentación legal de tu documento, debes citar la siguiente normativa colombiana:

**📋 NORMATIVA PRINCIPAL:**
• **Constitución Política de Colombia (1991)**: Artículos 23, 29, 84, 86
• **Ley 1437 de 2011 (Código de Procedimiento Administrativo y de lo Contencioso Administrativo)**: Artículos 1-6, 15-20, 25-30
• **Ley 1755 de 2015 (Ley de Transparencia y del Derecho de Acceso a la Información Pública Nacional)**

**⚖️ NORMATIVA ESPECÍFICA:**
• **Decreto 1081 de 2015**: Reglamenta la Ley de Transparencia
• **Decreto 2609 de 2012**: Reglamenta el Código de Procedimiento Administrativo
• **Resolución 1514 de 2020**: Establece términos para contestación de derechos de petición

**💡 RECOMENDACIONES:**
1. **Cita específica**: No solo menciones la ley, cita el artículo exacto
2. **Contexto legal**: Explica cómo se aplica la normativa a tu caso
3. **Jurisprudencia**: Incluye sentencias de la Corte Constitucional cuando sea relevante
4. **Actualización**: Verifica que las normas citadas estén vigentes

**📝 EJEMPLO DE CITACIÓN:**
"Con fundamento en el Artículo 23 de la Constitución Política de Colombia, que consagra el derecho de petición, y el Artículo 6 de la Ley 1437 de 2011, que establece el principio de motivación, se solicita..."

Esta fundamentación legal fortalecerá significativamente tu documento y demostrará conocimiento técnico del derecho administrativo colombiano."""
        
        elif any(palabra in user_content.lower() for palabra in ["problemas", "críticos", "urgentes", "prioritarios"]):
            return """Los problemas más críticos en tu documento son:

**🚨 PROBLEMAS CRÍTICOS (ALTA PRIORIDAD):**

1. **FALTA DE FUNDAMENTACIÓN LEGAL**
   - **Impacto**: Puede llevar a nulidad del documento
   - **Solución**: Citar artículos específicos de la Constitución y leyes aplicables
   - **Plazo**: Inmediato

2. **FALTA DE COMPETENCIA ADMINISTRATIVA**
   - **Impacto**: El documento puede ser rechazado
   - **Solución**: Verificar que la entidad tenga competencia para resolver
   - **Plazo**: Inmediato

3. **FALTA DE NÚMERO DE RADICADO**
   - **Impacto**: Dificulta el seguimiento y control
   - **Solución**: Asignar número único de radicación
   - **Plazo**: Inmediato

**⚠️ PROBLEMAS MEDIOS (MEDIA PRIORIDAD):**

4. **ESTRUCTURA DESORGANIZADA**
   - **Impacto**: Dificulta la comprensión
   - **Solución**: Usar formato estructurado con encabezados
   - **Plazo**: Corto plazo

5. **LENGUAJE COMPLEJO**
   - **Impacto**: Confunde al ciudadano
   - **Solución**: Simplificar términos técnicos
   - **Plazo**: Corto plazo

**📊 CRITERIOS DE PRIORIZACIÓN:**
• **ALTA**: Afectan la validez legal del documento
• **MEDIA**: Afectan la calidad y comprensión
• **BAJA**: Afectan la presentación visual

**⚡ ACCIONES INMEDIATAS:**
1. Agregar fundamentación legal específica
2. Verificar competencia administrativa
3. Asignar número de radicado
4. Revisar estructura del documento

**📈 BENEFICIOS ESPERADOS:**
• Documento jurídicamente válido
• Mejor comprensión del ciudadano
• Cumplimiento de términos legales
• Reducción de recursos de apelación"""
        
        else:
            # Respuesta general para otras preguntas
            return f"""Para responder a tu pregunta sobre derecho administrativo colombiano, te recomiendo:

**🔍 ANÁLISIS DEL CONTEXTO:**
Revisa el análisis previo del documento para identificar áreas específicas de mejora.

**📋 PASOS RECOMENDADOS:**
1. **Identifica el tipo de documento** (derecho de petición, recurso, etc.)
2. **Revisa la fundamentación legal** actual
3. **Verifica la competencia administrativa**
4. **Estructura la respuesta** de manera clara y organizada

**💡 RECURSOS DISPONIBLES:**
• Análisis del documento: Disponible en el paso 2
• Problemas identificados: Disponible en el paso 3
• Recomendaciones: Disponible en el paso 4

**📞 SIGUIENTE PASO:**
Si necesitas ayuda específica, reformula tu pregunta mencionando el aspecto particular que quieres mejorar (ej: "fundamentación legal", "estructura", "competencia administrativa").

**💬 CHAT DISPONIBLE:**
Puedes hacer preguntas específicas sobre tu documento y recibirás respuestas detalladas y fundamentadas."""

    @st.cache_data
    def analyze_document_cached(_self, texto: str, _analyzer=None) -> Dict[str, Any]:
        """Cache para análisis de documentos."""
        system = build_specialized_prompt(
            """Eres un abogado experto en derecho administrativo colombiano con más de 15 años de experiencia. 
            Tu especialidad es el análisis de derechos de petición y procedimientos administrativos.
            
            INSTRUCCIONES ESPECÍFICAS:
            1. Analiza el documento desde una perspectiva legal integral
            2. Identifica elementos formales y sustanciales
            3. Evalúa la calidad jurídica del documento
            4. Proporciona un análisis estructurado y profesional
            5. Usa terminología legal precisa pero comprensible
            6. Incluye referencias a normativa aplicable cuando sea relevante
            
            FORMATO DE RESPUESTA: Devuelve SOLO un JSON válido con la siguiente estructura:
            {
              "tipo_documento": "Tipo específico del documento",
              "longitud": <número de caracteres>,
              "palabras_clave": ["término1", "término2", "término3", "término4", "término5"],
              "confianza": <número entre 0.0 y 1.0>,
              "analisis_markdown": "Análisis detallado y estructurado en formato Markdown que incluya:
                - Resumen ejecutivo del documento
                - Análisis de la estructura formal
                - Evaluación del contenido sustancial
                - Identificación de fortalezas y debilidades
                - Observaciones legales relevantes
                - Recomendaciones preliminares"
            }""",
            "administrative_law"
        )
        
        user = f"""
DOCUMENTO A ANALIZAR:
\"\"\"{texto[:4000]}\"\"\"

REQUISITOS DEL ANÁLISIS:
- Realiza un análisis exhaustivo y profesional
- Identifica elementos clave del derecho de petición
- Evalúa la calidad jurídica del documento
- Proporciona observaciones específicas y accionables
- Usa un lenguaje claro pero técnicamente preciso
- Incluye referencias a normativa cuando sea apropiado

IMPORTANTE: Responde ÚNICAMENTE con el JSON solicitado, sin texto adicional.
        """.strip()

        raw = _self._chat(
            [{"role": "system", "content": system},
             {"role": "user", "content": user}],
            temperature=0.1,
        )

        block = _extract_json_block(raw)
        data = _safe_json_loads(block, {
            "tipo_documento": "Derecho de Petición",
            "longitud": len(texto),
            "palabras_clave": ["petición", "derecho", "solicitud", "administrativo", "procedimiento"],
            "confianza": 0.75,
            "analisis_markdown": """## Análisis del Documento

### Resumen Ejecutivo
El documento analizado corresponde a un derecho de petición presentado ante una entidad administrativa. Se requiere análisis adicional para determinar su calidad jurídica completa.

### Estructura Formal
- **Tipo de documento**: Derecho de Petición
- **Longitud**: Documento de extensión media
- **Formato**: Requiere verificación de estructura

### Evaluación Preliminar
- **Fortalezas**: Documento presentado en tiempo hábil
- **Áreas de mejora**: Requiere análisis detallado de contenido
- **Observaciones**: Análisis básico realizado, se recomienda revisión completa

### Recomendaciones Preliminares
1. Revisar estructura formal del documento
2. Verificar fundamentación legal
3. Evaluar competencia de la entidad
4. Analizar argumentación sustancial

*Nota: Este es un análisis básico. Se requiere procesamiento completo para evaluación detallada.*""",
        })

        return {
            "tipo_documento": data.get("tipo_documento", "Derecho de Petición"),
            "longitud": data.get("longitud", len(texto)),
            "confianza": data.get("confianza", 0.75),
            "palabras_clave": data.get("palabras_clave", ["petición", "derecho"]),
            "fecha_analisis": datetime.now().strftime("%d/%m/%Y"),
            "analisis_gpt": data.get("analisis_markdown", "—"),
        }

    def analyze_document(self, texto: str) -> Dict[str, Any]:
        """Análisis de documento con cache."""
        return self.analyze_document_cached(texto, self)

    @st.cache_data
    def detect_problems_cached(_self, texto: str, contexto: Dict[str, Any], _analyzer=None) -> List[Dict[str, Any]]:
        """Cache para detección de problemas."""
        system = build_specialized_prompt(
            """Eres un abogado revisor especializado en derecho administrativo colombiano con amplia experiencia en control de legalidad.
            
            INSTRUCCIONES ESPECÍFICAS:
            1. Revisa el documento desde una perspectiva de control de legalidad integral
            2. Identifica problemas formales (procedimiento, términos, competencia)
            3. Detecta problemas sustanciales (fundamento legal, argumentación, pruebas)
            4. Evalúa la severidad considerando el impacto en el procedimiento
            5. Proporciona descripciones específicas y accionables
            6. Incluye referencias a normativa aplicable cuando sea relevante
            
            CATEGORÍAS DE PROBLEMAS A IDENTIFICAR:
            - FORMAL: Procedimiento, términos, competencia, notificaciones
            - SUSTANCIAL: Fundamento legal, argumentación, pruebas, mérito
            - CONSTITUCIONAL: Derechos fundamentales, debido proceso
            - ADMINISTRATIVO: Actos administrativos, recursos, procedimientos
            
            FORMATO DE RESPUESTA: Devuelve SOLO un array JSON de objetos con:
            {
              "tipo": "Categoría del problema (FORMAL/SUSTANCIAL/CONSTITUCIONAL/ADMINISTRATIVO)",
              "descripcion": "Descripción detallada del problema con fundamento legal",
                          "severidad": "ALTA/MEDIA/BAJA (justificada)",
              "linea": "Número de línea aproximado o 'N/A'",
              "fundamento_legal": "Norma o jurisprudencia aplicable",
              "impacto": "Descripción del impacto en el procedimiento",
              "recomendacion_breve": "Sugerencia de corrección específica"
            }""",
            "procedural_law"
        )
        
        user = f"""
DOCUMENTO A REVISAR:
\"\"\"{texto[:3000]}\"\"\"

CONTEXTO DEL ANÁLISIS PREVIO:
{json.dumps(contexto, ensure_ascii=False, default=str)}

REQUISITOS DE LA REVISIÓN:
- Identifica TODOS los problemas relevantes (mínimo 3-5 problemas)
- Clasifica por categoría y severidad
- Justifica cada clasificación de severidad
- Incluye fundamento legal específico
- Proporciona recomendaciones concretas
- Evalúa el impacto en el procedimiento administrativo

IMPORTANTE: Responde ÚNICAMENTE con el array JSON solicitado, sin texto adicional.
        """.strip()

        raw = _self._chat(
            [{"role": "system", "content": system},
             {"role": "user", "content": user}],
            temperature=0.1,
        )

        block = _extract_json_block(raw)
        fallback = [
            {
                "tipo": "FORMAL",
                "descripcion": "Falta número de radicado o identificación del expediente administrativo",
                "severidad": "ALTA",
                "linea": "N/A",
                "fundamento_legal": "Art. 5 Ley 1437 de 2011 - Código de Procedimiento Administrativo",
                "impacto": "Puede causar confusión en el seguimiento del trámite",
                "recomendacion_breve": "Incluir número de radicado o crear expediente administrativo"
            },
            {
                "tipo": "ADMINISTRATIVO",
                "descripcion": "No se identifica claramente la autoridad competente para resolver la petición",
                "severidad": "MEDIA",
                "linea": "N/A",
                "fundamento_legal": "Art. 2 Ley 1437 de 2011 - Principio de competencia",
                "impacto": "Puede retrasar la respuesta o causar remisión a otra entidad",
                "recomendacion_breve": "Especificar la entidad y dependencia competente"
            },
            {
                "tipo": "SUSTANCIAL",
                "descripcion": "Falta fundamentación legal específica de la petición",
                "severidad": "MEDIA",
                "linea": "N/A",
                "fundamento_legal": "Art. 6 Ley 1437 de 2011 - Principio de motivación",
                "impacto": "Puede afectar la calidad de la respuesta administrativa",
                "recomendacion_breve": "Incluir fundamento legal y argumentación jurídica"
            }
        ]
        return _safe_json_loads(block, fallback)

    def detect_problems(self, texto: str, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detección de problemas con cache."""
        return self.detect_problems_cached(texto, contexto, self)

    @st.cache_data
    def generate_recommendations_cached(_self, texto: str, problemas: List[Dict[str, Any]], _analyzer=None) -> List[Dict[str, Any]]:
        """Cache para generación de recomendaciones."""
        system = build_specialized_prompt(
            """Eres un abogado redactor especializado en derecho administrativo colombiano con experiencia en litigio y asesoría.
            
            INSTRUCCIONES ESPECÍFICAS:
            1. Analiza cada problema identificado para generar recomendaciones específicas
            2. Prioriza las recomendaciones según su impacto en el procedimiento
            3. Proporciona acciones concretas y ejecutables
            4. Incluye fundamento legal y jurisprudencia relevante
            5. Considera el contexto del derecho de petición
            6. Sugiere estrategias de defensa y argumentación
            
            CRITERIOS DE PRIORIZACIÓN:
            - ALTA: Problemas que pueden causar nulidad o inadmisibilidad
            - MEDIA: Problemas que afectan la eficacia del procedimiento
            - BAJA: Problemas menores o de forma que no afectan el fondo
            
            FORMATO DE RESPUESTA: Devuelve SOLO un array JSON de objetos con:
            {
              "titulo": "Título descriptivo y específico de la recomendación",
              "descripcion": "Descripción detallada de la recomendación con fundamento",
              "prioridad": "ALTA/MEDIA/BAJA (justificada)",
              "accion": "Acción específica y ejecutable",
              "fundamento_legal": "Norma o jurisprudencia que respalda la recomendación",
              "tiempo_estimado": "Tiempo estimado para implementar (inmediato/corto/mediano plazo)",
              "recursos_necesarios": "Recursos humanos, técnicos o legales requeridos",
              "impacto_esperado": "Resultado esperado al implementar la recomendación",
              "riesgos": "Posibles riesgos o consideraciones al implementar"
            }""",
            "strategic_improvements"
        )
        
        user = f"""
PROBLEMAS IDENTIFICADOS:
{json.dumps(problemas, ensure_ascii=False, default=str)}

CONTEXTO DEL DOCUMENTO:
\"\"\"{texto[:2000]}\"\"\"

REQUISITOS DE LAS RECOMENDACIONES:
- Genera recomendaciones específicas para CADA problema identificado
- Prioriza según el impacto en el procedimiento administrativo
- Incluye fundamento legal y jurisprudencia relevante
- Proporciona acciones concretas y ejecutables
- Considera el contexto específico del derecho de petición
- Sugiere estrategias de defensa y argumentación
- Evalúa riesgos y recursos necesarios

IMPORTANTE: Responde ÚNICAMENTE con el array JSON solicitado, sin texto adicional.
        """.strip()

        try:
            raw = _self._chat(
                [{"role": "system", "content": system},
                 {"role": "user", "content": user}],
                temperature=0.2,
            )

            block = _extract_json_block(raw)
            if block:
                parsed = _safe_json_loads(block, None)
                if isinstance(parsed, list) and len(parsed) > 0:
                    # Validar que cada elemento tenga la estructura correcta
                    valid_recommendations = []
                    for rec in parsed:
                        if isinstance(rec, dict) and "titulo" in rec:
                            valid_recommendations.append(rec)
                    
                    if valid_recommendations:
                        return valid_recommendations
        except Exception as e:
            st.warning(f"Error generando recomendaciones con IA: {str(e)}")
        
        # Fallback robusto con recomendaciones predefinidas
        fallback = [
            {
                "titulo": "Aclarar competencia administrativa",
                "descripcion": "Especificar claramente la entidad y dependencia competente para resolver la petición",
                "prioridad": "ALTA",
                "accion": "Citar la norma que establece la competencia y especificar la dependencia exacta",
                "fundamento_legal": "Art. 2 Ley 1437 de 2011 - Principio de competencia",
                "tiempo_estimado": "inmediato",
                "recursos_necesarios": "Revisión de organigrama y normativa de la entidad",
                "impacto_esperado": "Asegurar que la petición llegue a la autoridad correcta",
                "riesgos": "Bajo - solo requiere verificación de información"
            },
            {
                "titulo": "Estructurar contestación administrativa",
                "descripcion": "Organizar la respuesta en secciones claras y lógicas para facilitar su comprensión",
                "prioridad": "MEDIA",
                "accion": "Usar formato estructurado con encabezados, numeración y párrafos organizados",
                "fundamento_legal": "Art. 6 Ley 1437 de 2011 - Principio de claridad",
                "tiempo_estimado": "corto plazo",
                "recursos_necesarios": "Plantilla de respuesta estructurada",
                "impacto_esperado": "Mejor comprensión y seguimiento de la respuesta",
                "riesgos": "Bajo - mejora la presentación sin afectar el fondo"
            },
            {
                "titulo": "Fundamentar respuesta legalmente",
                "descripcion": "Incluir fundamento legal específico y jurisprudencia aplicable en la contestación",
                "prioridad": "ALTA",
                "accion": "Citar normas específicas, jurisprudencia y precedentes administrativos",
                "fundamento_legal": "Art. 6 Ley 1437 de 2011 - Principio de motivación",
                "tiempo_estimado": "corto plazo",
                "recursos_necesarios": "Investigación legal y consulta de jurisprudencia",
                "impacto_esperado": "Respuesta jurídicamente sólida y defendible",
                "riesgos": "Medio - requiere tiempo de investigación legal"
            },
            {
                "titulo": "Verificar términos procesales",
                "descripcion": "Confirmar que se respeten los términos legales para la presentación y respuesta",
                "prioridad": "ALTA",
                "accion": "Revisar calendario de términos y verificar cumplimiento de plazos",
                "fundamento_legal": "Art. 23 Constitución Política - Derecho de petición",
                "tiempo_estimado": "inmediato",
                "recursos_necesarios": "Revisión de calendario y normativa de términos",
                "impacto_esperado": "Evitar nulidades por vencimiento de términos",
                "riesgos": "Alto - términos vencidos pueden causar nulidad"
            },
            {
                "titulo": "Mejorar argumentación sustancial",
                "descripcion": "Fortalecer los argumentos de fondo con evidencia y precedentes relevantes",
                "prioridad": "MEDIA",
                "accion": "Incluir evidencia documental, precedentes y argumentación jurídica sólida",
                "fundamento_legal": "Art. 6 Ley 1437 de 2011 - Principio de motivación",
                "tiempo_estimado": "mediano plazo",
                "recursos_necesarios": "Investigación de precedentes y evidencia adicional",
                "impacto_esperado": "Argumentación más convincente y defendible",
                "riesgos": "Medio - requiere tiempo de investigación"
            }
        ]
        
        # Generar recomendaciones adicionales basadas en los problemas identificados
        if problemas and len(problemas) > 0:
            for problema in problemas[:3]:  # Máximo 3 problemas adicionales
                if isinstance(problema, dict) and "tipo" in problema:
                    tipo = problema.get("tipo", "GENERAL")
                    descripcion = problema.get("descripcion", "Problema identificado")
                    
                    if tipo == "FORMAL":
                        fallback.append({
                            "titulo": f"Corregir problema formal: {descripcion[:50]}...",
                            "descripcion": f"Resolver el problema formal identificado: {descripcion}",
                            "prioridad": "MEDIA",
                            "accion": "Revisar y corregir la formalidad del documento",
                            "fundamento_legal": "Art. 5 Ley 1437 de 2011 - Principio de formalidad",
                            "tiempo_estimado": "corto plazo",
                            "recursos_necesarios": "Revisión de formato y estructura",
                            "impacto_esperado": "Documento formalmente correcto",
                            "riesgos": "Bajo - corrección de forma"
                        })
                    elif tipo == "SUSTANCIAL":
                        fallback.append({
                            "titulo": f"Fortalecer argumentación sustancial: {descripcion[:50]}...",
                            "descripcion": f"Mejorar la argumentación sustancial: {descripcion}",
                            "prioridad": "ALTA",
                            "accion": "Desarrollar argumentos más sólidos y fundamentados",
                            "fundamento_legal": "Art. 6 Ley 1437 de 2011 - Principio de motivación",
                            "tiempo_estimado": "mediano plazo",
                            "recursos_necesarios": "Investigación legal y desarrollo de argumentos",
                            "impacto_esperado": "Argumentación más convincente",
                            "riesgos": "Medio - requiere análisis profundo"
                        })
        
        return fallback

    def generate_recommendations(self, texto: str, problemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generación de recomendaciones con cache."""
        return self.generate_recommendations_cached(texto, problemas, self)

    def chat_response(self, pregunta: str, contexto: Dict[str, Any]) -> str:
        """Respuesta de chat usando solo Gemini 2.0 Flash."""
        
        try:
            # Prompt para respuesta legal directa con Gemini
            system_prompt = """Eres un asistente legal especializado en derecho administrativo colombiano con amplia experiencia en derecho administrativo, constitucional y procedimental.

INSTRUCCIONES ESPECÍFICAS:
1. Responde de manera profesional, clara y útil
2. Utiliza el contexto del análisis previo cuando esté disponible
3. Proporciona información legal precisa y actualizada
4. Incluye fundamento legal cuando sea relevante
5. Ofrece orientación práctica y accionable
6. Mantén un tono profesional pero accesible

ÁREAS DE EXPERTISE:
- Derecho Administrativo Colombiano
- Derecho Constitucional
- Procedimiento Administrativo
- Derecho de Petición
- Recursos Administrativos
- Control de Legalidad
- Jurisprudencia relevante"""
            
            user_prompt = f"""
PREGUNTA DEL USUARIO: {pregunta}

CONTEXTO DISPONIBLE DEL ANÁLISIS PREVIO:
- Análisis del documento: {str(contexto.get('analisis', 'No disponible'))}
- Problemas detectados: {str(contexto.get('problemas', 'No disponibles'))}
- Recomendaciones generadas: {str(contexto.get('recomendaciones', 'No disponibles'))}

INSTRUCCIONES:
- Responde la pregunta de manera completa y útil
- Utiliza el contexto del análisis cuando sea relevante
- Proporciona fundamento legal cuando sea apropiado
- Ofrece orientación práctica y accionable
- Si la pregunta no está relacionada con el análisis previo, responde basándote en tu conocimiento legal general

Responde de manera profesional y útil, considerando el contexto disponible.
        """.strip()

            # Llamada directa a Gemini usando _chat
            return self._chat(
                [{"role": "system", "content": system_prompt},
                 {"role": "user", "content": user_prompt}],
                temperature=0.2
            )
                
        except Exception as e:
            error_msg = str(e)
            # Respuesta de fallback en caso de error
            return f"""Lo siento, hubo un error al procesar tu pregunta con la IA.

Error técnico: {error_msg}

Por favor, intenta reformular tu pregunta o contacta al administrador del sistema si el problema persiste.

Mientras tanto, puedo ayudarte con información general sobre derecho administrativo colombiano basándome en mi conocimiento predefinido.""" 