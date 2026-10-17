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

# Inicialización de Base de Datos en Memoria (Session State)
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'quotes' not in st.session_state:
    st.session_state.quotes = []
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# Catálogo Inicial: Los 10 productos más solicitados en Venezuela
if 'products' not in st.session_state:
    st.session_state.products = [
        # Bisutería
        {"id": 1, "name": "Set de Cadenas Minimalistas Acero Quirúrgico", "category": "Bisuteria", "price_retail": 12.0, "price_wholesale": 8.5, "stock": 50, "image": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 2, "name": "Anillos Apilables con Zirconias (Set x5)", "category": "Bisuteria", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 40, "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 3, "name": "Pulsera Estilo Cartier de Lujo (Baño Oro 18k)", "category": "Bisuteria", "price_retail": 18.0, "price_wholesale": 13.0, "stock": 25, "image": "https://images.unsplash.com/photo-1611591475759-33534d119fdc?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 4, "name": "Zarcillos Huggie con Incrustaciones", "category": "Bisuteria", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 60, "image": "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 5, "name": "Kit Emprendedor Bisutería Surtida (20 pzas)", "category": "Bisuteria", "price_retail": 65.0, "price_wholesale": 48.0, "stock": 15, "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        
        # Tecnología y Gadgets
        {"id": 6, "name": "Smartwatch Deportivo Ultra Serie 8", "category": "Tecnologia", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 30, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 7, "name": "Audífonos Inalámbricos TWS Pro con Cancelación", "category": "Tecnologia", "price_retail": 15.0, "price_wholesale": 10.5, "stock": 45, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 8, "name": "Aro de Luz LED 10' con Trípode para Streamers", "category": "Tecnologia", "price_retail": 22.0, "price_wholesale": 16.0, "stock": 20, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 9, "name": "Power Bank Carga Rápida 20,000mAh", "category": "Tecnologia", "price_retail": 28.0, "price_wholesale": 21.0, "stock": 35, "image": "https://images.unsplash.com/photo-1609592424104-14d2e5d84c2a?auto=format&fit=crop&w=500&q=80", "type": "Local"},
        {"id": 10, "name": "Cargador Rápido Multipuerto USB-C GaN 65W", "category": "Tecnologia", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25, "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=500&q=80", "type": "Local"}
    ]

# ----------------- BARRA LATERAL (NAVEGACIÓN) -----------------
st.sidebar.markdown("# 💎 Creaciones Rodhe")
st.sidebar.markdown("*Moda y Tecnología en Venezuela*")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Menú Principal", [
    "🛍️ Catálogo y Tienda", 
    "📦 Cotizador Shein / Amazon", 
    "🛒 Carrito de Compras", 
    "📋 Mis Pedidos y Estatus", 
    "🔐 Panel de Administración"
])

# ----------------- VISTA 1: CATÁLOGO -----------------
if menu == "🛍️ Catálogo y Tienda":
    st.title("Catálogo Exclusivo - Creaciones Rodhe")
    st.markdown("Descubre nuestra selección en bisutería fina y gadgets tecnológicos al **Detal** y al **Mayor**.")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        selected_cat = st.selectbox("Filtrar por Categoría", ["Todas", "Bisuteria", "Tecnologia"])
    with col2:
        pricing_mode = st.radio("Modo de Compra", ["Detal", "Al Mayor (Pre-pedidos / Stock)"], horizontal=True)

    is_wholesale = "Mayor" in pricing_mode
    
    # Filtrar productos
    filtered_products = st.session_state.products
    if selected_cat != "Todas":
        filtered_products = [p for p in st.session_state.products if p["category"] == selected_cat]

    cols = st.columns(3)
    for index, product in enumerate(filtered_products):
        with cols[index % 3]:
            st.image(product["image"], use_container_width=True)
            st.subheader(product["name"])
            price = product["price_wholesale" if is_wholesale else "price_retail"]
            st.markdown(f"**Precio:** ${price:.2f} USD")
            st.markdown(f"📦 *Disponibles:* {product['stock']} unidades")
            
            # Botón de detalle / video demostrativo simulado
            with st.expander("Ver Video Demostrativo y Reels"):
                st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Video de muestra HD
                st.caption("Demostración en alta calidad de brillo y funcionalidad.")
            
            if st.button(f"Agregar al Carrito", key=f"add_{product['id']}"):
                st.session_state.cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": price,
                    "mode": "Mayor" if is_wholesale else "Detal"
                })
                st.success(f"¡{product['name']} agregado al carrito!")

