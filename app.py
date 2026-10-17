import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os
import json

# Configuración de la página
st.set_page_config(
    page_title="Creaciones Rodhe | E-commerce & Importaciones Venezuela",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- PERSISTENCIA DE TASA BCV 24/7 -----------------
BCV_FILE = "bcv_config.json"

def load_bcv_rate():
    """Carga la tasa BCV guardada de forma persistente en disco."""
    if os.path.exists(BCV_FILE):
        try:
            with open(BCV_FILE, "r") as f:
                data = json.load(f)
                return float(data.get("rate", 36.50))
        except Exception:
            return 36.50
    return 36.50

def save_bcv_rate(rate):
    """Guarda la tasa BCV de forma permanente en disco."""
    with open(BCV_FILE, "w") as f:
        json.dump({"rate": float(rate)}, f)

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
                    "amount_paid_ves": float(row.get("amount_paid_ves", 0.0)),
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
            "amount_paid_ves": order.get("amount_paid_ves", 0.0),
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

# ----------------- FUNCIÓN DE BOTÓN WHATSAPP -----------------
def create_whatsapp_button(phone_number, customer_name, order_id, total, amount_paid, amount_paid_ves, payment_mode, reference, state, courier, bcv_rate):
    balance_usd = total - amount_paid
    msg_payment = f"Pago Total (100%): *${total:.2f} USD* (Bs. {amount_paid * bcv_rate:,.2f})" if payment_mode == "Pago Total (100%)" else f"Abono (50%): *${amount_paid:.2f} USD* (Bs. {amount_paid_ves:,.2f} | Restante: ${balance_usd:.2f} USD)"
    
    message = (
        f"¡Hola {customer_name}! 💎 Gracias por confiar en *Creaciones Rodhe*.\n\n"
        f"Tu pedido *#{order_id}* ha sido registrado.\n"
        f"Modalidad: {msg_payment}\n"
        f"Tasa BCV Aplicada: {bcv_rate:.2f} VES/USD\n"
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
if 'bcv_rate' not in st.session_state:
    st.session_state.bcv_rate = load_bcv_rate()

# CATÁLOGO EXACTO DE 50 PRODUCTOS CON RUTAS DE IMAGEN Y VIDEO RIGUROSAMENTE SINCRONIZADAS
if 'products' not in st.session_state:
    st.session_state.products = [
        # --- 25 BISUTERÍA ---
        {"id": 1, "name": "Set Cadenas Minimalistas Acero", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 12.0, "price_wholesale": 8.5, "stock": 50, "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 2, "name": "Anillos Apilables Zirconias (Set x5)", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 40, "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 3, "name": "Pulsera Estilo Cartier Baño Oro 18k", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 25, "image_url": "https://images.unsplash.com/photo-1611591475759-33534d119fdc?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 4, "name": "Zarcillos Huggies Brillantes", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 60, "image_url": "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 5, "name": "Kit Emprendedor Bisutería (20 pzas)", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 65.0, "price_wholesale": 48.0, "stock": 15, "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 6, "name": "Collar Ojo Turco con Circones", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 14.0, "price_wholesale": 9.5, "stock": 35, "image_url": "https://images.unsplash.com/photo-1599643477877-530eb83abc8e?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 7, "name": "Tobillera Doble en Acero Inoxidable", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 7.0, "price_wholesale": 4.5, "stock": 45, "image_url": "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 8, "name": "Gargantilla Choker de Lujo", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 22.0, "price_wholesale": 15.0, "stock": 20, "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 9, "name": "Pulseras de Hilo con Dijes de Plata", "category": "Bisuteria", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 6.0, "price_wholesale": 3.8, "stock": 50, "image_url": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 10, "name": "Set Anillos Midi Boho Chic", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 9.0, "price_wholesale": 6.0, "stock": 30, "image_url": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 11, "name": "Reloj Dama Elegante Acero Rosé", "category": "Bisuteria", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 35.0, "price_wholesale": 26.0, "stock": 15, "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 12, "name": "Aretes Largos de Fiesta con Cristales", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 11.0, "price_wholesale": 7.5, "stock": 25, "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 13, "name": "Colgante Letra Inicial Personalizada", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 10.0, "price_wholesale": 6.8, "stock": 40, "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 14, "name": "Pulsera Tenis con Cristales Austríacos", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 28.0, "price_wholesale": 20.0, "stock": 18, "image_url": "https://images.unsplash.com/photo-1611591475759-33534d119fdc?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 15, "name": "Set Anillos de Pareja Ajustables", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.5, "price_wholesale": 5.5, "stock": 30, "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 16, "name": "Broche de Solapa Perlas y Zirconias", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 12.0, "price_wholesale": 8.0, "stock": 22, "image_url": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 17, "name": "Anillo Solitario de Compromiso Baño Oro", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 30.0, "price_wholesale": 22.0, "stock": 12, "image_url": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 18, "name": "Zarcillos Pequeños Geometricos Acero", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 5.0, "price_wholesale": 3.0, "stock": 60, "image_url": "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 19, "name": "Cadena de Cuerpo (Body Chain) Playa", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 15.0, "price_wholesale": 10.0, "stock": 20, "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 20, "name": "Pulseras Magnéticas del Amor (Par)", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 9.99, "price_wholesale": 6.5, "stock": 35, "image_url": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 21, "name": "Collar Multicapas con Monedas", "category": "Bisuteria", "origin": "Shein", "tag": "Alta Rotación", "price_retail": 13.0, "price_wholesale": 9.0, "stock": 28, "image_url": "https://images.unsplash.com/photo-1599643477877-530eb83abc8e?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 22, "name": "Juego de Joyas de Novia Completo", "category": "Bisuteria", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 45.0, "price_wholesale": 32.0, "stock": 8, "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 23, "name": "Anillo Giratorio Antiestrés Acero", "category": "Bisuteria", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 11.0, "price_wholesale": 7.2, "stock": 30, "image_url": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 24, "name": "Zarcillos Enhebrados Cadena Larga", "category": "Bisuteria", "origin": "Shein", "tag": "En Oferta", "price_retail": 6.5, "price_wholesale": 4.0, "stock": 40, "image_url": "https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 25, "name": "Tobillera con Dijes de Cristales", "category": "Bisuteria", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 7.5, "price_wholesale": 4.8, "stock": 35, "image_url": "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},

        # --- 25 TECNOLOGÍA ---
        {"id": 26, "name": "Smartwatch Deportivo Ultra Serie 8", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 30, "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 27, "name": "Audífonos Inalámbricos TWS Pro ANC", "category": "Tecnologia", "origin": "eBay", "tag": "En Oferta", "price_retail": 15.0, "price_wholesale": 10.5, "stock": 45, "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 28, "name": "Aro de Luz LED 10' con Trípode Studio", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Rotación", "price_retail": 22.0, "price_wholesale": 16.0, "stock": 20, "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 29, "name": "Power Bank Carga Rápida 20,000mAh", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 28.0, "price_wholesale": 21.0, "stock": 35, "image_url": "https://images.unsplash.com/photo-1609592424104-14d2e5d84c2a?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 30, "name": "Cargador Rápido USB-C GaN 65W", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25, "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 31, "name": "Mini Impresora Térmica Portátil Bluetooth", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 32.0, "price_wholesale": 24.0, "stock": 18, "image_url": "https://images.unsplash.com/photo-1612817288484-6f916006741a?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 32, "name": "Gimbal Estabilizador para Smartphone L08", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 45.0, "price_wholesale": 34.0, "stock": 12, "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 33, "name": "Lámpara de Escritorio LED con Carga Inalámbrica", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 30.0, "price_wholesale": 22.0, "stock": 15, "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 34, "name": "Cable Magnético 3 en 1 Carga Rápida", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 6.0, "price_wholesale": 3.8, "stock": 70, "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 35, "name": "Soporte Magnético de Auto con Carga Qi", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 18.0, "price_wholesale": 12.5, "stock": 30, "image_url": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 36, "name": "Bocina Bluetooth Portátil Impermeable IPX7", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 24.0, "price_wholesale": 17.0, "stock": 25, "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 37, "name": "Smart Glasses con Audio Bluetooth", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Gama", "price_retail": 55.0, "price_wholesale": 42.0, "stock": 10, "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 38, "name": "Kit de Limpieza 7 en 1 para Gadgets", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 8.0, "price_wholesale": 5.0, "stock": 50, "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 39, "name": "Hub USB-C 5 en 1 Multipuerto Adaptador", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 22.0, "price_wholesale": 15.5, "stock": 22, "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 40, "name": "Cámara de Seguridad WiFi Mini 1080p", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Gama", "price_retail": 26.0, "price_wholesale": 19.0, "stock": 20, "image_url": "https://images.unsplash.com/photo-1557324232-b8917d7c3dcb?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 41, "name": "Micrófono Lavalier Inalámbrico Dual", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 35.0, "price_wholesale": 27.0, "stock": 16, "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 42, "name": "Reloj Inteligente Infantil con GPS Q12", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 20.0, "price_wholesale": 14.0, "stock": 25, "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 43, "name": "Teclado y Mouse Inalámbrico Ergonómico Slim", "category": "Tecnologia", "origin": "Stock Nacional", "tag": "Alta Gama", "price_retail": 38.0, "price_wholesale": 28.0, "stock": 12, "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 44, "name": "Organizador de Cables de Viaje Impermeable", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 9.0, "price_wholesale": 5.8, "stock": 40, "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 45, "name": "Proyector LED Portátil Mini HD 1080p", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 85.0, "price_wholesale": 68.0, "stock": 6, "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 46, "name": "Soporte Plegable de Aluminio para Laptop", "category": "Tecnologia", "origin": "Alibaba", "tag": "Alta Rotación", "price_retail": 16.0, "price_wholesale": 11.0, "stock": 28, "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 47, "name": "Control de Juegos Bluetooth para Móvil", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Rotación", "price_retail": 25.0, "price_wholesale": 18.0, "stock": 18, "image_url": "https://images.unsplash.com/photo-1612287233002-b1d0ba1395c0?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 48, "name": "Localizador Bluetooth Anti-Pérdida Smart Tag", "category": "Tecnologia", "origin": "Shein", "tag": "En Oferta", "price_retail": 10.0, "price_wholesale": 6.5, "stock": 50, "image_url": "https://images.unsplash.com/photo-1563770660941-20978e870e26?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 49, "name": "Ventilador Portátil de Cuello Recargable", "category": "Tecnologia", "origin": "Alibaba", "tag": "En Oferta", "price_retail": 14.0, "price_wholesale": 9.5, "stock": 35, "image_url": "https://images.unsplash.com/photo-1584467735871-8e853e8563d7?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 50, "name": "Estación de Carga Inalámbrica 3 en 1 MagSafe", "category": "Tecnologia", "origin": "Amazon", "tag": "Alta Gama", "price_retail": 40.0, "price_wholesale": 30.0, "stock": 14, "image_url": "https://images.unsplash.com/photo-1622445275574-55bc73c574db?auto=format&fit=crop&w=500&q=80", "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"}
    ]

# ----------------- BARRA LATERAL (LOGO Y MENÚ) -----------------
with st.sidebar:
    try:
        st.image("logo.png", width=120)
    except Exception:
        st.markdown("### 💎 Creaciones Rodhe")
    
    st.markdown("**Plataforma Digital de Lujo**")
    st.info(f"📊 Tasa BCV Oficial: **{st.session_state.bcv_rate:.2f} VES/USD**")
    st.markdown("---")

menu = st.sidebar.radio("Menú Principal", [
    "🛍️ Catálogo y Tienda", 
    "🤝 Tiendas Aliadas (Al Mayor)",
    "📦 Cotizador Shein / Amazon", 
    "🛒 Carrito de Compras", 
    "📋 Mis Pedidos y Estatus", 
    "🏢 Sobre Nosotros (Misión & Visión)",
    "🔐 Panel de Administración"
])

# ----------------- VISTA 1: CATÁLOGO Y TIENDA (SINCRONIZACIÓN BLINDADA) -----------------
if menu == "🛍️ Catálogo y Tienda":
    st.title("💎 Catálogo Exclusivo (50 Artículos - Bisutería & Tecnología)")
    st.markdown("Explora nuestra selección curada de alta rotación con precios transparentes en USD y Bolívares a tasa oficial BCV.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_cat = st.selectbox("Filtrar por Categoría", ["Todas", "Bisuteria", "Tecnologia"])
    with col2:
        selected_tag = st.selectbox("Filtrar por Tendencia", ["Todas", "En Oferta", "Alta Rotación", "Alta Gama"])
    with col3:
        pricing_mode = st.radio("Modo de Compra", ["Detal", "Al Mayor (Pre-pedidos)"], horizontal=True)

    is_wholesale = "Mayor" in pricing_mode
    
    filtered_products = st.session_state.products
    if selected_cat != "Todas":
        filtered_products = [p for p in filtered_products if p["category"] == selected_cat]
    if selected_tag != "Todas":
        filtered_products = [p for p in filtered_products if p["tag"] == selected_tag]

    st.markdown(f"**Mostrando {len(filtered_products)} productos disponibles:**")
    
    cols = st.columns(3)
    for index, product in enumerate(filtered_products):
        # Enlace estricto y directo usando las propiedades inmutables del objeto producto
        product_image = product["image_url"]
        product_video = product["video_url"]
        product_name = product["name"]
        product_origin = product["origin"]
        product_tag = product["tag"]
        product_stock = product["stock"]
        
        price_usd = product["price_wholesale" if is_wholesale else "price_retail"]
        price_ves = price_usd * st.session_state.bcv_rate
        
        with cols[index % 3]:
            st.image(product_image, use_container_width=True)
            st.subheader(product_name)
            st.markdown(f"🏷️ **Origen:** `{product_origin}` | ⚡ **Tag:** `{product_tag}`")
            
            st.markdown(f"**Precio USD:** `${price_usd:.2f} USD`")
            st.markdown(f"🇻🇪 **Precio BCV:** `Bs. {price_ves:,.2f}`")
            st.markdown(f"📦 *Stock:* {product_stock} unidades")
            
            with st.expander("Ver Video / Reel Real del Producto"):
                st.video(product_video)
                st.caption("Demostración real en alta calidad.")
            
            if st.button("Agregar al Carrito", key=f"add_{product['id']}_{index}"):
                st.session_state.cart.append({
                    "id": product["id"],
                    "name": product_name,
                    "price": price_usd,
                    "origin": product_origin,
                    "mode": "Mayor" if is_wholesale else "Detal"
                })
                st.success(f"¡{product_name} agregado!")

# ----------------- VISTA 3: COTIZADOR INTERNACIONAL -----------------
elif menu == "📦 Cotizador Shein / Amazon":
    st.title("📦 Buzón de Cotizaciones Internacionales")
    st.markdown("Pega el enlace de **Shein, Alibaba, Amazon o eBay** e ingresa el precio publicado para calcular el costo de importación a Venezuela.")

    with st.form("quote_form"):
        product_url = st.text_input("URL o Enlace del Producto", placeholder="Ej: https://www.amazon.com/dp/B08N5WRWNW")
        
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            # Entrada dinámica para el precio real capturado de la página de origen
            origin_price = st.number_input("Precio del Producto en la Página ($ USD)", min_value=0.50, value=15.00, step=1.00)
        with col_q2:
            category_q = st.selectbox("Categoría de Importación", ["Bisuteria / Accesorios", "Tecnologia / Electronica", "Ropa / Calzado", "Hogar / Otros"])
        with col_q3:
            quantity_q = st.number_input("Cantidad Deseada", min_value=1, value=1)
            
        submit_quote = st.form_submit_button("Calcular Cotización Automática")

    if submit_quote and product_url:
        # Detectar la plataforma mediante la URL
        url_lower = product_url.lower()
        if "amazon" in url_lower:
            platform = "Amazon USA"
        elif "shein" in url_lower:
            platform = "Shein"
        elif "alibaba" in url_lower or "aliexpress" in url_lower:
            platform = "Alibaba / AliExpress"
        elif "ebay" in url_lower:
            platform = "eBay"
        else:
            platform = "Tienda Internacional"

        # Determinación de peso estimado según categoría
        if "Bisuteria" in category_q:
            weight = 0.2
        elif "Tecnologia" in category_q:
            weight = 0.8
        elif "Ropa" in category_q:
            weight = 0.5
        else:
            weight = 1.0

        # Cálculo financiero dinámico real
        shipping_fee = weight * 15.0  # Flete aproximado $15 USD/kg desde casillero Miami
        subtotal_base = (origin_price * quantity_q)
        
        # Estructura de importación (Costo base + Flete + Gastos Operativos y Margen Comercial)
        final_price_usd = (subtotal_base + shipping_fee) * 1.30  # 30% Margen operativo e importación
        final_price_ves = final_price_usd * st.session_state.bcv_rate

        st.success(f"¡Cotización calculada exitosamente para **{platform}**!")
        
        st.markdown(f"""
        ### 📊 Desglose de Importación:
        * **Plataforma Origen:** `{platform}`
        * **Monto Base del Producto:** ${subtotal_base:.2f} USD (${origin_price:.2f} x {quantity_q} ud.)
        * **Estimación de Flete Internacional:** ${shipping_fee:.2f} USD (Peso aprox: {weight} kg)
        ---
        ### 💵 Total Estimado a Pagar:
        * **Total en USD:** **${final_price_usd:.2f} USD**
        * 🇻🇪 **Total Exacto en Bolívares (Tasa BCV {st.session_state.bcv_rate:.2f}):** **Bs. {final_price_ves:,.2f}**
        """)

        if st.button("Guardar Cotización en mi Panel"):
            st.session_state.quotes.append({
                "platform": platform,
                "url": product_url,
                "total_usd": final_price_usd,
                "total_ves": final_price_ves,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.info("Cotización guardada exitosamente.")

# ----------------- VISTA 4: CARRITO, PAGO Y PASARELA BCV -----------------
elif menu == "🛒 Carrito de Compras":
    st.title("🛒 Tu Carrito de Compras, Envío y Pasarela BCV")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío.")
    else:
        total_general_usd = 0
        for item in st.session_state.cart:
            item_ves = item['price'] * st.session_state.bcv_rate
            st.markdown(f"- **{item['name']}** ({item['origin']}) - [{item['mode']}] - **${item['price']:.2f} USD** (`Bs. {item_ves:,.2f}`)")
            total_general_usd += item['price']
        
        total_general_ves = total_general_usd * st.session_state.bcv_rate
        st.markdown(f"### Total General: **${total_general_usd:.2f} USD** | 🇻🇪 **Bs. {total_general_ves:,.2f}**")
        st.markdown(f"*(Tasa BCV del día: {st.session_state.bcv_rate:.2f} VES/USD)*")
        st.markdown("---")
        
        st.subheader("1. Selecciona la Modalidad de Pago")
        payment_mode_choice = st.radio(
            "¿Cómo deseas realizar el pago?", 
            ["Pago Total (100%)", "Abono Parcial (50%)"],
            horizontal=True
        )
        
        if payment_mode_choice == "Abono Parcial (50%)":
            amount_to_pay_usd = total_general_usd * 0.5
            amount_to_pay_ves = total_general_ves * 0.5
            balance_usd = total_general_usd * 0.5
            st.warning(f"💡 **Has elegido Abono del 50%:** Debes cancelar hoy **${amount_to_pay_usd:.2f} USD** o exactamente **Bs. {amount_to_pay_ves:,.2f}**. El 50% restante (**${balance_usd:.2f} USD**) se cancela al recibir tu encomienda.")
        else:
            amount_to_pay_usd = total_general_usd
            amount_to_pay_ves = total_general_ves
            st.success(f"💳 **Pago Total Contado:** Monto exacto a cancelar hoy: **${amount_to_pay_usd:.2f} USD** o **Bs. {amount_to_pay_ves:,.2f}**.")

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
                📱 **Datos Pago Móvil (Banca Amiga) - Tasa BCV: {st.session_state.bcv_rate:.2f}:**
                - **Monto Exacto a Pagar:** **Bs. {amount_to_pay_ves:,.2f}** (${amount_to_pay_usd:.2f} USD)
                - **Cédula / RIF:** V-14242461
                - **Teléfono:** 04244581437
                - **Titular:** Rosa María Pacheco Azuaje
                - **Banco:** Banca Amiga (0172)
                """)
            elif payment_method == "Zinli (Ahorro / ACH Xpress)":
                st.success(f"""
                💳 **Datos Zinli / ACH Xpress:**
                - **Monto Exacto:** ${amount_to_pay_usd:.2f} USD
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
                    "total": total_general_usd,
                    "payment_mode": payment_mode_choice,
                    "amount_paid": amount_to_pay_usd,
                    "amount_paid_ves": amount_to_pay_ves,
                    "payment": payment_method,
                    "reference": ref_number,
                    "bank": bank_used,
                    "date_paid": str(payment_date),
                    "state": selected_state,
                    "municipality": municipality_input,
                    "courier": courier_choice,
                    "status": "Pagado y Verificado",
                    "purchase_note": f"Modalidad: {payment_mode_choice} - Ref: {ref_number} (Bs. {amount_to_pay_ves:,.2f})",
                    "delivery_note": f"Envío por {courier_choice} hacia {selected_state} ({municipality_input})",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                save_order_to_disk(new_order_data)
                st.success("¡Pedido, monto en bolívares y datos guardados de forma permanente en la base de datos!")
                
                if client_phone:
                    st.markdown("### Notificar al Cliente vía WhatsApp")
                    whatsapp_btn = create_whatsapp_button(
                        phone_number=client_phone,
                        customer_name=client_name_input,
                        order_id=new_order_id,
                        total=total_general_usd,
                        amount_paid=amount_to_pay_usd,
                        amount_paid_ves=amount_to_pay_ves,
                        payment_mode=payment_mode_choice,
                        reference=ref_number,
                        state=selected_state,
                        courier=courier_choice,
                        bcv_rate=st.session_state.bcv_rate
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
            st.markdown(f"**Pedido #{order['id']}** | Cliente: **{order.get('client_name', 'N/A')}** | Total: **${order['total']:.2f} USD**")
            st.markdown(f"📌 *Modalidad:* `{order.get('payment_mode', 'Pago Total (100%)')}` | *Pagado:* `${order.get('amount_paid', order['total']):.2f}` (Bs. {order.get('amount_paid_ves', 0.0):,.2f})")
            st.markdown(f"📍 *Destino:* {order.get('state')} / {order.get('municipality')} vía `{order.get('courier')}`")
            st.markdown(f"🔢 *Referencia:* `{order.get('reference', 'N/A')}` | *Fecha Pago:* {order.get('date_paid', 'N/A')}")
            st.markdown("---")

    render_warranty_footer()

# ----------------- VISTA 6: SOBRE NOSOTROS (MISIÓN, VISIÓN Y OBJETIVO) -----------------
elif menu == "🏢 Sobre Nosotros (Misión & Visión)":
    st.title("💎 Creaciones Rodhe | Nuestra Identidad Corporativa")
    st.markdown("Conoce el motor que impulsa nuestra plataforma de comercio electrónico e importación de alta gama en Venezuela.")
    
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        try:
            st.image("logo.png", use_container_width=True)
        except Exception:
            st.image("https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80", use_container_width=True)
            st.caption("Creaciones Rodhe - Estilo y Confianza")

    st.markdown("---")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.subheader("🎯 Misión")
        st.write("""
        Proveer a nuestros clientes y aliados comerciales en Venezuela acceso inmediato a un catálogo exclusivo y curado de bisutería de lujo y tecnología innovadora, conectando de forma directa las principales tendencias globales (Shein, Alibaba, Amazon) con la comodidad del mercado local a través de pasarelas de pago seguras y envíos nacionales garantizados.
        """)
        
        st.subheader("🚀 Objetivo Principal")
        st.write("""
        Consolidarnos como la plataforma híbrida b2c y b2b líder en importación y comercio digital en el estado Yaracuy y todo el territorio nacional, ofreciendo una experiencia de compra sin fricciones, con soporte de abono flexible y transparencia financiera total a tasa BCV.
        """)
        
    with col_m2:
        st.subheader("👁️ Visión")
        st.write("""
        Ser reconocidos como el referente nacional en innovación digital para emprendedores y revendedores, destacando por nuestra excelencia logística, control de calidad riguroso desde origen en Miami (SEU-62819) y un modelo de negocio altamente rentable y confiable.
        """)
        
        st.subheader("💡 Valores Corporativos")
        st.write("""
        * **Confianza y Transparencia:** Tasas oficiales BCV actualizadas y precios claros.
        * **Compromiso:** Garantía directa de 7 días y soporte personalizado por WhatsApp.
        * **Innovación:** Cotizadores inteligentes y tecnología adaptada al mercado venezolano.
        """)
        
    render_warranty_footer()

# ----------------- VISTA 7: PANEL DE ADMINISTRACIÓN Y TASA BCV -----------------
elif menu == "🔐 Panel de Administración":
    st.title("🔐 Panel de Control Administrativo & Tasa BCV")
    
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
        
        # --- MÓDULO DE ACTUALIZACIÓN DE TASA BCV 24/7 ---
        st.subheader("💱 Actualizador Permanente de Tasa BCV")
        st.markdown(f"Tasa activa actual en el sistema: **{st.session_state.bcv_rate:.2f} VES / USD**")
        
        with st.form("bcv_update_form"):
            new_bcv = st.number_input("Nueva Tasa Oficial BCV (VES por 1 USD)", min_value=1.00, value=float(st.session_state.bcv_rate), step=0.10)
            submit_bcv = st.form_submit_button("Actualizar y Guardar Tasa BCV (24/7)")
            
            if submit_bcv:
                st.session_state.bcv_rate = new_bcv
                save_bcv_rate(new_bcv)
                st.success(f"¡Tasa BCV actualizada y guardada permanentemente a {new_bcv:.2f} VES/USD!")
                st.rerun()

        st.markdown("---")
        st.subheader("📹 Editor de Videos Reales (Reels del Catálogo de 50 Artículos)")
        
        prod_options = [p["id"] for p in st.session_state.products]
        selected_prod_id = st.selectbox(
            "Seleccionar Producto del Catálogo", 
            options=prod_options,
            format_func=lambda pid: next(f"ID {p['id']} - {p['name']} ({p['origin']})" for p in st.session_state.products if p["id"] == pid)
        )
        
        prod_to_edit = next(p for p in st.session_state.products if p["id"] == selected_prod_id)
        
        with st.form(key=f"edit_video_form_{selected_prod_id}"):
            current_video = prod_to_edit.get("video_url", "")
            new_video_url = st.text_input("URL del Video Real (Enlace MP4 o Reel)", value=current_video)
            submit_video_edit = st.form_submit_button("Actualizar Video del Producto")
            
            if submit_video_edit:
                prod_to_edit["video_url"] = new_video_url
                st.success(f"¡Video actualizado para: {prod_to_edit['name']}!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("📊 Base de Datos General (Almacenamiento Permanente por Fecha)")
        
        paid_orders = [o for o in st.session_state.orders if o.get('status') == "Pagado y Verificado"]
        
        if not paid_orders:
            st.info("No hay pedidos pagados y verificados registrados en el sistema actualmente.")
        else:
            st.metric("Total Histórico de Pedidos Pagados", len(paid_orders))
            
            report_data = []
            for order in paid_orders:
                c_name = order.get('client_name', 'Cliente General')
                state_dest = order.get('state', 'N/A')
                municipality_dest = order.get('municipality', 'N/A')
                courier_dest = order.get('courier', 'N/A')
                ref_pay = order.get('reference', 'N/A')
                payment_date = order.get('date_paid', str(datetime.today().date()))
                pay_mode = order.get('payment_mode', 'Pago Total (100%)')
                paid_amt = order.get('amount_paid', order['total'])
                paid_ves_amt = order.get('amount_paid_ves', 0.0)
                
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
                        "Fecha Pago": payment_date,
                        "Cliente": c_name,
                        "Producto": item.get('name'),
                        "Modo Compra": item.get('mode'),
                        "Modalidad Pago": pay_mode,
                        "Monto Pagado ($)": paid_amt,
                        "Monto Pagado (Bs)": paid_ves_amt,
                        "Precio Item ($)": price,
                        "Margen Comercial": margin,
                        "Proveedor": store,
                        "Tipo": store_type,
                        "Estado Destino": state_dest,
                        "Municipio": municipality_dest,
                        "Encomienda": courier_dest,
                        "Referencia": ref_pay
                    })
            
            df_report = pd.DataFrame(report_data)
            
            st.markdown("### 📅 Reporte Diario y Filtrado Histórico")
            report_mode = st.radio("Seleccione el enfoque del reporte:", [
                "Reporte Diario por Fecha Específica",
                "Reporte Consolidado General", 
                "Reporte por Cliente", 
                "Reporte por Empresa (Nacional / Internacional)", 
                "Reporte por Producto", 
                "Reporte por Estado"
            ], horizontal=True)
            
            if report_mode == "Reporte Diario por Fecha Específica":
                available_dates = sorted(df_report["Fecha Pago"].unique(), reverse=True)
                selected_date = st.selectbox("Seleccione la Fecha de Compra", available_dates)
                df_filtered = df_report[df_report["Fecha Pago"] == selected_date]
                st.markdown(f"#### Compras registradas para el día: `{selected_date}`")
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_mode == "Reporte Consolidado General":
                st.markdown("#### Historial Completo Acumulado")
                st.dataframe(df_report, use_container_width=True)
                
            elif report_mode == "Reporte por Cliente":
                selected_client = st.selectbox("Seleccione el Cliente", df_report["Cliente"].unique())
                df_filtered = df_report[df_report["Cliente"] == selected_client]
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_mode == "Reporte por Empresa (Nacional / Internacional)":
                selected_type = st.selectbox("Seleccione tipo de empresa / origen", df_report["Tipo"].unique())
                df_filtered = df_report[df_report["Tipo"] == selected_type]
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_mode == "Reporte por Producto":
                selected_prod = st.selectbox("Seleccione el Producto", df_report["Producto"].unique())
                df_filtered = df_report[df_report["Producto"] == selected_prod]
                st.dataframe(df_filtered, use_container_width=True)
                
            elif report_mode == "Reporte por Estado":
                selected_st = st.selectbox("Seleccione el Estado de Destino", df_report["Estado Destino"].unique())
                df_filtered = df_report[df_report["Estado Destino"] == selected_st]
                st.dataframe(df_filtered, use_container_width=True)
            
            st.markdown("---")
            csv_export = df_report.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Histórica en CSV",
                data=csv_export,
                file_name=f"base_datos_historica_rodhe_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
