import streamlit as st, os, base64, re
import pandas as pd
from datetime import datetime, date, time

LOGO="logo.png"
def b64():
    if os.path.exists(LOGO):
        with open(LOGO,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg=b64()
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:56px;height:56px;border-radius:12px;background:white;padding:3px;object-fit:contain">' if bg else "🛡️"
st.set_page_config(page_title="BRAGI-IA V27 FINAL", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

is_login = "rol" not in st.session_state or st.session_state.rol is None

if is_login:
    st.markdown("""
    <style>
.stApp{background:#D6EED8}
    div[data-testid="stColumn"]:first-child > div > div > div[data-testid="stVerticalBlock"]{background:white;border-radius:20px;padding:22px 18px;box-shadow:0 10px 24px rgba(0,0,0,0.08);border:1.5px solid #C8E6C9;min-height:500px;background-image:none!important}
    div[data-testid="stColumn"]:last-child > div > div > div[data-testid="stVerticalBlock"]{background:#176B5E;border-radius:20px;padding:22px 18px;min-height:500px;display:flex;flex-direction:column;justify-content:center;text-align:center;background-image:none!important}
    /* SIN RALLAS EN LOGIN */
    div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div {background:white!important;background-image:none!important;border:1.5px solid #C8E6C9!important;border-radius:12px!important}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
.stApp{{background:#E8F5E9;background-image:none!important}}
    /* AZUL VERDOSO - QUITAMOS NEGRO #0F1720 */
    [data-testid="stSidebar"]{{background:#176B5E!important;min-width:295px;background-image:none!important}}
    [data-testid="stSidebar"] *{{color:#E0F2F1!important}}
    div[data-testid="stSidebar"] input{{background:white!important;color:#111!important;border-radius:12px!important;border:1px solid #B2DFDB!important;background-image:none!important}}
    div[data-testid="stExpander"]{{background:#1F7A6B!important;border:none!important;margin:4px 0;border-radius:12px;background-image:none!important}}
    div[data-testid="stExpander"][open]{{background:#248A7A!important}}
    div[data-testid="stExpander"] p{{color:white!important;font-weight:600}}

    /* QUITAR RALLAS EN CASILLAS - FONDO BLANCO LIMPIO */
    div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, div[data-testid="stNumberInput"] > div, div[data-testid="stFileUploader"] > div {{
        background:white!important;
        background-image:none!important;
        border:1.5px solid #C8E6C9!important;
        border-radius:12px!important;
        box-shadow:none!important;
    }}
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {{
        background:white!important;
        background-image:none!important;
        border:none!important;
        box-shadow:none!important;
    }}
    textarea, input, select {{background:white!important;background-image:none!important}}
.card{{background:white;border-radius:14px;padding:16px;box-shadow:0 4px 12px rgba(0,0,0,0.06);margin:8px 0;border:1px solid #E8F5E9;background-image:none!important}}
.kpi{{background:white;border-radius:14px;padding:14px 16px;box-shadow:0 6px 14px rgba(0,0,0,0.08);min-height:110px;border-left:6px solid;background-image:none!important}}
.kpi-red{{border-color:#E74C3C}}.kpi-orange{{border-color:#F39C12}}.kpi-green{{border-color:#27AE60}}.kpi-orange2{{border-color:#E67E22}}.kpi-blue{{border-color:#2980B9}}
.badge-psi{{background:#E0F2F1;color:#00695C;padding:4px 10px;border-radius:20px;font-size:11px;border:1px solid #B2DFDB}}
.badge-hv{{background:#E8F5E9;color:#1F4A3B;padding:4px 10px;border-radius:20px;font-size:11px;border:1px solid #C8E6C9}}
 .stButton > button[kind="primary"]{{background:#176B5E!important;border-color:#176B5E!important}}
    </style>
    <div style="background:white;padding:8px 18px;display:flex;align-items:center;justify-content:space-between;margin:-60px -80px 8px -80px;box-shadow:0 2px 8px rgba(23,107,94,0.15)">
    <div style="display:flex;align-items:center;gap:8px">{logo_html}<b style="color:#176B5E;font-size:13px">BRAGI-IA • V27 FINAL • AZUL VERDOSO #176B5E • SIN RALLAS</b></div>
    <div style="font-size:11px;color:#4DB6AC">RRHH • VERDE AZULADO</div></div>
    """, unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "hojas_vida" not in st.session_state: st.session_state.hojas_vida=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Dashboard"
if "plan_trabajo" not in st.session_state: st.session_state.plan_trabajo=[]
if "planeacion" not in st.session_state: st.session_state.planeacion=[]
if "pruebas_psicologicas" not in st.session_state:
    st.session_state.pruebas_psicologicas=[
        {"ID":1,"Nombre":"16PF - Cattell","Tipo":"Personalidad","Descripción":"16 factores - Opcional apoyo","Duración":"30 min"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento","Descripción":"Dominancia, Influencia, Estabilidad, Conciencia","Duración":"15 min"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva","Descripción":"8 cuadros proyectivos","Duración":"25 min"},
        {"ID":4,"Nombre":"ICF Inteligencia Emocional","Tipo":"Emocional","Descripción":"Test IE - Opcional","Duración":"20 min"},
        {"ID":5,"Nombre":"Zavic - Valores","Tipo":"Valores","Descripción":"Honestidad, trabajo","Duración":"15 min"},
    ]
if "categorias" not in st.session_state:
    st.session_state.categorias=[
        {"ID":1,"Descripción":"AUXILIAR CONTABLE","Área":"Contabilidad","Vida Util":"VU 1 AÑO"},
        {"ID":2,"Descripción":"ABOGADO TUTELAS PQR","Área":"Jurídica","Vida Util":"VU 1 AÑO"},
        {"ID":3,"Descripción":"QUÍMICO FARMACÉUTICO","Área":"Farmacia","Vida Util":"VU 1 AÑO"},
        {"ID":4,"Descripción":"REGENTE DE FARMACIA","Área":"Farmacia","Vida Util":"VU 1 AÑO"},
    ]
if "subcategorias" not in st.session_state: st.session_state.subcategorias=[]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","area":"Contabilidad","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0,"tipo":"Técnica"}]},
        "abogado":{"nombre":"Abogado Tutelas PQR","area":"Jurídica","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0,"tipo":"Técnica"}]},
        "quimico":{"nombre":"Químico Farmacéutico","area":"Farmacia","preguntas":[{"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago"],"ok":0,"tipo":"Técnica"}]},
        "regente":{"nombre":"Regente de Farmacia","area":"Farmacia","preguntas":[{"q":"¿Qué es dispensación?","opts":["Entrega informada de medicamentos","Venta libre","Almacenamiento"],"ok":0,"tipo":"Técnica"}]},
    }

