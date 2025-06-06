# test_imports.py
print("=== INICIO PRUEBA ===")

try:
    from ai import buscar_producto
    print("✅ Importación exitosa!")
    print("🔍 Probando función...")
    resultado = buscar_producto("pan", "TestUser")
    print(f"📦 Resultado:\n{resultado}")
except Exception as e:
    print(f"❌ Error: {e}")

print("=== FIN PRUEBA ===")