#!/usr/bin/env python3
"""
Script para configurar la API Key de Gemini 2.0 Flash
"""

import os
import streamlit as st

def setup_gemini():
    """Configura la API Key de Gemini"""
    st.title("🔑 Configuración de Gemini 2.0 Flash")
    
    st.markdown("""
    ### 📋 Pasos para obtener tu API Key:
    
    1. **Ve a Google AI Studio**: https://makersuite.google.com/app/apikey
    2. **Inicia sesión** con tu cuenta de Google
    3. **Crea una nueva API Key** o usa una existente
    4. **Copia la clave** (empieza con 'AIzaSy...')
    
    ### ⚠️ Importante:
    - La API Key es gratuita con cuota generosa
    - No compartas tu clave públicamente
    - Puedes revocar la clave en cualquier momento
    """)
    
    # Input para API Key
    api_key = st.text_input(
        "🔑 Tu API Key de Gemini:",
        type="password",
        placeholder="AIzaSy...",
        help="Pega tu API Key de Google AI Studio aquí"
    )
    
    if st.button("✅ Configurar Gemini", type="primary"):
        if api_key and api_key.startswith("AIzaSy"):
            # Guardar en .env
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"GEMINI_API_KEY={api_key}\n")
            
            st.success("✅ API Key configurada correctamente!")
            st.info("🔄 Reinicia la aplicación para que los cambios tomen efecto")
            
            # Mostrar información de uso
            st.markdown("""
            ### 🚀 Funcionalidades disponibles:
            
            - **Chat inteligente** con Gemini 2.0 Flash
            - **Análisis de documentos** con IA avanzada
            - **Respuestas contextualizadas** y actualizadas
            - **Fallback automático** si hay problemas de conectividad
            
            ### 📱 Próximos pasos:
            1. Reinicia la aplicación principal
            2. Ve al Paso 5 (Chat)
            3. Haz preguntas sobre derecho administrativo
            4. Disfruta de respuestas inteligentes con Gemini
            """)
            
        elif api_key:
            st.error("❌ API Key inválida. Debe empezar con 'AIzaSy...'")
        else:
            st.error("❌ Por favor ingresa tu API Key")
    
    # Mostrar estado actual
    st.divider()
    st.markdown("### 📊 Estado Actual:")
    
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                env_content = f.read()
                if "GEMINI_API_KEY=" in env_content:
                    st.success("✅ API Key configurada en .env")
                    # Mostrar solo los primeros caracteres por seguridad
                    key_line = [line for line in env_content.split('\n') if line.startswith('GEMINI_API_KEY=')][0]
                    api_key_value = key_line.split('=')[1]
                    if api_key_value:
                        st.info(f"🔑 Clave configurada: {api_key_value[:10]}...{api_key_value[-4:]}")
                    else:
                        st.warning("⚠️ API Key vacía en .env")
                else:
                    st.warning("⚠️ No se encontró GEMINI_API_KEY en .env")
        except Exception as e:
            st.error(f"❌ Error leyendo .env: {str(e)}")
    else:
        st.warning("⚠️ Archivo .env no encontrado")
    
    # Botón para reiniciar
    if st.button("🔄 Reiniciar Aplicación"):
        st.info("🔄 Por favor, detén la aplicación actual y ejecuta 'py -m streamlit run app.py' nuevamente")

if __name__ == "__main__":
    setup_gemini()
