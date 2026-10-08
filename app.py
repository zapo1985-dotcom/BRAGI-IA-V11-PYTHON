import streamlit as st, os, base64, io
import pandas as pd
from datetime import datetime

LOGO="logo.png"
def b64():
    if os.path.exists(LOGO):
        with open(LOGO,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg=b64()
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:72px;height:72px;border-radius:16px;background:white;padding:4px;object-fit:contain">' if bg else "🛡️"

st.set_page_config(page_title="BRAGI-IA V22", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

is_login = "rol" not in st.session_state or st.session_state.rol is None

if is_login:
    st.markdown("""
    <style>
   .stApp{background:#E8F5E9;background-image: radial-gradient(circle at 10% 20%, #D6EED8 0%, transparent 40%), radial-gradient(circle at 90% 80%, #C8E6C9 0%, transparent 40%)}
   .login-left{background:white;border-radius:24px;padding:26px 24px;box-shadow:0 12px 30px rgba(45,90,74,0.1);border:1px solid #D1E7DD;min-height:520px}
   .login-right{background:#1F4A3B;border-radius:24px;padding:28px 24px;color:white;min-height:520px;display:flex;flex-direction:column;justify-content:center;text-align:center;box-shadow:0 12px 30px rgba(0,0,0,0.15)}
   .login-title{color:#1F4A3B;font-size:26px;font-weight:900;margin:0 0 14px 0}
   .label-mini{color:#5A7D6B;font-size:13px;font-weight:600;margin:12px 0 4px 0}
   .footer-small{color:#6B9A7D;font-size:12px;text-align:center;margin-top:18px}
    div[data-testid="stSelectbox"] > div{background:#F6FBF7!important;border-radius:10px!important;border:1px solid #D1E7DD!important}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
   .stApp{{background:#D6EED8}}
   .header{{background:white;padding:10px 22px;display:flex;align-items:center;justify-content:space-between;margin:-60px -80px 12px -80px;box-shadow:0 2px 10px rgba(0,0,0,0.06)}}
   .card{{background:white;padding:18px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,0.05);margin:8px 0}}
    [data-testid="stSidebar"]{{background:white}}
    div[data-testid="stSidebar"] input{{background:#F3F8F4!important;border-radius:12px!important;border:1px solid #D1E7DD!important}}
    div[data-testid="stExpander"]{{background:#F6FBF7!important;border:1px solid #E8F5E9!important;border-radius:12px!important}}
    </style>
    <div class="header"><div style="display:flex;align-items:center;gap:12px">{logo_html}<div><h1 style="margin:0;color:#1A3C2A;font-size:19px">BRAGI-IA</h1><small style="color:#6B7280">TALENTO INTELIGENTE RR.HH</small></div></div></div>
    """, unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Dashboard"
if "categorias" not in st.session_state:
    st.session_state.categorias=[
        {"ID":1,"Descripcion":"CARGOS - BRAGI-IA","Vida Util":0},
        {"ID":2,"Descripcion":"PREGUNTAS POR CARGO","Vida Util":0},
        {"ID":3,"Descripcion":"PLAN DE TRABAJO","Vida Util":2},
        {"ID":4,"Descripcion":"PLANEACION DE PROCESOS","Vida Util":3},
        {"ID":5,"Descripcion":"INFORMES","Vida Util":1},
        {"ID":6,"Descripcion":"HISTORICOS","Vida Util":1},
    ]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0}]},
    }

