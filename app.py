import streamlit as st, os, base64
import pandas as pd
from datetime import datetime

LOGO="logo.png"
def b64():
    if os.path.exists(LOGO):
        with open(LOGO,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg=b64()
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:64px;height:64px;border-radius:14px;background:white;padding:4px;object-fit:contain">' if bg else "🛡️"
st.set_page_config(page_title="BRAGI-IA V23 - Dashboard Categorías", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

is_login = "rol" not in st.session_state or st.session_state.rol is None

if is_login:
    st.markdown("""
    <style>
   .stApp{background:#D6EED8}
    div[data-testid="stColumn"]:first-child > div > div > div[data-testid="stVerticalBlock"]{
        background:white;border-radius:22px;padding:24px 20px;box-shadow:0 10px 28px rgba(0,0,0,0.08);border:1.5px solid #C8E6C9;min-height:520px
    }
    div[data-testid="stColumn"]:last-child > div > div > div[data-testid="stVerticalBlock"]{
        background:#1F4A3B;border-radius:22px;padding:24px 20px;min-height:520px;display:flex;flex-direction:column;justify-content:center;text-align:center
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
   .stApp{{background:#F5F7F5}}
    [data-testid="stSidebar"]{{background:#1A1E23}}
    [data-testid="stSidebar"] *{{color:#CBD5E1}}
    div[data-testid="stSidebar"] input{{background:white!important;color:#111!important;border-radius:12px!important}}
    div[data-testid="stExpander"]{{background:#252A33!important;border:none!important;margin:3px 0}}
   .kpi-red{{background:#E74C3C;color:white;border-radius:14px;padding:18px;min-height:110px;box-shadow:0 6px 14px rgba(0,0,0,0.12)}}
   .kpi-orange{{background:#F39C12;color:white;border-radius:14px;padding:18px;min-height:110px}}
   .kpi-green{{background:#5A9A3B;color:white;border-radius:14px;padding:18px;min-height:110px}}
   .kpi-orange2{{background:#E67E22;color:white;border-radius:14px;padding:18px;min-height:110px}}
   .kpi-blue{{background:#2980B9;color:white;border-radius:14px;padding:18px;min-height:110px}}
   .card{{background:white;border-radius:14px;padding:18px;box-shadow:0 4px 12px rgba(0,0,0,0.05);margin:8px 0}}
   .table-head{{background:#1E2A4A;color:white}}
    </style>
    <div style="background:white;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;margin:-60px -80px 10px -80px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
    <div style="display:flex;align-items:center;gap:10px">{logo_html}<b style="color:#1A3C2A">BRAGI-IA • TALENTO INTELIGENTE RR.HH</b></div>
    <div style="font-size:12px;color:#6B7280">ZICO ALBERTO POLANIA OVALLE • Bodega: SUCURSAL UNICA • 🔔 ⚙️</div></div>
    """, unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Dashboard"
if "categorias" not in st.session_state:
    st.session_state.categorias=[
        {"ID":1,"Descripción":"CARGOS - BRAGI-IA","Vida Util":"VU TALENTO"},
        {"ID":2,"Descripción":"PREGUNTAS POR CARGO","Vida Util":"VU EVALUACION"},
        {"ID":3,"Descripción":"PLAN DE TRABAJO","Vida Util":"VU 2 AÑOS"},
        {"ID":4,"Descripción":"PLANEACION DE PROCESOS","Vida Util":"VU 3 AÑOS"},
        {"ID":5,"Descripción":"INFORMES - BRAGI-IA","Vida Util":"VU 1 AÑO"},
        {"ID":6,"Descripción":"HISTORICOS RRHH","Vida Util":"VU 5 AÑOS"},
    ]
if "subcategorias" not in st.session_state: st.session_state.subcategorias=[]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único","Pago","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0}]},
    }

