import streamlit as st, os, base64, io, re
import pandas as pd
from datetime import datetime, date, time

LOGO="logo.png"
def b64():
    if os.path.exists(LOGO):
        with open(LOGO,"rb") as f: return base64.b64encode(f.read()).decode()
    return None
bg=b64()
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:56px;height:56px;border-radius:12px;background:white;padding:3px;object-fit:contain">' if bg else "🛡️"
st.set_page_config(page_title="BRAGI-IA V25 Psicológico + HV IA", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

is_login = "rol" not in st.session_state or st.session_state.rol is None

if is_login:
    st.markdown("""
    <style>
  .stApp{background:#D6EED8}
    div[data-testid="stColumn"]:first-child > div > div > div[data-testid="stVerticalBlock"]{
        background:white;border-radius:20px;padding:22px 18px;box-shadow:0 10px 24px rgba(0,0,0,0.08);border:1.5px solid #C8E6C9;min-height:520px
    }
    div[data-testid="stColumn"]:last-child > div > div > div[data-testid="stVerticalBlock"]{
        background:#1F4A3B;border-radius:20px;padding:22px 18px;min-height:520px;display:flex;flex-direction:column;justify-content:center;text-align:center
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <style>
  .stApp{{
        background-color:#E8F5E9;
        background-image:
            radial-gradient(circle at 1px 1px, rgba(45,90,74,0.08) 1px, transparent 0),
            linear-gradient(90deg, rgba(198,120,80,0.12) 1px, transparent 1px);
        background-size: 28px 28px, 140px 140px;
    }}
    [data-testid="stSidebar"]{{background:#0F1720;min-width:290px}}
    [data-testid="stSidebar"] *{{color:#CBD5E1}}
    div[data-testid="stSidebar"] input{{background:white!important;color:#111!important;border-radius:10px!important}}
    div[data-testid="stExpander"]{{background:#1E293B!important;border:none!important;margin:2px 0;border-radius:10px}}
  .kpi{{background:white;border-radius:14px;padding:14px 16px;box-shadow:0 6px 14px rgba(0,0,0,0.08);min-height:110px;border-left:6px solid}}
  .kpi-red{{border-color:#E74C3C}}.kpi-orange{{border-color:#F39C12}}.kpi-green{{border-color:#27AE60}}.kpi-orange2{{border-color:#E67E22}}.kpi-blue{{border-color:#2980B9}}
  .card{{background:white;border-radius:14px;padding:16px;box-shadow:0 4px 12px rgba(0,0,0,0.06);margin:8px 0;border:1px solid #E8F5E9}}
  .badge-psi{{background:#E8F5E9;color:#1F4A3B;padding:4px 10px;border-radius:20px;font-size:11px;border:1px solid #C8E6C9}}
    </style>
    <div style="background:white;padding:8px 18px;display:flex;align-items:center;justify-content:space-between;margin:-60px -80px 8px -80px">
    <div style="display:flex;align-items:center;gap:8px">{logo_html}<b style="color:#1A3C2A;font-size:14px">BRAGI-IA • PSICOLÓGICO + HV IA OPCIONAL</b></div>
    <div style="font-size:11px;color:#6B7280">RRHH • CIRCUITO VERDE • IA ANÁLISIS</div></div>
    """, unsafe_allow_html=True)

# ESTADOS
if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "hojas_vida" not in st.session_state: st.session_state.hojas_vida=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Dashboard"
if "plan_trabajo" not in st.session_state: st.session_state.plan_trabajo=[]
if "planeacion" not in st.session_state: st.session_state.planeacion=[]
if "parametros" not in st.session_state:
    st.session_state.parametros=[
        {"ID":1,"Tipo":"Prueba Psicológica","Nombre":"16PF - Personalidad","Descripción":"16 factores de personalidad Cattell - Opcional apoyo evaluación"},
        {"ID":2,"Tipo":"Prueba Psicológica","Nombre":"DISC","Descripción":"Dominancia, Influencia, Estabilidad, Conciencia - Opcional"},
        {"ID":3,"Tipo":"Prueba Psicológica","Nombre":"Wartegg - Proyectiva","Descripción":"8 cuadros proyectivos - Análisis psicológico opcional"},
        {"ID":4,"Tipo":"Prueba Psicológica","Nombre":"ICF - Inteligencia Emocional","Descripción":"Test IE - Opcional para cargo"},
        {"ID":5,"Tipo":"Técnica","Nombre":"PUC - Conocimiento","Descripción":"Plan Único de Cuentas"},
        {"ID":6,"Tipo":"Hoja de Vida IA","Nombre":"Análisis HV con IA","Descripción":"Cargue hoja de vida - Análisis automático IA - Campo opcional, no requisito"},
    ]
if "categorias" not in st.session_state:
    st.session_state.categorias=[
        {"ID":1,"Descripción":"CARGOS - BRAGI-IA","Área":"RRHH","Vida Util":"VU TALENTO","Psicológico":"SI - Opcional"},
        {"ID":2,"Descripción":"PREGUNTAS PSICOLÓGICAS","Área":"Psicología","Vida Util":"VU 1 AÑO","Psicológico":"SI"},
        {"ID":3,"Descripción":"HOJA DE VIDA + IA","Área":"Evaluación","Vida Util":"VU 2 AÑOS","Psicológico":"Opcional"},
    ]
if "subcategorias" not in st.session_state: st.session_state.subcategorias=[]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","area":"Contabilidad","preguntas":[
            {"q":"¿Qué es PUC? (Técnica)","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0,"tipo":"Técnica"},
            {"q":"[PSICOLÓGICO - 16PF] ¿Cómo reaccionas bajo presión?","opts":["Mantengo calma y analizo","Me estreso rápido","Evito la situación"],"ok":0,"tipo":"Psicológica - Opcional"},
            {"q":"[PSICOLÓGICO - DISC] Prefieres trabajar:","opts":["Solo y con autonomía","En equipo liderando","Con instrucciones claras"],"ok":2,"tipo":"Psicológica - Opcional"},
        ]},
        "abogado":{"nombre":"Abogado Tutelas PQR","area":"Jurídica","preguntas":[
            {"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0,"tipo":"Técnica"},
            {"q":"[PSICOLÓGICO] ¿Cómo manejas conflictos?","opts":["Diálogo y mediación","Imposición","Evasión"],"ok":0,"tipo":"Psicológica - Opcional"},
        ]},
    }

