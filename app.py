import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Creaciones Rodhe | E-commerce & Importaciones Venezuela",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- FUNCIONES DE ACTUALIZACIÓN DIARIA DE IMÁGENES -----------------
# Bancos de imágenes de alta gama que rotan automáticamente según el día del año
JEWELRY_POOL = [
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1611591475759-33534d119fdc?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=500&q=80"
]

TECH_POOL = [
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1609592424104-14d2e5d84c2a?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=500&q=80",
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=500&q=80"
]

def get_daily_product_image(category, index):
    """Calcula un índice rotativo basado en el día actual del año (tm_yday)"""
    day_offset = datetime.now().timetuple().tm_yday
    pool = JEWELRY_POOL if category == "Bisuteria" else TECH_POOL
    rotated_index = (index + day_offset) % len(pool)
    return pool[rotated_index]

# ----------------- INICIALIZACIÓN DE ESTADOS -----------------
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'quotes' not in st.session_state:
    st.session_state.quotes = []
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# Catálogo Base con los 10 productos más solicitados en Venezuela
if 'products' not in st.session_state:
    st.session_state.products = [
        {"id": 1, "name": "Set de Cadenas Minimalistas Acero Quirúrgico", "category": "Bisuteria", "price_retail": 12.0, "price_wholesale": 8.5, "stock": 50},
        {"id": 2, "name": "Anillos Apilables con Zirconias (Set x5)", "category": "Bisuteria", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 40},
        {"id": 3, "name": "Pulsera Estilo Cartier de Lujo (Baño Oro 18k)", "category": "Bisuteria", "price_retail": 18.0, "price_wholesale": 13.0, "stock": 25},
        {"id": 4, "name": "Zarcillos Huggie con Incrustaciones", "category": "Bisuteria", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 60},
        {"id": 5, "name": "Kit Emprendedor Bisutería Surtida (20 pzas)", "category": "Bisuteria", "price_retail": 65.0, "price_wholesale": 48.0, "stock": 15},
        {"id": 6, "name": "Smartwatch Deportivo Ultra Serie 8", "category": "Tecnologia", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 30},
        {"id": 7, "name": "Audífonos Inalámbricos TWS Pro con Cancelación", "category": "Tecnologia", "price_retail": 15.0, "price_wholesale": 10.5, "stock": 45},
        {"id": 8, "name": "Aro de Luz LED 10' con Trípode para Streamers", "category": "Tecnologia", "price_retail": 22.0, "price_wholesale": 16.0, "stock": 20},
        {"id": 9, "name": "Power Bank Carga Rápida 20,000mAh", "category": "Tecnologia", "price_retail": 28.0, "price_wholesale": 21.0, "stock": 35},
        {"id": 10, "name": "Cargador Rápido Multipuerto USB-C GaN 65W", "category": "Tecnologia", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25}
    ]

# ----------------- BARRA LATERAL CON LOGOTIPO -----------------
with st.sidebar:
    # Logotipo Corporativo (Imagen estilizada o banner de marca)
    st.image("logorode.jpg", width=120)
    st.markdown("# 💎 Creaciones Rodhe")
    st.markdown("**Plataforma Digital de Lujo**")
    st.caption(f"📅 Rotación diaria activa - {datetime.now().strftime('%d/%m/%Y')}")
    st.markdown("---")

menu = st.sidebar.radio("Menú Principal", [
    "🛍️ Catálogo y Tienda", 
    "📦 Cotizador Shein / Amazon", 
    "🛒 Carrito de Compras", 
    "📋 Mis Pedidos y Estatus", 
    "🔐 Panel de Administración"
])

# ----------------- VISTA 1: CATÁLOGO CON IMÁGENES ROTATIVAS DIARIAS -----------------
if menu == "🛍️ Catálogo y Tienda":
    st.title("💎 Catálogo Exclusivo - Creaciones Rodhe")
    st.markdown("Bisutería fina y tecnología de alta demanda. *Las imágenes de exhibición se actualizan automáticamente cada día.*")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_cat = st.selectbox("Filtrar por Categoría", ["Todas", "Bisuteria", "Tecnologia"])
    with col2:
        pricing_mode = st.radio("Modo de Compra", ["Detal", "Al Mayor (Pre-pedidos / Stock)"], horizontal=True)

    is_wholesale = "Mayor" in pricing_mode
    
    filtered_products = st.session_state.products
    if selected_cat != "Todas":
        filtered_products = [p for p in st.session_state.products if p["category"] == selected_cat]

    cols = st.columns(3)
    for index, product in enumerate(filtered_products):
        # Asignación de imagen dinámica diaria según el índice y el día del año
        daily_image = get_daily_product_image(product["category"], product["id"])
        
        with cols[index % 3]:
            st.image(daily_image, use_container_width=True)
            st.subheader(product["name"])
            price = product["price_wholesale" if is_wholesale else "price_retail"]
            st.markdown(f"**Precio:** ${price:.2f} USD")
            st.markdown(f"📦 *Disponibles:* {product['stock']} unidades")
            
            with st.expander("Ver Video Demostrativo y Reels"):
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                st.caption("Calidad garantizada Creaciones Rodhe.")
            
            if st.button(f"Agregar al Carrito", key=f"add_{product['id']}"):
                st.session_state.cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": price,
                    "mode": "Mayor" if is_wholesale else "Detal"
                })
                st.success(f"¡{product['name']} agregado!")

