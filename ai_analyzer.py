# ai_analyzer.py
import os
import json
import re
from datetime import datetime
from typing import Any, Dict, List
import google.generativeai as genai

MODEL_DEFAULT = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

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
    def __init__(self, api_key: str | None = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key or key == "tu_clave_aqui":
            raise ValueError("API Key de Google Gemini no configurada.")
        
        # Configurar Gemini
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(MODEL_DEFAULT)
        self.model_name = MODEL_DEFAULT

    def _chat(self, prompt: str, temperature: float = 0.2) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                raise Exception("❌ Cuota de Google Gemini excedida. Verifica tu plan en https://makersuite.google.com/app/apikey")
            elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
                raise Exception("❌ API Key de Google Gemini inválida. Verifica tu clave en https://makersuite.google.com/app/apikey")
            else:
                raise Exception(f"❌ Error de Google Gemini: {error_msg}")

    def analyze_document(self, texto: str) -> Dict[str, Any]:
        system = ("Eres un abogado experto en derecho administrativo. "
                  "Analiza derechos de petición y devuelve un análisis claro.")
        
        prompt = f"""
{system}

Analiza el siguiente derecho de petición. Devuelve SOLO un JSON con:
{{
  "tipo_documento": "Derecho de Petición",
  "longitud": <int>,
  "palabras_clave": ["...", "..."],
  "confianza": <float entre 0 y 1>,
  "analisis_markdown": "Análisis detallado en Markdown"
}}

Documento:
\"\"\"{texto}\"\"\"
        """.strip()

        raw = self._chat(prompt, temperature=0.1)

        block = _extract_json_block(raw)
        data = _safe_json_loads(block, {
            "tipo_documento": "Derecho de Petición",
            "longitud": len(texto),
            "palabras_clave": ["petición", "derecho", "solicitud"],
            "confianza": 0.75,
            "analisis_markdown": "No se pudo extraer análisis estructurado.",
        })

        return {
            "tipo_documento": data.get("tipo_documento", "Derecho de Petición"),
            "longitud": data.get("longitud", len(texto)),
            "confianza": data.get("confianza", 0.75),
            "palabras_clave": data.get("palabras_clave", ["petición", "derecho"]),
            "fecha_analisis": datetime.now().strftime("%d/%m/%Y"),
            "analisis_gemini": data.get("analisis_markdown", "—"),
        }

    def detect_problems(self, texto: str, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        system = """Eres un abogado experto en derecho administrativo colombiano. 
        Analiza derechos de petición y detecta problemas formales y materiales específicos.
        Considera la normativa colombiana (CPACA, Constitución, jurisprudencia)."""
        
        prompt = f"""
{system}

Analiza este derecho de petición y detecta problemas específicos. Devuelve SOLO un array JSON de objetos con:

{{
  "tipo": "Formal|Material|Procedimental|Competencia",
  "descripcion": "Descripción detallada del problema",
  "severidad": "Alta|Media|Baja",
  "linea": "N/A o referencia específica",
  "fundamento_legal": "Norma o jurisprudencia aplicable",
  "impacto": "Cómo afecta la contestación"
}}

Documento a analizar:
\"\"\"{texto}\"\"\"

Contexto del análisis previo:
{json.dumps(contexto, ensure_ascii=False)}

Considera estos aspectos:
1. **Formales**: Faltas de requisitos, formato, firma, etc.
2. **Materiales**: Contenido, fundamentación, claridad
3. **Procedimentales**: Competencia, términos, trámites
4. **Competencia**: Si la entidad puede resolver la petición
        """.strip()

        raw = self._chat(prompt, temperature=0.1)

        block = _extract_json_block(raw)
        fallback = [
            {
                "tipo": "Formal", 
                "descripcion": "Falta identificación clara del peticionario y sus datos de contacto", 
                "severidad": "Alta", 
                "linea": "N/A",
                "fundamento_legal": "Art. 5 CPACA",
                "impacto": "Puede generar inadmisión del derecho de petición"
            },
            {
                "tipo": "Competencia", 
                "descripcion": "No se especifica claramente la autoridad competente para resolver", 
                "severidad": "Media", 
                "linea": "N/A",
                "fundamento_legal": "Art. 6 CPACA",
                "impacto": "Puede generar confusión en la contestación"
            }
        ]
        return _safe_json_loads(block, fallback)

    def generate_recommendations(self, texto: str, problemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        system = """Eres un abogado experto en derecho administrativo colombiano. 
        Genera recomendaciones específicas y accionables para mejorar la contestación del derecho de petición.
        Considera la normativa colombiana y mejores prácticas."""
        
        prompt = f"""
{system}

Basándote en los problemas detectados, genera recomendaciones específicas. Devuelve SOLO un array JSON con:

{{
  "titulo": "Título claro de la recomendación",
  "descripcion": "Descripción detallada de la acción a tomar",
  "prioridad": "Alta|Media|Baja",
  "accion": "Acción específica a realizar",
  "fundamento_legal": "Norma o jurisprudencia que respalda",
  "tiempo_estimado": "Tiempo estimado para implementar",
  "beneficio": "Beneficio de implementar esta recomendación"
}}

Problemas detectados:
{json.dumps(problemas, ensure_ascii=False)}

Documento original:
\"\"\"{texto}\"\"\"

Considera estos tipos de recomendaciones:
1. **Inmediatas**: Correcciones urgentes que deben hacerse
2. **Estructurales**: Mejoras en el formato y organización
3. **Fundamentación**: Fortalecer la base legal
4. **Procedimentales**: Optimizar el proceso de contestación
        """.strip()

        raw = self._chat(prompt, temperature=0.2)

        block = _extract_json_block(raw)
        fallback = [
            {
                "titulo": "Fundamentación legal específica",
                "descripcion": "Incluir citas específicas de la normativa aplicable y jurisprudencia relevante",
                "prioridad": "Alta",
                "accion": "Citar artículos específicos del CPACA y jurisprudencia",
                "fundamento_legal": "Art. 6 CPACA",
                "tiempo_estimado": "2-3 horas",
                "beneficio": "Mayor solidez legal de la contestación"
            },
            {
                "titulo": "Estructuración clara de la respuesta",
                "descripcion": "Organizar la contestación en secciones lógicas y numeradas",
                "prioridad": "Media",
                "accion": "Usar formato estructurado con encabezados",
                "fundamento_legal": "Principio de claridad administrativa",
                "tiempo_estimado": "1-2 horas",
                "beneficio": "Facilita la comprensión del peticionario"
            }
        ]
        return _safe_json_loads(block, fallback)

    def chat_response(self, pregunta: str, contexto: Dict[str, Any]) -> str:
        system = """Eres un abogado experto en derecho administrativo colombiano. 
        Responde preguntas sobre análisis de derechos de petición, problemas detectados y recomendaciones.
        Usa lenguaje claro y técnico, cita normativa cuando sea relevante."""
        
        prompt = f"""
{system}

Pregunta del usuario: {pregunta}

Contexto del análisis:
- Análisis del documento: {json.dumps(contexto.get('analisis', {}), ensure_ascii=False)}
- Problemas detectados: {json.dumps(contexto.get('problemas', []), ensure_ascii=False)}
- Recomendaciones generadas: {json.dumps(contexto.get('recomendaciones', []), ensure_ascii=False)}

Responde de manera específica y práctica, considerando:
1. La normativa colombiana aplicable
2. Los problemas específicos detectados
3. Las recomendaciones más relevantes
4. Mejores prácticas en derecho administrativo
        """.strip()

        return self._chat(prompt, temperature=0.2) 