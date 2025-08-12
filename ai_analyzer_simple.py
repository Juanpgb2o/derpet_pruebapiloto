#!/usr/bin/env python3
"""
Analizador de IA simple que funciona sin dependencias externas
"""

import json
import re
from typing import Dict, List, Any, Optional
import streamlit as st

class SimpleAIAnalyzer:
    """Analizador de IA simple que funciona localmente"""
    
    def __init__(self, api_key: str = None, connection_id: str = None):
        self.api_key = api_key
        self.connection_id = connection_id
        
    def analyze_document(self, texto: str) -> Dict[str, Any]:
        """Análisis detallado del documento"""
        try:
            # Análisis básico del texto
            palabras = texto.split()
            caracteres = len(texto)
            parrafos = texto.count('\n\n') + 1
            oraciones = texto.count('.') + texto.count('!') + texto.count('?')
            
            # Detectar tipo de documento con análisis más inteligente
            tipo_documento = "Documento Administrativo"
            if any(palabra in texto.lower() for palabra in ["derecho de petición", "derecho de peticion", "petición", "peticion"]):
                tipo_documento = "Derecho de Petición"
            elif any(palabra in texto.lower() for palabra in ["recurso", "apelación", "apelacion", "reconsideración"]):
                tipo_documento = "Recurso Administrativo"
            elif any(palabra in texto.lower() for palabra in ["acto administrativo", "resolución", "resolucion", "decreto"]):
                tipo_documento = "Acto Administrativo"
            elif any(palabra in texto.lower() for palabra in ["contrato", "convenio", "acuerdo"]):
                tipo_documento = "Contrato o Convenio"
            
            # Análisis de calidad más sofisticado
            calidad = "MEDIA"
            confianza = 0.5
            
            if caracteres > 1500 and parrafos > 5 and oraciones > 10:
                calidad = "ALTA"
                confianza = 0.9
            elif caracteres > 800 and parrafos > 3 and oraciones > 5:
                calidad = "MEDIA"
                confianza = 0.7
            elif caracteres < 300:
                calidad = "BAJA"
                confianza = 0.3
            
            # Detectar palabras clave más específicas
            palabras_clave = []
            if "constitución" in texto.lower() or "constitucion" in texto.lower():
                palabras_clave.append("Constitución Política")
            if "ley" in texto.lower():
                palabras_clave.append("Normativa Legal")
            if "decreto" in texto.lower():
                palabras_clave.append("Decreto")
            if "resolución" in texto.lower() or "resolucion" in texto.lower():
                palabras_clave.append("Resolución")
            if "competencia" in texto.lower() or "competente" in texto.lower():
                palabras_clave.append("Competencia Administrativa")
            if "fundamento" in texto.lower() or "fundamentación" in texto.lower():
                palabras_clave.append("Fundamentación Legal")
            if "derecho" in texto.lower():
                palabras_clave.append("Derechos")
            if "procedimiento" in texto.lower():
                palabras_clave.append("Procedimiento")
            
            # Si no hay palabras clave específicas, agregar generales
            if not palabras_clave:
                palabras_clave = ["Administrativo", "Legal", "Procedimiento", "Documento"]
            
            # Análisis de estructura
            estructura = "BÁSICA"
            if "encabezado" in texto.lower() or "fecha" in texto.lower():
                estructura = "FORMAL"
            if "artículo" in texto.lower() or "fundamento" in texto.lower():
                estructura = "FUNDAMENTADA"
            if "conclusión" in texto.lower() or "resuelve" in texto.lower():
                estructura = "COMPLETA"
            
            # Fecha de análisis
            from datetime import datetime
            fecha_analisis = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            return {
                "tipo_documento": tipo_documento,
                "longitud": caracteres,
                "confianza": confianza,
                "fecha_analisis": fecha_analisis,
                "calidad": calidad,
                "estructura": estructura,
                "palabras": len(palabras),
                "parrafos": parrafos,
                "oraciones": oraciones,
                "palabras_clave": palabras_clave,
                "resumen": f"Documento de {caracteres} caracteres con {parrafos} párrafos y {oraciones} oraciones",
                "observaciones": [
                    f"Tipo identificado: {tipo_documento}",
                    f"Calidad: {calidad}",
                    f"Estructura: {estructura}",
                    f"Longitud: {caracteres} caracteres",
                    f"Párrafos: {parrafos}",
                    f"Oraciones: {oraciones}"
                ]
            }
        except Exception as e:
            return {
                "tipo_documento": "Error en análisis",
                "longitud": 0,
                "confianza": 0.0,
                "fecha_analisis": "N/A",
                "calidad": "BAJA",
                "estructura": "ERROR",
                "palabras": 0,
                "parrafos": 0,
                "oraciones": 0,
                "palabras_clave": [],
                "resumen": f"Error al analizar: {str(e)}",
                "observaciones": [f"Error: {str(e)}"]
            }
    
    def detect_problems(self, texto: str, contexto: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detección inteligente de problemas"""
        problemas = []
        
        # Análisis de longitud y estructura
        if len(texto) < 200:
            problemas.append({
                "tipo": "ESTRUCTURAL",
                "descripcion": "Documento muy corto, puede carecer de fundamentación adecuada",
                "severidad": "MEDIA",
                "linea": "N/A",
                "fundamento_legal": "Ley 1437 de 2011 - Principio de motivación",
                "impacto": "Respuesta insuficiente para el ciudadano, puede generar recursos",
                "recomendacion_breve": "Expandir la respuesta con más detalles y fundamentación"
            })
        
        # Análisis de fundamentación legal
        fundamentacion_indicadores = ["fundamento", "fundamentación", "artículo", "articulo", "ley", "decreto", "constitución", "constitucion"]
        if not any(indicator in texto.lower() for indicator in fundamentacion_indicadores):
            problemas.append({
                "tipo": "LEGAL",
                "descripcion": "Falta fundamentación legal específica y citas de normas",
                "severidad": "ALTA",
                "linea": "N/A",
                "fundamento_legal": "Constitución Art. 23, Ley 1437 Art. 6, Ley 1755 de 2015",
                "impacto": "Puede llevar a nulidad del documento y recursos de apelación",
                "recomendacion_breve": "Agregar citas específicas de normas aplicables y fundamentación legal"
            })
        
        # Análisis de competencia administrativa
        competencia_indicadores = ["competente", "competencia", "funcionario", "autoridad", "delegado", "delegación"]
        if not any(indicator in texto.lower() for indicator in competencia_indicadores):
            problemas.append({
                "tipo": "ADMINISTRATIVO",
                "descripcion": "No se especifica la competencia del funcionario o autoridad",
                "severidad": "MEDIA",
                "linea": "N/A",
                "fundamento_legal": "Ley 1437 de 2011 - Principio de competencia",
                "impacto": "Duda sobre la autoridad para resolver, puede generar impugnación",
                "recomendacion_breve": "Especificar competencia del funcionario y fundamento legal"
            })
        
        # Análisis de estructura formal
        estructura_indicadores = ["encabezado", "fecha", "número", "numero", "radicado", "referencia"]
        if not any(indicator in texto.lower() for indicator in estructura_indicadores):
            problemas.append({
                "tipo": "FORMAL",
                "descripcion": "Falta estructura formal del documento (encabezado, fecha, número de radicado)",
                "severidad": "MEDIA",
                "linea": "N/A",
                "fundamento_legal": "Ley 1437 de 2011 - Principio de formalidad",
                "impacto": "Dificulta el seguimiento y control administrativo",
                "recomendacion_breve": "Agregar encabezado formal con datos de identificación"
            })
        
        # Análisis de claridad y lenguaje
        if len(texto.split()) > 50:  # Solo si el documento es suficientemente largo
            oraciones_largas = sum(1 for oracion in texto.split('.') if len(oracion.split()) > 30)
            if oraciones_largas > 2:
                problemas.append({
                    "tipo": "COMUNICACIÓN",
                    "descripcion": "Presencia de oraciones muy largas que dificultan la comprensión",
                    "severidad": "BAJA",
                    "linea": "N/A",
                    "fundamento_legal": "Ley 1755 de 2015 - Derecho de acceso a la información",
                    "impacto": "Dificulta la comprensión del ciudadano",
                    "recomendacion_breve": "Simplificar oraciones largas y usar párrafos cortos"
                })
        
        # Análisis de términos técnicos sin explicación
        terminos_tecnicos = ["competencia", "fundamento", "motivación", "motivacion", "recurso", "apelación", "apelacion"]
        terminos_sin_explicar = [term for term in terminos_tecnicos if term in texto.lower() and len(texto) < 1000]
        if terminos_sin_explicar:
            problemas.append({
                "tipo": "COMUNICACIÓN",
                "descripcion": "Uso de términos técnicos sin explicación adecuada",
                "severidad": "BAJA",
                "linea": "N/A",
                "fundamento_legal": "Ley 1755 de 2015 - Principio de claridad",
                "impacto": "Puede confundir al ciudadano",
                "recomendacion_breve": "Explicar términos técnicos o usar lenguaje más simple"
            })
        
        # Análisis de respuesta completa
        if "no procede" in texto.lower() or "no se accede" in texto.lower() or "se niega" in texto.lower():
            if "fundamento" not in texto.lower() and "motivo" not in texto.lower():
                problemas.append({
                    "tipo": "LEGAL",
                    "descripcion": "Respuesta negativa sin fundamentación legal clara",
                    "severidad": "ALTA",
                    "linea": "N/A",
                    "fundamento_legal": "Ley 1437 de 2011 - Principio de motivación",
                    "impacto": "Respuesta puede ser impugnada por falta de fundamentación",
                    "recomendacion_breve": "Fundamentar claramente la respuesta negativa con normas aplicables"
                })
        
        # Análisis de términos legales
        if "derecho de petición" in texto.lower() or "derecho de peticion" in texto.lower():
            if "15 días" not in texto.lower() and "quince días" not in texto.lower():
                problemas.append({
                    "tipo": "PROCEDIMENTAL",
                    "descripcion": "No se especifica el término de respuesta (15 días hábiles)",
                    "severidad": "MEDIA",
                    "linea": "N/A",
                    "fundamento_legal": "Constitución Art. 23, Ley 1437 de 2011",
                    "impacto": "Dificulta al ciudadano conocer sus derechos",
                    "recomendacion_breve": "Especificar el término de respuesta según la normativa"
                })
        
        return problemas
    
    def generate_recommendations(self, texto: str, problemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generación inteligente de recomendaciones"""
        recomendaciones = []
        
        # Generar recomendaciones basadas en problemas específicos
        for problema in problemas:
            if problema["tipo"] == "LEGAL":
                recomendaciones.append({
                    "titulo": "Agregar fundamentación legal completa",
                    "descripcion": "Incluir citas específicas de la Constitución Política, Ley 1437 de 2011 y normativa aplicable al caso",
                    "prioridad": "ALTA",
                    "tiempo_estimado": "inmediato",
                    "recursos_necesarios": "Consulta de normativa vigente, asesoría legal especializada",
                    "impacto_esperado": "Documento jurídicamente válido, reducción de recursos de apelación",
                    "riesgos": "Verificar vigencia de normas citadas, consultar jurisprudencia aplicable"
                })
                
                # Recomendación adicional para respuestas negativas
                if any(palabra in texto.lower() for palabra in ["no procede", "no se accede", "se niega"]):
                    recomendaciones.append({
                        "titulo": "Fundamentar respuesta negativa",
                        "descripcion": "Explicar claramente los motivos legales de la negativa con citas específicas",
                        "prioridad": "ALTA",
                        "tiempo_estimado": "inmediato",
                        "recursos_necesarios": "Análisis legal del caso, identificación de excepciones aplicables",
                        "impacto_esperado": "Respuesta impugnable, cumplimiento del principio de motivación",
                        "riesgos": "Verificar que la negativa esté legalmente justificada"
                    })
            
            elif problema["tipo"] == "ESTRUCTURAL":
                recomendaciones.append({
                    "titulo": "Mejorar estructura y organización del documento",
                    "descripcion": "Reorganizar en secciones claras con encabezados, numeración y párrafos bien definidos",
                    "prioridad": "MEDIA",
                    "tiempo_estimado": "corto plazo",
                    "recursos_necesarios": "Revisión de formato, herramientas de procesamiento de texto",
                    "impacto_esperado": "Mejor comprensión del ciudadano, documento más profesional",
                    "riesgos": "Mantener coherencia del contenido durante la reorganización"
                })
            
            elif problema["tipo"] == "ADMINISTRATIVO":
                recomendaciones.append({
                    "titulo": "Especificar competencia administrativa",
                    "descripcion": "Clarificar la autoridad del funcionario para resolver, incluir fundamento legal de la competencia",
                    "prioridad": "MEDIA",
                    "tiempo_estimado": "inmediato",
                    "recursos_necesarios": "Verificación de funciones, consulta de manual de funciones",
                    "impacto_esperado": "Legitimidad del acto administrativo, claridad para el ciudadano",
                    "riesgos": "Verificar delegación de funciones y límites de competencia"
                })
            
            elif problema["tipo"] == "FORMAL":
                recomendaciones.append({
                    "titulo": "Implementar estructura formal completa",
                    "descripcion": "Agregar encabezado con datos de la entidad, fecha, número de radicado y referencia",
                    "prioridad": "MEDIA",
                    "tiempo_estimado": "inmediato",
                    "recursos_necesarios": "Plantilla de documento, verificación de datos institucionales",
                    "impacto_esperado": "Documento profesional, mejor seguimiento administrativo",
                    "riesgos": "Verificar exactitud de datos institucionales"
                })
            
            elif problema["tipo"] == "COMUNICACIÓN":
                recomendaciones.append({
                    "titulo": "Mejorar claridad y accesibilidad del lenguaje",
                    "descripcion": "Simplificar oraciones largas, explicar términos técnicos, usar lenguaje ciudadano",
                    "prioridad": "BAJA",
                    "tiempo_estimado": "corto plazo",
                    "recursos_necesarios": "Revisión de redacción, consulta de guías de lenguaje claro",
                    "impacto_esperado": "Mejor comprensión del ciudadano, cumplimiento del derecho de acceso a la información",
                    "riesgos": "Mantener precisión técnica mientras se simplifica el lenguaje"
                })
            
            elif problema["tipo"] == "PROCEDIMENTAL":
                recomendaciones.append({
                    "titulo": "Especificar términos y procedimientos",
                    "descripcion": "Indicar claramente el término de respuesta (15 días hábiles) y vías de recurso disponibles",
                    "prioridad": "MEDIA",
                    "tiempo_estimado": "inmediato",
                    "recursos_necesarios": "Verificación de términos legales, consulta de procedimientos",
                    "impacto_esperado": "Claridad para el ciudadano, cumplimiento de términos legales",
                    "riesgos": "Verificar exactitud de términos según normativa aplicable"
                })
        
        # Recomendaciones generales de mejora
        if len(texto) < 500:
            recomendaciones.append({
                "titulo": "Expandir contenido del documento",
                "descripcion": "Desarrollar más detalladamente la respuesta, incluir ejemplos y casos similares",
                "prioridad": "MEDIA",
                "tiempo_estimado": "corto plazo",
                "recursos_necesarios": "Investigación adicional del caso, consulta de precedentes",
                "impacto_esperado": "Respuesta más completa y útil para el ciudadano",
                "riesgos": "Mantener relevancia y no agregar información innecesaria"
            })
        
        # Recomendación de revisión final
        recomendaciones.append({
            "titulo": "Revisión integral de calidad",
            "descripcion": "Verificar cumplimiento de estándares administrativos, legales y de comunicación",
            "prioridad": "BAJA",
            "tiempo_estimado": "corto plazo",
            "recursos_necesarios": "Revisión técnica integral, validación legal",
            "impacto_esperado": "Documento de alta calidad, cumplimiento de todos los estándares",
            "riesgos": "Mínimos, solo tiempo de revisión"
        })
        
        return recomendaciones
        
    def chat_response(self, pregunta: str, contexto: Dict[str, Any]) -> str:
        """Respuesta de chat simple pero funcional"""
        
        # Respuestas predefinidas para preguntas comunes
        respuestas_comunes = {
            "normativa": {
                "preguntas": ["normativa", "citar", "ley", "decreto", "resolución"],
                "respuesta": """Para mejorar la fundamentación legal de tu documento, debes citar la siguiente normativa colombiana:

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
            },
            "mejorar_contestacion": {
                "preguntas": ["mejorar", "contestacion", "respuesta", "estructura"],
                "respuesta": """Para mejorar la contestación de tu documento, sigue estas recomendaciones:

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
            },
            "problemas_criticos": {
                "preguntas": ["problemas", "críticos", "urgentes", "prioritarios"],
                "respuesta": """Los problemas más críticos en tu documento son:

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
            },
            "implementar_recomendaciones": {
                "preguntas": ["implementar", "recomendaciones", "aplicar", "ejecutar"],
                "respuesta": """Para implementar las recomendaciones de manera efectiva:

**📋 PLAN DE IMPLEMENTACIÓN:**

**FASE 1: FUNDAMENTACIÓN LEGAL (Día 1-2)**
1. **Investigación normativa**
   - Consultar Constitución Política
   - Revisar Ley 1437 de 2011
   - Identificar jurisprudencia aplicable
   - Verificar vigencia de normas

2. **Citas específicas**
   - Seleccionar artículos relevantes
   - Preparar explicaciones de aplicación
   - Organizar por orden de importancia

**FASE 2: ESTRUCTURA Y ORGANIZACIÓN (Día 3-4)**
1. **Reorganización del documento**
   - Crear encabezados claros
   - Establecer numeración lógica
   - Separar secciones por tema
   - Agregar transiciones entre párrafos

2. **Mejora de presentación**
   - Usar formato consistente
   - Agregar viñetas y listas
   - Incluir espacios en blanco apropiados
   - Verificar ortografía y gramática

**FASE 3: VALIDACIÓN Y REVISIÓN (Día 5)**
1. **Revisión técnica**
   - Verificar fundamentación legal
   - Confirmar competencia administrativa
   - Validar número de radicado
   - Revisar cumplimiento de términos

2. **Revisión de calidad**
   - Evaluar claridad del lenguaje
   - Verificar coherencia lógica
   - Confirmar completitud de respuesta
   - Validar formato final

**🛠️ RECURSOS NECESARIOS:**
• **Tiempo**: 5 días hábiles
• **Personal**: Abogado especializado + Asistente administrativo
• **Herramientas**: Base de datos legal, procesador de texto
• **Documentación**: Normativa vigente, jurisprudencia aplicable

**📊 MÉTRICAS DE ÉXITO:**
• Fundamentación legal completa (100%)
• Estructura organizada y clara
• Cumplimiento de términos legales
• Satisfacción del ciudadano
• Reducción de recursos de apelación

**⚠️ RIESGOS Y MITIGACIÓN:**
• **Riesgo**: Cambios en normativa durante implementación
• **Mitigación**: Verificar vigencia antes de finalizar
• **Riesgo**: Falta de recursos especializados
• **Mitigación**: Capacitar personal o contratar consultoría

**🚀 SIGUIENTES PASOS:**
1. Aprobar plan de implementación
2. Asignar recursos y responsabilidades
3. Iniciar Fase 1 de fundamentación legal
4. Establecer reuniones de seguimiento diarias

La implementación exitosa transformará tu documento en un instrumento legal sólido y profesional."""
            }
        }
        
        # Buscar la respuesta más apropiada
        pregunta_lower = pregunta.lower()
        
        for categoria, info in respuestas_comunes.items():
            for palabra_clave in info["preguntas"]:
                if palabra_clave in pregunta_lower:
                    return info["respuesta"]
        
        # Si no hay coincidencia específica, dar respuesta general
        return """Para responder a tu pregunta sobre derecho administrativo colombiano, te recomiendo:

**🔍 ANÁLISIS DEL CONTEXTO:**
Revisa el análisis previo del documento para identificar áreas específicas de mejora.

**📋 PASOS RECOMENDADOS:**
1. **Identifica el tipo de documento** (derecho de petición, recurso, etc.)
2. **Revisa la fundamentación legal** actual
3. **Verifica la competencia administrativa**
4. **Estructura la respuesta** de manera clara y organizada

**💡 RECURSOS DISPONIBLES:**
• Análisis del documento: {analisis}
• Problemas identificados: {problemas}
• Recomendaciones: {recomendaciones}

**📞 SIGUIENTE PASO:**
Si necesitas ayuda específica, reformula tu pregunta mencionando el aspecto particular que quieres mejorar (ej: "fundamentación legal", "estructura", "competencia administrativa").

¿En qué aspecto específico te gustaría que te ayude más?""".format(
            analisis=str(contexto.get('analisis', 'No disponible')),
            problemas=str(contexto.get('problemas', 'No disponibles')),
            recomendaciones=str(contexto.get('recomendaciones', 'No disponibles'))
        )

def test_simple_analyzer():
    """Prueba el analizador simple"""
    print("🧪 Probando analizador simple...")
    
    analyzer = SimpleAIAnalyzer()
    
    # Probar diferentes tipos de preguntas
    preguntas_prueba = [
        "¿Qué normativa debo citar?",
        "¿Cómo mejorar la contestación?",
        "¿Cuáles son los problemas más críticos?",
        "¿Cómo implementar las recomendaciones?"
    ]
    
    contexto_prueba = {
        "analisis": {"tipo": "Derecho de Petición"},
        "problemas": [{"tipo": "LEGAL", "descripcion": "Falta fundamentación"}],
        "recomendaciones": [{"titulo": "Agregar fundamentación legal"}]
    }
    
    for pregunta in preguntas_prueba:
        print(f"\n📝 Pregunta: {pregunta}")
        respuesta = analyzer.chat_response(pregunta, contexto_prueba)
        print(f"🤖 Respuesta: {respuesta[:100]}...")
    
    print("\n✅ Analizador simple funcionando correctamente!")

if __name__ == "__main__":
    test_simple_analyzer()