# ----------------- VISTA 2: COTIZADOR INTERNACIONAL (SHEIN / AMAZON) -----------------
elif menu == "📦 Cotizador Shein / Amazon":
    st.title("Buzón de Cotizaciones Internacionales")
    st.markdown("Pega el enlace de **Shein, Amazon, Alibaba o eBay** y calcula automáticamente el costo de importación puesto en Venezuela.")

    with st.form("quote_form"):
        product_url = st.text_input("URL del Producto (Shein, Amazon, etc.)")
        category_q = st.selectbox("Categoría del artículo", ["Bisuteria", "Tecnologia"])
        quantity_q = st.number_input("Cantidad deseada", min_value=1, value=1)
        submit_quote = st.form_submit_button("Calcular Cotización Automática")

    if submit_quote and product_url:
        with st.spinner("Analizando enlace y calculando flete a Venezuela..."):
            # Simulación inteligente de extracción de datos del enlace
            base_price = 15.0 # Precio base simulado de respaldo si el scraper encuentra bloqueo
            if "amazon" in product_url.lower():
                platform = "Amazon"
                base_price = 24.99
            elif "shein" in product_url.lower():
                platform = "Shein"
                base_price = 8.50
            else:
                platform = "Internacional (Alibaba/eBay)"
                base_price = 18.00
            
            # Lógica de costeo Venezuela (Courier + Aranceles + Margen)
            weight = 0.3 if category_q == "Bisuteria" else 1.2
            shipping_fee = weight * 20.0 # Tarifa Miami-Venezuela
            subtotal = (base_price * quantity_q) + shipping_fee
            final_price = subtotal * 1.35 # Margen comercial Rodhe
            
            st.success("¡Cotización Generada con Éxito!")
            st.markdown(f"### Resultados para {platform}")
            st.markdown(f"- **Precio Base Unitario:** ${base_price:.2f}")
            st.markdown(f"- **Peso Estimado Total:** {weight * quantity_q:.1f} lbs")
            st.markdown(f"- **Flete e Importación:** ${shipping_fee:.2f}")
            st.markdown(f"### **Precio Total Estimado en Venezuela:** ${final_price:.2f} USD")
            
            if st.button("Guardar Cotización en mi Panel"):
                st.session_state.quotes.append({
                    "url": product_url,
                    "platform": platform,
                    "total": final_price,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.info("Cotización guardada en tu panel de cliente.")

# ----------------- VISTA 3: CARRITO Y CHECKOUT -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("Tu Carrito de Compras")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general = 0
        for i, item in enumerate(st.session_state.cart):
            st.markdown(f"- **{item['name']}** ({item['mode']}) - **${item['price']:.2f}**")
            total_general += item['price']
        
        st.markdown(f"### Total a Pagar: **${total_general:.2f} USD**")
        st.markdown("---")
        st.subheader("Selecciona tu Método de Pago (Venezuela)")
        
        payment_method = st.selectbox("Pasarela de Pago", ["Pago Móvil (Bs. Tasa BCV)", "Zelle", "Efectivo Divisa"])
        
        if payment_method == "Pago Móvil (Bs. Tasa BCV)":
            st.info("Datos: Banco Mercantil | Rif: V-XXXXXXXX | Telf: 0414-XXXXXXX")
        elif payment_method == "Zelle":
            st.info("Datos: pagos@creacionesrodhe.com | Titular: Rodhe C.A.")
        
        if st.button("Confirmar Pedido y Generar Nota de Compra"):
            new_order = {
                "id": len(st.session_state.orders) + 1,
                "items": st.session_state.cart.copy(),
                "total": total_general,
                "payment": payment_method,
                "purchase_note": "Nota generada con éxito. Verificando transacción.",
                "delivery_note": "Pendiente por guía de envío nacional (MRW/Zoom).",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.orders.append(new_order)
            st.session_state.cart = [] # Vaciar carrito
            st.success("¡Pedido registrado exitosamente! Revisa el apartado de Mis Pedidos.")

# ----------------- VISTA 4: MIS PEDIDOS -----------------
elif menu == "📋 Mis Pedidos y Estatus":
    st.title("Historial de Pedidos y Cotizaciones")
    
    st.subheader("Tus Pedidos Realizados")
    if not st.session_state.orders:
        st.write("No tienes pedidos activos.")
    else:
        for order in st.session_state.orders:
            with st.container():
                st.markdown(f"**Pedido #{order['id']}** - Fecha: {order['date']}")
                st.markdown(f"- **Monto:** ${order['total']:.2f} ({order['payment']})")
                st.markdown(f"- 📝 *Nota de Compra:* {order['purchase_note']}")
                st.markdown(f"- 🚚 *Nota de Entrega / Guía:* {order['delivery_note']}")
                st.markdown("---")
                
    st.subheader("Tus Cotizaciones Internacionales Guardadas")
    if not st.session_state.quotes:
        st.write("No tienes cotizaciones guardadas.")
    else:
        for q in st.session_state.quotes:
            st.markdown(f"- **Plataforma:** {q['platform']} | **Estimado:** ${q['total']:.2f} | **Fecha:** {q['date']}")

# ----------------- VISTA 5: PANEL DE ADMINISTRACIÓN -----------------
elif menu == "🔐 Panel de Administración":
    st.title("Panel de Control Administrativo")
    
    if not st.session_state.admin_logged:
        admin_pass = st.text_input("Contraseña de Administrador", type="password")
        if st.button("Iniciar Sesión"):
            if admin_pass == "rodhe2026*": # Contraseña de ejemplo
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
    else:
        st.success("Acceso Autorizado como Administrador")
        if st.button("Cerrar Sesión Admin"):
            st.session_state.admin_logged = False
            st.rerun()
            
        st.markdown("---")
        st.subheader("Resumen de Operaciones")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pedidos Recibidos", len(st.session_state.orders))
        with col2:
            st.metric("Cotizaciones Solicitadas", len(st.session_state.quotes))
            
        st.subheader("Listado de Pedidos de Clientes")
        if st.session_state.orders:
            st.dataframe(pd.DataFrame(st.session_state.orders))
        else:
            st.write("Aún no hay pedidos registrados.")
