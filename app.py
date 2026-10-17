import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# Configuración de la página
st.set_page_config(
    page_title="Creaciones Rodhe | E-commerce & Importaciones Venezuela",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- PERSISTENCIA DE BASE DE DATOS LOCAL (CSV) -----------------
DB_FILE = "ventas_rodhe.csv"

def load_database():
    """Carga los pedidos desde el archivo CSV persistente en disco."""
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            orders_list = []
            for _, row in df.iterrows():
                orders_list.append({
                    "id": int(row["id"]),
                    "client_name": str(row["client_name"]),
                    "items": eval(row["items"]) if pd.notna(row["items"]) else [],
                    "total": float(row["total"]),
                    "payment_mode": str(row.get("payment_mode", "Pago Total (100%)")),
                    "amount_paid": float(row.get("amount_paid", row["total"])),
                    "payment": str(row["payment"]),
                    "reference": str(row["reference"]),
                    "bank": str(row["bank"]),
                    "date_paid": str(row["date_paid"]),
                    "state": str(row["state"]),
                    "municipality": str(row["municipality"]),
                    "courier": str(row["courier"]),
                    "status": str(row["status"]),
                    "purchase_note": str(row["purchase_note"]),
                    "delivery_note": str(row["delivery_note"]),
                    "created_at": str(row["created_at"])
                })
            return orders_list
        except Exception:
            return []
    return []

def save_order_to_disk(new_order):
    """Agrega un nuevo pedido y lo guarda de forma permanente en el archivo CSV."""
    st.session_state.orders.append(new_order)
    data_to_save = []
    for order in st.session_state.orders:
        data_to_save.append({
            "id": order["id"],
            "client_name": order["client_name"],
            "items": str(order["items"]),
            "total": order["total"],
            "payment_mode": order.get("payment_mode", "Pago Total (100%)"),
            "amount_paid": order.get("amount_paid", order["total"]),
            "payment": order["payment"],
            "reference": order["reference"],
            "bank": order["bank"],
            "date_paid": order["date_paid"],
            "state": order["state"],
            "municipality": order["municipality"],
            "courier": order["courier"],
            "status": order["status"],
            "purchase_note": order["purchase_note"],
            "delivery_note": order["delivery_note"],
            "created_at": order["created_at"]
        })
    df_save = pd.DataFrame(data_to_save)
    df_save.to_csv(DB_FILE, index=False)

# ----------------- COMPONENTE PIE DE PÁGINA: TÉRMINOS DE GARANTÍA -----------------
def render_warranty_footer():
    """Muestra el resumen visual con los términos de garantía en el pie de página."""
    st.markdown("---")
    st.info("""
    🛡️ **Términos de Garantía y Compromiso Rodhe:**
    * **Stock Nacional:** Todos nuestros productos disponen de **7 días continuos de garantía** por defectos de fábrica tras la recepción del paquete.
    * **Pre-pedidos Internacionales (Shein, Alibaba, Amazon):** Garantizamos inspección de calidad e integridad desde nuestro casillero en Miami (`SEU-62819`) hasta la entrega a la empresa de encomienda en Venezuela.
    * **Logística Inversa:** Los retornos por cambio de opinión corren por cuenta del comprador; las sustituciones por errores de despacho o defectos verificados son cubiertas al 100% por Creaciones Rodhe.
    """)

# ----------------- POOLS DE IMÁGENES ROTATIVAS -----------------
JEWELRY_POOL = [
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1611591475759-33534d119fdc?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80"
]

TECH_POOL = [
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1609592424104-14d2e5d84c2a?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=500&q=80"
]

def get_daily_product_image(category, index):
    day_offset = datetime.now().timetuple().tm_yday
    pool = JEWELRY_POOL if category == "Bisuteria" else TECH_POOL
    return pool[(index + day_offset) % len(pool)]

# ----------------- FUNCIÓN DE BOTÓN WHATSAPP -----------------
def create_whatsapp_button(phone_number, customer_name, order_id, total, amount_paid, payment_mode, reference, state, courier):
    balance = total - amount_paid
    msg_payment = f"Pago Total (100%): *${total:.2f} USD*" if payment_mode == "Pago Total (100%)" else f"Abono (50%): *${amount_paid:.2f} USD* (Restante:${balance:.2f} USD)"
    
    message = (
        f"¡Hola {customer_name}! 💎 Gracias por confiar en *Creaciones Rodhe*.\n\n"
        f"Tu pedido *#{order_id}* ha sido registrado.\n"
        f"Modalidad: {msg_payment}\n"
        f"Ref de pago: *{reference}* | Destino: *{state}* vía *{courier}*\n"
        f"📦 Tiempo estimado de entrega: *3 a 5 días hábiles*.\n\n"
        f"Te mantendremos informado. ¡Estamos a tu orden!"
    )
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
    
    button_html = f"""
    <a href="{whatsapp_url}" target="_blank" style="
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 12px 20px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        💬 Notificar por WhatsApp al Cliente
    </a>
    """
    return button_html

# ----------------- INICIALIZACIÓN DE ESTADOS -----------------
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = load_database()
if 'quotes' not in st.session_state:
    st.session_state.quotes = []
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# CATÁLOGO AMPLIADO A 50 PRODUCTOS (25 Bisutería + 25 Tecnología)
if 'products' not in st.session_state:
    st.session_state.products = [
        # --- 25 BISUTERÍA ---
        {"id": 1, "name": "Set Cadenas Minimalistas Acero", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 12.0, "price_wholesale": 8.5, "stock": 50, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 2, "name": "Anillos Apilables Zirconias (Set x5)", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 40, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 3, "name": "Pulsera Estilo Cartier Baño Oro 18k", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 25, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 4, "name": "Zarcillos Huggies Brillantes", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 60, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 5, "name": "Kit Emprendedor Bisutería (20 pzas)", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 65.0, "price_wholesale": 48.0, "stock": 15, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 6, "name": "Collar Ojo Turco con Circones", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 14.0, "price_wholesale": 9.5, "stock": 35, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 7, "name": "Tobillera Doble en Acero Inoxidable", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 7.0, "price_wholesale": 4.5, "stock": 45, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 8, "name": "Gargantilla Choker de Lujo", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 22.0, "price_wholesale": 15.0, "stock": 20, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 9, "name": "Pulseras de Hilo con Dijes de Plata", "category": "Bisuteria", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 6.0, "price_wholesale": 3.8, "stock": 50, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 10, "name": "Set Anillos Midi Boho Chic", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 9.0, "price_wholesale": 6.0, "stock": 30, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 11, "name": "Reloj Dama Elegante Acero Rosé", "category": "Bisuteria", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 35.0, "price_wholesale": 26.0, "stock": 15, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 12, "name": "Aretes Largos de Fiesta con Cristales", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 11.0, "price_wholesale": 7.5, "stock": 25, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 13, "name": "Colgante Letra Inicial Personalizada", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 10.0, "price_wholesale": 6.8, "stock": 40, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 14, "name": "Pulsera Tenis con Cristales Austríacos", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 28.0, "price_wholesale": 20.0, "stock": 18, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 15, "name": "Set Anillos de Pareja Ajustables", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.5, "price_wholesale": 5.5, "stock": 30, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 16, "name": "Broche de Solapa Perlas y Zirconias", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 12.0, "price_wholesale": 8.0, "stock": 22, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 17, "name": "Anillo Solitario de Compromiso Baño Oro", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 30.0, "price_wholesale": 22.0, "stock": 12, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 18, "name": "Zarcillos Pequeños Geometricos Acero", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 5.0, "price_wholesale": 3.0, "stock": 60, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 19, "name": "Cadena de Cuerpo (Body Chain) Playa", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 15.0, "price_wholesale": 10.0, "stock": 20, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 20, "name": "Pulseras Magnéticas del Amor (Par)", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 9.99, "price_wholesale": 6.5, "stock": 35, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 21, "name": "Collar Multicapas con Monedas", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 13.0, "price_wholesale": 9.0, "stock": 28, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 22, "name": "Juego de Joyas de Novia Completo", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 45.0, "price_wholesale": 32.0, "stock": 8, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 23, "name": "Anillo Giratorio Antiestrés Acero", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 11.0, "price_wholesale": 7.2, "stock": 30, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 24, "name": "Zarcillos Enhebrados Cadena Larga", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 6.5, "price_wholesale": 4.0, "stock": 40, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 25, "name": "Tobillera con Dijes de Cristales", "category": "Bisuteria", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 7.5, "price_wholesale": 4.8, "stock": 35, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},

        # --- 25 TECNOLOGÍA ---
        {"id": 26, "name": "Smartwatch Deportivo Ultra Serie 8", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 30, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 27, "name": "Audífonos Inalámbricos TWS Pro ANC", "category": "Tecnologia", "origin": "eBay", "tag": "En Oferta", "price_retail": 15.0, "price_wholesale": 10.5, "stock": 45, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 28, "name": "Aro de Luz LED 10' con Trípode Studio", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Rotación", "price_retail": 22.0, "price_wholesale": 16.0, "stock": 20, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 29, "name": "Power Bank Carga Rápida 20,000mAh", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 28.0, "price_wholesale": 21.0, "stock": 35, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 30, "name": "Cargador Rápido USB-C GaN 65W", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 31, "name": "Mini Impresora Térmica Portátil Bluetooth", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 32.0, "price_wholesale": 24.0, "stock": 18, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 32, "name": "Gimbal Estabilizador para Smartphone L08", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 45.0, "price_wholesale": 34.0, "stock": 12, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 33, "name": "Lámpara de Escritorio LED con Carga Inalámbrica", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 30.0, "price_wholesale": 22.0, "stock": 15, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 34, "name": "Cable Magnético 3 en 1 Carga Rápida", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 6.0, "price_wholesale": 3.8, "stock": 70, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 35, "name": "Soporte Magnético de Auto con Carga Qi", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 18.0, "price_wholesale": 12.5, "stock": 30, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 36, "name": "Bocina Bluetooth Portátil Impermeable IPX7", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 24.0, "price_wholesale": 17.0, "stock": 25, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 37, "name": "Smart Glasses con Audio Bluetooth", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Gama", "price_retail": 55.0, "price_wholesale": 42.0, "stock": 10, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 38, "name": "Kit de Limpieza 7 en 1 para Gadgets", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 50, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 39, "name": "Hub USB-C 5 en 1 Multipuerto Adaptador", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 22.0, "price_wholesale": 15.5, "stock": 22, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 40, "name": "Cámara de Seguridad WiFi Mini 1080p", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Gama", "price_retail": 26.0, "price_wholesale": 19.0, "stock": 20, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 41, "name": "Micrófono Lavalier Inalámbrico Dual", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 35.0, "price_wholesale": 27.0, "stock": 16, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 42, "name": "Reloj Inteligente Infantil con GPS Q12", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 43, "name": "Teclado y Mouse Inalámbrico Ergonómico Slim", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 38.0, "price_wholesale": 28.0, "stock": 12, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 44, "name": "Organizador de Cables de Viaje Impermeable", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 9.0, "price_wholesale": 5.8, "stock": 40, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 45, "name": "Proyector LED Portátil Mini HD 1080p", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 85.0, "price_wholesale": 68.0, "stock": 6, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 46, "name": "Soporte Plegable de Aluminio para Laptop", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 16.0, "price_wholesale": 11.0, "stock": 28, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 47, "name": "Control de Juegos Bluetooth para Móvil", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 18, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 48, "name": "Localizador Bluetooth Anti-Pérdida Smart Tag", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 50, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 49, "name": "Ventilador Portátil de Cuello Recargable", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 14.0, "price_wholesale": 9.5, "stock": 35, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 50, "name": "Estación de Carga Inalámbrica 3 en 1 MagSafe", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 40.0, "price_wholesale": 30.0, "stock": 14, "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"}
    ]

# ----------------- BARRA LATERAL (LOGO Y MENÚ) -----------------
with st.sidebar:
    try:
        st.image("logo.png", width=120)
    except:
        st.markdown("### 💎 Creaciones Rodhe")
    
    st.markdown("**Plataforma Digital de Lujo**")
    st.caption(f"📅 50 Productos Activos en Catálogo")
    st.markdown("---")

menu = st.sidebar.radio("Menú Principal", [
    "🛍️ Catálogo y Tienda", 
    "🤝 Tiendas Aliadas (Al Mayor)",
    "📦 Cotizador Shein / Amazon", 
    "🛒 Carrito de Compras", 
    "📋 Mis Pedidos y Estatus", 
    "🔐 Panel de Administración"
])

# ----------------- VISTA 1: CATÁLOGO Y TIENDA -----------------
if menu == "🛍️ Catálogo y Tienda":
    st.title("💎 Catálogo Exclusivo (50 Artículos - Bisutería & Tecnología)")
    st.markdown("Explora nuestra selección filtrada por categoría y etiquetada por categoría comercial (*En Oferta, Alta Rotación, Alta Gama*).")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_cat = st.selectbox("Filtrar por Categoría", ["Todas", "Bisuteria", "Tecnologia"])
    with col2:
        selected_tag = st.selectbox("Filtrar por Tendencia", ["Todas", "En Oferta", "Alta Rotación", "Alta Gama"])
    with col3:
        pricing_mode = st.radio("Modo de Compra", ["Detal", "Al Mayor (Pre-pedidos)"], horizontal=True)

    is_wholesale = "Mayor" in pricing_mode
    
    # Filtrado dinámico
    filtered_products = st.session_state.products
    if selected_cat != "Todas":
        filtered_products = [p for p in filtered_products if p["category"] == selected_cat]
    if selected_tag != "Todas":
        filtered_products = [p for p in filtered_products if p["tag"] == selected_tag]

    st.markdown(f"**Mostrando {len(filtered_products)} productos disponibles:**")
    
    cols = st.columns(3)
    for index, product in enumerate(filtered_products):
        daily_image = get_daily_product_image(product["category"], product["id"])
        
        with cols[index % 3]:
            st.image(daily_image, use_container_width=True)
            st.subheader(product["name"])
            st.markdown(f"🏷️ **Origen:** `{product['origin']}` | ⚡ **Tag:** `{product['tag']}`")
            
            price = product["price_wholesale" if is_wholesale else "price_retail"]
            st.markdown(f"**Precio:** ${price:.2f} USD")
            st.markdown(f"📦 *Stock:* {product['stock']} unidades")
            
            with st.expander("Ver Video / Reel Real del Producto"):
                st.video(product.get("video_url", "https://www.w3schools.com/html/mov_bbb.mp4"))
                st.caption("Demostración real en alta calidad.")
            
            if st.button(f"Agregar al Carrito", key=f"add_{product['id']}"):
                st.session_state.cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": price,
                    "origin": product["origin"],
                    "mode": "Mayor" if is_wholesale else "Detal"
                })
                st.success(f"¡{product['name']} agregado!")

