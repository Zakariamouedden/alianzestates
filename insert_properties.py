import sqlite3

def create_table():
    """Crea la tabla properties si no existe."""
    conn = sqlite3.connect('properties.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            bedrooms INTEGER NOT NULL,
            location TEXT NOT NULL,
            type TEXT NOT NULL,
            bathrooms INTEGER NOT NULL,
            size TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT,
            featured INTEGER NOT NULL DEFAULT 0,
            image TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_properties():
    """Inserta 12 propiedades en la base de datos."""
    conn = sqlite3.connect('properties.db')
    cursor = conn.cursor()

    # Lista de propiedades
    properties = [
        ('Villa Mediterránea', 1800000, 5, 'Marbella', 'Villa', 4, '450 m²', 2023, 'Espectacular villa mediterránea con piscina infinita y vistas al mar.', 1, '/static/images/default_property.jpg'),
        ('Ático de Diseño', 950000, 3, 'Málaga', 'Ático', 2, '180 m²', 2024, 'Ático moderno con terraza privada y vistas panorámicas al centro.', 1, '/static/images/default_property.jpg'),
        ('Apartamento Costero', 520000, 2, 'Fuengirola', 'Apartamento', 2, '110 m²', 2020, 'Apartamento luminoso a pocos pasos de la playa.', 1, '/static/images/default_property.jpg'),
        ('Adosado de Lujo', 700000, 4, 'Estepona', 'Adosado', 3, '200 m²', 2021, 'Adosado elegante en una urbanización de lujo con piscina.', 1, '/static/images/default_property.jpg'),
        ('Villa Panorámica', 2200000, 6, 'Benahavís', 'Villa', 5, '550 m²', 2022, 'Villa de ensueño con vistas panorámicas a las montañas.', 1, '/static/images/default_property.jpg'),
        ('Ático Exclusivo', 1100000, 4, 'Sotogrande', 'Ático', 3, '220 m²', 2023, 'Ático de lujo con vistas al puerto deportivo.', 1, '/static/images/default_property.jpg'),
        ('Apartamento Urbano', 480000, 2, 'Torremolinos', 'Apartamento', 1, '100 m²', 2019, 'Apartamento moderno en el corazón de Torremolinos.', 1, '/static/images/default_property.jpg'),
        ('Villa de Montaña', 1600000, 5, 'Mijas', 'Villa', 4, '400 m²', 2021, 'Villa con encanto rodeada de naturaleza.', 1, '/static/images/default_property.jpg'),
        ('Apartamento de Playa', 650000, 3, 'Manilva', 'Apartamento', 2, '150 m²', 2022, 'Apartamento con acceso directo a la playa.', 1, '/static/images/default_property.jpg'),
        ('Villa Moderna', 2500000, 7, 'Casares', 'Villa', 6, '600 m²', 2024, 'Villa ultramoderna con domótica y piscina climatizada.', 1, '/static/images/default_property.jpg'),
        ('Ático Panorámico', 800000, 3, 'Estepona', 'Ático', 2, '170 m²', 2021, 'Ático con vistas al mar y terraza de 50 m².', 1, '/static/images/default_property.jpg'),
        ('Adosado Familiar', 550000, 4, 'Fuengirola', 'Adosado', 3, '190 m²', 2020, 'Adosado ideal para familias con jardín privado.', 1, '/static/images/default_property.jpg')
    ]

    # Limpiar la tabla (opcional, elimina propiedades existentes)
    cursor.execute("DELETE FROM properties")

    # Insertar las propiedades
    cursor.executemany("""
        INSERT INTO properties (title, price, bedrooms, location, type, bathrooms, size, year, description, featured, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, properties)

    # Confirmar los cambios
    conn.commit()
    print("12 propiedades insertadas correctamente.")

    # Cerrar la conexión
    conn.close()

if __name__ == "__main__":
    create_table()
    insert_properties()