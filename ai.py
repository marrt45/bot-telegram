# ai.py
from sheets import get_productos
import random
import re

# Configuración de personalidad del vendedor
RESPUESTAS = {
    "saludo": [
        "¡Hola {nombre}! 😊 ¿En qué puedo ayudarte hoy?",
        "¡Buen día {nombre}! 🌟 ¿Qué necesitas pedir?"
    ],
    "producto_encontrado": [
        "¡Claro que sí {nombre}! Tenemos {producto} disponible:\n\n"
        "💵 *Precio:* ${precio}\n"
        "📦 *Stock actual:* {stock}\n"
        "🆔 *Código:* {codigo}\n"
        "📝 *Notas:* {info}\n\n"
        "¿Cuántas unidades necesitas?",

        "¡Excelente elección {nombre}! 😍\n\n"
        "🔹 *Producto:* {producto}\n"
        "🔹 *Precio especial:* ${precio}\n"
        "🔹 *Disponibilidad:* {stock} unidades\n\n"
        "Indícame la cantidad deseada:"
    ],
    "producto_no_encontrado": [
        "Lo siento {nombre}, no tengo '{busqueda}' en este momento. ¿Te interesa alguno de estos?\n\n{sugerencias}",

        "¡Ups! {nombre}, parece que '{busqueda}' no está disponible. Tenemos:\n\n{sugerencias}\n\n"
        "¿Alguna de estas opciones te sirve?"
    ],
    "agradecimiento": [
        "¡Gracias por tu pedido {nombre}! 💖 Estamos procesándolo...",
        "¡Perfecto {nombre}! 📝 Anoté tu pedido, ¿necesitas algo más?"
    ]
}

def generar_respuesta(tipo, **kwargs):
    """Genera respuestas naturales con plantillas"""
    return random.choice(RESPUESTAS[tipo]).format(**kwargs)

def buscar_producto(mensaje, nombre_usuario=""):
    try:
        productos = get_productos()
        mensaje = mensaje.lower().strip()
        
        # Limpia el mensaje (elimina "tenes", "quiero", etc.)
        mensaje_limpio = re.sub(r'(tenes|quiero|necesito|por favor|precio de)\s*', '', mensaje)
        
        # Busca coincidencias exactas primero
        for p in productos:
            if mensaje_limpio in p['descripción'].lower():
                return generar_respuesta(
                    "producto_encontrado",
                    nombre=nombre_usuario,
                    producto=p['descripción'],
                    precio=p['precio'],
                    stock=p['stock'],
                    codigo=p['código'],
                    info=p.get('info_adicional', 'Sin notas adicionales')
                )
        
        # Si no encuentra coincidencia exacta, busca parcial
        sugerencias = []
        for p in productos[:3]:  # Máximo 3 sugerencias
            if mensaje_limpio in p['descripción'].lower() or \
               any(palabra in p['descripción'].lower() for palabra in mensaje_limpio.split()):
                sugerencias.append(
                    f"➡️ *{p['descripción']}* (${p['precio']}) - Código: {p['código']}"
                )
        
        if sugerencias:
            return generar_respuesta(
                "producto_no_encontrado",
                nombre=nombre_usuario,
                busqueda=mensaje_limpio,
                sugerencias="\n".join(sugerencias)
            )
        else:
            # Si no hay sugerencias, muestra productos destacados
            destacados = "\n".join(
                f"➡️ *{p['descripción']}* (${p['precio']})" 
                for p in productos[:2]  # Muestra 2 productos destacados
            )
            return generar_respuesta(
                "producto_no_encontrado",
                nombre=nombre_usuario,
                busqueda=mensaje_limpio,
                sugerencias=destacados
            )
            
    except Exception as e:
        print(f"Error en buscar_producto: {e}")
        return "🔧 Estoy teniendo problemas técnicos. Por favor intenta nuevamente más tarde."

def es_agradecimiento(mensaje):
    palabras = ["gracias", "thanks", "agradecido", "merci"]
    return any(p in mensaje.lower() for p in palabras)