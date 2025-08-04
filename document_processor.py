# document_processor.py
import PyPDF2
import docx2txt
import tempfile
import os
import streamlit as st
from typing import Optional
import io

@st.cache_data
def _read_pdf_cached(file_content: bytes) -> str:
    """Extrae texto de un PDF con cache para mejor rendimiento."""
    try:
        file_stream = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(file_stream)
        texto = []
        for page in reader.pages:
            content = page.extract_text() or ""
            if content.strip():  # Solo agregar páginas con contenido
                texto.append(content)
        return "\n".join(texto).strip()
    except Exception as e:
        st.error(f"Error leyendo PDF: {e}")
        return ""

@st.cache_data
def _read_docx_cached(file_content: bytes) -> str:
    """Extrae texto de un DOCX con cache para mejor rendimiento."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        texto = docx2txt.process(tmp_path) or ""
        os.unlink(tmp_path)  # Limpiar archivo temporal
        return texto.strip()
    except Exception as e:
        st.error(f"Error leyendo DOCX: {e}")
        return ""

def process_document(file) -> Optional[str]:
    """
    Procesa un archivo subido (Streamlit UploadedFile) y devuelve texto.
    Soporta PDF y DOCX. Devuelve None si no se pudo extraer texto.
    Optimizado con cache para mejor rendimiento.
    """
    if not file:
        return None

    try:
        # Leer el contenido del archivo una sola vez
        file.seek(0)
        file_content = file.read()
        
        if file.type == "application/pdf":
            texto = _read_pdf_cached(file_content)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            texto = _read_docx_cached(file_content)
        else:
            st.warning(f"Tipo de archivo no soportado: {file.type}")
            return None

        # Validar que se extrajo texto
        texto = (texto or "").strip()
        if not texto:
            st.warning("No se pudo extraer texto del documento. Verifica que el archivo contenga texto legible.")
            return None
            
        return texto
        
    except Exception as e:
        st.error(f"Error procesando documento: {e}")
        return None 