# ----------------- VISTA 3: COTIZADOR INTERNACIONAL -----------------
elif menu == "📦 Cotizador Shein / Amazon":
    st.title("📦 Buzón de Cotizaciones Internacionales")
    st.markdown("Pega el enlace de **Shein, Alibaba, Amazon o eBay** para calcular tu importación.")

    with st.form("quote_form"):
        product_url = st.text_input("URL del Producto")
        category_q = st.selectbox("Categoría", ["Bisuteria", "Tecnologia"])
        quantity_q = st.number_input("Cantidad deseada", min_value=1, value=1)
        submit_quote = st.form_submit_button("Calcular Cotización Automática")

    if submit_quote and product_url:
        platform = "Amazon" if "amazon" in product_url.lower() else "Shein / Alibaba"
        base_price = 24.99 if "amazon" in product_url.lower() else 8.50
        weight = 0.3 if category_q == "Bisuteria" else 1.2
        shipping_fee = weight * 20.0
        final_price = ((base_price * quantity_q) + shipping_fee) * 1.35
        
        st.success("¡Cotización Generada!")
        st.markdown(f"### Estatus para {platform}")
        # LÍNEA 310 CORREGIDA:
        st.markdown(f"- **Precio Base:** ${base_price:.2f} | **Flete Estimado:** ${shipping_fee:.2f}")
        st.markdown(f"### **Total Estimado en Venezuela:** ${final_price:.2f} USD")
        
        if st.button("Guardar en mi Panel"):
            st.session_state.quotes.append({"platform": platform, "total": final_price, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
            st.info("Cotización guardada.")

# ----------------- VISTA 4: CARRITO, PAGO Y OPCIÓN DE ABONO -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("🛒 Tu Carrito de Compras, Envío y Modalidad de Pago")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general = 0
        for item in st.session_state.cart:
            st.markdown(f"- **{item['name']}** ({item['origin']}) - [{item['mode']}] - **${item['price']:.2f}**")
            total_general += item['price']
        
        st.markdown(f"### Total General del Pedido: **${total_general:.2f} USD**")
        st.markdown("---")
        
        st.subheader("1. Selecciona la Modalidad de Pago")
        payment_mode_choice = st.radio(
            "¿Cómo deseas realizar el pago?", 
            ["Pago Total (100%)", "Abono Parcial (50%)"],
            horizontal=True
        )
        
        if payment_mode_choice == "Abono Parcial (50%)":
            amount_to_pay_now = total_general * 0.5
            balance_due = total_general * 0.5
            st.warning(f"💡 **Has elegido Abono del 50%:** Debes cancelar hoy **${amount_to_pay_now:.2f} USD**. El 50\% restante (**${balance_due:.2f} USD**) se cancela al recibir tu encomienda.")
        else:
            amount_to_pay_now = total_general
            balance_due = 0.0
            st.success(f"💳 **Pago Total Contado:** Monto exacto a cancelar hoy: **${amount_to_pay_now:.2f} USD**.")

        st.markdown("---")
        st.subheader("2. Datos de Envío y Destino en Venezuela")
        with st.form("shipping_dest_form"):
            col_env1, col_env2, col_env3 = st.columns(3)
            with col_env1:
                venezuela_states = [
                    "Yaracuy", "Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", 
                    "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Distrito Capital", 
                    "Falcón", "Guárico", "Lara", "Mérida", "Miranda", "Monagas", 
                    "Nueva Esparta", "Portuguesa", "Sucre", "Táchira", "Trujillo", 
                    "Vargas (La Guaira)", "Zulia"
                ]
                selected_state = st.selectbox("Estado de Destino", sorted(list(set(venezuela_states))))
            with col_env2:
                municipality_input = st.text_input("Municipio / Ciudad", placeholder="Ej. San Felipe")
            with col_env3:
                courier_choice = st.selectbox("Empresa de Encomienda", ["MRW", "Zoom", "Tealca", "Domesa"])
            
            st.markdown("---")
            st.subheader("3. Selecciona tu Pasarela de Pago")
            payment_method = st.selectbox("Método", [
                "Pago Móvil - Banca Amiga", 
                "Zinli (Ahorro / ACH Xpress)", 
                "Efectivo Divisa"
            ])
            
            if payment_method == "Pago Móvil - Banca Amiga":
                st.success(f"""
                📱 **Datos Pago Móvil (Banca Amiga):**
                - **Cédula / RIF:** V-14242461
                - **Teléfono:** 04244581437
                - **Titular:** Rosa María Pacheco Azuaje
                - **Banco:** Banca Amiga (0172)
                """)
            elif payment_method == "Zinli (Ahorro / ACH Xpress)":
                st.success("""
                💳 **Datos Zinli / ACH Xpress:**
                - **Cuenta de Ahorro:** 3-002-05387291-65 | **Titular:** Rosa Pacheco
                """)
                
            st.markdown("---")
            st.subheader("4. Registro de Datos de Pago del Cliente")
            
            col_1, col_2 = st.columns(2)
            with col_1:
                client_name_input = st.text_input("Nombre y Apellido del Cliente", value="Cliente General")
                ref_number = st.text_input("Número de Referencia Bancaria / Operación")
                bank_used = st.text_input("Banco Emisor (Ej: Mercantil, Zinli)")
            with col_2:
                payment_date = st.date_input("Fecha del Pago", value=datetime.today())
                client_phone = st.text_input("Teléfono del Cliente (Ej: 584144581437 para WhatsApp)")
            
            submit_payment = st.form_submit_button("Confirmar y Registrar Pedido Definitivo")

        if submit_payment:
            if not ref_number:
                st.error("Por favor, ingresa el número de referencia del pago.")
            elif not municipality_input:
                st.error("Por favor, indica el municipio o ciudad de destino.")
            else:
                new_order_id = len(st.session_state.orders) + 1
                items_in_order = st.session_state.cart.copy()
                
                new_order_data = {
                    "id": new_order_id,
                    "client_name": client_name_input,
                    "items": items_in_order,
                    "total": total_general,
                    "payment_mode": payment_mode_choice,
                    "amount_paid": amount_to_pay_now,
                    "payment": payment_method,
                    "reference": ref_number,
                    "bank": bank_used,
                    "date_paid": str(payment_date),
                    "state": selected_state,
                    "municipality": municipality_input,
                    "courier": courier_choice,
                    "status": "Pagado y Verificado",
                    "purchase_note": f"Modalidad: {payment_mode_choice} - Ref: {ref_number} ({bank_used})",
                    "delivery_note": f"Envío por {courier_choice} hacia {selected_state} ({municipality_input})",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                save_order_to_disk(new_order_data)
                st.success("¡Pedido, modalidad de pago y datos guardados de forma permanente en la base de datos!")
                
                if client_phone:
                    st.markdown("### Notificar al Cliente vía WhatsApp")
                    whatsapp_btn = create_whatsapp_button(
                        phone_number=client_phone,
                        customer_name=client_name_input,
                        order_id=new_order_id,
                        total=total_general,
                        amount_paid=amount_to_pay_now,
                        payment_mode=payment_mode_choice,
                        reference=ref_number,
                        state=selected_state,
                        courier=courier_choice
                    )
                    st.markdown(whatsapp_btn, unsafe_allow_html=True)
                
                st.session_state.cart = []

    render_warranty_footer()

# ----------------- VISTA 5: MIS PEDIDOS -----------------
elif menu == "📋 Mis Pedidos y Estatus":
    st.title("📋 Historial de Pedidos y Estatus")
    if not st.session_state.orders and not st.session_state.quotes:
        st.write("Aún no tienes registros.")
    else:
        for order in st.session_state.orders:
            st.markdown(f"**Pedido #{order['id']}** | Cliente: **{order.get('client_name', 'N/A')}** | Total: **${order['total']:.2f}**")
            st.markdown(f"📌 *Modalidad:* `{order.get('payment_mode', 'Pago Total (100%)')}` | *Pagado:* `${order.get('amount_paid', order['total']):.2f}`")
            st.markdown(f"📍 *Destino:* {order.get('state')} / {order.get('municipality')} vía `{order.get('courier')}`")
            st.markdown(f"🔢 *Referencia:* `{order.get('reference', 'N/A')}` | *Fecha Pago:* {order.get('date_paid', 'N/A')}")
            st.markdown("---")

    render_warranty_footer()

# ----------------- VISTA 6: PANEL DE ADMINISTRACIÓN Y GESTIÓN DE VIDEOS -----------------
elif menu == "🔐 Panel de Administración":
    st.title("🔐 Panel de Control Administrativo & Gestión Multimedia")
    
    if not st.session_state.admin_logged:
        admin_pass = st.text_input("Contraseña de Administrador", type="password")
        if st.button("Entrar"):
            if admin_pass == "rodhe2026*":
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    else:
        st.success("Acceso Administrador Autorizado")
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged = False
            st.rerun()
            
        st.markdown("---")
        
        st.subheader("📹 Editor de Videos Reales (Reels del Catálogo de 50 Artículos)")
        selected_prod_id = st.selectbox(
            "Seleccionar Producto del Catálogo", 
            options=[p["id"] for p in st.session_state.products],
            format_func=lambda x: next(f"ID {p['id']} - {p['name']} ({p['origin']})" for p in st.session_state.products if p["id"] == x)
        )
        
        prod_to_edit = next(p for p in st.session_state.products if p["id"] == selected_prod_id)
        
        with st.form(f"edit_video_form_{selected_prod_id}"):
            current_video = prod_to_edit.get("video_url", "")
            new_video_url = st.text_input("URL del Video Real (Enlace MP4 o Reel)", value=current_video)
            submit_video_edit = st.form_submit_button("Actualizar Video del Producto")
            
            if submit_video_edit:
                prod_to_edit["video_url"] = new_video_url
                st.success(f"¡Video actualizado para: {prod_to_edit['name']}!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("📊 Base de Datos General (Almacenamiento Permanente por Fecha)")
        
        # LÍNEA CORREGIDA AQUÍ ABAJO:
        paid_orders = [o for o in st.session_state.orders if o.get('status') == "Pagado y Verificado"]
        
        if not paid_orders:
            st.info("No hay pedidos pagados y verificados registrados en el sistema actualmente.")
        else:
            st.metric("Total Histórico de Pedidos Pagados", len(paid_orders))
