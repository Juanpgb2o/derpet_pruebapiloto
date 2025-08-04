import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import random
import os
from dotenv import load_dotenv

# Importar módulos personalizados
from document_processor import process_document
from ai_analyzer import AIAnalyzer

# Cargar variables de entorno
try:
    load_dotenv()
except:
    # Si hay problemas con .env, usar configuración por defecto
    pass

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Contestación Automática de Derechos de Petición",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .step-container {
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        transition: all 0.3s ease;
    }
    
    .step-container.completed {
        border-color: #28a745;
        background: #f8fff9;
    }
    
    .step-container.active {
        border-color: #007bff;
        background: #f8f9ff;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    .problem-card, .recommendation-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .problem-card.high {
        border-left-color: #dc3545;
    }
    
    .recommendation-card.high {
        border-left-color: #28a745;
    }
    
    .chat-message {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización del estado de la sesión
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'problems_detected' not in st.session_state:
    st.session_state.problems_detected = False
if 'recommendations_generated' not in st.session_state:
    st.session_state.recommendations_generated = False
if 'ai_analyzer' not in st.session_state:
    st.session_state.ai_analyzer = None
if 'ai_connected' not in st.session_state:
    st.session_state.ai_connected = False

# Debug: Mostrar estado en la consola
st.caption(f"Estado actual: Paso {st.session_state.current_step}, Progreso: {st.session_state.progress}%")

# Cache para funciones costosas
@st.cache_data
def process_document_cached(uploaded_file):
    """Cache para el procesamiento de documentos"""
    return process_document(uploaded_file)

def connect_ai_with_key(key: str) -> bool:
    """Guarda la clave en sesión e inicializa el analizador IA."""
    try:
        if not key:
            return False
        st.session_state.gemini_api_key = key.strip()
        # Inicializa / re-inicializa el analizador con esa clave
        st.session_state.ai_analyzer = AIAnalyzer(api_key=st.session_state.gemini_api_key)
        st.session_state.ai_connected = True
        return True
    except Exception as e:
        st.error(f"❌ No se pudo conectar con IA: {e}")
        st.session_state.ai_connected = False
        return False

def ia_connected() -> bool:
    """True si hay analizador IA listo en sesión."""
    return st.session_state.get("ai_connected", False)

def initialize_ai():
    """Inicializa el analizador de IA"""
    try:
        if st.session_state.ai_analyzer is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key and api_key != "tu_clave_aqui":
                st.session_state.ai_analyzer = AIAnalyzer()
                st.session_state.ai_connected = True
                return True
            else:
                st.warning("⚠️ API Key de Google Gemini no configurada. Usando modo simulado.")
                st.session_state.ai_connected = False
                return False
        return st.session_state.ai_connected
    except Exception as e:
        st.error(f"❌ Error al inicializar IA: {str(e)}")
        st.session_state.ai_connected = False
        return False

def main():
    # Configurar página para mejor UX
    st.set_page_config(
        page_title="Sistema de Contestación Automática",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header compacto y funcional
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
        <h2 style='margin-bottom: 0; color: #1f77b4;'>🤖 Sistema de Contestación Automática</h2>
        <p style='margin-top: 0; color: #666; font-size: 14px;'>Análisis inteligente con IA para derechos de petición</p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background: #f0f2f6; border-radius: 10px;'>
            <strong>Paso {st.session_state.current_step}/5</strong><br>
            <small>Progreso: {st.session_state.progress}%</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if ia_connected():
            st.success("🤖 IA Conectada", icon="✅")
        else:
            st.warning("⚠️ Modo Simulado", icon="⚠️")
    
    st.divider()
    
    # Sidebar mejorado
    with st.sidebar:
        st.markdown("## 📋 Proceso de Análisis")
        
        # Barra de progreso visual
        progress_color = "#1f77b4" if st.session_state.progress < 100 else "#28a745"
        st.markdown(f"""
        <div style='background: #f0f2f6; border-radius: 10px; padding: 2px; margin: 10px 0;'>
            <div style='background: {progress_color}; height: 8px; border-radius: 8px; width: {st.session_state.progress}%; transition: width 0.3s;'></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pasos del proceso con mejor diseño
        steps = [
            ("📄 Cargar Documento", "Sube el derecho de petición", 1),
            ("🔍 Analizar", "IA analiza el contenido", 2),
            ("⚠️ Detectar Problemas", "IA identifica problemas", 3),
            ("💡 Recomendaciones", "IA sugiere respuestas", 4),
            ("💬 Chat", "Interactúa con la IA", 5)
        ]
        
        for icon_title, description, step_num in steps:
            if step_num < st.session_state.current_step:
                st.markdown(f"✅ **{icon_title}**")
                st.caption(description)
            elif step_num == st.session_state.current_step:
                st.markdown(f"🔄 **{icon_title}**", help="Paso actual")
                st.caption(description)
            else:
                st.markdown(f"⏳ {icon_title}")
                st.caption(description)
        
        st.divider()
        
        # Debug compacto
        with st.expander("🔧 Debug Info", expanded=False):
            st.caption(f"Paso: {st.session_state.current_step}")
            st.caption(f"Progreso: {st.session_state.progress}%")
            st.caption(f"IA: {'Conectada' if ia_connected() else 'Simulada'}")
    
    # Contenido principal con mejor espaciado
    st.markdown(f"## {get_step_title(st.session_state.current_step)}")
    
    if st.session_state.current_step == 1:
        step_1_upload_document()
    elif st.session_state.current_step == 2:
        step_2_analyze_document()
    elif st.session_state.current_step == 3:
        step_3_detect_problems()
    elif st.session_state.current_step == 4:
        step_4_generate_recommendations()
    elif st.session_state.current_step == 5:
        step_5_chat_system()
    else:
        st.error(f"❌ Paso no válido: {st.session_state.current_step}")
        st.session_state.current_step = 1
        st.rerun()

def get_step_title(step):
    """Retorna el título del paso actual"""
    titles = {
        1: "📄 Paso 1: Cargar Documento",
        2: "🔍 Paso 2: Análisis del Documento", 
        3: "⚠️ Paso 3: Detección de Problemas",
        4: "💡 Paso 4: Generar Recomendaciones",
        5: "💬 Paso 5: Chat con la IA"
    }
    return titles.get(step, f"Paso {step}")

def step_1_upload_document():
    # Configuración de API Key en un panel compacto
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🔑 Configuración de IA")
            api_key_input = st.text_input(
                "Google Gemini API Key",
                value=st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", "")),
                type="password",
                help="Ingresa tu API Key de Google Gemini",
                placeholder="AIzaSyB..."
            )
        with col2:
            st.markdown("### Acciones")
            if st.button("🔗 Conectar IA", type="primary", use_container_width=True):
                if connect_ai_with_key(api_key_input):
                    st.success("✅ IA conectada")
                else:
                    st.warning("⚠️ Error de conexión")
            if st.button("🗑️ Borrar clave", use_container_width=True):
                st.session_state.pop("gemini_api_key", None)
                st.session_state.pop("ai_analyzer", None)
                st.session_state.ai_connected = False
                st.info("Clave eliminada")
    
    st.divider()
    
    # Área de carga de archivos mejorada
    st.markdown("### 📄 Cargar Documento")
    uploaded_file = st.file_uploader(
        "Selecciona el documento (PDF o DOCX)",
        type=['pdf', 'docx'],
        help="Sube el derecho de petición que quieres analizar",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success(f"✅ Documento cargado: {uploaded_file.name}")
        
        # Procesar documento usando cache
        with st.spinner("Procesando documento..."):
            document_text = process_document_cached(uploaded_file)
            if document_text:
                st.session_state.document_text = document_text
                st.success("✅ Texto extraído correctamente")
                
                # Mostrar preview del texto
                with st.expander("📄 Vista previa del documento"):
                    st.text_area("Texto extraído:", document_text[:500] + "..." if len(document_text) > 500 else document_text, height=200)
            else:
                st.error("❌ Error al procesar el documento")
                return
        
        # Simular información del archivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tamaño", f"{uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.metric("Tipo", uploaded_file.type)
        with col3:
            st.metric("Fecha", datetime.now().strftime("%d/%m/%Y"))
        
        if st.button("🔍 Continuar al Análisis", type="primary"):
            st.session_state.current_step = 2
            st.session_state.progress = 20

def step_2_analyze_document():
    # Si el análisis no está completo, mostrar botón para iniciar
    if not st.session_state.get('analysis_complete', False):
        st.markdown("### 🔍 Iniciar Análisis")
        st.info("📋 El documento será analizado por la IA para identificar su contenido y estructura")
        
        if st.button("🔍 Iniciar Análisis con IA", type="primary", use_container_width=True):
            with st.spinner("Analizando documento con IA..."):
                # Simular tiempo de análisis
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                # Análisis con IA usando cache
                if initialize_ai() and st.session_state.document_text:
                    try:
                        analysis = st.session_state.ai_analyzer.analyze_document(st.session_state.document_text)
                        if analysis:
                            st.session_state.analysis = analysis
                        else:
                            raise Exception("No se pudo obtener análisis")
                    except Exception as e:
                        error_msg = str(e)
                        if "Cuota de Google Gemini excedida" in error_msg:
                            st.error(f"❌ {error_msg}")
                            st.info("💡 La aplicación continuará en modo simulado. Puedes:")
                            st.info("• Verificar tu cuota en https://makersuite.google.com/app/apikey")
                            st.info("• Gemini tiene cuota gratuita generosa")
                            st.info("• Usar la aplicación en modo simulado")
                        else:
                            st.error(f"❌ Error en análisis IA: {error_msg}")
                        
                        # Fallback a análisis simulado
                        analysis = {
                            "tipo_documento": "Derecho de Petición",
                            "longitud": len(st.session_state.document_text),
                            "confianza": 0.7,
                            "palabras_clave": ["petición", "derecho"],
                            "fecha_analisis": datetime.now().strftime("%d/%m/%Y"),
                            "error": str(e)
                        }
                        st.session_state.analysis = analysis
                else:
                    # Análisis simulado
                    analysis = {
                        "tipo_documento": "Derecho de Petición",
                        "longitud": len(st.session_state.document_text) if st.session_state.document_text else 0,
                        "confianza": 0.85,
                        "palabras_clave": ["petición", "derecho", "solicitud"],
                        "fecha_analisis": datetime.now().strftime("%d/%m/%Y")
                    }
                    st.session_state.analysis = analysis
                
                st.success("✅ Análisis completado")
                st.session_state.analysis_complete = True
                st.rerun()
    
    # Si el análisis está completo, mostrar resultados y botón para continuar
    if st.session_state.get('analysis_complete', False):
        st.success("✅ Análisis completado exitosamente")
        
        # Resultados del análisis en un panel mejorado
        with st.container():
            st.markdown("### 📊 Resultados del Análisis")
            
            # Métricas del análisis en cards uniformes
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='margin: 0; color: #1f77b4;'>Tipo</h4>
                    <p style='margin: 5px 0; font-size: 16px; line-height: 1.4;'>{st.session_state.analysis.get("tipo_documento", "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='margin: 0; color: #1f77b4;'>Longitud</h4>
                    <p style='margin: 5px 0; font-size: 16px; line-height: 1.4;'>{st.session_state.analysis.get('longitud', 0)} caracteres</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                confianza = st.session_state.analysis.get('confianza', 0)
                color = "#28a745" if confianza > 0.7 else "#ffc107" if confianza > 0.5 else "#dc3545"
                st.markdown(f"""
                <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='margin: 0; color: #1f77b4;'>Confianza</h4>
                    <p style='margin: 5px 0; font-size: 16px; color: {color}; line-height: 1.4;'>{confianza:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                    <h4 style='margin: 0; color: #1f77b4;'>Fecha</h4>
                    <p style='margin: 5px 0; font-size: 16px; line-height: 1.4;'>{st.session_state.analysis.get("fecha_analisis", "N/A")}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Palabras clave en un panel separado
            if 'palabras_clave' in st.session_state.analysis:
                st.markdown("### 🔑 Palabras Clave Identificadas")
                keywords = st.session_state.analysis['palabras_clave']
                for keyword in keywords:
                    st.markdown(f"• **{keyword}**")
        
        st.divider()
        
        # Botón para continuar al siguiente paso
        if st.button("⚠️ Continuar a Detección de Problemas", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.session_state.progress = 40
            st.rerun()

def step_3_detect_problems():
    # Si los problemas no están detectados, mostrar botón para iniciar
    if not st.session_state.get('problems_detected', False):
        st.markdown("### ⚠️ Detectar Problemas")
        st.info("📋 La IA analizará el documento para identificar problemas formales y materiales que requieren atención")
        
        if st.button("⚠️ Detectar Problemas con IA", type="primary", use_container_width=True):
            with st.spinner("Detectando problemas con IA..."):
                time.sleep(1.5)
                
                # Detección con IA usando cache
                if initialize_ai() and st.session_state.document_text and 'analysis' in st.session_state:
                    try:
                        problems = st.session_state.ai_analyzer.detect_problems(
                            st.session_state.document_text, 
                            st.session_state.analysis
                        )
                        if problems:
                            st.session_state.problems = problems
                        else:
                            raise Exception("No se pudieron detectar problemas")
                    except Exception as e:
                        st.error(f"❌ Error en detección IA: {str(e)}")
                        # Fallback a problemas simulados
                        problems = [
                            {
                                "tipo": "Error de análisis",
                                "descripcion": f"Error al procesar con IA: {str(e)}",
                                "severidad": "Media",
                                "linea": "N/A"
                            }
                        ]
                        st.session_state.problems = problems
                else:
                    # Problemas simulados
                    problems = [
                        {
                            "tipo": "Falta información",
                            "descripcion": "No se especifica claramente la autoridad requerida",
                            "severidad": "Media",
                            "linea": "N/A"
                        },
                        {
                            "tipo": "Formato",
                            "descripcion": "El documento no tiene número de radicado",
                            "severidad": "Alta",
                            "linea": "N/A"
                        },
                        {
                            "tipo": "Fundamentación",
                            "descripcion": "No se cita la normativa aplicable",
                            "severidad": "Baja",
                            "linea": "N/A"
                        }
                    ]
                    st.session_state.problems = problems
                
                st.success("✅ Problemas detectados")
                st.session_state.problems_detected = True
                st.rerun()
    
    # Si los problemas están detectados, mostrar resultados y botón para continuar
    if st.session_state.get('problems_detected', False):
        st.success("✅ Problemas detectados exitosamente")
        
        # Mostrar problemas con información detallada
        st.markdown("### 📋 Problemas Identificados")
        for i, problem in enumerate(st.session_state.problems, 1):
            # Validar que problem sea un diccionario
            if not isinstance(problem, dict):
                st.warning(f"⚠️ Problema {i} tiene formato inválido: {type(problem)}")
                continue
            
            # Obtener valores con validación
            tipo = problem.get('tipo', f'Problema {i}')
            descripcion = problem.get('descripcion', 'Sin descripción')
            severidad = problem.get('severidad', 'N/A')
            
            # Color según severidad
            if severidad == "Alta":
                st.error(f"**{tipo}** - {descripcion}")
            elif severidad == "Media":
                st.warning(f"**{tipo}** - {descripcion}")
            else:
                st.info(f"**{tipo}** - {descripcion}")
            
            # Información detallada
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"**Tipo:** {tipo}")
                st.caption(f"**Severidad:** {severidad}")
                if 'fundamento_legal' in problem:
                    st.caption(f"**Fundamento:** {problem['fundamento_legal']}")
            with col2:
                st.caption(f"**Línea:** {problem.get('linea', 'N/A')}")
                if 'impacto' in problem:
                    st.caption(f"**Impacto:** {problem['impacto']}")
            
            st.divider()
        
        st.divider()
        
        # Botón para continuar al siguiente paso
        if st.button("💡 Continuar a Recomendaciones", type="primary", use_container_width=True):
            st.session_state.current_step = 4
            st.session_state.progress = 60
            st.rerun()

def step_4_generate_recommendations():
    # Si las recomendaciones no están generadas, mostrar botón para iniciar
    if not st.session_state.get('recommendations_generated', False):
        st.markdown("### 💡 Generar Recomendaciones")
        st.info("📋 La IA analizará los problemas detectados y generará recomendaciones específicas para mejorar la contestación")
        
        if st.button("💡 Generar Recomendaciones con IA", type="primary", use_container_width=True):
            with st.spinner("Generando recomendaciones con IA..."):
                time.sleep(1.5)
                
                # Generación con IA usando cache
                if initialize_ai() and st.session_state.document_text and 'problems' in st.session_state:
                    try:
                        recommendations = st.session_state.ai_analyzer.generate_recommendations(
                            st.session_state.document_text,
                            st.session_state.problems
                        )
                        if recommendations:
                            st.session_state.recommendations = recommendations
                        else:
                            raise Exception("No se pudieron generar recomendaciones")
                    except Exception as e:
                        st.error(f"❌ Error en generación IA: {str(e)}")
                        # Fallback a recomendaciones simuladas
                        recommendations = [
                            {
                                "titulo": "Fundamentación legal",
                                "descripcion": "Incluir citas específicas de la normativa aplicable",
                                "prioridad": "Alta",
                                "accion": "Referenciar Código de Procedimiento Administrativo"
                            },
                            {
                                "titulo": "Estructurar respuesta",
                                "descripcion": "Organizar la contestación en secciones claras",
                                "prioridad": "Media",
                                "accion": "Usar formato estructurado"
                            }
                        ]
                        st.session_state.recommendations = recommendations
                else:
                    # Recomendaciones simuladas
                    recommendations = [
                        {
                            "titulo": "Fundamentación legal",
                            "descripcion": "Incluir citas específicas de la normativa aplicable",
                            "prioridad": "Alta",
                            "accion": "Referenciar Código de Procedimiento Administrativo"
                        },
                        {
                            "titulo": "Estructurar respuesta",
                            "descripcion": "Organizar la contestación en secciones claras",
                            "prioridad": "Media",
                            "accion": "Usar formato estructurado"
                        }
                    ]
                    st.session_state.recommendations = recommendations
                
                st.success("✅ Recomendaciones generadas")
                
                # Mostrar recomendaciones con información detallada
                for i, rec in enumerate(st.session_state.recommendations, 1):
                    # Validar que rec sea un diccionario
                    if not isinstance(rec, dict):
                        st.warning(f"⚠️ Recomendación {i} tiene formato inválido: {type(rec)}")
                        continue
                    
                    # Obtener valores con validación
                    titulo = rec.get('titulo', f'Recomendación {i}')
                    descripcion = rec.get('descripcion', 'Sin descripción')
                    prioridad = rec.get('prioridad', 'N/A')
                    accion = rec.get('accion', 'N/A')
                    
                    # Color según prioridad
                    if prioridad == "Alta":
                        st.success(f"**{titulo}** - {descripcion}")
                    else:
                        st.info(f"**{titulo}** - {descripcion}")
                    
                    # Información detallada
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"**Prioridad:** {prioridad}")
                        st.caption(f"**Acción:** {accion}")
                        if 'fundamento_legal' in rec:
                            st.caption(f"**Fundamento:** {rec['fundamento_legal']}")
                    with col2:
                        if 'tiempo_estimado' in rec:
                            st.caption(f"**Tiempo:** {rec['tiempo_estimado']}")
                        if 'beneficio' in rec:
                            st.caption(f"**Beneficio:** {rec['beneficio']}")
                    
                    st.divider()
                
                st.session_state.recommendations_generated = True
                st.rerun()
    
    # Si las recomendaciones están generadas, mostrar resultados y botón para continuar
    if st.session_state.get('recommendations_generated', False):
        st.success("✅ Recomendaciones generadas exitosamente")
        
        # Mostrar recomendaciones con información detallada
        st.markdown("### 📋 Recomendaciones Generadas")
        for i, rec in enumerate(st.session_state.recommendations, 1):
            # Validar que rec sea un diccionario
            if not isinstance(rec, dict):
                st.warning(f"⚠️ Recomendación {i} tiene formato inválido: {type(rec)}")
                continue
            
            # Obtener valores con validación
            titulo = rec.get('titulo', f'Recomendación {i}')
            descripcion = rec.get('descripcion', 'Sin descripción')
            prioridad = rec.get('prioridad', 'N/A')
            accion = rec.get('accion', 'N/A')
            
            # Color según prioridad
            if prioridad == "Alta":
                st.success(f"**{titulo}** - {descripcion}")
            else:
                st.info(f"**{titulo}** - {descripcion}")
            
            # Información detallada
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"**Prioridad:** {prioridad}")
                st.caption(f"**Acción:** {accion}")
                if 'fundamento_legal' in rec:
                    st.caption(f"**Fundamento:** {rec['fundamento_legal']}")
            with col2:
                if 'tiempo_estimado' in rec:
                    st.caption(f"**Tiempo:** {rec['tiempo_estimado']}")
                if 'beneficio' in rec:
                    st.caption(f"**Beneficio:** {rec['beneficio']}")
            
            st.divider()
        
        st.divider()
        
        # Botón para continuar al siguiente paso
        if st.button("💬 Continuar al Chat", type="primary", key="continue_to_chat", use_container_width=True):
            # Debug: Mostrar el cambio de paso
            st.info(f"🔄 Cambiando de paso {st.session_state.current_step} a paso 5")
            
            # Actualizar estado
            st.session_state.current_step = 5
            st.session_state.progress = 80
            
            # Debug: Confirmar el cambio
            st.success(f"✅ Paso actualizado a: {st.session_state.current_step}")
            
            # Forzar rerun para actualizar la interfaz
            st.rerun()

def step_5_chat_system():
    st.markdown("## 💬 Paso 5: Chat con la IA")
    
    # Asegurar que chat_history esté inicializado
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.info("💡 Puedes hacer preguntas sobre el análisis, problemas o recomendaciones")
    
    # Mostrar contexto disponible
    with st.expander("📋 Contexto Disponible"):
        if 'analysis' in st.session_state:
            st.success("✅ Análisis del documento disponible")
        if 'problems' in st.session_state:
            st.success(f"✅ {len(st.session_state.problems)} problemas detectados")
        if 'recommendations' in st.session_state:
            st.success(f"✅ {len(st.session_state.recommendations)} recomendaciones generadas")
    
    # Chat input con mejor UX
    col1, col2 = st.columns([3, 1])
    with col1:
        user_question = st.text_input(
            "Escribe tu pregunta:", 
            placeholder="Ej: ¿Cómo mejorar la contestación? ¿Qué problemas son más críticos? ¿Cómo implementar las recomendaciones?",
            key="chat_input"
        )
    with col2:
        send_button = st.button("💬 Enviar", type="primary", use_container_width=True)
    
    # Procesar pregunta cuando se envía
    if send_button and user_question and user_question.strip():
            with st.spinner("Procesando tu pregunta con IA..."):
                time.sleep(1)
                
                # Respuesta con IA
                if initialize_ai() and 'analysis' in st.session_state:
                    try:
                        context = {
                            "analisis": st.session_state.analysis,
                            "problemas": st.session_state.problems if 'problems' in st.session_state else [],
                            "recomendaciones": st.session_state.recommendations if 'recommendations' in st.session_state else []
                        }
                        response = st.session_state.ai_analyzer.chat_response(user_question, context)
                    except Exception as e:
                        response = f"Lo siento, hubo un error al procesar tu pregunta: {str(e)}"
                else:
                    # Respuestas simuladas mejoradas
                    responses = [
                        "Gracias por tu pregunta. Basándome en el análisis del documento, puedo ayudarte con información sobre los problemas detectados y las recomendaciones generadas.",
                        "El sistema ha identificado varios problemas en el documento que requieren atención. Te recomiendo revisar las recomendaciones generadas para mejorar la contestación.",
                        "Basándome en el análisis realizado, puedo sugerir que consideres incluir fundamentación legal específica y citar las normas aplicables.",
                        "Para una contestación más efectiva, asegúrate de especificar claramente la competencia de la entidad y fundamentar adecuadamente las decisiones.",
                        "Según el análisis del documento, es importante estructurar la respuesta de manera clara y concisa, incluyendo todos los elementos requeridos por la normativa vigente.",
                        "El sistema detectó que faltan elementos importantes en el documento. Te sugiero revisar las recomendaciones para asegurar una contestación completa y conforme a la ley."
                    ]
                    response = random.choice(responses)
                
                # Agregar al historial
                st.session_state.chat_history.append({
                    "user": user_question,
                    "system": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Limpiar el input después de enviar
                st.rerun()
    
    # Mostrar historial de chat mejorado
    if st.session_state.chat_history:
        st.markdown("### 📝 Historial del Chat")
        
        # Mostrar la conversación más reciente primero
        for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
            with st.expander(f"💬 Conversación {len(st.session_state.chat_history) - i + 1} - {chat.get('timestamp', '')}"):
                st.markdown(f"**👤 Usuario:** {chat['user']}")
                st.markdown(f"**🤖 IA:** {chat['system']}")
    
    # Sugerencias de preguntas
    st.markdown("### 💡 Sugerencias de Preguntas")
    suggestions = [
        "¿Cuáles son los problemas más críticos del documento?",
        "¿Cómo puedo mejorar la fundamentación legal?",
        "¿Qué recomendaciones son prioritarias?",
        "¿Cómo estructurar mejor la contestación?",
        "¿Qué normativa debo citar específicamente?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                # Simular que se hace clic en la sugerencia
                st.session_state.suggested_question = suggestion
                st.rerun()
    
    # Botón para reiniciar
    st.divider()
    if st.button("🔄 Reiniciar Proceso", type="secondary"):
        # Limpiar cache
        process_document_cached.clear()
        
        # Resetear estado
        st.session_state.current_step = 1
        st.session_state.progress = 0
        st.session_state.chat_history = []
        st.session_state.uploaded_file = None
        st.session_state.document_text = None
        st.session_state.analysis_complete = False
        st.session_state.problems_detected = False
        st.session_state.recommendations_generated = False
        st.session_state.ai_connected = False
        st.rerun()

if __name__ == "__main__":
    main() 