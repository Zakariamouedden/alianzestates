from flask import Flask, render_template, request, jsonify, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
from database import get_blog_posts, save_contact_message, get_blog_post_by_id

app = Flask(__name__)

# Gmail configuration (replace with your credentials or use environment variables for security)
GMAIL_USER = 'zmouedden2020@gmail.com'  # Replace with your Gmail address
GMAIL_PASSWORD = 'ztvx aidu fbir gonx'  # Replace with your Gmail App Password

locations = ['Málaga', 'Estepona', 'Fuengirola', 'Marbella', 'Mijas', 'Benahavís', 'Manilva', 'Casares', 'Sotogrande', 'Torremolinos']
types = ['Apartamento', 'Ático', 'Adosado', 'Villa']

# Lista estática de propiedades
properties_list = [
    {'id': 1, 'title': 'Villa Mediterránea', 'price': 1800000.0, 'bedrooms': 5, 'location': 'Marbella', 'type': 'Villa', 'bathrooms': 4, 'size': '450 m²', 'year': 2023, 'description': 'Espectacular villa mediterránea con piscina infinita y vistas al mar.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 2, 'title': 'Ático de Diseño', 'price': 950000.0, 'bedrooms': 3, 'location': 'Málaga', 'type': 'Ático', 'bathrooms': 2, 'size': '180 m²', 'year': 2024, 'description': 'Ático moderno con terraza privada y vistas panorámicas al centro.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 3, 'title': 'Apartamento Costero', 'price': 520000.0, 'bedrooms': 2, 'location': 'Fuengirola', 'type': 'Apartamento', 'bathrooms': 2, 'size': '110 m²', 'year': 2020, 'description': 'Apartamento luminoso a pocos pasos de la playa.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 4, 'title': 'Adosado de Lujo', 'price': 700000.0, 'bedrooms': 4, 'location': 'Estepona', 'type': 'Adosado', 'bathrooms': 3, 'size': '200 m²', 'year': 2021, 'description': 'Adosado elegante en una urbanización de lujo con piscina.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 5, 'title': 'Villa Panorámica', 'price': 2200000.0, 'bedrooms': 6, 'location': 'Benahavís', 'type': 'Villa', 'bathrooms': 5, 'size': '550 m²', 'year': 2022, 'description': 'Villa de ensueño con vistas panorámicas a las montañas.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 6, 'title': 'Ático Exclusivo', 'price': 1100000.0, 'bedrooms': 4, 'location': 'Sotogrande', 'type': 'Ático', 'bathrooms': 3, 'size': '220 m²', 'year': 2023, 'description': 'Ático de lujo con vistas al puerto deportivo.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 7, 'title': 'Apartamento Urbano', 'price': 480000.0, 'bedrooms': 2, 'location': 'Torremolinos', 'type': 'Apartamento', 'bathrooms': 1, 'size': '100 m²', 'year': 2019, 'description': 'Apartamento moderno en el corazón de Torremolinos.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 8, 'title': 'Villa de Montaña', 'price': 1600000.0, 'bedrooms': 5, 'location': 'Mijas', 'type': 'Villa', 'bathrooms': 4, 'size': '400 m²', 'year': 2021, 'description': 'Villa con encanto rodeada de naturaleza.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 9, 'title': 'Apartamento de Playa', 'price': 650000.0, 'bedrooms': 3, 'location': 'Manilva', 'type': 'Apartamento', 'bathrooms': 2, 'size': '150 m²', 'year': 2022, 'description': 'Apartamento con acceso directo a la playa.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 10, 'title': 'Villa Moderna', 'price': 2500000.0, 'bedrooms': 7, 'location': 'Casares', 'type': 'Villa', 'bathrooms': 6, 'size': '600 m²', 'year': 2024, 'description': 'Villa ultramoderna con domótica y piscina climatizada.', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 11, 'title': 'Ático Panorámico', 'price': 800000.0, 'bedrooms': 3, 'location': 'Estepona', 'type': 'Ático', 'bathrooms': 2, 'size': '170 m²', 'year': 2021, 'description': 'Ático con vistas al mar y terraza de 50 m².', 'featured': 1, 'image': '/static/images/default_property.jpg'},
    {'id': 12, 'title': 'Adosado Familiar', 'price': 550000.0, 'bedrooms': 4, 'location': 'Fuengirola', 'type': 'Adosado', 'bathrooms': 3, 'size': '190 m²', 'year': 2020, 'description': 'Adosado ideal para familias con jardín privado.', 'featured': 1, 'image': '/static/images/default_property.jpg'}
]

@app.template_filter('format_price')
def format_price(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def send_gmail(sender_email, sender_password, recipient_email, subject, body):
    """Send an email using Gmail's SMTP server."""
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/')
def index():
    try:
        featured = [p for p in properties_list if p['featured'] == 1][:12]
        if not featured:
            print("Advertencia: No se encontraron propiedades destacadas.")
        return render_template('index.html', featured=[tuple(p.values()) for p in featured], locations=locations, types=types)
    except Exception as e:
        print(f"Error en /: {str(e)}")
        print(traceback.format_exc())
        return "Error al cargar la página de inicio", 500

@app.route('/properties', methods=['GET'])
def properties():
    try:
        filters = {
            'price_min': float(request.args.get('price_min', 0)) if request.args.get('price_min') else 0,
            'price_max': float(request.args.get('price_max', 10000000)) if request.args.get('price_max') else 10000000,
            'bedrooms': int(request.args.get('bedrooms', 0)) if request.args.get('bedrooms') else 0,
            'bathrooms': int(request.args.get('bathrooms', 0)) if request.args.get('bathrooms') else 0,
            'location': request.args.get('location', ''),
            'type': request.args.get('type', ''),
            'size': request.args.get('size', '')
        }
        filtered = []
        for prop in properties_list:
            if (prop['price'] >= filters['price_min'] and
                prop['price'] <= filters['price_max']):
                if filters['bedrooms'] > 0 and prop['bedrooms'] < filters['bedrooms']:
                    continue
                if filters['bathrooms'] > 0 and prop['bathrooms'] < filters['bathrooms']:
                    continue
                if filters['location'] and prop['location'] != filters['location']:
                    continue
                if filters['type'] and prop['type'] != filters['type']:
                    continue
                if filters['size']:
                    size_num = int(prop['size'].replace(' m²', ''))
                    if size_num < int(filters['size'].replace(' m²', '')):
                        continue
                filtered.append(tuple(prop.values()))
        return render_template('properties.html', properties=filtered, locations=locations, types=types)
    except Exception as e:
        print(f"Error en /properties: {e}")
        return "Error al cargar las propiedades", 500

@app.route('/property/<int:id>')
def property_detail(id):
    try:
        property_data = next((p for p in properties_list if p['id'] == id), None)
        if not property_data:
            return "Propiedad no encontrada", 404

        property_dict = {
            'id': property_data['id'],
            'title': property_data['title'],
            'price': property_data['price'],
            'bedrooms': property_data['bedrooms'],
            'location': property_data['location'],
            'type': property_data['type'],
            'bathrooms': property_data['bathrooms'],
            'size': property_data['size'],
            'year': property_data['year'],
            'description': property_data['description'],
            'featured': property_data['featured'],
            'image': property_data['image'] or '/static/images/default_property.jpg'
        }

        return render_template('property_detail.html', property=property_dict)
    except Exception as e:
        print(f"Error en /property/{id}: {e}")
        return "Error al cargar la propiedad", 500

@app.route('/api/send-email', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    role = data.get('role')
    property_id = data.get('propertyId')

    try:
        save_contact_message(name, email, message)
        # Send email notification
        subject = f"Nuevo mensaje de contacto de {name}"
        body = f"Nombre: {name}\nCorreo: {email}\nTeléfono: {phone or 'No proporcionado'}\nMensaje: {message}\nRol: {role or 'No especificado'}\nID de Propiedad: {property_id or 'No especificado'}"
        if not send_gmail(GMAIL_USER, GMAIL_PASSWORD, GMAIL_USER, subject, body):
            return jsonify({'status': 'error', 'message': 'Error al enviar el correo'}), 500
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error en /api/send-email: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/service/<int:id>')
def service_detail(id):
    try:
        services = [
            {'id': 1, 'title': 'Venta de Propiedades', 'description': 'Ofrecemos una amplia selección de propiedades de lujo, desde villas hasta áticos, en las mejores ubicaciones de la Costa del Sol.', 'template': 'service-venta-propiedades.html'},
            {'id': 2, 'title': 'Obra Nueva', 'description': 'Descubre nuestros proyectos de obra nueva, diseñados con los más altos estándares de calidad y sostenibilidad.', 'template': 'service-obra-nueva.html'},
            {'id': 3, 'title': 'Consultoría de Inversiones', 'description': 'Nuestros expertos te guiarán para maximizar el retorno de tu inversión en el mercado inmobiliario.', 'template': 'service-consultoria-inversiones.html'},
            {'id': 4, 'title': 'Construcciones', 'description': 'Proyectos de construcción personalizados para crear el hogar de tus sueños.', 'template': 'service-construcciones.html'}
        ]
        service = next((s for s in services if s['id'] == id), None)
        if not service:
            return "Servicio no encontrado", 404
        return render_template(service['template'], service=service)
    except Exception as e:
        print(f"Error en /service/{id}: {e}")
        return "Error al cargar el servicio", 500

@app.route('/blog')
def blog():
    try:
        posts = get_blog_posts()
        return render_template('blog.html', posts=posts)
    except Exception as e:
        print(f"Error en /blog: {e}")
        return "Error al cargar el blog", 500

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    try:
        post = get_blog_post_by_id(post_id)
        if not post:
            return "Artículo no encontrado", 404
        return render_template('blog_post.html', post=post)
    except Exception as e:
        print(f"Error en /blog/{post_id}: {e}")
        return "Error al cargar el artículo", 500

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        print(f"Error en /about: {e}")
        return "Error al cargar la página", 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Save the contact message to the database
            save_contact_message(name, email, message)
            
            # Send email notification
            subject = f"Nuevo mensaje de contacto de {name}"
            body = f"Nombre: {name}\nCorreo: {email}\nMensaje: {message}"
            if not send_gmail(GMAIL_USER, GMAIL_PASSWORD, GMAIL_USER, subject, body):
                return "Error al enviar el correo", 500
            
            return redirect(url_for('contact', success=True))
        success = request.args.get('success', False)
        return render_template('contact.html', success=success)
    except Exception as e:
        print(f"Error en /contact: {e}")
        return "Error al cargar la página de contacto", 500

@app.route('/privacy-policy')
def privacy_policy():
    try:
        return render_template('privacy_policy.html')
    except Exception as e:
        print(f"Error en /privacy-policy: {e}")
        return "Error al cargar la página", 500

@app.route('/cookies-policy')
def cookies_policy():
    try:
        return render_template('cookies_policy.html')
    except Exception as e:
        print(f"Error en /cookies-policy: {e}")
        return "Error al cargar la página", 500

@app.route('/legal-notice')
def legal_notice():
    try:
        return render_template('legal_notice.html')
    except Exception as e:
        print(f"Error en /legal-notice: {e}")
        return "Error al cargar la página", 500
    
@app.route("/terms")
def terms():
    try:
        return render_template('terms.html')
    except Exception as e:
        print(f"Error en /terms: {e}")
        return "Error al cargar la página", 500

@app.route('/admin/new-post', methods=['GET', 'POST'])
def new_post():
    try:
        if request.method == 'POST':
            return redirect(url_for('blog'))
        return render_template('new_post.html')
    except Exception as e:
        print(f"Error en /admin/new-post: {e}")
        return "Error al cargar la página", 500

@app.route('/admin/properties', methods=['GET'])
def admin_properties():
    try:
        return render_template('admin_properties.html', properties=[tuple(p.values()) for p in properties_list])
    except Exception as e:
        print(f"Error en /admin/properties: {e}")
        return "Error al cargar las propiedades", 500

@app.route('/admin/property/new', methods=['GET', 'POST'])
@app.route('/admin/property/edit/<int:id>', methods=['GET', 'POST'])
def admin_property(id=None):
    try:
        global properties_list
        if request.method == 'POST':
            title = request.form.get('title')
            price = float(request.form.get('price'))
            bedrooms = int(request.form.get('bedrooms'))
            location = request.form.get('location')
            property_type = request.form.get('type')
            bathrooms = int(request.form.get('bathrooms'))
            size = request.form.get('size')
            year = int(request.form.get('year'))
            description = request.form.get('description')
            featured = 1 if request.form.get('featured') == 'on' else 0
            image = request.form.get('existing_image', '/static/images/default_property.jpg')

            if id:  # Editar propiedad existente
                for prop in properties_list:
                    if prop['id'] == id:
                        prop.update({
                            'title': title,
                            'price': price,
                            'bedrooms': bedrooms,
                            'location': location,
                            'type': property_type,
                            'bathrooms': bathrooms,
                            'size': size,
                            'year': year,
                            'description': description,
                            'featured': featured,
                            'image': image
                        })
                        break
            else:  # Nueva propiedad
                new_id = max([p['id'] for p in properties_list], default=0) + 1
                new_property = {
                    'id': new_id,
                    'title': title,
                    'price': price,
                    'bedrooms': bedrooms,
                    'location': location,
                    'type': property_type,
                    'bathrooms': bathrooms,
                    'size': size,
                    'year': year,
                    'description': description,
                    'featured': featured,
                    'image': image
                }
                properties_list.append(new_property)

            return redirect(url_for('admin_properties'))

        if id:
            property_data = next((tuple(p.values()) for p in properties_list if p['id'] == id), None)
            if not property_data:
                return "Propiedad no encontrada", 404
        else:
            property_data = None

        return render_template('admin_property.html', property=property_data, locations=locations, types=types)
    except Exception as e:
        print(f"Error en /admin/property{'/' + str(id) if id else ''}: {e}")
        return "Error al cargar la página", 500

if __name__ == '__main__':
    app.run(debug=True)