def analizar_hv_ia(texto, cargo):
    """Análisis simple IA de hoja de vida - opcional apoyo"""
    texto=texto.lower()
    score=0
    detalles=[]
    # Keywords por cargo
    if "aux" in cargo.lower() or "contable" in cargo.lower():
        keywords=["contabilidad","puc","excel","siigo","contable","nómina"]
    elif "abogado" in cargo.lower():
        keywords=["derecho","tutela","pqr","jurídica","contratación"]
    else:
        keywords=["experiencia","universidad","curso","trabajo"]

    for kw in keywords:
        if kw in texto:
            score+=15
            detalles.append(f"✅ {kw.upper()} encontrado")

    # Experiencia años
    años=re.findall(r'(\d+)\s*años', texto)
    if años:
        score+=10
        detalles.append(f"✅ Experiencia: {años[0]} años")

    # Estudios
    if "universidad" in texto or "profesional" in texto or "tecnólogo" in texto:
        score+=20
        detalles.append("✅ Formación académica detectada")

    # Psicológico hints
    if "trabajo en equipo" in texto or "liderazgo" in texto or "responsable" in texto:
        score+=15
        detalles.append("✅ Competencias blandas (psicológico) detectadas")

    score=min(score,100)
    if score>=80: concepto="PERFIL ALTO - Recomendado para entrevista psicológica profunda"
    elif score>=60: concepto="PERFIL MEDIO - Apoyo evaluación, continuar proceso"
    else: concepto="PERFIL BÁSICO - Requiere validación adicional"

    return score, concepto, detalles