# LOGIN 2 PARTES - FONDO CLARO - PEQUEÑO
if st.session_state.rol is None:
    col1, col2 = st.columns([1,1], gap="large")

    with col1:
        st.markdown('<div class="login-left">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Iniciar Sesión</div>', unsafe_allow_html=True)

        st.markdown('<div class="label-mini">Organización</div>', unsafe_allow_html=True)
        org=st.selectbox("org", ["RRHH","INVITADO A PRUEBA"], label_visibility="collapsed", key="org_v22")

        st.markdown('<div class="label-mini">Tipo de Acceso</div>', unsafe_allow_html=True)
        if org=="RRHH":
            cargo_sel=st.selectbox("cargo", ["RRHH - ADMINISTRADOR","SELECCIONAR CARGO","AUXILIAR CONTABLE","ABOGADO","QUIMICO"], label_visibility="collapsed", key="cargo_rrhh")
        else:
            cargo_sel=st.selectbox("cargo", ["INVITADO A PRUEBA - CANDIDATO","SELECCIONAR CARGO","AUXILIAR CONTABLE","ABOGADO","QUIMICO"], label_visibility="collapsed", key="cargo_inv")

        if org=="RRHH":
            st.markdown('<div class="label-mini">Usuario</div>', unsafe_allow_html=True)
            u=st.text_input("user", placeholder="admin", label_visibility="collapsed", key="u_v22")
            st.markdown('<div class="label-mini">Contraseña</div>', unsafe_allow_html=True)
            p=st.text_input("pass", type="password", placeholder="admin123", label_visibility="collapsed", key="p_v22")

            c1,c2=st.columns([1,3])
            with c1: st.markdown('<div style="background:#E74C3C;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white">←</div>', unsafe_allow_html=True)
            with c2:
                if st.button("LOG IN", type="primary", use_container_width=True, key="btn_rrhh"):
                    if u=="admin" and p=="admin123":
                        st.session_state.rol="rrhh"
                        st.rerun()
                    else:
                        st.error("Credenciales: admin / admin123")
            st.caption("Credenciales: admin / admin123")
        else:
            st.markdown('<div style="background:#E8F5E9;border-radius:12px;padding:12px;margin:12px 0;border:1px solid #C8E6C9"><b>Modo Invitado</b><br><small>Para invitado, solo cédula - RRHH ya creó todo</small></div>', unsafe_allow_html=True)
            st.markdown('<div class="label-mini">Cédula</div>', unsafe_allow_html=True)
            ced=st.text_input("ced", placeholder="Ingrese cédula", label_visibility="collapsed", key="ced_v22")
            c1,c2=st.columns([1,3])
            with c1: st.markdown('<div style="background:#E74C3C;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white">←</div>', unsafe_allow_html=True)
            with c2:
                if st.button("LOG IN", type="primary", use_container_width=True, key="btn_inv"):
                    if ced:
                        # RRHH ya creó la asignación, solo validar que exista
                        existe = any(a["cedula"]==ced for a in st.session_state.asignaciones)
                        if not existe:
                            # Si no existe, crear una por defecto para demo (en real RRHH lo crea antes)
                            st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","asignado_por":"RRHH BRAGI-IA","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                        st.session_state.ced_actual=ced
                        st.session_state.rol="candidato"
                        st.rerun()
                    else:
                        st.warning("Ingresa cédula")

        st.markdown('<div class="footer-small">¿Olvidaste tu contraseña?</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="login-right">
            <div style="display:flex;justify-content:center;margin-bottom:18px">{logo_html}</div>
            <div style="font-size:12px;letter-spacing:1px;color:#A8D5B5;margin-bottom:8px">TALENTO INTELIGENTE • RR.HH • BRAGI-IA</div>
            <div style="font-size:48px;font-weight:900;letter-spacing:1px;margin:8px 0">BRAGI-IA</div>
            <div style="font-size:22px;font-weight:600;color:#C8E6C9;line-height:1.2">Plataforma de<br>Talento Humano</div>
            <div style="margin-top:18px;font-size:14px;color:#A8D5B5">TALENTO INTELIGENTE RR.HH</div>
            <div style="margin-top:40px;font-size:12px;color:#7FB08A">IA • Gestión • Selección • Desarrollo<br>© 2024 BRAGI-IA • Versión 2.1.0</div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# PLATAFORMA INTERNA - FONDO CLARO VERDE
with st.sidebar:
    search=st.text_input("search", placeholder="Buscar en el módulo... 🔍", label_visibility="collapsed")
    with st.expander("📦 Categorías", expanded=True):
        if st.button("📋 Lista Categorías", use_container_width=True): st.session_state.view="ListaCat"; st.rerun()
        if st.button("➕ Crear Categoría", use_container_width=True): st.session_state.view="CrearCat"; st.rerun()
    with st.expander("👥 Gestión de Talento"):
        if st.button("📌 Asignar Pruebas (RRHH crea invitado)", use_container_width=True): st.session_state.view="Asignar"; st.rerun()
    with st.expander("📅 Plan de Trabajo"):
        if st.button("📅 Ver Planes", use_container_width=True): st.session_state.view="VerPlanes"; st.rerun()
    with st.expander("📊 Dashboard"):
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view
    if v=="Dashboard":
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Invitados Creados", len(st.session_state.asignaciones))
        with c2: st.metric("Pruebas Completadas", len(st.session_state.resultados))
        with c3: st.metric("Categorías", len(st.session_state.categorias))
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)
    elif v=="Asignar":
        st.markdown('<div class="card"><h3>📌 RRHH - Crear Invitado a Prueba - Solo cédula para invitado</h3><p>RRHH crea todo, invitado solo pone cédula</p></div>', unsafe_allow_html=True)
        with st.form("asig_rrhh"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula Invitado* - Solo esto pedirá al invitado")
                nom=st.text_input("Nombre Invitado (interno RRHH)*")
            with c2:
                cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                asig=st.text_input("Asignado por*", value="RRHH BRAGI-IA")
            if st.form_submit_button("✅ Crear Invitado - Ya puede entrar solo con cédula", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Invitado {ced} creado - Ahora solo pone cédula {ced} y presenta pruebas")
        st.dataframe(pd.DataFrame(st.session_state.asignaciones), use_container_width=True)

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis:
        st.error(f"Cédula {ced} sin pruebas - RRHH debe crearte primero en Asignar Pruebas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig["cargo_key"])
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>👋 Invitado {ced} - {cargo["nombre"]}</h3><p>Presentar pruebas - RRHH ya creó todo</p></div>', unsafe_allow_html=True)
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo["preguntas"]):
                    st.write(f"**{i+1}. {pr['q']}**")
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                if st.form_submit_button("🚀 FINALIZAR PRUEBA", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0])
                    tot=len(cargo["preguntas"]) or 1
                    sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig["nombre"],"cargo_nombre":cargo["nombre"],"score":f"{sc}%","score_num":sc,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons()
                    st.success(f"✅ {sc}% - Enviado a RRHH")
    if st.button("Cerrar sesión invitado"): st.session_state.rol=None; st.rerun()
