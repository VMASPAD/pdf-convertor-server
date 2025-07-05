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
<html>
<head>
    <meta charset="utf-8">
    <title>Factura de Prueba</title>
</head>
<body>
    <h1>FACTURA</h1>
    
    <aside>
        <address id="from">
            Mi Empresa S.A.
            Calle Principal 123
            Ciudad, CP 12345
            Email: contacto@miempresa.com
        </address>
        <address id="to">
            Cliente Ejemplo
            Avenida Secundaria 456
            Otra Ciudad, CP 67890
            Email: cliente@ejemplo.com
        </address>
    </aside>
    
    <dl>
        <dt>Fecha</dt>
        <dd>2025-07-04</dd>
        <dt>Factura #</dt>
        <dd>INV-2025-001</dd>
        <dt>Vencimiento</dt>
        <dd>2025-08-04</dd>
    </dl>
    
    <table>
        <thead>
            <tr>
                <th>Descripción</th>
                <th>Cantidad</th>
                <th>Precio Unit.</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Consultoría de Desarrollo</td>
                <td>10</td>
                <td>$150.00</td>
                <td>$1,500.00</td>
            </tr>
            <tr>
                <td>Mantenimiento de Sistema</td>
                <td>5</td>
                <td>$100.00</td>
                <td>$500.00</td>
            </tr>
            <tr>
                <td>Soporte Técnico</td>
                <td>8</td>
                <td>$75.00</td>
                <td>$600.00</td>
            </tr>
        </tbody>
    </table>
    
    <table id="total">
        <tr>
            <td>TOTAL</td>
            <td>$2,600.00</td>
        </tr>
    </table>
    
    <footer></footer>
</body>
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
    for template in [1, 2, 3]:
        test_template(template)
    
    print("\n🎉 Pruebas completadas!")
    print("📁 Revisa los archivos PDF generados en el directorio actual")