# LOGIN
if st.session_state.rol is None:
    c1,c2=st.columns([1,1], gap="medium")
    with c1:
        st.markdown('<h3 style="color:#1F4A3B;margin:0">Iniciar Sesión</h3>', unsafe_allow_html=True)
        org=st.selectbox("Organización", ["RRHH","INVITADO A PRUEBA"], key="orgv25")
        if org=="RRHH":
            u=st.text_input("Usuario", placeholder="admin", key="uv25")
            p=st.text_input("Contraseña", type="password", placeholder="admin123", key="pv25")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                else: st.error("admin / admin123")
        else:
            st.info("Modo Invitado - Solo cédula - HV opcional")
            ced=st.text_input("Cédula", placeholder="Solo cédula", key="cedv25")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if ced:
                    if not any(a.get("cedula")==ced for a in st.session_state.asignaciones):
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","area":"Contabilidad","asignado_por":"RRHH","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with c2:
        st.markdown(f"""
        <div style="color:white;text-align:center">
        <div style="display:flex;justify-content:center">{logo_html}</div>
        <div style="font-size:30px;font-weight:900">BRAGI-IA</div>
        <div style="font-size:14px;color:#C8E6C9">Psicológico + Hoja de Vida IA<br><span style="font-size:11px;background:#2D5A4A;padding:3px 10px;border-radius:12px">Campo HV Opcional - No requisito</span></div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# SIDEBAR FIJO
with st.sidebar:
    st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0"><div>{logo_html}</div><b style="color:white">BRAGI-IA PSI + IA</b></div>', unsafe_allow_html=True)
    bus=st.text_input("Buscar", placeholder="Buscar en el m... 🔍", label_visibility="collapsed")
    sf=bus.lower() if bus else ""
    def show(t): return sf in t.lower() if sf else True

    with st.expander("⚙️ Parametrizacion", expanded=True):
        if st.button("📦 Categorías (Cargos + Área + Psicológico)", use_container_width=True): st.session_state.view="ListaCategorias"; st.rerun()
        if st.button("📂 SubCategorías (Preguntas)", use_container_width=True): st.session_state.view="ListaSubCat"; st.rerun()
        if st.button("🔧 Parámetros (Psicológico + HV IA)", use_container_width=True): st.session_state.view="Parametros"; st.rerun()
        if st.button("🔗 Parámetros x SubCat", use_container_width=True): st.session_state.view="ParXSub"; st.rerun()

    with st.expander("📄 Hoja de Vida IA - Opcional", expanded=True):
        if st.button("📄 Cargue HV + Análisis IA", use_container_width=True): st.session_state.view="HojaVidaIA"; st.rerun()

    with st.expander("👥 Gestión Talento + Psicológico", expanded=True):
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()
        if st.button("📌 Asignar Pruebas (Técnica + Psicológica)", use_container_width=True): st.session_state.view="Asignar"; st.rerun()

    with st.expander("📅 Plan / Planeación", expanded=True):
        if st.button("📅 Plan de Trabajo", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("🗓️ Planeación (por día)", use_container_width=True): st.session_state.view="Planeacion"; st.rerun()

    with st.expander("📈 Informes / Históricos", expanded=True):
        if st.button("📈 Informes + HV IA", use_container_width=True): st.session_state.view="Informes"; st.rerun()
        if st.button("🕘 Históricos Aprob/No Aprob", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(f'<div class="kpi kpi-red"><b>VENCIMIENTOS</b><br><span style="font-size:32px">❌ {len([r for r in st.session_state.resultados if r.get("score_num",0)<60])}</span></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi kpi-orange"><b>PRUEBAS PENDIENTES</b><br><span style="font-size:32px">📄 {len(st.session_state.asignaciones)}</span></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi kpi-green"><b>HV IA ANALIZADAS</b><br><span style="font-size:32px">🧠 {len(st.session_state.hojas_vida)}</span></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi kpi-orange2"><b>PSICOLÓGICAS</b><br><span style="font-size:32px">🧩 {len([p for p in st.session_state.parametros if "Psicológica" in p.get("Tipo","")])}</span></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="kpi kpi-blue"><b>HISTÓRICOS</b><br><span style="font-size:32px">📊 {len(st.session_state.resultados)}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>LISTA CATEGORIAS - Con campo Psicológico opcional</h3></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)

    elif v=="ListaCategorias":
        st.markdown('<div class="card"><h2>LISTA CATEGORIAS</h2><p>Cargos con área + flag psicológico opcional</p></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)
        if st.button("➕ Crear Categoría", type="primary"): st.session_state.view="CrearCategoria"; st.rerun()

    elif v=="CrearCategoria":
        st.markdown('<div class="card"><h2>CREAR CATEGORIA - Cargo + Área + Psicológico</h2></div>', unsafe_allow_html=True)
        with st.form("crear_cat_v25"):
            desc=st.text_input("* Descripción Cargo", placeholder="Ej: AUXILIAR CONTABLE")
            area=st.text_input("* Área", placeholder="Contabilidad, Jurídica")
            psic=st.selectbox("¿Incluye evaluación psicológica? (Opcional)", ["SI - Opcional apoyo","SI - Obligatoria","NO - Solo técnica"])
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear Categoría", type="primary"):
                if desc:
                    new_id=max([c.get("ID",0) for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Descripción":desc.upper(),"Área":area.upper(),"Vida Util":vida,"Psicológico":psic})
                    nid=desc.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":desc,"area":area,"psicologico":psic,"preguntas":[]}
                    st.success(f"Cargo {desc} creado con psicológico: {psic}"); st.session_state.view="ListaCategorias"; st.rerun()

    elif v=="Parametros":
        st.markdown('<div class="card"><h2>Parámetros - TODO PSICOLÓGICO + HV IA OPCIONAL</h2><p>Como teníamos antes - cargue hoja de vida con análisis IA, campo opcional no requisito</p></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.parametros), use_container_width=True, hide_index=True)
        with st.form("param_v25"):
            tipo=st.selectbox("Tipo", ["Prueba Psicológica","Hoja de Vida IA - Opcional","Técnica","Psicotécnica","Otras clases"])
            nombre=st.text_input("Nombre Prueba", placeholder="Ej: 16PF, DISC, Análisis HV IA")
            desc=st.text_area("Descripción", placeholder="Descripción detallada - si es HV IA, explicar que es opcional apoyo")
            if st.form_submit_button("➕ Crear Parámetro Psicológico/HV IA", type="primary"):
                new_id=max([p.get("ID",0) for p in st.session_state.parametros], default=0)+1
                st.session_state.parametros.append({"ID":new_id,"Tipo":tipo,"Nombre":nombre,"Descripción":desc})
                st.success("Parámetro psicológico/HV IA creado"); st.rerun()

    elif v=="HojaVidaIA":
        st.markdown('<div class="card"><h2>📄 Cargue Hoja de Vida + Análisis con IA - CAMPO OPCIONAL</h2><p style="color:#27AE60"><b>NO es requisito - Es opcional para mejor apoyo al evaluar personal entrevistado</b></p><p>Como teníamos en el anterior sistema</p></div>', unsafe_allow_html=True)
        with st.form("hv_ia"):
            ced=st.text_input("Cédula candidato (opcional vincular)")
            cargo_sel=st.selectbox("Cargo a evaluar", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
            archivo=st.file_uploader("Cargar Hoja de Vida (PDF, DOCX, TXT) - OPCIONAL", type=["pdf","docx","txt"])
            texto_manual=st.text_area("O pegar texto hoja de vida aquí (opcional)", placeholder="Pega aquí texto de HV si no tienes archivo - Campo opcional")
            if st.form_submit_button("🧠 Analizar con IA - Apoyo Evaluación", type="primary"):
                texto=""
                if archivo:
                    try:
                        texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except:
                        texto="Archivo cargado"
                if texto_manual:
                    texto+= " " + texto_manual
                if not texto:
                    texto="Hoja de vida no proporcionada - evaluación solo con pruebas"

                score, concepto, detalles = analizar_hv_ia(texto, st.session_state.cargos_db[cargo_sel]["nombre"])

                st.session_state.hojas_vida.append({
                    "cedula":ced or "SIN CEDULA - Opcional",
                    "cargo":st.session_state.cargos_db[cargo_sel]["nombre"],
                    "score_ia":score,
                    "concepto":concepto,
                    "fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "opcional":"SI - No requisito"
                })

                st.success(f"✅ Análisis IA Completado - Score: {score}%")
                st.markdown(f"**Concepto IA:** {concepto}")
                for d in detalles:
                    st.markdown(f"- {d}")
                st.info("Este análisis es OPCIONAL, es apoyo para evaluar al personal entrevistado, no es requisito excluyente")

        if st.session_state.hojas_vida:
            st.markdown("### 📊 Hojas de Vida Analizadas con IA - Apoyo")
            st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="ListaSubCat":
        st.markdown('<div class="card"><h2>LISTA SUBCATEGORIAS - Preguntas Técnicas + Psicológicas</h2></div>', unsafe_allow_html=True)
        if st.session_state.subcategorias:
            st.dataframe(pd.DataFrame(st.session_state.subcategorias), use_container_width=True)
        else: st.info("Sin subcategorías")
        if st.button("➕ Crear SubCategoría", type="primary"): st.session_state.view="CrearSubCat"; st.rerun()

    elif v=="CrearSubCat":
        st.markdown('<div class="card"><h2>CREAR SUBCATEGORIA - Pregunta + Tipo Psicológico</h2><p>Preguntas que responderán los cargos - Incluir psicológicas</p></div>', unsafe_allow_html=True)
        with st.form("crear_sub_v25"):
            desc=st.text_area("* Descripción / Pregunta", placeholder="Ej: [PSICOLÓGICO 16PF] ¿Cómo manejas estrés?")
            cats=[c.get("Descripción","") for c in st.session_state.categorias]
            cat=st.selectbox("* Categoría (Cargo)", cats if cats else ["CARGOS - BRAGI-IA"])
            tipo=st.selectbox("Tipo", ["Técnica","Psicológica - 16PF","Psicológica - DISC","Psicológica - Wartegg","Psicológica - IE","Hoja de Vida IA - Opcional"])
            if st.form_submit_button("➕ Crear Subcategoría", type="primary"):
                if desc and cat:
                    cargo_key=list(st.session_state.cargos_db.keys())[0] if st.session_state.cargos_db else "aux_contable"
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cat.upper() or cat.upper() in v.get("nombre","").upper():
                            cargo_key=k; break
                    if cargo_key in st.session_state.cargos_db:
                        st.session_state.cargos_db[cargo_key]["preguntas"].append({"q":desc,"opts":["Opción A Correcta","Opción B","Opción C"],"ok":0,"tipo":tipo})
                    st.session_state.subcategorias.append({"Descripción":desc[:100],"Categoría":cat,"Tipo":tipo,"Fecha":datetime.now().strftime("%Y-%m-%d")})
                    st.success("Pregunta psicológica/técnica creada"); st.session_state.view="ListaSubCat"; st.rerun()

    elif v=="PlanTrabajo":
        st.markdown('<div class="card"><h2>Plan de Trabajo - Todas las entrevistas por realizar</h2></div>', unsafe_allow_html=True)
        with st.form("plan"):
            titulo=st.text_input("Título Plan*")
            fecha=st.date_input("Fecha", value=date.today())
            cant=st.number_input("Cuántas entrevistas", min_value=1, max_value=100, value=5)
            tareas=st.text_area("Detalle - Ej: Martes 5 octubre 12 entrevistas + psicológicas")
            if st.form_submit_button("💾 Guardar", type="primary"):
                st.session_state.plan_trabajo.append({"Titulo":titulo,"Fecha":str(fecha),"Cantidad":cant,"Detalle":tareas,"Psicológico":"Incluido","HV IA":"Opcional"})
                st.success("Plan creado")
        if st.session_state.plan_trabajo: st.dataframe(pd.DataFrame(st.session_state.plan_trabajo), use_container_width=True)

    elif v=="Planeacion":
        st.markdown('<div class="card"><h2>Planeación - Cuántas entrevistas por día</h2><p>Ej: Martes 5 octubre - 5 entrevistas</p></div>', unsafe_allow_html=True)
        with st.form("plane"):
            fecha=st.date_input("Fecha", value=date.today())
            hora=st.time_input("Hora", value=time(8,0))
            entrevistas=st.number_input("Entrevistas", min_value=1, max_value=50, value=5)
            if st.form_submit_button("💾 Guardar", type="primary"):
                st.session_state.planeacion.append({"Fecha":str(fecha),"Hora":str(hora),"Entrevistas":entrevistas})
                st.success("Guardado")
        if st.session_state.planeacion: st.dataframe(pd.DataFrame(st.session_state.planeacion), use_container_width=True)

    elif v=="Asignar":
        st.markdown('<div class="card"><h3>📌 Asignar Pruebas + Psicológico + HV IA Opcional</h3><p>RRHH crea - Invitado solo cédula - HV opcional no requisito</p></div>', unsafe_allow_html=True)
        with st.form("asig"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula*")
                nom=st.text_input("Nombre*")
            with c2:
                cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                psic=st.checkbox("Incluir pruebas psicológicas (opcional apoyo)", value=True)
                hv_opcional=st.checkbox("Solicitar hoja de vida IA - Opcional no requisito", value=False, help="Como teníamos antes - campo opcional para mejor apoyo evaluación")
            if st.form_submit_button("✅ Crear Invitado", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({
                    "cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],
                    "psicologico":"SI" if psic else "NO","hv_ia_opcional":"SI - Opcional" if hv_opcional else "NO",
                    "fecha":datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success(f"Invitado {ced} creado - Psicológico: {psic} - HV Opcional: {hv_opcional}")

    elif v=="Informes":
        st.markdown('<div class="card"><h2>📈 Informes - Resultados + Psicológico + HV IA</h2></div>', unsafe_allow_html=True)
        if st.session_state.resultados:
            st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
        if st.session_state.hojas_vida:
            st.markdown("### 🧠 Análisis HV IA - Apoyo")
            st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="Historicos":
        st.markdown('<div class="card"><h2>🕘 Históricos - Aprobados / No Aprobados + Psicológico + HV IA</h2></div>', unsafe_allow_html=True)
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            c1,c2=st.columns(2)
            with c1:
                st.markdown("**✅ Aprobados**")
                aprob=df[df["score_num"]>=70] if "score_num" in df.columns else df
                st.dataframe(aprob, use_container_width=True)
            with c2:
                st.markdown("**❌ No Aprobados**")
                no_aprob=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
                st.dataframe(no_aprob, use_container_width=True)
            st.markdown("**📊 Informe diario/mensual/por hora para gerencia**")
            st.bar_chart(df["cargo_nombre"].value_counts() if "cargo_nombre" in df.columns else pd.Series([1]))
        else:
            st.info("Sin históricos")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin pruebas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>Invitado {ced} - {cargo["nombre"]}</h3><span class="badge-psi">Psicológico: {asig.get("psicologico","SI")} | HV IA: {asig.get("hv_ia_opcional","Opcional")}</span></div>', unsafe_allow_html=True)

            # HOJA DE VIDA OPCIONAL - NO REQUISITO
            st.markdown('<div class="card"><h4>📄 Hoja de Vida + Análisis IA - CAMPO OPCIONAL (No requisito)</h4><p style="font-size:12px;color:#27AE60">Como teníamos antes - opcional para mejor apoyo evaluación - No es obligatorio</p></div>', unsafe_allow_html=True)
            hv_file=st.file_uploader("Cargar Hoja de Vida - OPCIONAL - No requisito", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_text=st.text_area("O pegar texto HV - OPCIONAL", key=f"hv_txt_{idx}", placeholder="Opcional - apoyo evaluación")

            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"**{i+1}. {pr['q']}** <span class='badge-psi'>{pr.get('tipo','Técnica')}</span>", unsafe_allow_html=True)
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                if st.form_submit_button("🚀 FINALIZAR PRUEBAS (Técnica + Psicológica)", type="primary", use_container_width=True):
                    # Análisis HV IA opcional
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV cargado"
                    if hv_text: texto_hv+= " " + hv_text

                    if texto_hv:
                        score_ia, concepto_ia, detalles_ia = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({
                            "cedula":ced,"cargo":cargo["nombre"],"score_ia":score_ia,"concepto":concepto_ia,
                            "fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"opcional":"SI - Apoyo evaluación"
                        })
                        st.info(f"🧠 Análisis IA HV: {score_ia}% - {concepto_ia} - Es apoyo opcional, no requisito")

                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    # Score psicológico separado
                    psic_questions=[pr for pr in cargo.get("preguntas",[]) if "Psicológica" in pr.get("tipo","")]
                    st.session_state.resultados.append({
                        "cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],
                        "score":f"{sc}%","score_num":sc,
                        "psicologico_incluido":"SI","hv_ia_opcional":"SI" if texto_hv else "NO - Opcional no proporcionada",
                        "fecha":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons(); st.success(f"✅ {sc}% - Pruebas técnicas + psicológicas enviadas a RRHH - HV IA opcional procesada como apoyo")

    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
