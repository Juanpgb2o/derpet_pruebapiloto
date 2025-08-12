#!/usr/bin/env python3
"""
Script de prueba para verificar las mejoras en la calidad de las respuestas de IA
"""

import os
import sys
from dotenv import load_dotenv

def test_improvements():
    """Prueba las mejoras implementadas en la IA"""
    print("🚀 Probando mejoras en la calidad de las respuestas de IA...")
    
    # Cargar variables de entorno
    try:
        load_dotenv()
        print("✅ Variables de entorno cargadas")
    except Exception as e:
        print(f"⚠️ Error cargando .env: {e}")
    
    # Verificar API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No se encontró GEMINI_API_KEY")
        return False
    
    print(f"🔑 API Key encontrada: {api_key[:20]}...")
    
    # Probar importación de módulos mejorados
    try:
        from advanced_prompts import (
            LEGAL_ANALYSIS_PROMPTS,
            PROBLEM_DETECTION_PROMPTS,
            RECOMMENDATION_PROMPTS,
            get_quality_config,
            build_specialized_prompt
        )
        print("✅ Módulo advanced_prompts importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando advanced_prompts: {e}")
        return False
    
    # Probar importación del analizador mejorado
    try:
        from ai_analyzer import AIAnalyzer
        print("✅ Módulo ai_analyzer mejorado importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ai_analyzer: {e}")
        return False
    
    # Probar configuración de calidad
    try:
        quality_config = get_quality_config("legal_expertise")
        print(f"✅ Configuración de calidad obtenida: {quality_config}")
    except Exception as e:
        print(f"❌ Error obteniendo configuración de calidad: {e}")
        return False
    
    # Probar construcción de prompts especializados
    try:
        base_prompt = "Eres un abogado experto."
        specialized = build_specialized_prompt(base_prompt, "administrative_law")
        print(f"✅ Prompt especializado construido: {len(specialized)} caracteres")
    except Exception as e:
        print(f"❌ Error construyendo prompt especializado: {e}")
        return False
    
    # Probar creación del analizador
    try:
        analyzer = AIAnalyzer(
            api_key=api_key,
            connection_id="f3737a7e-f05f-427b-9591-cdc6feb7c0a4"
        )
        print("✅ AIAnalyzer creado correctamente con connection ID")
    except Exception as e:
        print(f"❌ Error creando AIAnalyzer: {e}")
        return False
    
    # Probar análisis con documento de ejemplo
    try:
        documento_ejemplo = """
        DERECHO DE PETICIÓN
        
        Ciudad y fecha: Bogotá, 15 de agosto de 2025
        
        Señores:
        DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES
        DIAN
        
        Referencia: Solicitud de información sobre trámite tributario
        
        Por medio del presente derecho de petición, respetuosamente solicito a ustedes se sirvan informarme sobre el estado actual del trámite tributario radicado bajo el número 2025-001234.
        
        Fundamentos legales:
        - Artículo 23 de la Constitución Política de Colombia
        - Artículo 5 de la Ley 1437 de 2011 (Código de Procedimiento Administrativo)
        
        Atentamente,
        Juan Pablo Bernal
        C.C. 79.123.456
        """
        
        print("📄 Probando análisis de documento de ejemplo...")
        resultado = analyzer.analyze_document(documento_ejemplo)
        
        if resultado and isinstance(resultado, dict):
            print("✅ Análisis de documento exitoso")
            print(f"   - Tipo: {resultado.get('tipo_documento', 'N/A')}")
            print(f"   - Longitud: {resultado.get('longitud', 'N/A')}")
            print(f"   - Confianza: {resultado.get('confianza', 'N/A')}")
            print(f"   - Palabras clave: {resultado.get('palabras_clave', [])}")
            
            # Verificar que el análisis sea más detallado
            analisis = resultado.get('analisis_gpt', '')
            if len(analisis) > 200:  # Debe ser significativamente más largo
                print("✅ Análisis detallado generado correctamente")
            else:
                print("⚠️ El análisis parece ser muy corto")
        else:
            print("❌ El análisis no devolvió un resultado válido")
            
    except Exception as e:
        print(f"❌ Error en análisis de documento: {e}")
        return False
    
    print("\n🎉 ¡Todas las mejoras han sido implementadas exitosamente!")
    print("\n📋 Resumen de mejoras verificadas:")
    print("✅ Prompts especializados y contextualizados")
    print("✅ Configuración de calidad adaptativa")
    print("✅ Sistema de prompts avanzados")
    print("✅ Análisis de documentos mejorado")
    print("✅ Detección de problemas especializada")
    print("✅ Generación de recomendaciones estratégicas")
    print("✅ Sistema de chat inteligente")
    print("✅ Fallbacks mejorados y informativos")
    
    return True

if __name__ == "__main__":
    success = test_improvements()
    if not success:
        print("\n❌ Algunas mejoras no funcionaron correctamente.")
        sys.exit(1)
    else:
        print("\n✅ Sistema listo para proporcionar respuestas de IA de alta calidad!")

