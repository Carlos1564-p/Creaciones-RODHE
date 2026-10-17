import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# Configuración de la página
st.set_page_config(
    page_title="Creaciones Rodhe | E-commerce & Importaciones Venezuela",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- FUNCIONES DE ROTACIÓN DIARIA DE IMÁGENES -----------------
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
def create_whatsapp_button(phone_number, customer_name, order_id, total):
    message = (
        f"¡Hola {customer_name}! 💎 Gracias por confiar en *Creaciones Rodhe*.\n\n"
        f"Tu pedido *#{order_id}* por un monto de *${total:.2f} USD* ha sido registrado con éxito.\n"
        f"📦 El tiempo promedio para que tu pedido esté en la puerta de tu casa es de *3 a 5 días hábiles* (según disponibilidad y despacho nacional).\n\n"
        f"Te mantendremos informado con tu nota de entrega. ¡Estamos a tu orden!"
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
    st.session_state.orders = []
if 'quotes' not in st.session_state:
    st.session_state.quotes = []
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# Catálogo con origen detallado
if 'products' not in st.session_state:
    st.session_state.products = [
        {"id": 1, "name": "Set de Cadenas Minimalistas Acero Quirúrgico", "category": "Bisuteria", "origin": "Shein", "price_retail": 12.0, "price_wholesale": 8.5, "stock": 50},
        {"id": 2, "name": "Anillos Apilables con Zirconias (Set x5)", "category": "Bisuteria", "origin": "Alibaba", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 40},
        {"id": 3, "name": "Pulsera Estilo Cartier de Lujo (Baño Oro 18k)", "category": "Bisuteria", "origin": "Stock Nacional", "price_retail": 18.0, "price_wholesale": 13.0, "stock": 25},
        {"id": 4, "name": "Zarcillos Huggie con Incrustaciones", "category": "Bisuteria", "origin": "Shein", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 60},
        {"id": 5, "name": "Kit Emprendedor Bisutería Surtida (20 pzas)", "category": "Bisuteria", "origin": "Alibaba", "price_retail": 65.0, "price_wholesale": 48.0, "stock": 15},
        {"id": 6, "name": "Smartwatch Deportivo Ultra Serie 8", "category": "Tecnologia", "origin": "Amazon", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 30},
        {"id": 7, "name": "Audífonos Inalámbricos TWS Pro con Cancelación", "category": "Tecnologia", "origin": "eBay", "price_retail": 15.0, "price_wholesale": 10.5, "stock": 45},
        {"id": 8, "name": "Aro de Luz LED 10' con Trípode para Streamers", "category": "Tecnologia", "origin": "Stock Nacional", "price_retail": 22.0, "price_wholesale": 16.0, "stock": 20},
        {"id": 9, "name": "Power Bank Carga Rápida 20,000mAh", "category": "Tecnologia", "origin": "Amazon", "price_retail": 28.0, "price_wholesale": 21.0, "stock": 35},
        {"id": 10, "name": "Cargador Rápido Multipuerto USB-C GaN 65W", "category": "Tecnologia", "origin": "Alibaba", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25}
    ]

# ----------------- BARRA LATERAL (LOGO Y MENÚ) -----------------
with st.sidebar:
    try:
        st.image("logo.png", width=120)
    except:
        st.markdown("### 💎 Creaciones Rodhe")
    
    st.markdown("**Plataforma Digital de Lujo**")
    st.caption(f"📅 Actualización Diaria Activa")
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
    st.title("💎 Catálogo Exclusivo - Creaciones Rodhe")
    st.markdown("Explora nuestra selección identificando el **origen del producto** (Stock Nacional o importado de plataformas globales).")
    
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
        daily_image = get_daily_product_image(product["category"], product["id"])
        
        with cols[index % 3]:
            st.image(daily_image, use_container_width=True)
            st.subheader(product["name"])
            st.markdown(f"🏷️ **Origen / Proveedor:** `{product['origin']}`")
            
            price = product["price_wholesale" if is_wholesale else "price_retail"]
            st.markdown(f"**Precio:** ${price:.2f} USD")
            st.markdown(f"📦 *Disponibles:* {product['stock']} unidades")
            
            with st.expander("Ver Video Demostrativo y Reels"):
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                st.caption("Demostración en alta calidad.")
            
            if st.button(f"Agregar al Carrito", key=f"add_{product['id']}"):
                st.session_state.cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": price,
                    "origin": product["origin"],
                    "mode": "Mayor" if is_wholesale else "Detal"
                })
                st.success(f"¡{product['name']} agregado!")