def analizar_hv_ia(texto, cargo):
    texto=texto.lower(); score=0; detalles=[]
    keywords=["experiencia","universidad","trabajo"]
    if "contable" in cargo.lower(): keywords=["contabilidad","puc","excel","siigo","nómina"]
    elif "abogado" in cargo.lower(): keywords=["derecho","tutela","pqr","jurídica"]
    elif "químico" in cargo.lower() or "farmacia" in cargo.lower() or "regente" in cargo.lower(): keywords=["farmacia","invima","medicamentos","dispensación","bpm"]
    for kw in keywords:
        if kw in texto: score+=20; detalles.append(f"✅ {kw.upper()}")
    if "años" in texto: score+=15; detalles.append("✅ Experiencia años")
    if "universidad" in texto or "profesional" in texto or "tecnólogo" in texto: score+=20; detalles.append("✅ Formación")
    if "trabajo en equipo" in texto or "liderazgo" in texto or "responsable" in texto: score+=15; detalles.append("✅ Competencias blandas")
    score=min(score,100)
    concepto="PERFIL ALTO - Recomendado" if score>=75 else "PERFIL MEDIO - Continuar" if score>=50 else "PERFIL BÁSICO - Validar"
    return score, concepto, detalles

# LOGIN 2 PARTES - TODO DENTRO DEL CUADRO BLANCO - FONDO VERDE CLARO - SOLO CEDULA INVITADO
if st.session_state.rol is None:
    c1,c2=st.columns([1,1], gap="medium")
    with c1:
        st.markdown('<h3 style="color:#176B5E;margin:0">Iniciar Sesión</h3>', unsafe_allow_html=True)
        org=st.selectbox("Organización", ["RRHH","INVITADO A PRUEBA"], key="orgv27")
        if org=="RRHH":
            u=st.text_input("Usuario", placeholder="admin", key="uv27")
            p=st.text_input("Contraseña", type="password", placeholder="admin123", key="pv27")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                else: st.error("Credenciales: admin / admin123")
            st.caption("admin / admin123")
        else:
            st.info("Modo Invitado - Solo cédula (RRHH ya creó todo)")
            ced=st.text_input("Cédula", placeholder="Solo cédula", key="cedv27")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if ced:
                    if not any(a.get("cedula")==ced for a in st.session_state.asignaciones):
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","area":"Contabilidad","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
                else: st.warning("Ingresa cédula")
        st.markdown('<div style="color:#7FB08A;font-size:11px;text-align:center;margin-top:10px">¿Olvidaste tu contraseña?</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="color:white;text-align:center">
        <div style="display:flex;justify-content:center">{logo_html}</div>
        <div style="font-size:30px;font-weight:900;margin-top:8px">BRAGI-IA</div>
        <div style="font-size:13px;color:#B2DFDB">Plataforma Talento Humano<br>
        <span style="background:white;color:#176B5E;padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700">1.CATEGORÍA</span>
        <span style="background:#E0F2F1;color:#00695C;padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700">2.PSICOLOGÍA</span>
        <span style="background:#E8F5E9;color:#1F4A3B;padding:3px 9px;border-radius:10px;font-size:10px;font-weight:700">3.HOJA DE VIDA</span><br>
        <span style="font-size:11px;margin-top:8px;display:inline-block">Azul Verdoso #176B5E • Sin rallas en casillas</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# SIDEBAR CON 3 MODULOS SEPARADOS - AZUL VERDOSO
with st.sidebar:
    st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0"><div>{logo_html}</div><b style="color:white">BRAGI-IA V27</b></div>', unsafe_allow_html=True)
    bus=st.text_input("Buscar", placeholder="Buscar en el m... 🔍", label_visibility="collapsed")
    sf=bus.lower() if bus else ""
    def show(t): return sf in t.lower() if sf else True

    with st.expander("📦 1. Categoría - Cargos", expanded=True):
        if st.button("📋 Lista Categorías", use_container_width=True, key="sb_cat27"): st.session_state.view="ListaCategorias"; st.rerun()
        if st.button("➕ Crear Categoría (Cargo)", use_container_width=True, key="sb_ccat27"): st.session_state.view="CrearCategoria"; st.rerun()
        if st.button("📂 SubCategorías", use_container_width=True, key="sb_sub27"): st.session_state.view="ListaSubCat"; st.rerun()
        if st.button("➕ Crear SubCategoría", use_container_width=True, key="sb_csub27"): st.session_state.view="CrearSubCat"; st.rerun()

    with st.expander("🧠 2. Área de Psicología", expanded=True):
        if st.button("🧩 Pruebas Psicológicas", use_container_width=True, key="sb_psi27"): st.session_state.view="Psicologia"; st.rerun()
        if st.button("➕ Crear Prueba Psicológica", use_container_width=True, key="sb_cpsi27"): st.session_state.view="CrearPsicologia"; st.rerun()

    with st.expander("📄 3. Hoja de Vida - IA Opcional", expanded=True):
        if st.button("📄 Cargue HV + Análisis IA", use_container_width=True, key="sb_hv27"): st.session_state.view="HojaVidaIA"; st.rerun()
        if st.button("📋 Hojas Analizadas", use_container_width=True, key="sb_hva27"): st.session_state.view="HojasAnalizadas"; st.rerun()

    with st.expander("👥 Gestión Talento", expanded=False):
        if st.button("📊 Dashboard", use_container_width=True, key="sb_dash27"): st.session_state.view="Dashboard"; st.rerun()
        if st.button("📌 Asignar Pruebas", use_container_width=True, key="sb_asig27"): st.session_state.view="Asignar"; st.rerun()

    with st.expander("📅 Plan / Planeación / Informes", expanded=False):
        if st.button("📅 Plan de Trabajo", use_container_width=True, key="sb_plan27"): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("🗓️ Planeación", use_container_width=True, key="sb_plane27"): st.session_state.view="Planeacion"; st.rerun()
        if st.button("📈 Informes", use_container_width=True, key="sb_inf27"): st.session_state.view="Informes"; st.rerun()
        if st.button("🕘 Históricos", use_container_width=True, key="sb_hist27"): st.session_state.view="Historicos"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(f'<div class="kpi kpi-red"><b style="color:#E74C3C">VENCIMIENTOS</b><br><span style="font-size:32px">❌ {len([r for r in st.session_state.resultados if r.get("score_num",0)<60])}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi kpi-orange"><b style="color:#F39C12">OC PENDIENTES</b><br><span style="font-size:32px">📄 {len(st.session_state.asignaciones)}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi kpi-green"><b style="color:#27AE60">HV IA</b><br><span style="font-size:32px">📄 {len(st.session_state.hojas_vida)}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi kpi-orange2"><b style="color:#E67E22">PSICOLOGÍA</b><br><span style="font-size:32px">🧠 {len(st.session_state.pruebas_psicologicas)}</span></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="kpi kpi-blue"><b style="color:#2980B9">RESULTADOS</b><br><span style="font-size:32px">📊 {len(st.session_state.resultados)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>LISTA CATEGORIAS - Módulo 1 - Azul Verdoso</h3></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)

    elif v=="ListaCategorias":
        st.markdown('<div class="card"><h2>📦 1. CATEGORÍA - Lista Categorías (Cargos)</h2><p>En el área quédate crear categoría - Módulo separado</p></div>', unsafe_allow_html=True)
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("Buscar", placeholder="🔍 Buscar categorías", label_visibility="collapsed", key="bcat27")
        with col2:
            if st.button("➕ Crear Categoría", type="primary", use_container_width=True): st.session_state.view="CrearCategoria"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Descripción"].str.contains(b.upper(), na=False)]
        st.write(f"Total Registros: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="CrearCategoria":
        st.markdown('<div class="card"><h2>📦 CREAR CATEGORÍA - Módulo 1 - Solo Cargos</h2><p>Sin rallas en casillas - Fondo blanco limpio</p></div>', unsafe_allow_html=True)
        with st.form("crear_cat27"):
            desc=st.text_input("* Descripción Cargo", placeholder="Ej: AUXILIAR CONTABLE")
            area=st.text_input("* Área", placeholder="Contabilidad, Jurídica, Farmacia")
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear Categoría", type="primary"):
                if desc:
                    new_id=max([c.get("ID",0) for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Descripción":desc.upper(),"Área":area.upper(),"Vida Util":vida})
                    nid=desc.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":desc,"area":area,"preguntas":[]}
                    st.success("Categoría creada"); st.session_state.view="ListaCategorias"; st.rerun()

    elif v=="ListaSubCat":
        st.markdown('<div class="card"><h2>SubCategorías - Preguntas por Cargo - Sin rallas</h2></div>', unsafe_allow_html=True)
        if st.session_state.subcategorias: st.dataframe(pd.DataFrame(st.session_state.subcategorias), use_container_width=True)
        else: st.info("Sin subcategorías")
        if st.button("➕ Crear SubCategoría", type="primary"): st.session_state.view="CrearSubCat"; st.rerun()

    elif v=="CrearSubCat":
        st.markdown('<div class="card"><h2>CREAR SUBCATEGORIA - Pregunta + Tipo - Sin rallas en casillas</h2><p>Preguntas que responderán los cargos - Incluir psicológicas - Casillas blancas limpias</p></div>', unsafe_allow_html=True)
        with st.form("crear_sub27"):
            desc=st.text_area("* Descripción / Pregunta", placeholder="Ej: [PSICOLÓGICO 16PF] ¿Cómo manejas estrés?")
            cats=[c.get("Descripción","") for c in st.session_state.categorias]
            cat=st.selectbox("* Categoría (Cargo)", cats if cats else ["CARGOS - BRAGI-IA"])
            tipo=st.selectbox("Tipo", ["Técnica","Psicológica - 16PF","Psicológica - DISC","Psicológica - Wartegg","Psicológica - IE","Hoja de Vida IA - Opcional"])
            if st.form_submit_button("➕ Crear Subcategoría", type="primary"):
                if desc:
                    cargo_key=list(st.session_state.cargos_db.keys())[0] if st.session_state.cargos_db else "aux_contable"
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cat.upper() or cat.upper() in v.get("nombre","").upper(): cargo_key=k; break
                    if cargo_key in st.session_state.cargos_db:
                        st.session_state.cargos_db[cargo_key]["preguntas"].append({"q":desc,"opts":["Opción A Correcta","Opción B","Opción C"],"ok":0,"tipo":tipo})
                    st.session_state.subcategorias.append({"Descripción":desc[:100],"Categoría":cat,"Tipo":tipo,"Fecha":datetime.now().strftime("%Y-%m-%d")})
                    st.success("Creada sin rallas"); st.session_state.view="ListaSubCat"; st.rerun()

    elif v=="Psicologia":
        st.markdown('<div class="card"><h2>🧠 2. ÁREA DE PSICOLOGÍA - Módulo Separado - Azul Verdoso</h2><p>En otro módulo colocar el área de psicología</p></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.pruebas_psicologicas), use_container_width=True, hide_index=True)
        if st.button("➕ Crear Prueba Psicológica", type="primary"): st.session_state.view="CrearPsicologia"; st.rerun()

    elif v=="CrearPsicologia":
        st.markdown('<div class="card"><h2>🧠 CREAR PRUEBA PSICOLÓGICA - Módulo 2 - Sin rallas</h2></div>', unsafe_allow_html=True)
        with st.form("crear_psi27"):
            nombre=st.text_input("* Nombre Prueba Psicológica", placeholder="Ej: 16PF, DISC, Wartegg, ICF")
            tipo=st.selectbox("* Tipo", ["Personalidad","Comportamiento","Proyectiva","Emocional","Valores","Inteligencia"])
            desc=st.text_area("* Descripción")
            dur=st.text_input("Duración", value="20 min")
            if st.form_submit_button("➕ Crear Prueba Psicológica", type="primary"):
                if nombre:
                    new_id=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":new_id,"Nombre":nombre.upper(),"Tipo":tipo,"Descripción":desc,"Duración":dur})
                    st.success("Prueba psicológica creada"); st.session_state.view="Psicologia"; st.rerun()

    elif v=="HojaVidaIA":
        st.markdown('<div class="card"><h2>📄 3. HOJA DE VIDA - En otro lado - Módulo Separado - Sin rallas</h2><p style="color:#27AE60"><b>Campo opcional no requisito - Mejor apoyo evaluación</b></p></div>', unsafe_allow_html=True)
        with st.form("hv_ia27"):
            ced=st.text_input("Cédula candidato (opcional)")
            cargo_sel=st.selectbox("Cargo a evaluar", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
            archivo=st.file_uploader("Cargar Hoja de Vida (PDF, DOCX, TXT) - OPCIONAL", type=["pdf","docx","txt"])
            texto_manual=st.text_area("O pegar texto hoja de vida aquí - OPCIONAL", placeholder="Texto HV opcional - sin rallas")
            if st.form_submit_button("🧠 Analizar HV con IA - Apoyo", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo cargado"
                if texto_manual: texto+= " " + texto_manual
                if not texto: texto="Sin HV - solo pruebas"
                score, concepto, detalles = analizar_hv_ia(texto, st.session_state.cargos_db[cargo_sel]["nombre"])
                st.session_state.hojas_vida.append({"cedula":ced or "SIN CEDULA - Opcional","cargo":st.session_state.cargos_db[cargo_sel]["nombre"],"score_ia":score,"concepto":concepto,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"modulo":"3. HOJA DE VIDA"})
                st.success(f"✅ HV Analizada: {score}% - {concepto}")
                for d in detalles: st.markdown(f"- {d}")

        if st.session_state.hojas_vida:
            st.markdown("### 📋 Hojas Analizadas - Módulo 3")
            st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="HojasAnalizadas":
        st.markdown('<div class="card"><h2>📄 Hojas de Vida Analizadas - Módulo 3 - Sin rallas</h2></div>', unsafe_allow_html=True)
        if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)
        else: st.info("Sin hojas de vida")

    elif v=="PlanTrabajo":
        st.markdown('<div class="card"><h2>Plan de Trabajo</h2></div>', unsafe_allow_html=True)
        with st.form("plan27"):
            titulo=st.text_input("Título")
            fecha=st.date_input("Fecha", value=date.today())
            cant=st.number_input("Entrevistas", min_value=1, max_value=100, value=5)
            if st.form_submit_button("💾 Guardar", type="primary"):
                st.session_state.plan_trabajo.append({"Titulo":titulo,"Fecha":str(fecha),"Cantidad":cant})
                st.success("Guardado")
        if st.session_state.plan_trabajo: st.dataframe(pd.DataFrame(st.session_state.plan_trabajo), use_container_width=True)

    elif v=="Planeacion":
        st.markdown('<div class="card"><h2>Planeación - Por día</h2></div>', unsafe_allow_html=True)
        with st.form("plane27"):
            fecha=st.date_input("Fecha", value=date.today())
            entrevistas=st.number_input("Entrevistas", min_value=1, max_value=50, value=5)
            if st.form_submit_button("💾 Guardar", type="primary"):
                st.session_state.planeacion.append({"Fecha":str(fecha),"Entrevistas":entrevistas})
                st.success("Guardado")
        if st.session_state.planeacion: st.dataframe(pd.DataFrame(st.session_state.planeacion), use_container_width=True)

    elif v=="Asignar":
        st.markdown('<div class="card"><h3>📌 Asignar - Con los 3 módulos - Sin rallas</h3></div>', unsafe_allow_html=True)
        with st.form("asig27"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula*")
                nom=st.text_input("Nombre*")
            with c2:
                cargo=st.selectbox("Cargo* (Módulo 1)", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                psi_sel=st.selectbox("Prueba Psicológica (Módulo 2)", [p.get("Nombre","") for p in st.session_state.pruebas_psicologicas])
                hv_check=st.checkbox("Incluir HV IA Opcional (Módulo 3)", value=False)
            if st.form_submit_button("✅ Crear", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"psicologica":psi_sel,"hv_opcional":"SI - Módulo 3" if hv_check else "NO","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Invitado {ced} creado con 3 módulos")

    elif v=="Informes":
        st.markdown('<div class="card"><h2>📈 Informes - 3 módulos - Sin rallas</h2></div>', unsafe_allow_html=True)
        if st.session_state.resultados: st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
        if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="Historicos":
        st.markdown('<div class="card"><h2>🕘 Históricos - Aprob/No Aprob - Sin rallas</h2></div>', unsafe_allow_html=True)
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            c1,c2=st.columns(2)
            with c1: st.markdown("**✅ Aprobados**"); st.dataframe(df[df["score_num"]>=70] if "score_num" in df.columns else df, use_container_width=True)
            with c2: st.markdown("**❌ No Aprobados**"); st.dataframe(df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame(), use_container_width=True)
        else: st.info("Sin históricos")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin pruebas - RRHH debe crearte")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>Invitado {ced} - {cargo["nombre"]}</h3><span class="badge-psi">🧠 {asig.get("psicologica","DISC")}</span> <span class="badge-hv">📄 HV: {asig.get("hv_opcional","NO")}</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="card"><h4>📄 Módulo 3 - Hoja de Vida - OPCIONAL - Sin rallas</h4></div>', unsafe_allow_html=True)
            hv_file=st.file_uploader("Cargar HV - OPCIONAL", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_txt=st.text_area("Texto HV opcional - sin rallas", key=f"hvtxt_{idx}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"**{i+1}. {pr['q']}**")
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                st.markdown("**🧠 Módulo 2 - Área Psicología**")
                psi_r=st.radio("Psicológica - ¿Cómo te describes?", ["Dominante - Decidido","Influyente - Sociable","Estable - Paciente","Concienzudo - Analítico"], index=None, key=f"psi_{idx}")
                if st.form_submit_button("🚀 FINALIZAR - 3 Módulos", type="primary", use_container_width=True):
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV"
                    if hv_txt: texto_hv+= " " + hv_txt
                    if texto_hv:
                        score_ia, concepto_ia, _ = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({"cedula":ced,"cargo":cargo["nombre"],"score_ia":score_ia,"concepto":concepto_ia,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"modulo":"3. HOJA DE VIDA"})
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],"score":f"{sc}%","score_num":sc,"psicologica":psi_r or asig.get("psicologica",""),"hv":"SI" if texto_hv else "NO - Opcional","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% - 3 módulos completados")

    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
