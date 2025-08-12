#!/usr/bin/env python3
"""
Script para verificar la lectura del archivo .env
"""

import os
from dotenv import load_dotenv

def test_env_reading():
    """Prueba la lectura del archivo .env"""
    print("🔍 VERIFICANDO LECTURA DEL ARCHIVO .ENV")
    print("=" * 60)
    
    # 1. Verificar si el archivo existe
    print("📁 VERIFICACIÓN DEL ARCHIVO:")
    print("-" * 40)
    if os.path.exists(".env"):
        print("   ✅ Archivo .env encontrado")
        size = os.path.getsize(".env")
        print(f"   📏 Tamaño: {size} bytes")
        
        # Leer contenido del archivo
        try:
            with open(".env", "r", encoding="utf-8") as f:
                content = f.read()
                print(f"   📄 Contenido: {content}")
        except Exception as e:
            print(f"   ❌ Error leyendo archivo: {str(e)}")
    else:
        print("   ❌ Archivo .env no encontrado")
    
    print()
    
    # 2. Verificar variables de entorno del sistema
    print("🌐 VARIABLES DE ENTORNO DEL SISTEMA:")
    print("-" * 40)
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        print(f"   ✅ GEMINI_API_KEY en sistema: {gemini_key[:20]}...{gemini_key[-4:]}")
    else:
        print("   ❌ GEMINI_API_KEY no encontrada en sistema")
    
    print()
    
    # 3. Probar load_dotenv()
    print("📖 PRUEBA DE LOAD_DOTENV():")
    print("-" * 40)
    try:
        # Cargar .env
        load_dotenv()
        print("   ✅ load_dotenv() ejecutado sin errores")
        
        # Verificar si se cargó la variable
        gemini_key_loaded = os.getenv("GEMINI_API_KEY")
        if gemini_key_loaded:
            print(f"   ✅ GEMINI_API_KEY cargada: {gemini_key_loaded[:20]}...{gemini_key_loaded[-4:]}")
        else:
            print("   ❌ GEMINI_API_KEY no se cargó")
            
    except Exception as e:
        print(f"   ❌ Error en load_dotenv(): {str(e)}")
    
    print()
    
    # 4. Verificar encoding del archivo
    print("🔤 VERIFICACIÓN DE ENCODING:")
    print("-" * 40)
    try:
        # Probar diferentes encodings
        encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
        
        for encoding in encodings:
            try:
                with open(".env", "r", encoding=encoding) as f:
                    content = f.read()
                    if "GEMINI_API_KEY=" in content:
                        print(f"   ✅ Encoding {encoding}: Funciona")
                        print(f"      Contenido: {content}")
                        break
                    else:
                        print(f"   ⚠️ Encoding {encoding}: No contiene la clave")
            except Exception as e:
                print(f"   ❌ Encoding {encoding}: Error - {str(e)}")
                
    except Exception as e:
        print(f"   ❌ Error general: {str(e)}")
    
    print()
    
    # 5. Verificar si hay caracteres ocultos
    print("👁️ VERIFICACIÓN DE CARACTERES OCULTOS:")
    print("-" * 40)
    try:
        with open(".env", "rb") as f:
            raw_content = f.read()
            print(f"   📊 Bytes totales: {len(raw_content)}")
            print(f"   🔍 Bytes en hex: {raw_content.hex()[:100]}...")
            
            # Buscar caracteres especiales
            if b'\x00' in raw_content:
                print("   ⚠️ Contiene caracteres NULL")
            if b'\xff' in raw_content:
                print("   ⚠️ Contiene BOM UTF-8")
            if b'\xef\xbb\xbf' in raw_content:
                print("   ⚠️ Contiene BOM UTF-8")
                
    except Exception as e:
        print(f"   ❌ Error leyendo bytes: {str(e)}")

if __name__ == "__main__":
    test_env_reading()