# ----------------- VISTA 2: TIENDAS ALIADAS (AL MAYOR) -----------------
elif menu == "🤝 Tiendas Aliadas (Al Mayor)":
    st.title("🤝 Módulo de Tiendas Aliadas & Mayoristas")
    st.markdown("Red de abastecimiento directo para emprendedores y revendedores en Venezuela con conexiones logísticas optimizadas.")
    
    st.info("💡 **Beneficios Mayoristas:** Acceso directo a lotes de alta rotación con tarifas preferenciales y despacho nacional garantizado.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🌐 Aliados Internacionales directos")
        st.markdown("""
        - **Shein Partner Hub:** Acceso a catálogos masivos de moda y accesorios.
        - **Alibaba Direct Supply:** Compra de lotes tecnológicos e industriales al costo de fábrica.
        - **Amazon / eBay Bulk:** Suministro de gadgets certificados.
        """)
    with col_b:
        st.subheader("📦 Aliados Logísticos en Venezuela")
        st.markdown("""
        - Despachos nacionales asegurados a través de **MRW, Zoom y Tealca**.
        - Consolidación de carga semanal desde Miami.
        """)

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
        st.markdown(f"- **Precio Base:** ${base_price:.2f} \vert{} **Flete Estimado:**${shipping_fee:.2f}")
        st.markdown(f"### **Total Estimado en Venezuela:** ${final_price:.2f} USD")
        
        if st.button("Guardar en mi Panel"):
            st.session_state.quotes.append({"platform": platform, "total": final_price, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
            st.info("Cotización guardada.")

# ----------------- VISTA 4: CARRITO Y CHECKOUT CON DATOS DE PAGO -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("🛒 Tu Carrito de Compras y Pasarela de Pago")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general = 0
        for item in st.session_state.cart:
            st.markdown(f"- **{item['name']}** ({item['origin']}) - [{item['mode']}] - **${item['price']:.2f}**")
            total_general += item['price']
        
        st.markdown(f"### Total a Pagar: **${total_general:.2f} USD**")
        st.markdown("---")
        
        st.subheader("Selecciona tu Método de Pago Configurado")
        payment_method = st.selectbox("Pasarela de Pago", [
            "Pago Móvil - Banca Amiga", 
            "Zinli (Ahorro / ACH Xpress)", 
            "Efectivo Divisa"
        ])
        
        if payment_method == "Pago Móvil - Banca Amiga":
            st.success("""
            📱 **Instrucciones Pago Móvil (Banca Amiga):**
            - **Banco:** Banca Amiga
            - **Titular:** Rosa María Pacheco Azuaje
            - **Teléfono:** 04244581437
            """)
        elif payment_method == "Zinli (Ahorro / ACH Xpress)":
            st.success("""
            💳 **Instrucciones Zinli / ACH Xpress:**
            - **Cuenta de Ahorro:** 3-002-05387291-65
            - **Titular:** Rosa Pacheco
            - **Plataforma:** Transacciones ACH Xpress
            """)
        
        client_phone = st.text_input("Número de Teléfono del Cliente (Ej: 584144581437 para WhatsApp)")

        if st.button("Confirmar Pedido"):
            new_order_id = len(st.session_state.orders) + 1
            st.session_state.orders.append({
                "id": new_order_id,
                "total": total_general,
                "payment": payment_method,
                "purchase_note": "Pendiente de verificación de pago.",
                "delivery_note": "Pendiente guía de envío nacional (MRW/Zoom/Tealca).",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("¡Pedido registrado exitosamente!")
            
            # Botón de WhatsApp integrado
            if client_phone:
                st.markdown("### Enviar Notificación al Cliente")
                whatsapp_btn = create_whatsapp_button(
                    phone_number=client_phone,
                    customer_name="Estimado Cliente",
                    order_id=new_order_id,
                    total=total_general
                )
                st.markdown(whatsapp_btn, unsafe_allow_html=True)
            else:
                st.warning("Introduce un número de teléfono arriba para habilitar el botón de WhatsApp automático.")
            
            st.session_state.cart = []

# ----------------- VISTA 5: MIS PEDIDOS -----------------
elif menu == "📋 Mis Pedidos y Estatus":
    st.title("📋 Historial de Pedidos y Estatus")
    if not st.session_state.orders and not st.session_state.quotes:
        st.write("Aún no tienes registros.")
    else:
        for order in st.session_state.orders:
            st.markdown(f"**Pedido #{order['id']}** | Total: **${order['total']:.2f}** vía *{order['payment']}*")
            st.markdown(f"📝 *Nota de Compra:* {order['purchase_note']}")
            st.markdown(f"🚚 *Nota de Entrega:* {order['delivery_note']}")
            st.markdown("---")

# ----------------- VISTA 6: ADMIN -----------------
elif menu == "🔐 Panel de Administración":
    st.title("🔐 Panel de Control Administrativo")
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
        st.metric("Total Pedidos Recibidos", len(st.session_state.orders))
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders))
