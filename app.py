import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="BRAGI-IA V33 MENU NUEVO", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp{background:#E8F5E9!important}
[data-testid="stSidebar"]{background:#176B5E!important;min-width:330px!important;max-width:330px!important}
button[data-testid="stSidebarCollapsedControl"]{display:none!important}
[data-testid="stSidebar"] input{background:white!important;color:black!important;border-radius:12px!important}
section[data-testid="stSidebar"].stButton > button{
    background:white!important;color:black!important;border-radius:10px!important;
    font-weight:800!important;border:1.5px solid #B2DFDB!important;height:46px!important;margin:4px 0!important;width:100%!important;text-align:left!important;
}
section[data-testid="stSidebar"].stButton > button p, section[data-testid="stSidebar"].stButton > button span{
    color:black!important;font-weight:800!important;font-size:12.5px!important;
}
section[data-testid="stSidebar"].stButton > button:hover{background:#E0F2F1!important}
div[data-testid="stExpander"]{background:#1F7A6B!important;border-radius:12px!important;margin:6px 0!important;border:none!important}
div[data-testid="stExpander"][open]{background:#248A7A!important}
div[data-testid="stExpander"] summary p{color:white!important;font-weight:700!important;font-size:13px!important}
div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, div[data-testid="stNumberInput"] > div, div[data-testid="stDateInput"] > div{
    background:white!important;border:1.5px solid #C8E6C9!important;border-radius:12px!important;
}
input, textarea{color:black!important;font-weight:600!important;background:white!important}
h1,h2,h3,p,label{color:black!important}
div[data-testid="stDataFrame"] *{color:black!important}
</style>
""", unsafe_allow_html=True)

# SESSION
if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "hojas_vida" not in st.session_state: st.session_state.hojas_vida=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Dashboard"
if "categorias" not in st.session_state:
    st.session_state.categorias=[
        {"ID":1,"Cargo":"AUXILIAR CONTABLE","Área":"Contabilidad","Vida Util":"VU 1 AÑO"},
        {"ID":2,"Cargo":"ABOGADO TUTELAS PQR","Área":"Jurídica","Vida Util":"VU 1 AÑO"},
        {"ID":3,"Cargo":"QUÍMICO FARMACÉUTICO","Área":"Farmacia","Vida Util":"VU 1 AÑO"},
        {"ID":4,"Cargo":"REGENTE DE FARMACIA","Área":"Farmacia","Vida Util":"VU 1 AÑO"},
    ]
if "preguntas" not in st.session_state:
    st.session_state.preguntas=[
        {"ID":1,"Cargo":"AUXILIAR CONTABLE","Pregunta":"¿Qué es PUC?","Respuesta Correcta":"Plan Único de Cuentas","Opción B":"Pago Único","Opción C":"Presupuesto","Tipo":"Técnica"},
        {"ID":2,"Cargo":"ABOGADO TUTELAS PQR","Pregunta":"¿Término tutela?","Respuesta Correcta":"10 días","Opción B":"1 año","Opción C":"30 días","Tipo":"Técnica"},
    ]
if "pruebas_psicologicas" not in st.session_state:
    st.session_state.pruebas_psicologicas=[
        {"ID":1,"Nombre":"16PF","Tipo":"Personalidad","Duración":"30 min"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento","Duración":"15 min"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva","Duración":"25 min"},
        {"ID":4,"Nombre":"ICF IE","Tipo":"Emocional","Duración":"20 min"},
    ]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas PQR","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año","30 días"],"ok":0}]},
        "quimico":{"nombre":"Químico Farmacéutico","preguntas":[{"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago","Almacenamiento"],"ok":0}]},
        "regente":{"nombre":"Regente de Farmacia","preguntas":[{"q":"¿Qué es dispensación?","opts":["Entrega informada de medicamentos","Venta libre","Almacenamiento"],"ok":0}]},
    }

def analizar_hv_ia(texto, cargo):
    texto=texto.lower(); score=0
    for kw in ["contabilidad","puc","excel","derecho","tutela","farmacia","invima","medicamentos","experiencia","universidad","años"]:
        if kw in texto: score+=12
    score=min(score,100)
    if score>=90: concepto, mejora = "PERSONAL APTO - ALTO DESEMPEÑO","Excelente perfil. Recomendación: Continuar proceso contratación inmediata. Mantener fortalezas."
    elif score>=70: concepto, mejora = "PERSONAL APTO","Perfil aprobado. Recomendación: Apto para contratación con inducción normal."
    else: concepto, mejora = "NO APTO","Recomendación: No contratar por ahora. Debe mejorar: Formación técnica, experiencia específica, competencias del cargo."
    return score, concepto, mejora

def recomendacion_por_score(sc):
    if sc>=90:
        return f"APTO 90%+ - Calificación {sc}% - Recomendación: CONTRATAR - Personal sobresaliente. Debe mejorar: Perfeccionar liderazgo y gestión del tiempo. Fortalezas: Conocimiento técnico alto."
    elif sc>=70:
        return f"APTO - Calificación {sc}% - Recomendación: CONTRATAR - Cumple requisitos. Debe mejorar: Reforzar conocimientos específicos del cargo."
    else:
        return f"NO APTO - Calificación {sc}% - Recomendación: NO CONTRATAR por debajo de 70%. Debe mejorar: Capacitación técnica, experiencia, comprensión del rol, puntualidad en pruebas."

# LOGIN
if st.session_state.rol is None:
    st.markdown("<h2 style='text-align:center;color:black'>BRAGI-IA - V33 MENÚ NUEVO</h2>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
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
    with c2:
        st.success("NUEVO MENÚ V33")
        st.write("● LISTA DE CATEGORÍAS")
        st.write("● ASIGNACIÓN DE ENTREVISTA")
        st.write("● ÁREA PSICOLÓGICA")
        st.write("● INFORMES")
        st.write("● PERSONAL APTO - 90%")
        st.write("● NO APTOS - <70%")
    st.stop()

# SIDEBAR - NUEVO MENU EXACTO QUE PEDISTE
with st.sidebar:
    st.markdown("<h3 style='color:white!important'>BRAGI-IA V33</h3><p style='color:#B2DFDB!important;font-size:11px;margin-top:-10px'>Menú fijo</p>", unsafe_allow_html=True)

    with st.expander("● LISTA DE CATEGORÍAS", expanded=True):
        if st.button("📋 Lista Categorías", use_container_width=True, key="cat_list"): st.session_state.view="ListaCategorias"; st.rerun()
        if st.button("➕ Crear cargos", use_container_width=True, key="cat_cargo"): st.session_state.view="CrearCargos"; st.rerun()
        if st.button("❓ Crear preguntas y respuestas", use_container_width=True, key="cat_preg"): st.session_state.view="CrearPreguntas"; st.rerun()
        if st.button("📄 Análisis de hoja de vida IA (Opcional)", use_container_width=True, key="cat_hv"): st.session_state.view="HojaVidaIA"; st.rerun()

    with st.expander("● ASIGNACIÓN DE ENTREVISTA", expanded=True):
        if st.button("📌 Crear entrevista (Cargo + Psicológica + Fecha)", use_container_width=True, key="asig_crear"): st.session_state.view="CrearEntrevista"; st.rerun()
        if st.button("📋 Entrevistas Creadas", use_container_width=True, key="asig_list"): st.session_state.view="ListaEntrevistas"; st.rerun()

    with st.expander("● ÁREA PSICOLÓGICA", expanded=True):
        if st.button("➕ Crear prueba", use_container_width=True, key="psi_crear"): st.session_state.view="CrearPruebaPsi"; st.rerun()
        if st.button("📊 Resultados de la prueba psicológica", use_container_width=True, key="psi_res"): st.session_state.view="ResultadosPsi"; st.rerun()

    with st.expander("● INFORMES", expanded=True):
        if st.button("📊 Dashboard", use_container_width=True, key="inf_dash"): st.session_state.view="Dashboard"; st.rerun()
        if st.button("🗓️ Plan de trabajo - Entrevistas programadas", use_container_width=True, key="inf_plan"): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("✅ Reporte de entrevistas realizadas", use_container_width=True, key="inf_real"): st.session_state.view="ReporteRealizadas"; st.rerun()
        if st.button("❌ Reporte de entrevistas rechazadas", use_container_width=True, key="inf_rech"): st.session_state.view="ReporteRechazadas"; st.rerun()
        if st.button("🕘 Históricos", use_container_width=True, key="inf_hist"): st.session_state.view="Historicos"; st.rerun()

    with st.expander("● PERSONAL APTO", expanded=True):
        if st.button("✅ Reporte Personal Apto 90% +", use_container_width=True, key="apto_rep"): st.session_state.view="PersonalApto"; st.rerun()

    with st.expander("● NO APTOS", expanded=True):
        if st.button("❌ Reporte Personal No Apto <70%", use_container_width=True, key="noapto_rep"): st.session_state.view="NoAptos"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

# RRHH VIEWS
if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Entrevistas", len(st.session_state.asignaciones))
        c2.metric("Realizadas", len(st.session_state.resultados))
        c3.metric("HV IA", len(st.session_state.hojas_vida))
        c4.metric("Aptos 90%+", len([r for r in st.session_state.resultados if r.get("score_num",0)>=90]))
        c5.metric("No Aptos <70%", len([r for r in st.session_state.resultados if r.get("score_num",0)<70]))
        st.subheader("Dashboard - Resumen")
        if st.session_state.resultados: st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)

    elif v=="ListaCategorias":
        st.subheader("● LISTA DE CATEGORÍAS - Cargos")
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("Buscar", placeholder="🔍 Buscar cargo", label_visibility="collapsed")
        with col2:
            if st.button("➕ Crear cargos", type="primary", use_container_width=True): st.session_state.view="CrearCargos"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Cargo"].str.contains(b.upper(), na=False)]
        st.write(f"Total Cargos: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif v=="CrearCargos":
        st.subheader("● LISTA DE CATEGORÍAS - Crear cargos")
        with st.form("crear_cargos"):
            cargo=st.text_input("Cargo *", placeholder="Ej: AUXILIAR CONTABLE")
            area=st.text_input("Área *", placeholder="Contabilidad, Jurídica, Farmacia")
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear cargo", type="primary"):
                if cargo:
                    new_id=max([c.get("ID",0) for c in st.session_state.categorias], default=0)+1
                    st.session_state.categorias.append({"ID":new_id,"Cargo":cargo.upper(),"Área":area.upper(),"Vida Util":vida})
                    nid=cargo.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":cargo,"area":area,"preguntas":[]}
                    st.success(f"Cargo {cargo.upper()} creado"); st.session_state.view="ListaCategorias"; st.rerun()

    elif v=="CrearPreguntas":
        st.subheader("● LISTA DE CATEGORÍAS - Crear preguntas y respuestas")
        with st.form("crear_preg"):
            cargos=[c.get("Cargo","") for c in st.session_state.categorias]
            cargo_sel=st.selectbox("Seleccionar Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
            pregunta=st.text_area("Pregunta *", placeholder="Ej: ¿Qué es PUC?")
            correcta=st.text_input("Respuesta Correcta *", placeholder="Ej: Plan Único de Cuentas")
            opB=st.text_input("Opción B", placeholder="Opción incorrecta")
            opC=st.text_input("Opción C", placeholder="Opción incorrecta")
            tipo=st.selectbox("Tipo", ["Técnica","Psicológica","Comportamental"])
            if st.form_submit_button("➕ Crear pregunta y respuestas", type="primary"):
                if pregunta and correcta:
                    new_id=max([p.get("ID",0) for p in st.session_state.preguntas], default=0)+1
                    st.session_state.preguntas.append({"ID":new_id,"Cargo":cargo_sel,"Pregunta":pregunta,"Respuesta Correcta":correcta,"Opción B":opB,"Opción C":opC,"Tipo":tipo})
                    # agregar a cargos_db
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper():
                            v["preguntas"].append({"q":pregunta,"opts":[correcta,opB,opC],"ok":0})
                            break
                    st.success("Pregunta creada"); st.session_state.view="ListaPreguntas"; st.rerun()
        st.divider()
        if st.button("📋 Ver preguntas creadas"): st.session_state.view="ListaPreguntas"; st.rerun()

    elif v=="ListaPreguntas":
        st.subheader("Preguntas y Respuestas Creadas")
        if st.session_state.preguntas: st.dataframe(pd.DataFrame(st.session_state.preguntas), use_container_width=True)
        else: st.info("Sin preguntas")
        if st.button("➕ Crear más preguntas"): st.session_state.view="CrearPreguntas"; st.rerun()

    elif v=="HojaVidaIA":
        st.subheader("● LISTA DE CATEGORÍAS - Análisis de hoja de vida IA - OPCIONAL")
        st.info("Esta es opcional - No es requisito")
        with st.form("hv_ia"):
            ced=st.text_input("Cédula candidato (opcional)")
            cargos=[c.get("Cargo","") for c in st.session_state.categorias]
            cargo_sel=st.selectbox("Cargo a evaluar", cargos if cargos else ["AUXILIAR CONTABLE"])
            archivo=st.file_uploader("Cargar Hoja de Vida - OPCIONAL", type=["pdf","docx","txt"])
            texto_manual=st.text_area("O pegar texto HV - OPCIONAL")
            if st.form_submit_button("🧠 Analizar HV con IA - Opcional", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo"
                if texto_manual: texto+= " " + texto_manual
                if not texto: texto="Sin HV - Opcional"
                score, concepto, mejora = analizar_hv_ia(texto, cargo_sel)
                st.session_state.hojas_vida.append({"cedula":ced or "Opcional","cargo":cargo_sel,"score_ia":score,"concepto":concepto,"mejora":mejora,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"✅ {score}% - {concepto} - {mejora}")
        if st.session_state.hojas_vida: st.dataframe(pd.DataFrame(st.session_state.hojas_vida), use_container_width=True)

    elif v=="CrearEntrevista":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Crear entrevista")
        st.write("Dentro de esta que tenga la opción de seleccionar el cargo y seleccionar la prueba de psicología y la fecha")
        with st.form("crear_entrevista"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula candidato *", placeholder="Solo cédula")
                nom=st.text_input("Nombre candidato *", placeholder="Nombre completo")
                fecha_ent=st.date_input("Fecha entrevista *", value=date.today())
                hora_ent=st.time_input("Hora entrevista")
            with c2:
                cargos=[c.get("Cargo","") for c in st.session_state.categorias]
                cargo_sel=st.selectbox("Seleccionar el cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
                pruebas=[p.get("Nombre","") for p in st.session_state.pruebas_psicologicas]
                prueba_sel=st.selectbox("Seleccionar la prueba de psicología *", pruebas if pruebas else ["DISC","16PF"])
                hv_check=st.checkbox("Incluir Análisis Hoja de Vida IA - Opcional", value=False)
            if st.form_submit_button("📌 Crear entrevista", type="primary", use_container_width=True):
                if ced and nom:
                    cargo_key=list(st.session_state.cargos_db.keys())[0]
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper(): cargo_key=k; break
                    st.session_state.asignaciones.append({
                        "cedula":ced,"nombre":nom,"cargo_key":cargo_key,"cargo_nombre":cargo_sel,
                        "prueba_psicologia":prueba_sel,"fecha_entrevista":str(fecha_ent),"hora_entrevista":str(hora_ent),
                        "hv_opcional":"SI" if hv_check else "NO","fecha_creacion":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success(f"Entrevista creada para {nom} - {cargo_sel} - {prueba_sel} - {fecha_ent}")
                    st.session_state.view="ListaEntrevistas"; st.rerun()

    elif v=="ListaEntrevistas":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Entrevistas Creadas")
        if st.session_state.asignaciones: st.dataframe(pd.DataFrame(st.session_state.asignaciones), use_container_width=True)
        else: st.info("Sin entrevistas creadas")
        if st.button("📌 Crear nueva entrevista", type="primary"): st.session_state.view="CrearEntrevista"; st.rerun()

    elif v=="CrearPruebaPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Crear prueba")
        with st.form("crear_psi"):
            nombre=st.text_input("Nombre Prueba Psicológica *", placeholder="Ej: 16PF, DISC, Wartegg")
            tipo=st.selectbox("Tipo *", ["Personalidad","Comportamiento","Proyectiva","Emocional","Valores"])
            desc=st.text_area("Descripción prueba")
            dur=st.text_input("Duración", value="20 min")
            if st.form_submit_button("➕ Crear prueba", type="primary"):
                if nombre:
                    new_id=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":new_id,"Nombre":nombre.upper(),"Tipo":tipo,"Descripción":desc,"Duración":dur})
                    st.success("Prueba creada"); st.session_state.view="ResultadosPsi"; st.rerun()

    elif v=="ResultadosPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Resultados de la prueba psicológica")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            st.dataframe(df, use_container_width=True)
            if "psicologica" in df.columns:
                st.bar_chart(df["psicologica"].value_counts())
        else: st.info("Sin resultados psicológicos aún")
        if st.session_state.pruebas_psicologicas:
            st.subheader("Pruebas disponibles")
            st.dataframe(pd.DataFrame(st.session_state.pruebas_psicologicas), use_container_width=True, hide_index=True)

    elif v=="PlanTrabajo":
        st.subheader("● INFORMES - Plan de trabajo - Entrevistas programadas para realizar")
        if st.session_state.asignaciones:
            df=pd.DataFrame(st.session_state.asignaciones)
            st.write(f"Total entrevistas programadas: {len(df)}")
            st.dataframe(df, use_container_width=True)
            if "fecha_entrevista" in df.columns:
                st.write("📅 Por fecha:")
                st.dataframe(df.sort_values("fecha_entrevista"), use_container_width=True)
        else: st.info("Sin entrevistas programadas - Ve a ASIGNACIÓN DE ENTREVISTA - Crear entrevista")

    elif v=="ReporteRealizadas":
        st.subheader("● INFORMES - Reporte de entrevistas realizadas")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            st.write(f"Total realizadas: {len(df)}")
            st.dataframe(df, use_container_width=True)
        else: st.info("Sin entrevistas realizadas aún - Los invitados deben finalizar su entrevista")

    elif v=="ReporteRechazadas":
        st.subheader("● INFORMES - Reporte de entrevistas rechazadas")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            rech=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            st.write(f"Total rechazadas (<70%): {len(rech)}")
            st.dataframe(rech, use_container_width=True)
        else: st.info("Sin rechazadas aún")

    elif v=="Historicos":
        st.subheader("● INFORMES - Históricos")
        if st.session_state.resultados:
            st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
        else: st.info("Sin históricos")

    elif v=="PersonalApto":
        st.subheader("● PERSONAL APTO - Reporte - Calificación y recomendaciones 90%+")
        st.info("Dentro de esta que se vea la calificación de las pruebas y las recomendaciones del personal que paso la entrevista con el 90% y que debe mejorar - Todos los informes realizados")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            aptos=df[df["score_num"]>=90] if "score_num" in df.columns else pd.DataFrame()
            st.write(f"✅ Total Personal Apto 90%+: {len(aptos)}")
            if not aptos.empty:
                # agregar recomendaciones
                aptos["Recomendación"] = aptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                aptos["Debe Mejorar"] = "Liderazgo, gestión tiempo, perfeccionar conocimientos avanzados del cargo"
                st.dataframe(aptos, use_container_width=True)
                for _, row in aptos.iterrows():
                    st.success(f"**{row.get('nombre','')} - {row.get('cargo_nombre','')} - {row.get('score','')}** - {row.get('Recomendación','')}")
            else:
                st.warning("Aún no hay personal con 90%+ - Se muestran todos los aptos >=70%")
                aptos70=df[df["score_num"]>=70] if "score_num" in df.columns else df
                if not aptos70.empty:
                    aptos70["Recomendación"] = aptos70["score_num"].apply(lambda x: recomendacion_por_score(x))
                    st.dataframe(aptos70, use_container_width=True)
        else:
            st.info("Sin entrevistas realizadas - Todos los informes realizados aparecerán aquí")
        # incluir HV IA aptos
        if st.session_state.hojas_vida:
            st.divider()
            st.subheader("HV IA - Personal Apto")
            df_hv=pd.DataFrame(st.session_state.hojas_vida)
            df_hv_apto=df_hv[df_hv["score_ia"]>=90] if "score_ia" in df_hv.columns else df_hv
            st.dataframe(df_hv_apto, use_container_width=True)

    elif v=="NoAptos":
        st.subheader("● NO APTOS - Reporte - Personal que no paso entrevista por debajo de 70%")
        st.info("Y las recomendación si se debe o no contratar y con recomendaciones a mejorar - Todos los informes realizados")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            noaptos=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            st.write(f"❌ Total No Aptos <70%: {len(noaptos)}")
            if not noaptos.empty:
                noaptos["Recomendación Contratar"] = noaptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                noaptos["Debe Mejorar"] = "Capacitación técnica, experiencia específica del cargo, comprensión del rol, puntualidad, reforzar conocimientos básicos"
                noaptos["¿Contratar?"] = "NO - Requiere plan de mejora"
                st.dataframe(noaptos, use_container_width=True)
                for _, row in noaptos.iterrows():
                    st.error(f"**{row.get('nombre','')} - {row.get('cargo_nombre','')} - {row.get('score','')}** - {row.get('Recomendación Contratar','')} - Debe mejorar: {row.get('Debe Mejorar','')}")
            else:
                st.success("No hay personal no apto - Todos aprobaron")
        else:
            st.info("Sin entrevistas - Todos los informes realizados aparecerán aquí")
        if st.session_state.hojas_vida:
            st.divider()
            st.subheader("HV IA - No Aptos")
            df_hv=pd.DataFrame(st.session_state.hojas_vida)
            df_hv_no=df_hv[df_hv["score_ia"]<70] if "score_ia" in df_hv.columns else pd.DataFrame()
            if not df_hv_no.empty: st.dataframe(df_hv_no, use_container_width=True)

# CANDIDATO
if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin entrevistas asignadas - RRHH debe crearte una en ASIGNACIÓN DE ENTREVISTA")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.subheader(f"Entrevista - {ced} - {cargo['nombre']} - Fecha: {asig.get('fecha_entrevista','')} - Prueba Psi: {asig.get('prueba_psicologia','')}")
            hv_file=st.file_uploader("Cargar Hoja de Vida - OPCIONAL", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_txt=st.text_area("Texto HV opcional", key=f"hvtxt_{idx}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"{i+1}. {pr['q']}")
                    r=st.radio("Elige respuesta", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                st.markdown(f"**🧠 Prueba Psicológica Asignada: {asig.get('prueba_psicologia','DISC')}**")
                psi_r=st.radio("Responde prueba psicológica - ¿Cómo te describes?", ["Dominante - Decidido","Influyente - Sociable","Estable - Paciente","Concienzudo - Analítico"], index=None, key=f"psi_{idx}")
                if st.form_submit_button("🚀 FINALIZAR ENTREVISTA", type="primary", use_container_width=True):
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV"
                    if hv_txt: texto_hv+= " " + hv_txt
                    score_hv=0; concepto_hv=""
                    if texto_hv:
                        score_hv, concepto_hv, mejora_hv = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({"cedula":ced,"cargo":cargo["nombre"],"score_ia":score_hv,"concepto":concepto_hv,"mejora":mejora_hv,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    total_sc = int((sc + (score_hv if score_hv else sc))/2) if score_hv else sc
                    st.session_state.resultados.append({
                        "cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],
                        "cargo":cargo["nombre"],"score":f"{total_sc}%","score_num":total_sc,
                        "psicologica":psi_r or asig.get("prueba_psicologia",""),"prueba_psicologia":asig.get("prueba_psicologia",""),
                        "hv_score":score_hv,"hv_concepto":concepto_hv,"fecha_entrevista":asig.get("fecha_entrevista",""),
                        "recomendacion":recomendacion_por_score(total_sc),"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    if total_sc>=90: st.success(f"✅ {total_sc}% - PERSONAL APTO - Excelente")
                    elif total_sc>=70: st.success(f"✅ {total_sc}% - APTO")
                    else: st.error(f"❌ {total_sc}% - NO APTO - {recomendacion_por_score(total_sc)}")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
