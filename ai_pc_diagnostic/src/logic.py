import os
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno (seguridad)
load_dotenv()

class SistemaExperto:
    def __init__(self):
        # Base de conocimiento local (Reglas)
        self.__base_conocimiento = {
            "pantalla_azul": ("BSOD Windows", "ALTA", "Reinicia en modo seguro y actualiza drivers."),
            "ruido_fuerte": ("Ventilador Sucio", "MEDIA", "Limpia el polvo y revisa obstrucciones."),
            "internet_lento": ("Red Saturada", "BAJA", "Reinicia el router o llama a tu proveedor."),
            "olor_quemado": ("Cortocircuito", "CRÍTICA", "¡APAGA TODO YA! Desconecta de la corriente."),
            "pc_no_prende": ("Problema de Placa Madre", "CRÍTICA", "Revisa conexiones o lleva a servicio técnico."),
            "teclado_no_funciona": ("Conexión floja o dañada", "Media", "Revisa el cable o prueba con otro teclado."),
            "programas_se_cierran": ("Infección de Malware", "Alta", "Ejecuta un análisis con un software anti-malware confiable."),
            "virus_detectado": ("Infección de Virus", "CRÍTICA", "Ejecuta un análisis completo con un antivirus confiable."),
        }
        
        # Cliente OpenAI (IA Generativa)
        # Intenta obtener la clave, si no existe, usa None
        api_key = os.getenv("GROQ_API_KEY")
        self.cliente_gpt = Groq(api_key=api_key) if api_key else None

    def consultar(self, sintoma):
        """
        Busca primero en reglas locales. Si no encuentra y hay API Key, pregunta a GPT.
        """
        key = sintoma.lower().replace(" ", "_")
        
        # 1. Búsqueda Local (Rápida y Gratis)
        if key in self.__base_conocimiento:
            nombre, gravedad, consejo = self.__base_conocimiento[key]
            return nombre, f"Nivel: {gravedad}\nConsejo: {consejo}"
        
        # 2. Búsqueda IA (Si tenemos clave)
        elif self.cliente_gpt:
            try:
                response = self.cliente_gpt.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "Eres un técnico de PC experto. Responde brevemente con el diagnóstico y solución."},
                        {"role": "user", "content": f"Síntoma: {sintoma}"}
                    ]
                )
                return "Diagnóstico IA (LLama 3)", response.choices[0].message.content
            except Exception as e:
                return "Error IA", f"Falló la conexión: {str(e)}"
        
        # 3. Fallo total
        else:
            return None, None
