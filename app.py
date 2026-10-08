import streamlit as st
st.set_page_config(page_title="BRAGI-IA V11", layout="wide")

st.markdown("""
<style>
.stApp{background:#F2F3F4}
.header-verde{background:#2D5A4A;padding:22px 30px;display:flex;align-items:center;gap:15px;margin:-60px -80px 20px -80px}
.header-verde h1{color:white;font-size:32px;font-weight:900;margin:0;letter-spacing:0.5px}
.card-login{background:white;padding:32px 28px;border-radius:24px;box-shadow:0 12px 30px rgba(0,0,0,0.08);border:1px solid #EFEFEF}
.icon-circ{background:#2D5A4A;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:26px;float:left;margin-right:12px}
.input-login input{border-radius:12px !important;padding:14px !important;border:1px solid #E5E7EB !important}
.btn-verde button{background:#2D8A5E !important;color:white !important;border-radius:12px !important;padding:12px !important;font-weight:800 !important;border:none !important;width:100%}
.watermark{position:fixed;top:28%;left:-12%;transform:rotate(-24deg);font-size:22px;color:rgba(45,90,74,0.08);font-weight:800;pointer-events:none;z-index:0;width:250%;line-height:70px}
.footer{position:fixed;bottom:10px;left:0;width:100%;text-align:center;font-size:12px;color:#6B7280}
</style>
<div class="watermark">TALENTO INTELIGENTE - BRAGI-IA - TALENTO INTELIGENTE - BRAGI-IA - TALENTO INTELIGENTE - BRAGI-IA - TALENTO INTELIGENTE - BRAGI-IA</div>
<div class="header-verde"><div style="background:#3A7A5E;width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center">🧠</div><h1>BRAGI-IA V11 - TALENTO INTELIGENTE</h1></div>
""", unsafe_allow_html=True)

# ... aquí sigue tu código de cargos_db que ya te pasé arriba ...

if "rol" not in st.session_state: st.session_state.rol=None

if st.session_state.rol is None:
    c1,c2=st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card-login"><div class="icon-circ">👤</div><h2 style="margin:6px 0 20px 0;color:#2B2F32">Candidato</h2><label style="font-weight:600">Cédula</label>', unsafe_allow_html=True)
        ced = st.text_input("Cédula", placeholder="Ingrese su cédula", label_visibility="collapsed", key="ced_login_img")
        st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
        if st.button("Iniciar Sesión", key="btn_cand_img", use_container_width=True):
            if ced:
                st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card-login"><div class="icon-circ">💼</div><h2 style="margin:6px 0 20px 0;color:#2B2F32">RRHH Admin</h2><label style="font-weight:600">Usuario</label>', unsafe_allow_html=True)
        u = st.text_input("Usuario", placeholder="Ingrese su usuario", label_visibility="collapsed", key="user_login_img")
        st.markdown('<label style="font-weight:600;margin-top:12px;display:block">Contraseña</label>', unsafe_allow_html=True)
        p = st.text_input("Contraseña", type="password", placeholder="••••••••", label_visibility="collapsed", key="pass_login_img")
        st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
        if st.button("Acceder", key="btn_rrhh_img", use_container_width=True):
            if u=="admin" and p=="admin123":
                st.session_state.rol="rrhh"; st.rerun()
            else: st.error("Usuario o clave incorrecta")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">v1.1 • © 2024 BRAGI-IA • Soporte: soporte@bragi-ia.com</div>', unsafe_allow_html=True)
    st.stop()
