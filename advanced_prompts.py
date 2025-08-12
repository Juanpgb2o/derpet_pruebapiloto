# advanced_prompts.py
"""
Prompts avanzados y especializados para mejorar la calidad de las respuestas de IA
en el análisis de derechos de petición.
"""

# Prompts especializados para análisis legal
LEGAL_ANALYSIS_PROMPTS = {
    "constitutional_rights": """
    Eres un experto en derecho constitucional colombiano. Analiza el documento considerando:
    - Derechos fundamentales involucrados
    - Principios constitucionales aplicables
    - Jurisprudencia de la Corte Constitucional
    - Mecanismos de protección constitucional
    """,
    
    "administrative_law": """
    Eres un especialista en derecho administrativo colombiano. Evalúa:
    - Procedimientos administrativos aplicables
    - Actos administrativos involucrados
    - Recursos administrativos disponibles
    - Principios de la función administrativa
    """,
    
    "procedural_law": """
    Eres un experto en derecho procesal administrativo. Revisa:
    - Términos y plazos procesales
    - Formalidades del procedimiento
    - Medios de prueba aplicables
    - Recursos y medios de impugnación
    """
}

# Prompts para detección de problemas específicos
PROBLEM_DETECTION_PROMPTS = {
    "formal_issues": """
    Identifica problemas formales específicos:
    - Falta de identificación del peticionario
    - Ausencia de fecha o lugar
    - Falta de firma o autenticación
    - Problemas de competencia territorial
    - Incumplimiento de términos procesales
    """,
    
    "substantive_issues": """
    Detecta problemas sustanciales:
    - Falta de fundamentación legal
    - Argumentación insuficiente
    - Ausencia de pruebas o documentos
    - Solicitudes imprecisas o ambiguas
    - Falta de legitimación o interés
    """,
    
    "constitutional_issues": """
    Identifica problemas constitucionales:
    - Violación de derechos fundamentales
    - Falta de debido proceso
    - Discriminación o arbitrariedad
    - Restricciones desproporcionadas
    - Falta de motivación suficiente
    """
}

# Prompts para recomendaciones estratégicas
RECOMMENDATION_PROMPTS = {
    "immediate_actions": """
    Recomendaciones de acción inmediata:
    - Correcciones que deben hacerse antes de presentar
    - Documentos adicionales necesarios
    - Plazos críticos a considerar
    - Recursos urgentes requeridos
    """,
    
    "strategic_improvements": """
    Mejoras estratégicas a mediano plazo:
    - Fortalecimiento de argumentación legal
    - Estrategias de defensa
    - Alianzas o apoyos necesarios
    - Recursos y capacidades a desarrollar
    """,
    
    "risk_mitigation": """
    Mitigación de riesgos:
    - Identificación de puntos débiles
    - Estrategias de defensa preventiva
    - Recursos de contingencia
    - Planes alternativos
    """
}

# Prompts para análisis de contexto
CONTEXT_ANALYSIS_PROMPTS = {
    "legal_framework": """
    Analiza el marco legal aplicable:
    - Normas constitucionales relevantes
    - Leyes y decretos aplicables
    - Jurisprudencia pertinente
    - Doctrina administrativa
    """,
    
    "procedural_context": """
    Evalúa el contexto procedimental:
    - Etapa del procedimiento administrativo
    - Plazos y términos aplicables
    - Recursos disponibles
    - Posibles obstáculos
    """,
    
    "institutional_context": """
    Considera el contexto institucional:
    - Naturaleza de la entidad
    - Competencias específicas
    - Procedimientos internos
    - Relaciones con otras entidades
    """
}

# Prompts para respuestas de chat especializadas
CHAT_SPECIALIZATION_PROMPTS = {
    "legal_advice": """
    Proporciona asesoría legal especializada:
    - Explicación de conceptos jurídicos
    - Interpretación de normas aplicables
    - Análisis de jurisprudencia
    - Recomendaciones estratégicas
    """,
    
    "procedural_guidance": """
    Orienta en procedimientos administrativos:
    - Pasos a seguir
    - Documentos necesarios
    - Plazos importantes
    - Recursos disponibles
    """,
    
    "strategic_planning": """
    Ayuda en planificación estratégica:
    - Análisis de fortalezas y debilidades
    - Identificación de oportunidades
    - Evaluación de riesgos
    - Desarrollo de estrategias
    """
}

# Configuración de calidad para diferentes tipos de análisis
QUALITY_CONFIGS = {
    "basic_analysis": {
        "temperature": 0.1,
        "max_tokens": 2000,
        "top_p": 0.8,
        "top_k": 40
    },
    "detailed_analysis": {
        "temperature": 0.2,
        "max_tokens": 4000,
        "top_p": 0.9,
        "top_k": 50
    },
    "creative_solutions": {
        "temperature": 0.3,
        "max_tokens": 3000,
        "top_p": 0.95,
        "top_k": 60
    },
    "legal_expertise": {
        "temperature": 0.1,
        "max_tokens": 5000,
        "top_p": 0.85,
        "top_k": 45
    }
}

# Funciones de ayuda para construir prompts
def build_specialized_prompt(base_prompt: str, specialization: str, context: str = "") -> str:
    """Construye un prompt especializado combinando diferentes elementos."""
    specialized = LEGAL_ANALYSIS_PROMPTS.get(specialization, "")
    return f"{base_prompt}\n\n{specialized}\n\n{context}".strip()

def get_quality_config(analysis_type: str = "detailed_analysis"):
    """Obtiene la configuración de calidad para un tipo de análisis."""
    return QUALITY_CONFIGS.get(analysis_type, QUALITY_CONFIGS["detailed_analysis"])

def enhance_prompt_with_context(base_prompt: str, context_elements: dict) -> str:
    """Mejora un prompt base con elementos de contexto específicos."""
    context_str = ""
    for key, value in context_elements.items():
        context_str += f"\n- {key}: {value}"
    
    return f"{base_prompt}\n\nCONTEXTO ADICIONAL:{context_str}"

