import streamlit as st, os, base64, io
import pandas as pd
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

LOGO="logo.png"
def b64():
    if os.path.exists(LOGO):
        with open(LOGO,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg=b64()
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:88px;height:88px;border-radius:18px;object-fit:contain;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.4))">' if bg else "🛡️"

st.set_page_config(page_title="BRAGI-IA V21 - RRHH", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

is_login = "rol" not in st.session_state or st.session_state.rol is None

if is_login:
    st.markdown(f"""
    <style>
   .stApp{{background:#0F1514;background-image: radial-gradient(circle at 20% 50%, rgba(45,90,74,0.15) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(45,90,74,0.2) 0%, transparent 50%);}}
   .login-card{{background:#3A424E;border-radius:24px;padding:28px 26px;max-width:420px;margin:20px auto;box-shadow:0 20px 60px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08)}}
   .login-title{{color:white;font-size:42px;font-weight:900;text-align:center;margin:12px 0 4px 0;letter-spacing:1px}}
   .login-sub{{color:#CBD5E1;font-size:13px;text-align:center;margin-bottom:18px}}
   .label-pill{{background:#5A5F6A;color:white;font-size:11px;padding:4px 10px;border-radius:6px;display:inline-block;margin-bottom:6px;margin-top:12px}}
   .footer-login{{color:#9CA3AF;font-size:12px;text-align:center;margin-top:18px}}
    div[data-testid="stSelectbox"] > div{{background:white!important;border-radius:12px!important;height:52px}}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
   .stApp{{background:#D6EED8}}
   .header{{background:white;padding:10px 22px;display:flex;align-items:center;justify-content:space-between;margin:-60px -80px 12px -80px;box-shadow:0 2px 10px rgba(0,0,0,0.06)}}
   .card{{background:white;padding:18px;border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,0.05);margin:8px 0;border:1px solid #E8F5E9}}
   .kpi-card{{border-radius:16px;padding:16px;color:white;min-height:110px;box-shadow:0 6px 16px rgba(0,0,0,0.12)}}
   .kpi-red{{background:#E74C3C}}.kpi-orange{{background:#F39C12}}.kpi-green{{background:#5A9A3B}}.kpi-blue{{background:#2E86DE}}.kpi-orange2{{background:#E67E22}}
    [data-testid="stSidebar"]{{background:white;border-right:1px solid #D1E7DD}}
    [data-testid="stSidebar"] *{{color:#1F2937}}
    div[data-testid="stSidebar"] input{{background:#F3F8F4!important;border-radius:12px!important;border:1px solid #D1E7DD!important}}
    div[data-testid="stExpander"]{{background:#F6FBF7!important;border:1px solid #E8F5E9!important;border-radius:12px!important;margin:5px 0}}
    </style>
    <div class="header"><div style="display:flex;align-items:center;gap:12px">{logo_html}<div><h1 style="margin:0;color:#1A3C2A;font-size:20px">BRAGI-IA</h1><small style="color:#6B7280">TALENTO INTELIGENTE • RR.HH • BRAGI-IA</small></div></div><div style="background:#D6EED8;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center">ZP</div></div>
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
if "subcategorias" not in st.session_state: st.session_state.subcategorias=[]
if "plan_trabajo" not in st.session_state: st.session_state.plan_trabajo=[]
if "procesos" not in st.session_state: st.session_state.procesos=[]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas PQR Contratación","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año","6 meses"],"ok":0}]},
        "quimico":{"nombre":"Químico Farmacéutico","preguntas":[{"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago"],"ok":0}]},
    }

def gen_pdf(d):
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=letter)
    if os.path.exists(LOGO):
        try: c.drawImage(LOGO,35,730,width=45,height=45,mask='auto')
        except: pass
    c.setFont("Helvetica-Bold",11); c.setFillColor(HexColor("#2D5A4A")); c.drawString(90,750,"BRAGI-IA - TALENTO INTELIGENTE • RR.HH - CONFIDENCIAL")
    c.setFont("Helvetica",10); c.setFillColor(HexColor("#000000")); y=700
    for k,v in d.items():
        if y<80: c.showPage(); y=700
        if k not in ["score_num"]: c.drawString(40,y,f"{k}: {str(v)[:110]}"); y-=14
    c.showPage(); c.save(); buf.seek(0); return buf

# LOGIN QUE TE GUSTO - RRHH / INVITADO A PRUEBA
if st.session_state.rol is None:
    st.markdown(f'<div class="login-card"><div style="display:flex;justify-content:center">{logo_html}</div><div class="login-title">LOGIN</div><div class="login-sub">Plataforma de Talento Humano • BRAGI-IA</div>', unsafe_allow_html=True)

    st.markdown('<div class="label-pill">Organización</div>', unsafe_allow_html=True)
    org=st.selectbox("org", ["RRHH","INVITADO A PRUEBA"], label_visibility="collapsed", key="org_login")

    st.markdown('<div class="label-pill">Tipo de Acceso</div>', unsafe_allow_html=True)
    cargo_sel=st.selectbox("cargo", ["SELECCIONAR CARGO","INVITADO A PRUEBA - CANDIDATO","RRHH - ADMINISTRADOR","AUXILIAR CONTABLE","ABOGADO TUTELAS","QUIMICO FARMACEUTICO"], label_visibility="collapsed", key="cargo_login")

    st.markdown('<div style="margin-top:18px"></div>', unsafe_allow_html=True)

    if "RRHH" in org or "RRHH" in cargo_sel or "ADMINISTRADOR" in cargo_sel:
        u=st.text_input("user", placeholder="Usuario: admin", label_visibility="collapsed", key="user_login")
        p=st.text_input("pass", type="password", placeholder="Clave: admin123", label_visibility="collapsed", key="pass_login")
        c1,c2=st.columns([1,4])
        with c1: st.markdown('<div style="background:#E74C3C;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:22px">←</div>', unsafe_allow_html=True)
        with c2:
            if st.button("LOG IN", type="primary", use_container_width=True, key="login_rrhh"):
                if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                else: st.error("Credenciales: admin / admin123")
    else:
        ced=st.text_input("ced", placeholder="Cédula Invitado a Prueba", label_visibility="collapsed", key="ced_login")
        nom=st.text_input("nom", placeholder="Nombre completo", label_visibility="collapsed", key="nom_login")
        c1,c2=st.columns([1,4])
        with c1: st.markdown('<div style="background:#E74C3C;width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:22px">←</div>', unsafe_allow_html=True)
        with c2:
            if st.button("LOG IN", type="primary", use_container_width=True, key="login_cand"):
                if ced:
                    st.session_state.ced_actual=ced
                    st.session_state.nombre_actual=nom or "Invitado"
                    # Auto-asignar si no tiene
                    if not any(a["cedula"]==ced for a in st.session_state.asignaciones):
                        # asignar segun cargo seleccionado
                        key_cargo="aux_contable"
                        if "ABOGADO" in cargo_sel: key_cargo="abogado"
                        if "QUIMICO" in cargo_sel: key_cargo="quimico"
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":nom or "Invitado","cargo_key":key_cargo,"cargo_nombre":st.session_state.cargos_db[key_cargo]["nombre"],"asignado_por":"RRHH BRAGI-IA","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.rol="candidato"
                    st.rerun()
                else: st.warning("Ingresa cédula")

    st.markdown('<div class="footer-login">© 2024 BRAGI-IA • Versión 2.1.0 • Soporte</div></div>', unsafe_allow_html=True)
    st.stop()

# SIDEBAR CLARO VERDE MODA
with st.sidebar:
    search=st.text_input("search", placeholder="Buscar en el módulo... 🔍", label_visibility="collapsed")
    s=search.lower() if search else ""
    def show(t): return s in t.lower() if s else True

    if show("categoria"):
        with st.expander("📦 Categorías", expanded=True):
            if st.button("📋 Lista Categorías", use_container_width=True): st.session_state.view="ListaCat"; st.rerun()
            if st.button("➕ Crear Categoría", use_container_width=True): st.session_state.view="CrearCat"; st.rerun()
            if st.button("📂 SubCategorías", use_container_width=True): st.session_state.view="ListaSubCat"; st.rerun()
            if st.button("➕ Crear SubCategoría", use_container_width=True): st.session_state.view="CrearSubCat"; st.rerun()

    if show("talento") or show("cargos"):
        with st.expander("👥 Gestión de Talento"):
            if st.button("📌 Asignar Pruebas", use_container_width=True): st.session_state.view="Asignar"; st.rerun()
            if st.button("💼 Ver Cargos", use_container_width=True): st.session_state.view="VerCargos"; st.rerun()

    if show("plan trabajo"):
        with st.expander("📅 Plan de Trabajo", expanded=True):
            if st.button("📅 Crear Plan", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
            if st.button("📋 Ver Planes", use_container_width=True): st.session_state.view="VerPlanes"; st.rerun()

    if show("planeacion") or show("procesos"):
        with st.expander("🔄 Planeación de Procesos", expanded=True):
            if st.button("🔄 Nuevo Proceso", use_container_width=True): st.session_state.view="AddProceso"; st.rerun()
            if st.button("🔍 Ver Procesos", use_container_width=True): st.session_state.view="VerProcesos"; st.rerun()

    if show("dashboard") or show("evaluaciones"):
        with st.expander("✅ Evaluaciones", expanded=True):
            if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()

    if show("informes"):
        with st.expander("📈 Informes"):
            if st.button("📈 Generar Informes", use_container_width=True): st.session_state.view="Informes"; st.rerun()

    if show("historicos"):
        with st.expander("🕘 Históricos"):
            if st.button("🕘 Ver Históricos", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

# CONTENIDO RRHH
if st.session_state.rol=="rrhh":
    v=st.session_state.view
    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(f'<div class="kpi-card kpi-red"><b>VENCIMIENTOS</b><br><span style="font-size:28px">🗓️ 0</span><br><small>Sin evaluar</small></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi-card kpi-orange"><b>INVITADOS PENDIENTES</b><br><span style="font-size:28px">📄 {len(st.session_state.asignaciones)}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi-card kpi-green"><b>PRUEBAS COMPLETADAS</b><br><span style="font-size:28px">💊 {len(st.session_state.resultados)}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi-card kpi-orange2"><b>PLANES</b><br><span style="font-size:28px">📋 {len(st.session_state.plan_trabajo)}</span></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="kpi-card kpi-blue"><b>CATEGORIAS</b><br><span style="font-size:28px">📦 {len(st.session_state.categorias)}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>LISTA CATEGORIAS - BRAGI-IA</h3></div>', unsafe_allow_html=True)
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("buscar", placeholder="🔍 Buscar categorías", label_visibility="collapsed")
        with col2:
            if st.button("➕ Crear Categoría", type="primary", use_container_width=True): st.session_state.view="CrearCat"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Descripcion"].str.contains(b.upper(), na=False)]
        st.write(f"Total Registros: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="ListaCat":
        st.markdown('<div class="card"><h3>LISTA CATEGORIAS</h3></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)
        if st.button("➕ Crear Categoría", type="primary"): st.session_state.view="CrearCat"; st.rerun()

    elif v=="CrearCat":
        st.markdown('<div class="card"><h3>CREAR CATEGORIA</h3></div>', unsafe_allow_html=True)
        with st.form("crear_cat"):
            desc=st.text_input("* Descripción Ej: CARGOS, PLAN TRABAJO")
            if st.form_submit_button("➕ Crear Categoría", type="primary"):
                if desc:
                    new_id=max([c["ID"] for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Descripcion":desc.upper(),"Vida Util":1})
                    st.success("Creada"); st.session_state.view="ListaCat"; st.rerun()

    elif v=="ListaSubCat":
        st.markdown('<div class="card"><h3>LISTA SUBCATEGORIAS</h3></div>', unsafe_allow_html=True)
        if st.session_state.subcategorias: st.dataframe(pd.DataFrame(st.session_state.subcategorias), use_container_width=True)
        else: st.info("Sin subcategorías")
        if st.button("➕ Crear SubCategoría", type="primary"): st.session_state.view="CrearSubCat"; st.rerun()

    elif v=="CrearSubCat":
        st.markdown('<div class="card"><h3>CREAR SUBCATEGORIA</h3></div>', unsafe_allow_html=True)
        with st.form("crear_subcat"):
            desc=st.text_input("* Descripción")
            cat=st.selectbox("* Categoría", [c["Descripcion"] for c in st.session_state.categorias])
            if st.form_submit_button("➕ Crear Subcategoría", type="primary", use_container_width=True):
                if desc and cat:
                    st.session_state.subcategorias.append({"Descripcion":desc.upper(),"Categoria":cat,"Fecha":datetime.now().strftime("%Y-%m-%d")})
                    st.success("Creada"); st.session_state.view="ListaSubCat"; st.rerun()

    elif v=="Asignar":
        st.markdown('<div class="card"><h3>📌 Asignar Pruebas - RRHH</h3></div>', unsafe_allow_html=True)
        with st.form("asig"):
            c1,c2=st.columns(2)
            with c1: ced=st.text_input("Cédula Invitado*"); nom=st.text_input("Nombre Invitado*")
            with c2: cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"]); asig=st.text_input("Asignado por*", value="RRHH BRAGI-IA")
            if st.form_submit_button("✅ Asignar como INVITADO A PRUEBA", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success(f"Invitado {nom} asignado")
        if st.session_state.asignaciones: st.dataframe(pd.DataFrame(st.session_state.asignaciones), use_container_width=True)

    elif v=="PlanTrabajo":
        st.markdown('<div class="card"><h3>📅 Plan de Trabajo</h3></div>', unsafe_allow_html=True)
        with st.form("plan"):
            titulo=st.text_input("Título*"); resp=st.text_input("Responsable*"); cargo_rel=st.selectbox("Cargo", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
            tareas=st.text_area("Tareas")
            if st.form_submit_button("💾 Guardar Plan", type="primary", use_container_width=True):
                st.session_state.plan_trabajo.append({"titulo":titulo,"responsable":resp,"cargo_nombre":st.session_state.cargos_db[cargo_rel]["nombre"],"tareas":tareas,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success("Plan creado")

    elif v=="Informes":
        st.markdown('<div class="card"><h3>📈 Informes - Históricos - BRAGI-IA</h3></div>', unsafe_allow_html=True)
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados); st.dataframe(df, use_container_width=True)
            for i,r in enumerate(df.to_dict(orient="records")):
                pdf=gen_pdf(r); st.download_button(f"🔒 PDF {r['cedula']} {r['score']}", pdf, f"RRHH_{r['cedula']}.pdf","application/pdf", key=f"pdf_{i}")
        else: st.info("Sin resultados")

    elif v=="Historicos":
        st.markdown('<div class="card"><h3>🕘 Históricos</h3></div>', unsafe_allow_html=True)
        t1,t2=st.tabs(["Categorías","Asignaciones / Resultados"])
        with t1: st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True)
        with t2:
            st.write("Asignaciones"); st.dataframe(pd.DataFrame(st.session_state.asignaciones), use_container_width=True)
            st.write("Resultados"); st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)

    else:
        st.markdown(f'<div class="card"><h3>{v}</h3></div>', unsafe_allow_html=True)

if st.session_state.rol=="candidato":
    with st.sidebar:
        st.markdown(f'<div style="text-align:center;padding:10px"><b>{st.session_state.ced_actual}</b><br><span style="font-size:11px">INVITADO A PRUEBA</span></div>', unsafe_allow_html=True)
    ced=st.session_state.ced_actual; mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis: st.error("Sin pruebas asignadas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig["cargo_key"])
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>👋 Hola {asig["nombre"]} - Invitado a Prueba {cargo["nombre"]}</h3></div>', unsafe_allow_html=True)
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo["preguntas"]):
                    st.write(f"**{i+1}. {pr['q']}**"); r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}"); resps.append(r)
                if st.form_submit_button("🚀 FINALIZAR PRUEBA", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]); tot=len(cargo["preguntas"]) or 1; sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig["nombre"],"cargo_nombre":cargo["nombre"],"asignado_por":asig["asignado_por"],"score":f"{sc}%","score_num":sc,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% - Prueba enviada a RRHH")
    if st.button("Cerrar sesión invitado"): st.session_state.rol=None; st.rerun()
