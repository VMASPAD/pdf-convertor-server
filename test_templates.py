#!/usr/bin/env python3
"""
Script de prueba para verificar las plantillas CSS
"""
import requests
import json

# URL del servidor (ajusta si es necesario)
BASE_URL = "http://localhost:5000"

# HTML de prueba para las facturas
test_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>tailwind</title>
    
</head>

<body>
<main class="invoice-container"><div class="invoice-wrapper"><div class="invoice-header"><div class="invoice-header-content clearfix"><div class="header-left"><h1 class="text-2xl font-bold mb-3">FACTURA</h1><div class="company-info"><p class="font-semibold text-base">Tu Empresa S.A.</p><p class="opacity-90 text-sm">Calle Principal 123</p><p class="opacity-90 text-sm">Ciudad, Provincia 12345</p><p class="opacity-90 text-sm">Tel: (011) 1234-5678</p></div></div><div class="header-center"><img alt="logo" class="max-h-24 rounded-2xl" src="https://placehold.co/300x85"></div><div class="header-right"><div class="invoice-number"><p class="text-xs font-medium opacity-80">FACTURA N°</p><p class="text-lg font-bold">001-0001234</p></div></div></div><div class="header-decoration"></div></div><div class="invoice-details"><div class="general-info"><h3 class="text-lg font-semibold mb-3 text-secondary-foreground">Información General</h3><div class="info-card"><div class="simple-grid"><p><span class="font-medium text-primary">Fecha:</span></p><p>08/05/2025</p><p><span class="font-medium text-primary">Orden:</span></p><p>PO-2025-0156</p><p><span class="font-medium text-primary">Vendedor:</span></p><p>Juan Pérez</p></div></div></div></div><div class="products-section"><div class="products-header"><h2 class="text-xl font-bold text-primary">Detalle de Productos</h2></div><table class="products-table"><thead><tr class="table-header"><th class="text-left py-3 px-3 font-bold text-primary">Descripción</th><th class="text-center py-3 px-3 font-bold w-16 text-primary">Cant.</th><th class="text-right py-3 px-3 font-bold w-24 text-primary">Precio Unit.</th><th class="text-right py-3 px-3 font-bold w-24 text-primary">Total</th></tr></thead><tbody><tr class="table-row hover:bg-opacity-50"><td class="px-3"><div class="product-item"><p class="font-medium text-card-foreground">Barrera BLDC uso intensivo</p></div></td><td class="py-3 px-3 text-center font-medium text-card-foreground">1</td><td class="py-3 px-3 text-right font-medium text-card-foreground">$1.478.139,00</td><td class="py-3 px-3 text-right font-bold text-chart-1">$1.478.139,00</td></tr><tr class="table-row"><td class="py-3 px-3"><div class="product-item"><p class="font-medium text-card-foreground">Teclado de acceso</p></div></td><td class="py-3 px-3 text-center font-medium text-card-foreground">2</td><td class="py-3 px-3 text-right font-medium text-card-foreground">$800.000,00</td><td class="py-3 px-3 text-right font-bold text-chart-1">$1.600.000,00</td></tr><tr class="table-row"><td class="py-3 px-3"><div class="product-item"><p class="font-medium text-card-foreground">Llavero de proximidad</p></div></td><td class="py-3 px-3 text-center font-medium text-card-foreground">150</td><td class="py-3 px-3 text-right font-medium text-card-foreground">$41.000,00</td><td class="py-3 px-3 text-right font-bold text-chart-1">$6.150.000,00</td></tr></tbody></table></div><div class="totals-section"><div class="totals-content"><div class="payment-info"><h3 class="payment-header">Información de Pago</h3><div class="payment-card"><div class="simple-grid text-card-foreground"><p><span class="font-medium text-primary">Cuenta:</span></p><p>058-214570/7</p><p><span class="font-medium text-primary">CUIT/CUIL:</span></p><p>test</p><p><span class="font-medium text-primary">CBU:</span></p><p class="text-sm">0720058880000214570721</p><p><span class="font-medium text-primary">Alias:</span></p><p>test</p></div></div></div><div class="summary-section"><h3 class="summary-header">Resumen</h3><div class="summary-card"><div class="summary-row"><span class="font-medium text-muted-foreground">Subtotal:</span><span class="font-bold text-foreground">$9.228.139,00</span></div><div class="summary-row"><span class="font-medium text-muted-foreground">IVA (21%):</span><span class="font-bold text-chart-2">$1.937.909,19</span></div><div class="summary-total"><span class="text-lg font-bold text-primary">Total:</span><span class="total-amount">$11.166.048,19</span></div></div></div></div></div><div class="invoice-footer"><div class="footer-content"><p class="text-base font-semibold mb-2 text-primary">Dirección</p><p class="text-base font-semibold mb-2 text-primary">Instagram</p><p class="text-base font-semibold mb-2 text-primary">Contacto</p></div></div></div></main> </body>
</html>
"""

def test_template(template_num):
    """Prueba una plantilla específica"""
    print(f"\n--- Probando Plantilla {template_num} ---")
    
    payload = {
        "name": f"factura_plantilla_{template_num}",
        "content": test_html,
        "template": template_num
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-pdf",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Guardar el PDF
            filename = f"test_plantilla_{template_num}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ PDF generado exitosamente: {filename}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está ejecutándose?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_server_status():
    """Verifica que el servidor esté funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        return False

if __name__ == "__main__":
    print("🧪 Iniciando pruebas de plantillas CSS...")
    
    # Verificar que el servidor esté funcionando
    if not test_server_status():
        print("\n💡 Para ejecutar las pruebas:")
        print("1. Ejecuta: python main.py")
        print("2. Luego ejecuta: python test_templates.py")
        exit(1)
    
    # Probar cada plantilla
    for template in [1, 2, 3, 4, 5, 6, 7]:
        test_template(template)
    
    print("\n🎉 Pruebas completadas!")
    print("📁 Revisa los archivos PDF generados en el directorio actual")
