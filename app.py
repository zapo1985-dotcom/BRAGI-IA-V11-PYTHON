import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="BRAGI-IA V30 MENU FIJO", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# CSS - MENU FIJO QUE NO SE ESCONDE + LETRAS NEGRAS + SIN RALLAS + AZUL VERDOSO #176B5E
st.markdown("""
<style>
.stApp{background:#E8F5E9!important}

/* MENU FIJO QUE NO SE ESCONDE - FIX TU ULTIMA FOTO */
button[data-testid="stSidebarCollapsedControl"], button[data-testid="collapsedControl"], div[data-testid="stSidebarCollapsedControl"]{display:none!important;visibility:hidden!important}
[data-testid="stSidebar"]{
    background:#176B5E!important;
    min-width:310px!important;
    max-width:310px!important;
    position:fixed!important;
    left:0!important;
    top:0!important;
    height:100vh!important;
    z-index:999999!important;
    transform:none!important;
    visibility:visible!important;
    overflow-y:auto!important;
}
section[data-testid="stSidebar"]{transform:none!important;visibility:visible!important}
[data-testid="stSidebar"] > div{padding-top:10px!important}

/* BOTONES SIDEBAR FONDO BLANCO LETRA NEGRA - FIX NO SE VEIA */
section[data-testid="stSidebar"] button{
    background:white!important;
    color:black!important;
    border-radius:10px!important;
    font-weight:800!important;
    border:1.5px solid #B2DFDB!important;
    height:44px!important;
    margin:3px 0!important;
}
section[data-testid="stSidebar"] button p,
section[data-testid="stSidebar"] button span,
section[data-testid="stSidebar"] button div{
    color:black!important;
    font-weight:800!important;
    font-size:13px!important;
}
section[data-testid="stSidebar"] button:hover{background:#E0F2F1!important}

[data-testid="stSidebar"] input{background:white!important;color:black!important;border-radius:12px!important}
div[data-testid="stExpander"]{background:#1F7A6B!important;border-radius:12px!important;margin:6px 0!important}
div[data-testid="stExpander"][open]{background:#248A7A!important}
div[data-testid="stExpander"] summary p{color:white!important;font-weight:700!important}

/* CASILLAS BLANCAS SIN RALLAS LETRA NEGRA */
div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, div[data-testid="stNumberInput"] > div, div[data-testid="stFileUploader"] > div{
    background:white!important;border:1.5px solid #C8E6C9!important;border-radius:12px!important;background-image:none!important;
}
input, textarea{color:black!important;font-weight:600!important;background:white!important}

/* TODO TEXTO NEGRO EN AREA BLANCA - QUITAR <div sty */
h1,h2,h3,p,label{color:black!important}
div[data-testid="stDataFrame"] *{color:black!important}

/* CONTENIDO PRINCIPAL CON MARGEN PARA NO TAPAR MENU FIJO */
section.main > div{margin-left:310px!important;padding-left:20px!important}
</style>
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
        {"ID":1,"Nombre":"16PF","Tipo":"Personalidad","Descripción":"16 factores","Duración":"30 min"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento","Descripción":"DISC","Duración":"15 min"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva","Descripción":"8 cuadros","Duración":"25 min"},
        {"ID":4,"Nombre":"ICF IE","Tipo":"Emocional","Descripción":"Inteligencia Emocional","Duración":"20 min"},
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
        "aux_contable":{"nombre":"Auxiliar Contable","area":"Contabilidad","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas PQR","area":"Jurídica","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0}]},
        "quimico":{"nombre":"Químico Farmacéutico","area":"Farmacia","preguntas":[{"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago"],"ok":0}]},
        "regente":{"nombre":"Regente de Farmacia","area":"Farmacia","preguntas":[{"q":"¿Qué es dispensación?","opts":["Entrega informada","Venta libre","Almacenamiento"],"ok":0}]},
    }

def analizar_hv_ia(texto, cargo):
    texto=texto.lower(); score=0
    for kw in ["contabilidad","puc","derecho","tutela","farmacia","invima","medicamentos","experiencia","universidad"]:
        if kw in texto: score+=15
    score=min(score,100)
    concepto="PERFIL ALTO" if score>=70 else "PERFIL MEDIO" if score>=40 else "PERFIL BÁSICO"
    return score, concepto

if st.session_state.rol is None:
    st.markdown("<h2 style='color:black;text-align:center'>BRAGI-IA V30 - MENU FIJO - LETRAS NEGRAS</h2>", unsafe_allow_html=True)
    col1,col2=st.columns(2)
    with col1:
        st.subheader("Iniciar Sesión")
        org=st.selectbox("Organización", ["RRHH","INVITADO A PRUEBA"])
        if org=="RRHH":
            u=st.text_input("Usuario", placeholder="admin")
            p=st.text_input("Contraseña", type="password", placeholder="admin123")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                else: st.error("admin / admin123")
        else:
            ced=st.text_input("Cédula - Solo cédula")
            if st.button("LOG IN Invitado", type="primary", use_container_width=True):
                if ced:
                    if not any(a.get("cedula")==ced for a in st.session_state.asignaciones):
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","area":"Contabilidad","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with col2:
        st.info("V30 - Menú fijo que no se esconde - Azul Verdoso #176B5E - Letras Negras - Sin <div style")
    st.stop()

with st.sidebar:
    st.markdown("<h3 style='color:white!important;margin:0'>BRAGI-IA V30</h3><p style='color:#B2DFDB!important;font-size:11px'>MENU FIJO - NO SE ESCONDE</p>", unsafe_allow_html=True)
    bus=st.text_input("Buscar", placeholder="Buscar en el m... 🔍", label_visibility="collapsed")

    with st.expander("📦 1. Categoría - Cargos", expanded=True):
        if st.button("📋 Lista Categorías", use_container_width=True): st.session_state.view="ListaCategorias"; st.rerun()
        if st.button("➕ Crear Categoría", use_container_width=True): st.session_state.view="CrearCategoria"; st.rerun()
        if st.button("📂 SubCategorías", use_container_width=True): st.session_state.view="ListaSubCat"; st.rerun()
        if st.button("➕ Crear SubCategoría", use_container_width=True): st.session_state.view="CrearSubCat"; st.rerun()

    with st.expander("🧠 2. Área de Psicología", expanded=True):
        if st.button("🧩 Pruebas Psicológicas", use_container_width=True): st.session_state.view="Psicologia"; st.rerun()
        if st.button("➕ Crear Prueba Psicológica", use_container_width=True): st.session_state.view="CrearPsicologia"; st.rerun()

    with st.expander("📄 3. Hoja de Vida - IA Opcional", expanded=True):
        if st.button("📄 Cargue HV + Análisis IA", use_container_width=True): st.session_state.view="HojaVidaIA"; st.rerun()
        if st.button("📋 Hojas Analizadas", use_container_width=True): st.session_state.view="HojasAnalizadas"; st.rerun()

    with st.expander("👥 Gestión / Plan / Informes", expanded=False):
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()
        if st.button("📌 Asignar Pruebas", use_container_width=True): st.session_state.view="Asignar"; st.rerun()
        if st.button("📅 Plan de Trabajo", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("🗓️ Planeación", use_container_width=True): st.session_state.view="Planeacion"; st.rerun()
        if st.button("📈 Informes", use_container_width=True): st.session_state.view="Informes"; st.rerun()
        if st.button("🕘 Históricos", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view
    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("VENCIMIENTOS", "0")
        c2.metric("PENDIENTES", f"{len(st.session_state.asignaciones)}")
        c3.metric("HV IA", f"{len(st.session_state.hojas_vida)}")
        c4.metric("PSICOLOGÍA", f"{len(st.session_state.pruebas_psicologicas)}")
        c5.metric("RESULTADOS", f"{len(st.session_state.resultados)}")
        st.subheader("LISTA CATEGORIAS - Módulo 1 - Menú Fijo")
        st.dataframe(pd.DataFrame(st.session_state.categorias), use_container_width=True, hide_index=True)

    elif v=="ListaCategorias":
        st.subheader("📦 1. CATEGORÍA - Lista Categorías")
        st.write("En el área quédate crear categoría - Módulo separado - Menú fijo no se esconde")
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("Buscar", placeholder="🔍 Buscar categorías", label_visibility="collapsed", key="bcat")
        with col2:
            if st.button("➕ Crear Categoría", type="primary", use_container_width=True): st.session_state.view="CrearCategoria"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Descripción"].str.contains(b.upper(), na=False)]
        st.write(f"Total Registros: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="CrearCategoria":
        st.subheader("📦 CREAR CATEGORÍA")
        with st.form("crear_cat"):
            desc=st.text_input("Descripción Cargo *", placeholder="Ej: AUXILIAR CONTABLE")
            area=st.text_input("Área *", placeholder="Contabilidad, Jurídica")
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear Categoría", type="primary"):
                if desc:
                    new_id=max([c.get("ID",0) for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Descripción":desc.upper(),"Área":area.upper(),"Vida Util":vida})
                    nid=desc.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":desc,"area":area,"preguntas":[]}
                    st.success("Categoría creada"); st.session_state.view="ListaCategorias"; st.rerun()

    elif v=="ListaSubCat":
        st.subheader("SubCategorías")
        if st.session_state.subcategorias: st.dataframe(pd.DataFrame(st.session_state.subcategorias), use_container_width=True)
        else: st.info("Sin subcategorías")
        if st.button("➕ Crear SubCategoría", type="primary"): st.session_state.view="CrearSubCat"; st.rerun()

    elif v=="CrearSubCat":
        st.subheader("CREAR SUBCATEGORIA - Sin rallas")
        with st.form("crear_sub"):
            desc=st.text_area("Descripción / Pregunta *")
            cats=[c.get("Descripción","") for c in st.session_state.categorias]
            cat=st.selectbox("Categoría (Cargo) *", cats if cats else ["CARGOS"])
            tipo=st.selectbox("Tipo", ["Técnica","Psicológica - 16PF","Psicológica - DISC","Hoja de Vida IA - Opcional"])
            if st.form_submit_button("➕ Crear Subcategoría", type="primary"):
                if desc:
                    cargo_key=list(st.session_state.cargos_db.keys())[0]
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cat.upper() or cat.upper() in v.get("nombre","").upper(): cargo_key=k; break
                    if cargo_key in st.session_state.cargos_db:
                        st.session_state.cargos_db[cargo_key]["preguntas"].append({"q":desc,"opts":["Opción A Correcta","Opción B","Opción C"],"ok":0,"tipo":tipo})
                    st.session_state.subcategorias.append({"Descripción":desc[:100],"Categoría":cat,"Tipo":tipo,"Fecha":datetime.now().strftime("%Y-%m-%d")})
                    st.success("Creada"); st.session_state.view="ListaSubCat"; st.rerun()

    elif v=="Psicologia":
        st.subheader("🧠 2. ÁREA DE PSICOLOGÍA")
        st.dataframe(pd.DataFrame(st.session_state.pruebas_psicologicas), use_container_width=True, hide_index=True)
        if st.button("➕ Crear Prueba Psicológica", type="primary"): st.session_state.view="CrearPsicologia"; st.rerun()

    elif v=="CrearPsicologia":
        st.subheader("🧠 CREAR PRUEBA PSICOLÓGICA")
        with st.form("crear_psi"):
            nombre=st.text_input("Nombre Prueba *")
            tipo=st.selectbox("Tipo *", ["Personalidad","Comportamiento","Proyectiva","Emocional"])
            desc=st.text_area("Descripción")
            dur=st.text_input("Duración", value="20 min")
            if st.form_submit_button("➕ Crear Prueba", type="primary"):
                if nombre:
                    new_id=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":new_id,"Nombre":nombre.upper(),"Tipo":tipo,"Descripción":desc,"Duración":dur})
                    st.success("Creada"); st.session_state.view="Psicologia"; st.rerun()

    elif v=="HojaVidaIA":
        st.subheader("📄 3. HOJA DE VIDA - En otro lado - IA Opcional")
        st.write("Campo opcional no requisito")
        with st.form("hv_ia"):
            ced=st.text_input("Cédula candidato (opcional)")
            cargo_sel=st.selectbox("Cargo a evaluar", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
            archivo=st.file_uploader("Cargar Hoja de Vida - OPCIONAL", type=["pdf","docx","txt"])
            texto_manual=st.text_area("O pegar texto HV - OPCIONAL")
            if st.form_submit_button("🧠 Analizar HV con IA", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo"
                if texto_manual: texto+= " " + texto_manual
                if not texto: texto="Sin HV"
                score, concepto = analizar_hv_ia(texto, st.session_state.cargos_db[cargo_sel]["nombre"])
                st.session_state.hojas_vida.append({"cedula":ced or "Opcional","cargo":st.session_state.cargos_db[cargo_sel]["nombre"],"score_ia":score,"concepto":concepto,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"✅ {score}% - {concepto}")
        if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="HojasAnalizadas":
        st.subheader("📄 Hojas Analizadas - Módulo 3")
        if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)
        else: st.info("Sin hojas")

    elif v=="Asignar":
        st.subheader("📌 Asignar - 3 Módulos")
        with st.form("asig"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula*")
                nom=st.text_input("Nombre*")
            with c2:
                cargo=st.selectbox("Cargo* (Módulo 1)", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                psi_sel=st.selectbox("Prueba Psicológica (Módulo 2)", [p.get("Nombre","") for p in st.session_state.pruebas_psicologicas])
                hv_check=st.checkbox("Incluir HV IA Opcional (Módulo 3)", value=False)
            if st.form_submit_button("✅ Crear", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"psicologica":psi_sel,"hv_opcional":"SI" if hv_check else "NO","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Invitado {ced} creado")

    elif v in ["PlanTrabajo","Planeacion","Informes","Historicos"]:
        st.subheader(v)
        if v=="PlanTrabajo":
            with st.form("plan"):
                titulo=st.text_input("Título")
                fecha=st.date_input("Fecha", value=date.today())
                cant=st.number_input("Entrevistas", min_value=1, max_value=100, value=5)
                if st.form_submit_button("💾 Guardar", type="primary"):
                    st.session_state.plan_trabajo.append({"Titulo":titulo,"Fecha":str(fecha),"Cantidad":cant})
                    st.success("Guardado")
            if st.session_state.plan_trabajo: st.dataframe(pd.DataFrame(st.session_state.plan_trabajo), use_container_width=True)
        elif v=="Planeacion":
            with st.form("plane"):
                fecha=st.date_input("Fecha", value=date.today())
                entrevistas=st.number_input("Entrevistas", min_value=1, max_value=50, value=5)
                if st.form_submit_button("💾 Guardar", type="primary"):
                    st.session_state.planeacion.append({"Fecha":str(fecha),"Entrevistas":entrevistas})
                    st.success("Guardado")
            if st.session_state.planeacion: st.dataframe(pd.DataFrame(st.session_state.planeacion), use_container_width=True)
        elif v=="Informes":
            if st.session_state.resultados: st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
            if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)
            if not st.session_state.resultados and not st.session_state.hojas_vida: st.info("Sin datos")
        elif v=="Historicos":
            if st.session_state.resultados:
                df=pd.DataFrame(st.session_state.resultados)
                c1,c2=st.columns(2)
                with c1: st.write("✅ Aprobados"); st.dataframe(df[df["score_num"]>=70] if "score_num" in df.columns else df, use_container_width=True)
                with c2: st.write("❌ No Aprobados"); st.dataframe(df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame(), use_container_width=True)
            else: st.info("Sin históricos")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin pruebas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.subheader(f"Invitado {ced} - {cargo['nombre']}")
            hv_file=st.file_uploader("Cargar HV - OPCIONAL", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_txt=st.text_area("Texto HV opcional", key=f"hvtxt_{idx}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"{i+1}. {pr['q']}")
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                psi_r=st.radio("Psicológica - ¿Cómo te describes?", ["Dominante","Influyente","Estable","Concienzudo"], index=None, key=f"psi_{idx}")
                if st.form_submit_button("🚀 FINALIZAR", type="primary", use_container_width=True):
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV"
                    if hv_txt: texto_hv+= " " + hv_txt
                    if texto_hv:
                        score_ia, concepto_ia = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({"cedula":ced,"cargo":cargo["nombre"],"score_ia":score_ia,"concepto":concepto_ia,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],"score":f"{sc}%","score_num":sc,"psicologica":psi_r or "","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% - Completado")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