# ----------------- VISTA 2: COTIZADOR INTERNACIONAL -----------------
elif menu == "📦 Cotizador Shein / Amazon":
    st.title("📦 Buzón de Cotizaciones Internacionales")
    st.markdown("Pega el enlace de **Shein, Amazon, Alibaba o eBay** para calcular tu importación a Venezuela.")

    with st.form("quote_form"):
        product_url = st.text_input("URL del Producto")
        category_q = st.selectbox("Categoría del artículo", ["Bisuteria", "Tecnologia"])
        quantity_q = st.number_input("Cantidad deseada", min_value=1, value=1)
        submit_quote = st.form_submit_button("Calcular Cotización Automática")

    if submit_quote and product_url:
        with st.spinner("Procesando con la pasarela internacional..."):
            base_price = 24.99 if "amazon" in product_url.lower() else 8.50
            platform = "Amazon" if "amazon" in product_url.lower() else "Shein / Alibaba"
            
            weight = 0.3 if category_q == "Bisuteria" else 1.2
            shipping_fee = weight * 20.0
            subtotal = (base_price * quantity_q) + shipping_fee
            final_price = subtotal * 1.35
            
            st.success("¡Cotización Generada!")
            st.markdown(f"### Estatus para {platform}")
            st.markdown(f"- **Precio Base:** ${base_price:.2f}")
            st.markdown(f"- **Flete Miami-Venezuela:** ${shipping_fee:.2f}")
            st.markdown(f"### **Total Estimado:** ${final_price:.2f} USD")
            
            if st.button("Guardar en mi Panel"):
                st.session_state.quotes.append({
                    "platform": platform,
                    "total": final_price,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.info("Cotización guardada exitosamente.")

# ----------------- VISTA 3: CARRITO Y CHECKOUT -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("🛒 Tu Carrito de Compras")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general = 0
        for item in st.session_state.cart:
            st.markdown(f"- **{item['name']}** ({item['mode']}) - **${item['price']:.2f}**")
            total_general += item['price']
        
        st.markdown(f"### Total a Pagar: **${total_general:.2f} USD**")
        st.markdown("---")
        
        payment_method = st.selectbox("Método de Pago (Venezuela)", ["Pago Móvil (Tasa BCV)", "Zelle", "Efectivo Divisa"])
        
        if payment_method.startswith("Pago Móvil"):
            st.info("Banco Mercantil | RIF: V-XXXXXXXX | Telf: 0414-XXXXXXX")
        elif payment_method == "Zelle":
            st.info("Correo: pagos@creacionesrodhe.com")
            
        if st.button("Confirmar Pedido"):
            st.session_state.orders.append({
                "id": len(st.session_state.orders) + 1,
                "total": total_general,
                "payment": payment_method,
                "purchase_note": "Verificando pago recibido.",
                "delivery_note": "Pendiente guía nacional (MRW/Zoom).",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.session_state.cart = []
            st.success("¡Pedido registrado con éxito!")

# ----------------- VISTA 4: MIS PEDIDOS -----------------
elif menu == "📋 Mis Pedidos y Estatus":
    st.title("📋 Historial de Pedidos y Cotizaciones")
    if not st.session_state.orders and not st.session_state.quotes:
        st.write("Aún no tienes registros en el sistema.")
    else:
        for order in st.session_state.orders:
            st.markdown(f"**Pedido #{order['id']}** | Total: **${order['total']:.2f}** ({order['payment']})")
            st.markdown(f"📝 *Compra:* {order['purchase_note']} | 🚚 *Entrega:* {order['delivery_note']}")
            st.markdown("---")

# ----------------- VISTA 5: ADMIN -----------------
elif menu == "🔐 Panel de Administración":
    st.title("🔐 Panel de Control")
    if not st.session_state.admin_logged:
        admin_pass = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if admin_pass == "rodhe2026*":
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    else:
        st.success("Acceso Admin Autorizado")
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged = False
            st.rerun()
        st.metric("Total Pedidos", len(st.session_state.orders))
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders))
