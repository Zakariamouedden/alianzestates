def get_blog_posts():
    """Función simulada para blog."""
    return [
        (1, "Tendencias Inmobiliarias 2025", "Explora las tendencias del mercado inmobiliario.", "2025-01-01"),
        (2, "Guía para Comprar en la Costa del Sol", "Consejos para invertir en propiedades.", "2025-02-01")
    ]

def get_blog_post_by_id(post_id):
    """Función simulada para blog."""
    posts = get_blog_posts()
    for post in posts:
        if post[0] == post_id:
            return post
    return None

def save_contact_message(name, email, message):
    """Función simulada para mensajes de contacto."""
    print(f"Mensaje recibido de {name} ({email}): {message}")