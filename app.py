import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

st.set_page_config(page_title="BRAGI-IA V34 CHULETA + CARGO", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp{background:#E8F5E9!important}
[data-testid="stSidebar"]{background:#176B5E!important;min-width:340px!important;max-width:340px!important}
button[data-testid="stSidebarCollapsedControl"]{display:none!important}
[data-testid="stSidebar"] input{background:white!important;color:black!important;border-radius:12px!important}
section[data-testid="stSidebar"].stButton > button{
    background:white!important;color:black!important;border-radius:10px!important;
    font-weight:800!important;border:1.5px solid #B2DFDB!important;min-height:46px!important;margin:4px 0!important;width:100%!important;text-align:left!important;
}
section[data-testid="stSidebar"].stButton > button p, section[data-testid="stSidebar"].stButton > button span{
    color:black!important;font-weight:800!important;font-size:12.5px!important;
}
div[data-testid="stExpander"]{background:#1F7A6B!important;border-radius:12px!important;margin:6px 0!important;border:none!important}
div[data-testid="stExpander"][open]{background:#248A7A!important}
div[data-testid="stExpander"] summary p{color:white!important;font-weight:700!important}
div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, div[data-testid="stNumberInput"] > div, div[data-testid="stDateInput"] > div, div[data-testid="stMultiSelect"] > div{
    background:white!important;border:1.5px solid #C8E6C9!important;border-radius:12px!important;
}
input, textarea{color:black!important;font-weight:600!important;background:white!important}
h1,h2,h3,p,label{color:black!important}
div[data-testid="stDataFrame"] *{color:black!important}
.stCheckbox label{color:black!important;font-weight:600!important}
</style>
""", unsafe_allow_html=True)

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
if "preguntas" not in st.session_state: st.session_state.preguntas=[]
if "pruebas_psicologicas" not in st.session_state:
    st.session_state.pruebas_psicologicas=[
        {"ID":1,"Nombre":"16PF - Cattell","Tipo":"Personalidad","Descripción":"16 factores personalidad","Duración":"30 min"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento","Descripción":"Dominancia, Influencia, Estabilidad, Conciencia","Duración":"15 min"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva","Descripción":"8 cuadros proyectivos","Duración":"25 min"},
        {"ID":4,"Nombre":"ICF Inteligencia Emocional","Tipo":"Emocional","Descripción":"Test Inteligencia Emocional","Duración":"20 min"},
        {"ID":5,"Nombre":"Zavic Valores","Tipo":"Valores","Descripción":"Honestidad, trabajo","Duración":"15 min"},
        {"ID":6,"Nombre":"IPV Ventas","Tipo":"Comercial","Descripción":"Perfil vendedor","Duración":"20 min"},
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
    for kw in ["contabilidad","puc","excel","siigo","derecho","tutela","pqr","farmacia","invima","medicamentos","experiencia","universidad","años"]:
        if kw in texto: score+=10
    score=min(score,100)
    if score>=90: concepto="APTO 90%+"; mejora="Excelente perfil. Recomendación: Contratar inmediato. Mejora: Liderazgo, gestión tiempo."
    elif score>=70: concepto="APTO"; mejora="Perfil aprobado. Recomendación: Apto contratación. Mejora: Reforzar conocimientos específicos."
    else: concepto="NO APTO"; mejora="No contratar por ahora. Mejora: Formación técnica, experiencia, competencias cargo."
    return score, concepto, mejora

def recomendacion_por_score(sc):
    if sc>=90: return f"APTO 90%+ - {sc}% - CONTRATAR - Sobresaliente. Mejora: Liderazgo avanzado."
    elif sc>=70: return f"APTO - {sc}% - CONTRATAR - Cumple. Mejora: Reforzar específicos cargo."
    else: return f"NO APTO - {sc}% - NO CONTRATAR <70%. Mejora: Capacitación técnica, experiencia, comprensión rol."

def tabla_con_descarga(df, nombre_archivo):
    """Visualización sin necesidad de descargar + descarga opcional en español"""
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.write(f"Total registros: {len(df)}")
    # Visualización siempre, descarga opcional
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label=f"📥 Descargar como CSV - {nombre_archivo}",
        data=csv_buffer.getvalue(),
        file_name=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        key=f"dl_{nombre_archivo}_{datetime.now().microsecond}"
    )

# LOGIN
if st.session_state.rol is None:
    st.markdown("<h2 style='text-align:center;color:black'>BRAGI-IA V34 - CHULETA + CARGO + DESCARGA ESPAÑOL</h2>", unsafe_allow_html=True)
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
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","pruebas_asignadas":["DISC"],"fecha_creacion":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with c2:
        st.success("V34 - Nuevo: Cargo en crear prueba psicológica + chuleta + resultados con usuarios + descarga español opcional")
    st.stop()

# SIDEBAR - MENU V33 PERO CON NOMBRE crear cargos
with st.sidebar:
    st.markdown("<h3 style='color:white!important'>BRAGI-IA V34</h3><p style='color:#B2DFDB!important;font-size:11px;margin-top:-10px'>Chuleta + Cargo + CSV Español</p>", unsafe_allow_html=True)

    with st.expander("● LISTA DE CATEGORÍAS", expanded=True):
        if st.button("📋 Lista de categorías", use_container_width=True): st.session_state.view="ListaCategorias"; st.rerun()
        if st.button("➕ Crear cargos", use_container_width=True): st.session_state.view="CrearCargos"; st.rerun()
        if st.button("❓ Crear preguntas y respuestas", use_container_width=True): st.session_state.view="CrearPreguntas"; st.rerun()
        if st.button("📄 Análisis hoja de vida IA (Opcional)", use_container_width=True): st.session_state.view="HojaVidaIA"; st.rerun()

    with st.expander("● ASIGNACIÓN DE ENTREVISTA", expanded=True):
        if st.button("📌 Crear entrevista (Cargo + Psicológica + Fecha)", use_container_width=True): st.session_state.view="CrearEntrevista"; st.rerun()
        if st.button("📋 Entrevistas creadas", use_container_width=True): st.session_state.view="ListaEntrevistas"; st.rerun()

    with st.expander("● ÁREA PSICOLÓGICA", expanded=True):
        if st.button("➕ Crear prueba psicológica (con Cargo + Chuleta)", use_container_width=True): st.session_state.view="CrearPruebaPsi"; st.rerun()
        if st.button("📊 Resultados prueba psicológica (Usuarios)", use_container_width=True): st.session_state.view="ResultadosPsi"; st.rerun()

    with st.expander("● INFORMES", expanded=True):
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()
        if st.button("🗓️ Plan de trabajo - Programadas", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("✅ Reporte realizadas", use_container_width=True): st.session_state.view="ReporteRealizadas"; st.rerun()
        if st.button("❌ Reporte rechazadas", use_container_width=True): st.session_state.view="ReporteRechazadas"; st.rerun()
        if st.button("🕘 Históricos", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    with st.expander("● PERSONAL APTO", expanded=True):
        if st.button("✅ Reporte Personal Apto 90%+", use_container_width=True): st.session_state.view="PersonalApto"; st.rerun()

    with st.expander("● NO APTOS", expanded=True):
        if st.button("❌ Reporte No Apto <70%", use_container_width=True): st.session_state.view="NoAptos"; st.rerun()

    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

# RRHH
if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Entrevistas", len(st.session_state.asignaciones))
        c2.metric("Realizadas", len(st.session_state.resultados))
        c3.metric("HV IA", len(st.session_state.hojas_vida))
        c4.metric("Aptos 90%+", len([r for r in st.session_state.resultados if r.get("score_num",0)>=90]))
        c5.metric("No Aptos <70%", len([r for r in st.session_state.resultados if r.get("score_num",0)<70]))
        st.subheader("Dashboard - Visualización sin descarga + Descarga opcional")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            tabla_con_descarga(df, "Dashboard_Entrevistas")
        else: st.info("Sin datos")

    elif v=="ListaCategorias":
        st.subheader("● LISTA DE CATEGORÍAS - Lista de categorías (Submenu: crear cargos)")
        col1,col2=st.columns([3,1])
        with col1: b=st.text_input("Buscar", placeholder="🔍 Buscar cargo", label_visibility="collapsed")
        with col2:
            if st.button("➕ Crear cargos", type="primary", use_container_width=True): st.session_state.view="CrearCargos"; st.rerun()
        df=pd.DataFrame(st.session_state.categorias)
        if b: df=df[df["Cargo"].str.contains(b.upper(), na=False)]
        st.write(f"Total Cargos: {len(df)} - Visualización directa")
        tabla_con_descarga(df, "Lista_Categorias_Cargos")

    elif v=="CrearCargos":
        st.subheader("● LISTA DE CATEGORÍAS - Crear cargos (Submenu)")
        st.write("Nombre del submenu es crear cargos - como pediste")
        with st.form("crear_cargos"):
            cargo=st.text_input("Cargo *", placeholder="Ej: AUXILIAR CONTABLE")
            area=st.text_input("Área *", placeholder="Contabilidad, Jurídica, Farmacia")
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear cargos", type="primary"):
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
            pregunta=st.text_area("Pregunta *")
            correcta=st.text_input("Respuesta Correcta *")
            opB=st.text_input("Opción B")
            opC=st.text_input("Opción C")
            tipo=st.selectbox("Tipo", ["Técnica","Psicológica","Comportamental"])
            if st.form_submit_button("➕ Crear pregunta y respuestas", type="primary"):
                if pregunta and correcta:
                    new_id=len(st.session_state.preguntas)+1
                    st.session_state.preguntas.append({"ID":new_id,"Cargo":cargo_sel,"Pregunta":pregunta,"Respuesta Correcta":correcta,"Opción B":opB,"Opción C":opC,"Tipo":tipo})
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper():
                            v["preguntas"].append({"q":pregunta,"opts":[correcta,opB,opC],"ok":0}); break
                    st.success("Pregunta creada")
        if st.session_state.preguntas:
            st.subheader("Preguntas creadas - Visualización + Descarga opcional")
            tabla_con_descarga(pd.DataFrame(st.session_state.preguntas), "Preguntas_Respuestas")

    elif v=="HojaVidaIA":
        st.subheader("● Análisis hoja de vida IA - Opcional - Visualización + Descarga opcional")
        with st.form("hv_ia"):
            ced=st.text_input("Cédula (opcional)")
            cargos=[c.get("Cargo","") for c in st.session_state.categorias]
            cargo_sel=st.selectbox("Cargo a evaluar", cargos if cargos else ["AUXILIAR CONTABLE"])
            archivo=st.file_uploader("Cargar HV - OPCIONAL", type=["pdf","docx","txt"])
            texto_manual=st.text_area("Texto HV - OPCIONAL")
            if st.form_submit_button("🧠 Analizar HV con IA - Opcional", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo"
                if texto_manual: texto+= " " + texto_manual
                if not texto: texto="Sin HV"
                score, concepto, mejora = analizar_hv_ia(texto, cargo_sel)
                st.session_state.hojas_vida.append({"cedula":ced or "Opcional","cargo":cargo_sel,"score_ia":score,"concepto":concepto,"mejora":mejora,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"✅ {score}% - {concepto}")
        if st.session_state.hojas_vida:
            tabla_con_descarga(pd.DataFrame(st.session_state.hojas_vida), "Hoja_Vida_IA")

    elif v=="CrearEntrevista":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Crear entrevista - Cargo + Prueba Psicológica + Fecha")
        with st.form("crear_entrevista"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula *")
                nom=st.text_input("Nombre *")
                fecha_ent=st.date_input("Fecha entrevista *", value=date.today())
                hora_ent=st.time_input("Hora entrevista")
            with c2:
                cargos=[c.get("Cargo","") for c in st.session_state.categorias]
                cargo_sel=st.selectbox("Seleccionar el cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
                # Chuleta para pruebas psicológicas
                st.write("Seleccionar la prueba de psicología * (chuleta)")
                pruebas_dict = {p.get("Nombre",""): p.get("Nombre","") for p in st.session_state.pruebas_psicologicas}
                pruebas_seleccionadas=[]
                for nombre in pruebas_dict.keys():
                    if st.checkbox(nombre, key=f"chk_psi_{nombre}"):
                        pruebas_seleccionadas.append(nombre)
                hv_check=st.checkbox("Incluir Análisis HV IA - Opcional")
            if st.form_submit_button("📌 Crear entrevista", type="primary", use_container_width=True):
                if ced and nom:
                    cargo_key=list(st.session_state.cargos_db.keys())[0]
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper(): cargo_key=k; break
                    if not pruebas_seleccionadas: pruebas_seleccionadas=["DISC"]
                    st.session_state.asignaciones.append({
                        "cedula":ced,"nombre":nom,"cargo_key":cargo_key,"cargo_nombre":cargo_sel,
                        "pruebas_asignadas":", ".join(pruebas_seleccionadas),"fecha_entrevista":str(fecha_ent),"hora":str(hora_ent),
                        "hv_opcional":"SI" if hv_check else "NO","fecha_creacion":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success(f"Entrevista creada: {nom} - {cargo_sel} - Pruebas: {', '.join(pruebas_seleccionadas)} - {fecha_ent}")

    elif v=="ListaEntrevistas":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Entrevistas Creadas - Visualización + Descarga opcional")
        if st.session_state.asignaciones:
            tabla_con_descarga(pd.DataFrame(st.session_state.asignaciones), "Entrevistas_Creadas")
        else: st.info("Sin entrevistas")

    elif v=="CrearPruebaPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Crear prueba psicológica (con Cargo + Chuleta)")
        st.write("Ahora aparece el cargo y puedes seleccionar con chuleta las pruebas a realizar - como pediste")
        with st.form("crear_psi"):
            cargos=[c.get("Cargo","") for c in st.session_state.categorias]
            cargo_sel=st.selectbox("Seleccionar Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"], help="Cargo al que aplica esta prueba psicológica")
            st.divider()
            st.write("**Tipo de prueba - Seleccione con chuleta (checkbox) las pruebas a realizar:**")
            # Chuleta para tipo de prueba
            check_16pf = st.checkbox("16PF - Cattell - 16 factores personalidad")
            check_disc = st.checkbox("DISC - Dominancia, Influencia, Estabilidad, Conciencia")
            check_wartegg = st.checkbox("Wartegg - 8 cuadros proyectivos")
            check_icf = st.checkbox("ICF Inteligencia Emocional - Test IE")
            check_zavic = st.checkbox("Zavic Valores - Honestidad, trabajo")
            check_ipv = st.checkbox("IPV Ventas - Perfil vendedor")
            check_otro = st.checkbox("Otra prueba personalizada")
            nombre_personalizado=st.text_input("Si es otra, nombre prueba")
            desc=st.text_area("Descripción de las pruebas seleccionadas")
            dur=st.text_input("Duración", value="20 min")
            if st.form_submit_button("➕ Crear prueba psicológica con cargo + chuleta", type="primary"):
                pruebas_creadas=[]
                if check_16pf: pruebas_creadas.append("16PF")
                if check_disc: pruebas_creadas.append("DISC")
                if check_wartegg: pruebas_creadas.append("Wartegg")
                if check_icf: pruebas_creadas.append("ICF IE")
                if check_zavic: pruebas_creadas.append("Zavic")
                if check_ipv: pruebas_creadas.append("IPV")
                if check_otro and nombre_personalizado: pruebas_creadas.append(nombre_personalizado.upper())
                if not pruebas_creadas: pruebas_creadas=["DISC"]
                for prueba in pruebas_creadas:
                    new_id=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":new_id,"Nombre":prueba,"Tipo":"Chuleta seleccionada","Cargo":cargo_sel,"Descripción":desc,"Duración":dur})
                st.success(f"Pruebas creadas para cargo {cargo_sel}: {', '.join(pruebas_creadas)}")
                st.session_state.view="ResultadosPsi"; st.rerun()

    elif v=="ResultadosPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Resultado de prueba psicológica")
        st.write("Salen los usuarios que realizaron las pruebas y tener la opción de seleccionar la que se quiere ver con chuleta - Download as CSV en español")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            st.write(f"**Total usuarios que realizaron pruebas: {len(df)}** - Visualización directa sin necesidad de descargar")
            # Chuleta para seleccionar usuarios
            st.write("**Seleccione con chuleta los usuarios que quiere ver:**")
            cedulas_unicas=df["cedula"].unique().tolist() if "cedula" in df.columns else []
            seleccionados=[]
            cols=st.columns(3)
            for i, ced in enumerate(cedulas_unicas):
                col=cols[i%3]
                with col:
                    nombre=df[df["cedula"]==ced]["nombre"].iloc[0] if "nombre" in df.columns and len(df[df["cedula"]==ced])>0 else ced
                    if st.checkbox(f"{nombre} - {ced}", key=f"user_{ced}", value=True):
                        seleccionados.append(ced)
            if seleccionados:
                df_filtrado=df[df["cedula"].isin(seleccionados)] if "cedula" in df.columns else df
                st.divider()
                st.subheader(f"Usuarios seleccionados ({len(seleccionados)}) - Visualización")
                st.dataframe(df_filtrado, use_container_width=True)
                # Download as CSV en español + visualización
                csv_buffer = io.StringIO()
                df_filtrado.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Descargar como CSV - Resultados Psicológicos Seleccionados",
                    data=csv_buffer.getvalue(),
                    file_name=f"Resultados_Psicologicos_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Seleccione al menos un usuario con chuleta para ver")
            st.divider()
            st.subheader("Todos los resultados - Visualización completa + Descarga opcional")
            tabla_con_descarga(df, "Resultados_Psicologicos_Todos")
        else:
            st.info("Sin usuarios que hayan realizado pruebas aún")
        if st.session_state.pruebas_psicologicas:
            st.divider()
            st.subheader("Pruebas psicológicas disponibles")
            tabla_con_descarga(pd.DataFrame(st.session_state.pruebas_psicologicas), "Pruebas_Psicologicas_Disponibles")

    elif v=="PlanTrabajo":
        st.subheader("● INFORMES - Plan de trabajo - Entrevistas programadas")
        if st.session_state.asignaciones:
            df=pd.DataFrame(st.session_state.asignaciones)
            st.write("Visualización directa - Sin necesidad de descargar - Descarga opcional")
            tabla_con_descarga(df.sort_values("fecha_entrevista") if "fecha_entrevista" in df.columns else df, "Plan_Trabajo_Programadas")
        else: st.info("Sin programadas")

    elif v=="ReporteRealizadas":
        st.subheader("● INFORMES - Reporte de entrevistas realizadas - Visualización + Descarga opcional")
        if st.session_state.resultados:
            tabla_con_descarga(pd.DataFrame(st.session_state.resultados), "Entrevistas_Realizadas")
        else: st.info("Sin realizadas")

    elif v=="ReporteRechazadas":
        st.subheader("● INFORMES - Reporte de entrevistas rechazadas - Visualización + Descarga opcional")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            rech=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not rech.empty: tabla_con_descarga(rech, "Entrevistas_Rechazadas")
            else: st.success("No hay rechazadas")
        else: st.info("Sin datos")

    elif v=="Historicos":
        st.subheader("● INFORMES - Históricos - Visualización + Descarga opcional")
        if st.session_state.resultados:
            tabla_con_descarga(pd.DataFrame(st.session_state.resultados), "Historicos_Entrevistas")
        else: st.info("Sin históricos")

    elif v=="PersonalApto":
        st.subheader("● PERSONAL APTO - Reporte 90%+ - Visualización + Descarga opcional")
        st.write("Calificación de las pruebas y recomendaciones del personal que paso la entrevista con el 90% y que debe mejorar - Todos los informes realizados")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            aptos=df[df["score_num"]>=90] if "score_num" in df.columns else pd.DataFrame()
            if aptos.empty:
                st.warning("Aún no hay 90%+, mostrando >=70% como APTO")
                aptos=df[df["score_num"]>=70] if "score_num" in df.columns else df
            if not aptos.empty:
                aptos["Recomendación"] = aptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                aptos["Debe Mejorar"] = "Liderazgo, gestión tiempo, perfeccionar conocimientos avanzados"
                tabla_con_descarga(aptos, "Personal_APTO_90porciento")
                for _, row in aptos.iterrows():
                    st.success(f"{row.get('nombre','')} - {row.get('cargo_nombre','')} - {row.get('score','')} - {row.get('Recomendación','')}")
        else: st.info("Sin entrevistas - Todos los informes aparecerán aquí")

    elif v=="NoAptos":
        st.subheader("● NO APTOS - Reporte <70% - Visualización + Descarga opcional")
        st.write("Personal que no paso por debajo de 70% y recomendación si se debe o no contratar y recomendaciones a mejorar")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            noaptos=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not noaptos.empty:
                noaptos["¿Contratar?"] = "NO - Requiere plan mejora"
                noaptos["Recomendación"] = noaptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                noaptos["Debe Mejorar"] = "Capacitación técnica, experiencia, comprensión rol, puntualidad"
                tabla_con_descarga(noaptos, "Personal_NO_APTO_70porciento")
                for _, row in noaptos.iterrows():
                    st.error(f"{row.get('nombre','')} - {row.get('score','')} - {row.get('Recomendación','')}")
            else: st.success("No hay NO APTOS")
        else: st.info("Sin datos")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin entrevistas asignadas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.subheader(f"Entrevista - {ced} - {cargo['nombre']} - Fecha: {asig.get('fecha_entrevista','')} - Pruebas: {asig.get('pruebas_asignadas','')}")
            hv_file=st.file_uploader("Cargar HV - OPCIONAL", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_txt=st.text_area("Texto HV opcional", key=f"hvtxt_{idx}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"{i+1}. {pr['q']}")
                    r=st.radio("Elige respuesta", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                st.write(f"**🧠 Pruebas Psicológicas Asignadas: {asig.get('pruebas_asignadas','')}**")
                # Chuleta para responder pruebas psicológicas
                st.write("Seleccione con chuleta cómo se describe (puede marcar varias):")
                chk_dom=st.checkbox("Dominante - Decidido", key=f"dom_{idx}")
                chk_inf=st.checkbox("Influyente - Sociable", key=f"inf_{idx}")
                chk_est=st.checkbox("Estable - Paciente", key=f"est_{idx}")
                chk_con=st.checkbox("Concienzudo - Analítico", key=f"con_{idx}")
                if st.form_submit_button("🚀 FINALIZAR ENTREVISTA", type="primary", use_container_width=True):
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV"
                    if hv_txt: texto_hv+= " " + hv_txt
                    score_hv=0; concepto_hv=""
                    if texto_hv:
                        score_hv, concepto_hv, _ = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({"cedula":ced,"cargo":cargo["nombre"],"score_ia":score_hv,"concepto":concepto_hv,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    psi_desc=[]
                    if chk_dom: psi_desc.append("Dominante")
                    if chk_inf: psi_desc.append("Influyente")
                    if chk_est: psi_desc.append("Estable")
                    if chk_con: psi_desc.append("Concienzudo")
                    psi_str=", ".join(psi_desc) if psi_desc else "No marcado"
                    total_sc = int((sc + (score_hv if score_hv else sc))/2) if score_hv else sc
                    st.session_state.resultados.append({
                        "cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],
                        "score":f"{total_sc}%","score_num":total_sc,"psicologica":psi_str,
                        "pruebas_realizadas":asig.get("pruebas_asignadas",""),"fecha_entrevista":asig.get("fecha_entrevista",""),
                        "recomendacion":recomendacion_por_score(total_sc),"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    if total_sc>=90: st.success(f"✅ {total_sc}% - PERSONAL APTO 90%+")
                    elif total_sc>=70: st.success(f"✅ {total_sc}% - APTO")
                    else: st.error(f"❌ {total_sc}% - NO APTO - {recomendacion_por_score(total_sc)}")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
