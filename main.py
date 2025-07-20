from flask import Flask, request, jsonify, send_file
import shutil
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def savePdf(name, template):
    html_path = f"./pdfs/{name}/{name}.html"
    pdf_path = f"./pdfs/{name}/{name}.pdf"
    print(f"Generando PDF desde {html_path} a {pdf_path} con plantilla {template}")
    print(f"savePdf: {template}")
    # Seleccionar el archivo CSS según la plantilla
    css_file = f"./{template}.css"
    css_path = Path(css_file)
    
    font_config = FontConfiguration()
    
    # Leer el contenido del archivo CSS seleccionado
    if css_path.exists():
        css_content = css_path.read_text(encoding='utf-8')
        css = CSS(string=css_content, font_config=font_config)
        HTML(html_path).write_pdf(pdf_path, stylesheets=[css], font_config=font_config)
    else:
        print(f"Archivo CSS {css_file} no encontrado, usando CSS vacío")
        css = CSS(string='', font_config=font_config)
        HTML(html_path).write_pdf(pdf_path, stylesheets=[css], font_config=font_config)

@app.route('/eliminate-pdf', methods=['POST'])
def eliminateFolder():
    """
    Elimina la carpeta y su contenido
    """

    data = request.get_json()
    name = data.get('name')
    folder_path = f"./pdfs/{name}"

    if Path(folder_path).exists():
        shutil.rmtree(folder_path)
        print(f"Carpeta {folder_path} eliminada")
        return jsonify({"message": f"Carpeta {name} eliminada"}), 200
    else:
        print(f"La carpeta {folder_path} no existe")
        return jsonify({"message": f"Carpeta {name} no existe"}), 404

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Endpoint para generar PDF desde HTML
    Espera JSON con:
    - name: nombre del archivo (sin extensión)
    - content: contenido HTML a convertir
    - template: número de plantilla CSS (1, 2, o 3) - opcional, por defecto 1
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400
        
        name = data.get('name')
        content = data.get('content')
        template = data.get('template')  # Valor por defecto: plantilla 1
        
        if not name or not content:
            return jsonify({"error": "Se requieren 'name' y 'content'"}), 400
        print(template)
        # Crear carpeta y archivo HTML
        Path(f"pdfs/{name}/").mkdir(parents=True, exist_ok=True)
        Path(f"pdfs/{name}/{name}.html").write_text(f"{content}", encoding='utf-8')
        
        # Generar PDF
        savePdf(name, template)
        
        # Devolver el archivo PDF
        pdf_path = f"pdfs/{name}/{name}.pdf"
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{name}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        # Eliminar la carpeta creada en caso de error
        folder_path = f"./pdfs/{name}"
        if Path(folder_path).exists():
            shutil.rmtree(folder_path)
        return jsonify({"error": f"Error al generar PDF: {str(e)}"}), 500
        

@app.route('/', methods=['GET'])
def home():
    """Endpoint de inicio con información de uso"""
    return jsonify({
        "message": "Server on"
    })

if __name__ == '__main__':
    # Crear directorios necesarios
    Path("pdfs").mkdir(exist_ok=True)
    
    # Ejecutar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
