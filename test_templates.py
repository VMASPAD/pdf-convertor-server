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

<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="description" content="Presupuesto de automatizaciones">
    <link rel="stylesheet" href="./1.css">
</head>
<body>
    <div class="container">
        <div class="header"> 
            <h1 class="main-title">{PRESUPUESTO}</h1>
        </div>
        
        <div class="client-info">
            <div class="client-section">Datos del cliente</div>
            <div class="client-section"> </div>
            <div class="client-details">
                <strong>Cliente/Razon social:</strong> Facultad de Ciencias Exactas UNLP<br>
                <strong>CUIT:</strong> 30-54666670-7<br>
                <strong>Ubicación:</strong> Buenos Aires, Argentina<br>
                <strong>Telefono:</strong> 241234134<br>
                <strong>Informacion Adicional: </strong>
            </div>
            <div class="date-badge">08/05/2025</div>
        </div>
        
        <div class="table-container">
            <table class="content-table">
                <thead>
                    <tr>
                        <th>Descripción</th>
                        <th>Cantidad</th>
                        <th>Precio</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Barrera BLDC uso intensivo</td>
                        <td>1</td>
                        <td>$1.478.139</td>
                    </tr>
                    <tr>
                        <td>Teclado de acceso</td>
                        <td>2</td>
                        <td>$1.600.000</td>
                    </tr>
                    <tr>
                        <td>Llavero</td>
                        <td>150</td>
                        <td>$6.150.000</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
    <div class="totals-section">
        <div class="payment-info">
            <div class="payment-title">Información de Pago</div>
            <div class="payment-card">
                <div class="payment-details">
                    <strong>EFECTIVO / TRANSFERENCIA</strong><br><br>
                    <strong>Cuenta:</strong> 058-214570/7<br>
                    <strong>CUIT/CUIL:</strong> 23317324830<br>
                    <strong>CBU:</strong> 0720058880000214570721<br>
                    <strong>Alias:</strong> <span class="payment-highlight">MARIO.BARRIOS</span>
                </div>
            </div> 
        </div>
        <div class="totals-grid">
            <div class="totals-row">
                <div class="totals-label subtotal-label">Subtotal</div>
                <div class="totals-value subtotal-value">$26.338.392</div>
            </div>
            <div class="totals-row">
                <div class="totals-label tax-label">IVA (21%)</div>
                <div class="totals-value tax-value">$5.531.062</div>
            </div>
            <div class="totals-row total-row">
                <div class="totals-label total-label">Total</div>
                <div class="totals-value total-value">$31.869.454</div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-content">
            <div class="company-info">
                <div class="company-name">Nombre de la Empresa</div>
                <div class="company-details">
                    <span>Dirección: Calle Ejemplo 123, Ciudad</span><br>
                    <span>Teléfono: +54 11 1234-5678</span><br>
                    <span>Email: contacto@empresa.com</span>
                </div>
            </div>
            <div class="footer-right">
                <div class="footer-note">Gracias por su confianza</div>
                <div class="footer-website">www.empresa.com</div>
            </div>
        </div>
    </div>

    </div>
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
    for template in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        test_template(template)
    
    print("\n🎉 Pruebas completadas!")
    print("📁 Revisa los archivos PDF generados en el directorio actual")
