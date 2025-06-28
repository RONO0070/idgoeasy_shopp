import streamlit as st
from datetime import date
from PIL import Image
import base64
import io

# Set page config and improved styling
st.set_page_config(page_title="Sharma Glass & Tin", layout="wide")
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        div.stButton > button {
            background-color: #28a745;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1.5em;
            border: none;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #218838;
            transform: scale(1.05);
        }
        .profile-icon {
            text-align: right;
        }
    </style>
""", unsafe_allow_html=True)

# Session state defaults
if "page" not in st.session_state:
    st.session_state.page = "front"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {}
if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "Glass Bottle", "stock": 100, "rate": 20},
        {"name": "Tin Box", "stock": 50, "rate": 30},
    ]
if "customers" not in st.session_state:
    st.session_state.customers = {}
if "store_title" not in st.session_state:
    st.session_state.store_title = "SHARMA STORE"
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "wallpaper" not in st.session_state:
    st.session_state.wallpaper = None

# ---------------------- AUTH ----------------------
if not st.session_state.logged_in:
    if st.session_state.page == "front":
        st.markdown("""
        <h1 style='text-align:center; font-size: 40px; color: #28a745;'>
        🌟 Your Store Hub
        </h1>
        <h4 style='text-align:center; color: gray;'>
        Manage products, customers, and dues effortlessly
        </h4>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Login"):
                st.session_state.page = "login"
                st.experimental_rerun()
        with col2:
            if st.button("📝 Register"):
                st.session_state.page = "register"
                st.experimental_rerun()

    elif st.session_state.page == "login":
        st.title("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.session_state.current_user = email
                st.experimental_rerun()
            else:
                st.error("❌ Invalid email or password")
        if st.button("🔙 Back"):
            st.session_state.page = "front"
            st.experimental_rerun()

    elif st.session_state.page == "register":
        st.title("📝 Register")
        new_email = st.text_input("New Email")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if len(new_pass) == 8:
                st.session_state.users[new_email] = new_pass
                st.success("✅ Registered successfully! Redirecting to store...")
                st.session_state.logged_in = True
                st.session_state.page = "home"
                st.session_state.current_user = new_email
                st.experimental_rerun()
            else:
                st.warning("❌ Password must be 8 digits")
        if st.button("🔙 Back"):
            st.session_state.page = "front"
            st.experimental_rerun()

    st.stop()

# ---------------------- MAIN FUNCTIONS ----------------------
def set_page(p):
    st.session_state.page = p

def home():
    if st.session_state.wallpaper:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('data:image/jpeg;base64,{st.session_state.wallpaper}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"""
        <div style='text-align:center; font-size: 42px; color: white; font-weight: bold; padding: 20px; border-radius: 15px; background: linear-gradient(to right, #20c997, #198754); box-shadow: 2px 2px 10px rgba(0,0,0,0.3);'>
        🏪 {st.session_state.store_title}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("👤 Profile"):
            set_page("profile")
            st.experimental_rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Search Product"): set_page("search")
        if st.button("📂 View Customer Due"): set_page("view_due")
    with col2:
        if st.button("➕ Add to Due"): set_page("due")
        if st.button("🧶 Calculator"): set_page("calculator")
    with col3:
        if st.button("💠 Manage Products"): set_page("manage")

def profile_page():
    st.title("👤 Profile Settings")
    st.text_input("Change Store Title", key="store_title_input", value=st.session_state.store_title)
    if st.button("Update Title"):
        st.session_state.store_title = st.session_state.store_title_input
        st.success("✅ Title updated!")

    st.text_input("Update Password (8 digits)", key="new_pass", type="password")
    if st.button("Change Password"):
        new_pass = st.session_state.new_pass
        if len(new_pass) == 8:
            st.session_state.users[st.session_state.current_user] = new_pass
            st.success("✅ Password updated!")
        else:
            st.warning("❌ Password must be exactly 8 digits")

    wallpaper = st.file_uploader("Upload Wallpaper (image)", type=["jpg", "jpeg", "png"])
    if wallpaper:
        img = Image.open(wallpaper)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode()
        st.session_state.wallpaper = encoded_img
        st.success("✅ Wallpaper set for store page")

    if st.button("🔙 Back to Store"):
        set_page("home")
        st.experimental_rerun()

def search_page():
    st.title("🔍 Search Product")
    search = st.text_input("Enter product name:")
    for p in st.session_state.products:
        if search.lower() in p["name"].lower():
            st.success(f"{p['name']} | Stock: {p['stock']} | Rate: ₹{p['rate']}")
    if st.button("🔙 Back"): set_page("home")

def manage_page():
    st.title("💠 Manage Products")
    for p in st.session_state.products:
        st.write(f"{p['name']} | Stock: {p['stock']} | ₹{p['rate']}")
    name = st.text_input("New Product Name")
    stock = st.number_input("Stock", min_value=1, step=1)
    rate = st.number_input("Rate", min_value=1, step=1)
    if st.button("Add Product"):
        st.session_state.products.append({"name": name, "stock": stock, "rate": rate})
        st.success("✅ Product added")
    selected = st.selectbox("Sell Product", [p["name"] for p in st.session_state.products])
    qty = st.number_input("Quantity to Sell", min_value=1)
    if st.button("Sell"):
        for p in st.session_state.products:
            if p["name"] == selected and p["stock"] >= qty:
                p["stock"] -= qty
                st.success("✅ Sold")
            elif p["name"] == selected:
                st.error("❌ Not enough stock")
    if st.button("🔙 Back"): set_page("home")

def due_page():
    st.title("➕ Add to Due")
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone")
    product = st.selectbox("Product", [p["name"] for p in st.session_state.products])
    qty = st.number_input("Quantity", min_value=1)
    date_ = st.date_input("Date", value=date.today())
    if st.button("Add Due"):
        product_info = next(p for p in st.session_state.products if p["name"] == product)
        if name not in st.session_state.customers:
            st.session_state.customers[name] = {"phone": phone, "dues": []}
        st.session_state.customers[name]["dues"].append({
            "product": product, "qty": qty, "rate": product_info["rate"], "date": str(date_)
        })
        set_page(f"customer_{name}")
    if st.button("🔙 Back"): set_page("home")

def view_due():
    st.title("📂 View Customer Due")
    name = st.text_input("Search Customer")
    for n in st.session_state.customers:
        if name.lower() in n.lower():
            if st.button(f"View {n}"):
                set_page(f"customer_{n}")
    if st.button("📊 Summary"):
        total = 0
        for n, info in st.session_state.customers.items():
            dues = info.get("dues", [])
            due_total = sum(d['qty'] * d['rate'] for d in dues)
            st.write(f"{n} | ₹{due_total}")
            total += due_total
        st.info(f"💰 Total: ₹{total}")
    if st.button("🔙 Back"): set_page("home")

def customer_page(name):
    st.title(f"Due for {name}")
    info = st.session_state.customers.get(name, {})
    dues = info.get("dues", [])
    total = 0
    for i, d in enumerate(dues):
        subtotal = d['qty'] * d['rate']
        total += subtotal
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"{d['product']} | Qty: {d['qty']} | ₹{d['rate']} | {d['date']} = ₹{subtotal}")
        with col2:
            if st.button("➖", key=f"del_{i}"):
                dues.pop(i)
                st.experimental_rerun()
    st.success(f"Total Due: ₹{total}")
    if st.button("✅ Clear All"):
        del st.session_state.customers[name]
        set_page("view_due")
    if st.button("🔙 Back"): set_page("view_due")

def calculator_page():
    st.title("🧶 Calculator")
    expr = st.text_input("Expression:")
    try:
        if expr:
            result = eval(expr, {"__builtins__": None}, {})
            st.success(f"Result: {result}")
    except:
        st.error("Invalid expression")
    if st.button("🔙 Back"): set_page("home")

# ---------------------- ROUTER ----------------------
def router():
    p = st.session_state.page
    if p == "home": home()
    elif p == "search": search_page()
    elif p == "manage": manage_page()
    elif p == "due": due_page()
    elif p == "view_due": view_due()
    elif p == "calculator": calculator_page()
    elif p == "profile": profile_page()
    elif p.startswith("customer_"):
        customer_page(p.replace("customer_", ""))

router()
