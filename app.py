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
def create_whatsapp_button(phone_number, customer_name, order_id, total, reference, state, courier):
    message = (
        f"¡Hola {customer_name}! 💎 Gracias por confiar en *Creaciones Rodhe*.\n\n"
        f"Tu pedido *#{order_id}* por un monto de *${total:.2f} USD* ha sido registrado.\n"
        f"Ref de pago: *{reference}* | Destino: *{state}* vía *{courier}*\n"
        f"📦 El tiempo promedio para que tu pedido esté en la puerta de tu casa es de *3 a 5 días hábiles*.\n\n"
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
    st.markdown("Red de abastecimiento directo para emprendedores y revendedores en Venezuela.")
    st.info("💡 **Beneficios Mayoristas:** Acceso directo a lotes de alta rotación con tarifas preferenciales y despacho nacional garantizado.")

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

# ----------------- VISTA 4: CARRITO, PAGO Y DATOS DE ENVÍO (ESTADO, MUNICIPIO, MRW) -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("🛒 Tu Carrito de Compras, Envío y Pago Definitivo")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general = 0
        for item in st.session_state.cart:
            st.markdown(f"- **{item['name']}** ({item['origin']}) - [{item['mode']}] - **${item['price']:.2f}**")
            total_general += item['price']
        
        st.markdown(f"### Total a Pagar: **${total_general:.2f} USD**")
        st.markdown("---")
        
        st.subheader("1. Datos de Envío y Destino en Venezuela")
        with st.form("shipping_dest_form"):
            col_env1, col_env2, col_env3 = st.columns(3)
            with col_env1:
                venezuela_states = [
                    "Yaracuy", "Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", 
                    "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Distrito Capital", 
                    "Falcón", "Guárico", "Lara", "Mérida", "Miranda", "Monagas", 
                    "Nueva Esparta", "Portuguesa", "Sucre", "Táchira", "Trujillo", 
                    "Vargas (La Guaira)", "Yaracuy", "Zulia"
                ]
                selected_state = st.selectbox("Estado de Destino", sorted(list(set(venezuela_states))))
            with col_env2:
                municipality_input = st.text_input("Municipio / Ciudad", placeholder="Ej. San Felipe")
            with col_env3:
                courier_choice = st.selectbox("Empresa de Encomienda", ["MRW", "Zoom", "Tealca", "Domesa"])
            
            st.markdown("---")
            st.subheader("2. Selecciona tu Método de Pago")
            payment_method = st.selectbox("Pasarela", [
                "Pago Móvil - Banca Amiga", 
                "Zinli (Ahorro / ACH Xpress)", 
                "Efectivo Divisa"
            ])
            
            if payment_method == "Pago Móvil - Banca Amiga":
                st.success("""
                📱 **Datos Pago Móvil (Banca Amiga):**
                - **Titular:** Rosa María Pacheco Azuaje | **Teléfono:** 04244581437
                """)
            elif payment_method == "Zinli (Ahorro / ACH Xpress)":
                st.success("""
                💳 **Datos Zinli / ACH Xpress:**
                - **Cuenta de Ahorro:** 3-002-05387291-65 | **Titular:** Rosa Pacheco
                """)
                
            st.markdown("---")
            st.subheader("3. Registro de Datos de Pago del Cliente")
            
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
                
                st.session_state.orders.append({
                    "id": new_order_id,
                    "client_name": client_name_input,
                    "items": items_in_order,
                    "total": total_general,
                    "payment": payment_method,
                    "reference": ref_number,
                    "bank": bank_used,
                    "date_paid": str(payment_date),
                    "state": selected_state,
                    "municipality": municipality_input,
                    "courier": courier_choice,
                    "status": "Pagado y Verificado",
                    "purchase_note": f"Pago verificado - Ref: {ref_number} ({bank_used})",
                    "delivery_note": f"Envío por {courier_choice} hacia {selected_state} ({municipality_input})",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("¡Pedido y datos de envío/pago registrados exitosamente!")
                
                if client_phone:
                    st.markdown("### Notificar al Cliente vía WhatsApp")
                    whatsapp_btn = create_whatsapp_button(
                        phone_number=client_phone,
                        customer_name=client_name_input,
                        order_id=new_order_id,
                        total=total_general,
                        reference=ref_number,
                        state=selected_state,
                        courier=courier_choice
                    )
                    st.markdown(whatsapp_btn, unsafe_allow_html=True)
                
                st.session_state.cart = []

# ----------------- VISTA 5: MIS PEDIDOS -----------------
elif menu == "📋 Mis Pedidos y Estatus":
    st.title("📋 Historial de Pedidos y Estatus")
    if not st.session_state.orders and not st.session_state.quotes:
        st.write("Aún no tienes registros.")
    else:
        for order in st.session_state.orders:
            st.markdown(f"**Pedido #{order['id']}** | Cliente: **{order.get('client_name', 'N/A')}** | Total: **${order['total']:.2f}**")
            st.markdown(f"📍 *Destino:* {order.get('state')} / {order.get('municipality')} vía `{order.get('courier')}`")
            st.markdown(f"🔢 *Referencia:* `{order.get('reference', 'N/A')}` | *Estado:* `{order.get('status', 'Pagado')}`")
            st.markdown("---")

# ----------------- VISTA 6: PANEL DE ADMINISTRACIÓN Y REPORTES AVANZADOS -----------------
elif menu == "🔐 Panel de Administración":
    st.title("🔐 Panel de Control Administrativo & Reportes Logísticos")
    
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
        st.subheader("📊 Base de Datos General de Compras Pagadas")
        
        paid_orders = [o for o in st.session_state.orders if o.get('status') == "Pagado y Verificado"]
        
        if not paid_orders:
            st.info("No hay pedidos pagados y verificados registrados en el sistema actualmente.")
        else:
            st.metric("Total Pedidos Pagados", len(paid_orders))
            
            # --- CONSOLIDACIÓN DE DATOS PARA REPORTES ---
            report_data = []
            for order in paid_orders:
                c_name = order.get('client_name', 'Cliente General')
                state_dest = order.get('state', 'N/A')
                municipality_dest = order.get('municipality', 'N/A')
                courier_dest = order.get('courier', 'N/A')
                ref_pay = order.get('reference', 'N/A')
                
                for item in order.get('items', []):
                    store = item.get('origin', 'Stock Nacional')
                    price = item.get('price', 0.0)
                    
                    if store in ["Shein", "Alibaba"]:
                        margin = "35% (Pre-pedido)"
                        delivery_time = "5 a 8 días hábiles"
                        store_type = "Internacional"
                    elif store in ["Amazon", "eBay"]:
                        margin = "30% (Importación)"
                        delivery_time = "4 a 6 días hábiles"
                        store_type = "Internacional"
                    else:
                        margin = "40% (Stock Local)"
                        delivery_time = "1 a 3 días (Nacional)"
                        store_type = "Nacional"
                        
                    report_data.append({
                        "Cliente": c_name,
                        "Producto": item.get('name'),
                        "Modo": item.get('mode'),
                        "Precio (USD)": price,
                        "Margen Comercial": margin,
                        "Tienda / Proveedor": store,
                        "Tipo Empresa": store_type,
                        "Estado Destino": state_dest,
                        "Municipio": municipality_dest,
                        "Encomienda": courier_dest,
                        "Tiempo Estimado": delivery_time,
                        "Referencia Pago": ref_pay
                    })
            
            df_report = pd.DataFrame(report_data)
            
            # --- MÓDULO DE GENERACIÓN DE REPORTES ESPECÍFICOS ---
            st.markdown("### 🔍 Selector de Reportes Avanzados")
            report_type = st.selectbox("Seleccione el tipo de reporte a generar:", [
                "Reporte General Consolidado", 
                "Reporte por Cliente", 
                "Reporte por Empresa (Nacional / Internacional)", 
                "Reporte por Producto", 
                "Reporte por Estado"
            ])
            
            if report_type == "Reporte General Consolidado":
                st.markdown("#### Vista General de Todas las Compras")
                st.dataframe(df_report, use_container_width=True)
                
            elif report_type == "Reporte por Cliente":
                selected_client = st.selectbox("Seleccione el Cliente", df_report["Cliente"].unique())
                df_filtered = df_report[df_report["Cliente"] == selected_client]
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_type == "Reporte por Empresa (Nacional / Internacional)":
                selected_type = st.selectbox("Seleccione tipo de empresa / origen", df_report["Tipo Empresa"].unique())
                df_filtered = df_report[df_report["Tipo Empresa"] == selected_type]
                st.markdown(f"*Mostrando compras para origen: {selected_type} (Ideal para consolidar pedidos con proveedores)*")
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_type == "Reporte por Producto":
                selected_prod = st.selectbox("Seleccione el Producto", df_report["Producto"].unique())
                df_filtered = df_report[df_report["Producto"] == selected_prod]
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_type == "Reporte por Estado":
                selected_st = st.selectbox("Seleccione el Estado de Destino", df_report["Estado Destino"].unique())
                df_filtered = df_report[df_report["Estado Destino"] == selected_st]
                st.dataframe(df_filtered, use_container_width=True)
            
            st.markdown("---")
            # Botón de descarga CSV del reporte seleccionado o general
            csv_export = df_report.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Completa en CSV para Compras",
                data=csv_export,
                file_name=f"reporte_logistico_rodhe_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
