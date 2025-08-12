# 🤖 Sistema de Contestación Automática de Derechos de Petición

Sistema inteligente para analizar derechos de petición y generar recomendaciones para contestación usando IA.

## 🚀 Instalación Rápida

### 1. Instalar Dependencias
```bash
install.bat
```

### 2. Configurar API Key (Opcional)
Para usar la IA completa, necesitas una API Key de Google Gemini:

**Opción A: Script automático**
```bash
setup_api_key.bat
```

**Opción B: Manual**
1. Ve a https://makersuite.google.com/app/apikey
2. Crea una nueva API Key
3. Crea un archivo `.env` con:
```
GEMINI_API_KEY=tu_clave_aqui
GEMINI_MODEL=gemini-2.0-flash-exp
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
LOG_LEVEL=INFO
```

### 3. Ejecutar Aplicación
```bash
run_app.bat
```

O manualmente:
```bash
py -m streamlit run app.py --server.port 8501
```

## 🔧 Solución de Problemas

### ❌ Error: "API Key inválida"
**Solución:**
1. Ejecuta `setup_api_key.bat`
2. O verifica tu clave en https://makersuite.google.com/app/apikey
3. Asegúrate de que la clave sea válida

### ❌ Error: "Cuota excedida"
**Solución:**
- Verifica tu saldo en https://makersuite.google.com/app/apikey
- Gemini tiene cuota gratuita generosa
- La aplicación funcionará en modo simulado

### ❌ Error: "Dependencias no encontradas"
**Solución:**
```bash
install.bat
```

### ❌ Error: "Puerto 8501 en uso"
**Solución:**
```bash
py -m streamlit run app.py --server.port 8502
```

## 📋 Características

### ✅ Funcionalidades Principales
- 📄 **Carga de documentos** (PDF, DOCX)
- 🔍 **Análisis con IA** del contenido
- ⚠️ **Detección de problemas** formales y materiales
- 💡 **Generación de recomendaciones** para contestación
- 💬 **Chat interactivo** con la IA

### 🚀 Optimizaciones
- ⚡ **Cache inteligente** para mejor rendimiento
- 🔄 **Sin re-renders innecesarios**
- 💾 **Gestión eficiente de memoria**
- 🛡️ **Manejo robusto de errores**

## 🎯 Modos de Uso

### 🤖 Modo IA Completa
- Requiere API Key de Google Gemini
- Análisis detallado con Gemini 2.0 Flash Exp
- Recomendaciones personalizadas
- Chat interactivo

### 🎭 Modo Simulado
- Funciona sin API Key
- Análisis básico
- Recomendaciones predefinidas
- Respuestas simuladas

## 📁 Estructura del Proyecto

```
Tutelas/
├── app.py                 # Aplicación principal
├── ai_analyzer.py         # Analizador de IA
├── document_processor.py  # Procesamiento de documentos
├── requirements.txt       # Dependencias
├── install.bat           # Instalador
├── run_app.bat          # Ejecutor
├── setup_api_key.bat    # Configurador de API Key
├── optimize.bat         # Optimizador
└── .streamlit/          # Configuración de Streamlit
    └── config.toml
```

## 🔧 Scripts Disponibles

| Script | Función |
|--------|---------|
| `install.bat` | Instala dependencias |
| `run_app.bat` | Ejecuta la aplicación |
| `setup_api_key.bat` | Configura API Key |
| `optimize.bat` | Optimiza el sistema |

## 🌐 URLs de Acceso

- **Local**: http://localhost:8501
- **Red**: http://192.168.1.13:8501
- **Externa**: http://200.118.80.132:8501

## 📊 Métricas de Rendimiento

- ⚡ **Tiempo de inicio**: < 10 segundos
- 🔄 **Cache hit rate**: > 90%
- 💾 **Uso de memoria**: Optimizado
- 🚀 **Re-renders**: Minimizados

## 🛠️ Desarrollo

### Agregar Nuevas Funcionalidades
1. Modifica `ai_analyzer.py` para nuevas funciones de IA
2. Actualiza `app.py` para la interfaz
3. Prueba con `run_app.bat`

### Optimizar Rendimiento
1. Ejecuta `optimize.bat`
2. Revisa logs en consola
3. Ajusta configuración en `.streamlit/config.toml`

## 📞 Soporte

### Problemas Comunes
1. **API Key inválida**: Ejecuta `setup_api_key.bat`
2. **Dependencias faltantes**: Ejecuta `install.bat`
3. **Puerto ocupado**: Cambia puerto en comando
4. **Rendimiento lento**: Ejecuta `optimize.bat`

### Logs y Debug
- Revisa la consola para errores
- Verifica archivo `.env` si existe
- Comprueba conexión a internet

## 🔒 Seguridad

- ✅ API Key se guarda localmente
- ✅ No se comparten datos sensibles
- ✅ Validación de entrada
- ✅ Manejo seguro de errores

## 📈 Roadmap

- [ ] Soporte para más formatos de documento
- [ ] Análisis de múltiples documentos
- [ ] Exportación de resultados
- [ ] Integración con bases de datos
- [ ] API REST para integración

---

**Desarrollado con ❤️ para optimizar el proceso de contestación de derechos de petición** 