# LOGIN 2 PARTES - TODO DENTRO DEL CUADRO BLANCO - FONDO VERDE CLARO
if st.session_state.rol is None:
    col1, col2 = st.columns([1,1], gap="medium")
    with col1:
        st.markdown('<h3 style="color:#1F4A3B;margin:0">Iniciar Sesión</h3>', unsafe_allow_html=True)
        org=st.selectbox("Organización", ["RRHH","INVITADO A PRUEBA"], key="org_final")
        tipo=st.selectbox("Tipo de Acceso", ["SELECCIONAR CARGO","RRHH - ADMINISTRADOR","INVITADO A PRUEBA - CANDIDATO","AUXILIAR CONTABLE","ABOGADO"], key="tipo_final")

        if org=="RRHH":
            u=st.text_input("Usuario", placeholder="admin", key="u_final")
            p=st.text_input("Contraseña", type="password", placeholder="admin123", key="p_final")
            c1,c2=st.columns([1,4])
            with c1: st.markdown('<div style="background:#E74C3C;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white">←</div>', unsafe_allow_html=True)
            with c2:
                if st.button("LOG IN", type="primary", use_container_width=True, key="btn_rrhh_final"):
                    if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                    else: st.error("admin / admin123")
            st.caption("Credenciales: admin / admin123")
        else:
            st.success("Modo Invitado - Solo cédula (RRHH ya creó todo)")
            ced=st.text_input("Cédula", placeholder="Ingrese solo cédula", key="ced_final")
            c1,c2=st.columns([1,4])
            with c1: st.markdown('<div style="background:#E74C3C;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white">←</div>', unsafe_allow_html=True)
            with c2:
                if st.button("LOG IN", type="primary", use_container_width=True, key="btn_inv_final"):
                    if ced:
                        if not any(a["cedula"]==ced for a in st.session_state.asignaciones):
                            st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","asignado_por":"RRHH","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                        st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
        st.markdown('<div style="color:#7FB08A;font-size:11px;text-align:center;margin-top:10px">¿Olvidaste tu contraseña?</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="color:white;text-align:center">
        <div style="display:flex;justify-content:center">{logo_html}</div>
        <div style="font-size:11px;color:#A8D5B5;margin:6px 0">TALENTO INTELIGENTE • RR.HH • BRAGI-IA</div>
        <div style="font-size:38px;font-weight:900">BRAGI-IA</div>
        <div style="font-size:18px;color:#C8E6C9">Plataforma de<br>Talento Humano</div>
        <div style="font-size:12px;color:#8FC0A0;margin-top:12px">TALENTO INTELIGENTE RR.HH • BRAGI-IA<br>IA • Gestión • Selección • Desarrollo</div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# SIDEBAR COMO TUS FOTOS - BUSCAR EN EL M... + ACTIVOS FIJOS ETC AJUSTADO A BRAGI
with st.sidebar:
    st.markdown(f'<div style="padding:10px 0;display:flex;align-items:center;gap:8px"><div>{logo_html}</div><b style="color:white">BRAGI-IA</b></div>', unsafe_allow_html=True)
    s=st.text_input("Buscar", placeholder="Buscar en el m... 🔍", label_visibility="collapsed", key="search_side")
    sf=s.lower() if s else ""
    def show(t): return sf in t.lower() if sf else True

    if show("activos") or show("talento") or show("parametrizacion"):
        with st.expander("🏛️ Parametrizacion", expanded=True):
            if st.button("📦 Categorías", use_container_width=True, key="sb_cat"): st.session_state.view="ListaCategorias"; st.rerun()
            if st.button("📂 SubCategorías", use_container_width=True, key="sb_sub"): st.session_state.view="ListaSubCat"; st.rerun()
            if st.button("⚙️ Parámetros", use_container_width=True, key="sb_par"): st.session_state.view="Parametros"; st.rerun()
            if st.button("🔗 Parámetros x SubCategoría", use_container_width=True, key="sb_parx"): st.session_state.view="ParXSub"; st.rerun()

    if show("gestion") or show("evaluaciones"):
        with st.expander("👥 Gestión de Talento", expanded=False):
            if st.button("📊 Dashboard", use_container_width=True, key="sb_dash"): st.session_state.view="Dashboard"; st.rerun()
            if st.button("📌 Asignar Pruebas", use_container_width=True, key="sb_asig"): st.session_state.view="Asignar"; st.rerun()

    if show("plan"):
        with st.expander("📅 Plan de Trabajo"):
            if st.button("📅 Crear Plan", use_container_width=True, key="sb_plan"): st.session_state.view="PlanTrabajo"; st.rerun()
            if st.button("🔄 Planeación Procesos", use_container_width=True, key="sb_proc"): st.session_state.view="Planeacion"; st.rerun()

    if show("informes") or show("historicos") or show("datos"):
        with st.expander("📈 Datos / Informes"):
            if st.button("📈 Informes", use_container_width=True, key="sb_inf"): st.session_state.view="Informes"; st.rerun()
            if st.button("🕘 Históricos", use_container_width=True, key="sb_hist"): st.session_state.view="Historicos"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

# DASHBOARD COMO TU FOTO 1 - 5 TARJETAS COLORES AJUSTADO A BRAGI-IA
if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        # TARJETAS COMO TU FOTO 1 - ROJO, NARANJA, VERDE, NARANJA, AZUL
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(f'<div class="kpi-red"><div style="font-size:13px;font-weight:700">VENCIMIENTOS</div><div style="font-size:34px;margin-top:12px">🗓️❌ {len([r for r in st.session_state.resultados if r.get("score_num",0)<60])}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi-orange"><div style="font-size:13px;font-weight:700">PRUEBAS PENDIENTES</div><div style="font-size:34px;margin-top:12px">📄 $ {len(st.session_state.asignaciones)}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi-green"><div style="font-size:13px;font-weight:700">PENDIENTES DISPENSACIÓN</div><div style="font-size:13px">(RESULTADOS)</div><div style="font-size:34px;margin-top:8px">💊 {len(st.session_state.resultados)}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi-orange2"><div style="font-size:12px;font-weight:700">TRASLADOS SIN ACEPTAR (PLANES)</div><div style="font-size:34px;margin-top:12px">🛒 ↑ {len(st.session_state.categorias)}</div></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="kpi-blue"><div style="font-size:12px;font-weight:700">TRASLADOS POR ACEPTAR</div><div style="font-size:34px;margin-top:12px">🛒 ↓ {len(st.session_state.subcategorias)}</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        # LISTA CATEGORIAS COMO TU FOTO 3 DENTRO DEL DASHBOARD
        st.markdown('<div class="card"><h3 style="margin:0">LISTA CATEGORIAS - BRAGI-IA</h3></div>', unsafe_allow_html=True)
        col_search,col_btn=st.columns([3,1])
        with col_search: b=st.text_input("Buscar categorías", placeholder="🔍 Buscar categorías", label_visibility="collapsed", key="bus_cat_dash")
        with col_btn:
            if st.button("➕ Crear Categoría", type="primary", use_container_width=True): st.session_state.view="CrearCategoria"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Descripción"].str.contains(b.upper(), na=False)]
        st.write(f"Total Registros: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="ListaCategorias":
        st.markdown('<div class="card"><h2 style="margin:0">LISTA CATEGORIAS</h2></div>', unsafe_allow_html=True)
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("Buscar", placeholder="🔍 Buscar categorías", label_visibility="collapsed", key="bus_cat")
        with col2:
            if st.button("➕ Crear Categoría", type="primary", use_container_width=True): st.session_state.view="CrearCategoria"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Descripción"].str.contains(b.upper(), na=False)]
        st.write(f"Total Registros: {len(df)}")
        # TABLA COMO TU FOTO 3 - ID / Descripción / Vida Util
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="CrearCategoria":
        st.markdown('<div class="card"><h2>CREAR CATEGORIA</h2><p style="color:#6B7280">Como tu foto 3 - BRAGI-IA</p></div>', unsafe_allow_html=True)
        with st.form("crear_cat"):
            desc=st.text_input("* Descripción", placeholder="Ej: CARGOS, PLAN TRABAJO, INFORMES BRAGI-IA")
            vida=st.text_input("Vida Útil", placeholder="Ej: VU 2 AÑOS")
            if st.form_submit_button("➕ Crear Categoría", type="primary"):
                if desc:
                    new_id=max([c["ID"] for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Descripción":desc.upper(),"Vida Util":vida.upper() or "VU 1 AÑO"})
                    st.success("Categoría creada"); st.session_state.view="ListaCategorias"; st.rerun()

    elif v=="ListaSubCat":
        st.markdown('<div class="card"><h2>LISTA SUBCATEGORIAS</h2></div>', unsafe_allow_html=True)
        if st.session_state.subcategorias:
            st.dataframe(pd.DataFrame(st.session_state.subcategorias), use_container_width=True)
        else:
            st.info("Sin subcategorías - crea una")
        if st.button("➕ Crear SubCategoría", type="primary"): st.session_state.view="CrearSubCat"; st.rerun()

    elif v=="CrearSubCat":
        # COMO TU FOTO 2 - CREAR SUBCATEGORIA - DESCRIPCION + CATEGORIA
        st.markdown('<div class="card"><h2>CREAR SUBCATEGORIA</h2><p style="color:#6B7280">Exacto a tu foto 2 - ajustado BRAGI-IA</p></div>', unsafe_allow_html=True)
        with st.form("crear_sub"):
            st.markdown('<span style="color:red">*</span> Descripción', unsafe_allow_html=True)
            desc=st.text_input("Descripción", placeholder="", label_visibility="collapsed", key="desc_sub")
            st.markdown('<div style="height:12px"></div><span style="color:red">*</span> Categoría', unsafe_allow_html=True)
            cat=st.selectbox("Categoría", [c["Descripción"] for c in st.session_state.categorias], placeholder="Selecciona la categoría", label_visibility="collapsed", key="cat_sub")
            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
            if st.form_submit_button("➕ Crear Subcategoría", type="primary"):
                if desc and cat:
                    st.session_state.subcategorias.append({"Descripción":desc.upper(),"Categoría":cat,"Fecha":datetime.now().strftime("%Y-%m-%d")})
                    # Si es de CARGOS crear en cargos_db
                    if "CARGO" in cat:
                        nid=desc.lower().replace(" ","_")
                        st.session_state.cargos_db[nid]={"nombre":desc,"preguntas":[]}
                    st.success(f"SubCategoría {desc} creada en {cat}"); st.session_state.view="ListaSubCat"; st.rerun()

    elif v=="Asignar":
        st.markdown('<div class="card"><h3>📌 RRHH - Crear Invitado a Prueba - Solo cédula</h3><p>RRHH crea todo, invitado solo pone cédula y presenta</p></div>', unsafe_allow_html=True)
        with st.form("asig"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula Invitado* (solo esto pedirá)")
                nom=st.text_input("Nombre interno RRHH*")
            with c2:
                cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
            if st.form_submit_button("✅ Crear Invitado", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"asignado_por":"RRHH BRAGI-IA","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Invitado {ced} creado")

    elif v=="PlanTrabajo":
        st.markdown('<div class="card"><h3>📅 Plan de Trabajo - BRAGI-IA</h3></div>', unsafe_allow_html=True)
        with st.form("plan"):
            titulo=st.text_input("Título Plan*"); resp=st.text_input("Responsable*"); tareas=st.text_area("Tareas")
            if st.form_submit_button("💾 Guardar", type="primary"): st.success("Plan creado")

    elif v=="Informes":
        st.markdown('<div class="card"><h3>📈 Informes - BRAGI-IA</h3></div>', unsafe_allow_html=True)
        if st.session_state.resultados: st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
        else: st.info("Sin resultados")

    else:
        st.markdown(f'<div class="card"><h3>{v}</h3><p>Módulo {v} - BRAGI-IA ajustado a tu interfaz</p></div>', unsafe_allow_html=True)

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis: st.error("Sin pruebas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig["cargo_key"])
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>Invitado {ced} - {cargo["nombre"]}</h3><p>RRHH ya creó todo - solo presenta</p></div>', unsafe_allow_html=True)
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo["preguntas"]):
                    st.write(f"**{i+1}. {pr['q']}**"); r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}"); resps.append(r)
                if st.form_submit_button("🚀 FINALIZAR", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]); sc=int(ac/len(cargo["preguntas"])*100) if cargo["preguntas"] else 0
                    st.session_state.resultados.append({"cedula":ced,"cargo_nombre":cargo["nombre"],"score":f"{sc}%","score_num":sc,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% Enviado a RRHH")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
