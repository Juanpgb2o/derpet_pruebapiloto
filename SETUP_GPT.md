# 🤖 Configuración de GPT para el Sistema de Derechos de Petición

## 📋 Requisitos Previos

### 1. Cuenta de OpenAI
- Ve a [OpenAI Platform](https://platform.openai.com/)
- Crea una cuenta o inicia sesión
- Verifica tu cuenta (requerido para usar la API)

### 2. API Key
- Ve a [API Keys](https://platform.openai.com/api-keys)
- Crea una nueva API Key
- **⚠️ IMPORTANTE**: Guarda la clave de forma segura, no la compartas

## 🔧 Configuración

### Opción 1: Archivo .env (Recomendado)

1. Crea un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=sk-tu_api_key_aqui
```

2. Ejecuta la aplicación:
```bash
streamlit run app.py
```

### Opción 2: Configuración en la Aplicación

1. Ejecuta la aplicación:
```bash
streamlit run app.py
```

2. En el Paso 1, expande "🔑 Configuración de OpenAI API Key"
3. Ingresa tu API Key en el campo de texto
4. La aplicación se configurará automáticamente

## 🧪 Prueba de Configuración

### Verificar Conexión
1. Abre la aplicación en tu navegador
2. En el sidebar, verifica que aparezca:
   - ✅ **IA Conectada**
   - **Usando GPT-3.5-turbo**

### Probar Funcionalidad
1. Sube un documento de prueba (PDF o DOCX)
2. Ve al Paso 2: Análisis
3. Haz clic en "🔍 Iniciar Análisis con IA"
4. Deberías ver análisis detallado de GPT

## 🔒 Seguridad

### Buenas Prácticas
- ✅ Nunca compartas tu API Key
- ✅ No subas el archivo `.env` a repositorios públicos
- ✅ Usa variables de entorno en producción
- ✅ Rota las API Keys regularmente

### Archivo .gitignore
Asegúrate de que tu `.gitignore` incluya:
```
.env
*.env
config.env
```

## 💰 Costos

### Precios de OpenAI (GPT-3.5-turbo)
- **Input**: $0.0015 por 1K tokens
- **Output**: $0.002 por 1K tokens

### Estimación de Costos
- **Documento típico**: ~500-1000 tokens
- **Análisis completo**: ~$0.01-0.02 por documento
- **Chat adicional**: ~$0.005 por pregunta

## 🐛 Solución de Problemas

### Error: "API Key no válida"
```
❌ Error al inicializar IA: Invalid API key
```
**Solución**: Verifica que la API Key sea correcta y esté activa

### Error: "Cuota excedida"
```
❌ Error: Rate limit exceeded
```
**Solución**: 
- Verifica tu saldo en OpenAI
- Espera unos minutos antes de intentar de nuevo
- Considera actualizar tu plan

### Error: "Modelo no disponible"
```
❌ Error: Model not found
```
**Solución**: El modelo GPT-3.5-turbo está disponible por defecto

### Modo Simulado
Si no puedes configurar GPT, la aplicación funciona en modo simulado:
- Análisis básico sin IA
- Problemas y recomendaciones predefinidos
- Chat con respuestas simuladas

## 📊 Monitoreo de Uso

### Dashboard de OpenAI
- Ve a [Usage](https://platform.openai.com/usage)
- Monitorea tu consumo de tokens
- Revisa los costos acumulados

### Logs de la Aplicación
Los errores de API se muestran en:
- La interfaz de la aplicación
- La consola donde ejecutas Streamlit

## 🔮 Optimización

### Reducir Costos
- Limita el tamaño de documentos procesados
- Optimiza los prompts para usar menos tokens
- Usa el modo simulado para pruebas

### Mejorar Rendimiento
- Procesa documentos en lotes
- Implementa caché de análisis previos
- Usa streaming para respuestas largas

## 📞 Soporte

### OpenAI Support
- [Documentación oficial](https://platform.openai.com/docs)
- [Comunidad](https://community.openai.com/)
- [Soporte técnico](https://help.openai.com/)

### Problemas de la Aplicación
- Revisa los logs de error
- Verifica la configuración de red
- Contacta al equipo de desarrollo

---

**¡Con GPT configurado, tu sistema estará listo para análisis inteligente de documentos legales! 🚀** 