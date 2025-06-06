from fuzzywuzzy import fuzz, process
import re
import logging
from datetime import datetime

# Configura logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def extract_products(text, products_data):
    """Extrae productos del texto usando coincidencia aproximada"""
    try:
        # Diccionario para búsqueda {nombre: (código, precio, stock)}
        product_map = {
            p[1].lower(): (p[0], float(p[2]), int(p[3])) 
            for p in products_data if len(p) >= 4
        }
        
        matches = []
        # Busca patrones como "2 panes" o "3x100"
        for qty, name in re.findall(r'(\d+)\s?(?:x|\*)?\s?([^\d,;]+)', text, re.IGNORECASE):
            name = name.strip().lower()
            # Busca coincidencia exacta
            if name in product_map:
                code, price, stock = product_map[name]
                matches.append({
                    'code': code,
                    'name': next(p[1] for p in products_data if p[0] == code),  # Nombre original
                    'price': price,
                    'qty': int(qty),
                    'stock': stock
                })
            else:
                # Búsqueda aproximada
                best_match = process.extractOne(
                    name,
                    product_map.keys(),
                    scorer=fuzz.token_sort_ratio
                )
                if best_match and best_match[1] > 75:
                    code, price, stock = product_map[best_match[0]]
                    matches.append({
                        'code': code,
                        'name': next(p[1] for p in products_data if p[0] == code),  # Nombre original
                        'price': price,
                        'qty': int(qty),
                        'stock': stock
                    })
        return matches
    except Exception as e:
        logging.error(f"Error extrayendo productos: {e}")
        return []

def calculate_total(items):
    """Calcula el total del pedido"""
    try:
        return round(sum(item['price'] * item['qty'] for item in items if item['qty'] <= item['stock']), 2)
    except Exception as e:
        logging.error(f"Error calculando total: {e}")
        return 0.0

def prepare_order_summary(products):
    """Genera un resumen legible del pedido"""
    if not products:
        return "No se encontraron productos válidos"
    
    available = []
    unavailable = []
    
    for p in products:
        if p['qty'] <= p['stock']:
            available.append(f"{p['qty']} x {p['name']} (${p['price']} c/u)")
        else:
            unavailable.append(f"{p['qty']} x {p['name']} (Stock: {p['stock']})")
    
    summary = []
    if available:
        summary.append("📦 Pedido confirmado:")
        summary.extend(available)
        summary.append(f"\n💵 Total: ${calculate_total(products):.2f}")
    if unavailable:
        summary.append("\n⚠️ No disponible:")
        summary.extend(unavailable)
    
    return "\n".join(summary)