import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

st.set_page_config(page_title="BRAGI-IA V36 AREAS LIMPIO", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

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
div[data-testid="stTextInput"] > div, div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, div[data-testid="stNumberInput"] > div, div[data-testid="stDateInput"] > div{
    background:white!important;border:1.5px solid #C8E6C9!important;border-radius:12px!important;
}
input, textarea{color:black!important;font-weight:600!important;background:white!important}
h1,h2,h3,p,label{color:black!important}
div[data-testid="stDataFrame"] *{color:black!important}
</style>
""", unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "hojas_vida" not in st.session_state: st.session_state.hojas_vida=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="CrearAreas"
if "areas" not in st.session_state:
    st.session_state.areas=[
        {"ID":1,"Área":"Contabilidad","Cargo":"AUXILIAR CONTABLE","Vida Util":"VU 1 AÑO"},
        {"ID":2,"Área":"Jurídica","Cargo":"ABOGADO TUTELAS PQR","Vida Util":"VU 1 AÑO"},
        {"ID":3,"Área":"Farmacia","Cargo":"QUÍMICO FARMACÉUTICO","Vida Util":"VU 1 AÑO"},
        {"ID":4,"Área":"Farmacia","Cargo":"REGENTE DE FARMACIA","Vida Util":"VU 1 AÑO"},
    ]
if "preguntas" not in st.session_state: st.session_state.preguntas=[]
if "pruebas_psicologicas" not in st.session_state:
    st.session_state.pruebas_psicologicas=[
        {"ID":1,"Nombre":"16PF","Tipo":"Personalidad"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva"},
        {"ID":4,"Nombre":"ICF IE","Tipo":"Emocional"},
        {"ID":5,"Nombre":"Zavic","Tipo":"Valores"},
        {"ID":6,"Nombre":"IPV","Tipo":"Comercial"},
    ]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","area":"Contabilidad","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0}]},
        "abogado":{"nombre":"Abogado Tutelas PQR","area":"Jurídica","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año","30 días"],"ok":0}]},
        "quimico":{"nombre":"Químico Farmacéutico","area":"Farmacia","preguntas":[{"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago","Almacenamiento"],"ok":0}]},
        "regente":{"nombre":"Regente de Farmacia","area":"Farmacia","preguntas":[{"q":"¿Qué es dispensación?","opts":["Entrega informada de medicamentos","Venta libre","Almacenamiento"],"ok":0}]},
    }

def analizar_hv_ia(texto, cargo):
    texto=texto.lower(); score=0
    for kw in ["contabilidad","puc","excel","derecho","tutela","farmacia","invima","medicamentos","experiencia","universidad","años"]:
        if kw in texto: score+=12
    score=min(score,100)
    return score, "APTO" if score>=70 else "NO APTO", "Recomendación según score"

def recomendacion_por_score(sc):
    if sc>=90: return f"APTO 90%+ - {sc}% - CONTRATAR"
    elif sc>=70: return f"APTO - {sc}% - CONTRATAR"
    else: return f"NO APTO - {sc}% - NO CONTRATAR"

def tabla_con_descarga_limpia(df, nombre_archivo):
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.write(f"Total: {len(df)}")
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(label=f"📥 Descargar como CSV", data=csv_buffer.getvalue(), file_name=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", key=f"dl_{nombre_archivo}_{datetime.now().microsecond}")

# LOGIN
if st.session_state.rol is None:
    st.markdown("<h2 style='text-align:center;color:black'>BRAGI-IA V36 - ÁREAS LIMPIO</h2>", unsafe_allow_html=True)
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
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","area":"Contabilidad","pruebas_asignadas":"DISC","fecha_creacion":datetime.now().strftime("%Y-%m-%d")})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with c2:
        st.success("V36 - Limpio sin textos azules largos")
    st.stop()

with st.sidebar:
    st.markdown("<h3 style='color:white!important'>BRAGI-IA V36</h3><p style='color:#B2DFDB!important;font-size:11px;margin-top:-10px'>ÁREAS LIMPIO</p>", unsafe_allow_html=True)

    with st.expander("● LISTA DE ÁREAS", expanded=True):
        if st.button("➕ Crear áreas", use_container_width=True): st.session_state.view="CrearAreas"; st.rerun()
        if st.button("❓ Crear preguntas y respuestas", use_container_width=True): st.session_state.view="CrearPreguntas"; st.rerun()
        if st.button("📄 Análisis hoja de vida", use_container_width=True): st.session_state.view="HojaVidaIA"; st.rerun()

    with st.expander("● ASIGNACIÓN DE ENTREVISTA", expanded=True):
        if st.button("📌 Crear entrevista", use_container_width=True): st.session_state.view="CrearEntrevista"; st.rerun()
        if st.button("📋 Entrevistas creadas", use_container_width=True): st.session_state.view="ListaEntrevistas"; st.rerun()

    with st.expander("● ÁREA PSICOLÓGICA", expanded=True):
        if st.button("➕ Crear prueba psicológica", use_container_width=True): st.session_state.view="CrearPruebaPsi"; st.rerun()
        if st.button("📊 Resultado de prueba psicológica", use_container_width=True): st.session_state.view="ResultadosPsi"; st.rerun()

    with st.expander("● INFORMES", expanded=True):
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dashboard"; st.rerun()
        if st.button("🗓️ Plan de trabajo", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
        if st.button("✅ Entrevistas programadas", use_container_width=True): st.session_state.view="ReporteRealizadas"; st.rerun()
        if st.button("❌ Entrevistas rechazadas", use_container_width=True): st.session_state.view="ReporteRechazadas"; st.rerun()
        if st.button("🕘 Históricos", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    with st.expander("● PERSONAL APTO", expanded=True):
        if st.button("✅ Personal apto", use_container_width=True): st.session_state.view="PersonalApto"; st.rerun()

    with st.expander("● NO APTOS", expanded=True):
        if st.button("❌ No aptos", use_container_width=True): st.session_state.view="NoAptos"; st.rerun()

    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view

    if v=="Dashboard":
        st.subheader("● INFORMES - Dashboard")
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("Entrevistas", len(st.session_state.asignaciones))
        c2.metric("Realizadas", len(st.session_state.resultados))
        c3.metric("HV IA", len(st.session_state.hojas_vida))
        c4.metric("Aptos 90%+", len([r for r in st.session_state.resultados if r.get("score_num",0)>=90]))
        c5.metric("No Aptos", len([r for r in st.session_state.resultados if r.get("score_num",0)<70]))
        if st.session_state.resultados:
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.resultados), "Dashboard")

    elif v=="CrearAreas":
        st.subheader("● LISTA DE ÁREAS - Crear áreas")
        st.write("Áreas existentes:")
        df_areas=pd.DataFrame(st.session_state.areas)
        tabla_con_descarga_limpia(df_areas, "Areas")
        st.divider()
        with st.form("crear_areas_v36"):
            st.write("**Nombre del submenú es crear áreas - como pediste**")
            area=st.text_input("Área *", placeholder="Ej: Contabilidad, Jurídica, Farmacia")
            cargo=st.text_input("Cargo *", placeholder="Ej: AUXILIAR CONTABLE")
            vida=st.text_input("Vida Útil", value="VU 1 AÑO")
            if st.form_submit_button("➕ Crear área", type="primary"):
                if area and cargo:
                    new_id=max([c.get("ID",0) for c in st.session_state.areas], default=0)+1
                    st.session_state.areas.append({"ID":new_id,"Área":area.upper(),"Cargo":cargo.upper(),"Vida Util":vida})
                    nid=cargo.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":cargo,"area":area,"preguntas":[]}
                    st.success(f"Área {area.upper()} - Cargo {cargo.upper()} creado"); st.rerun()

    elif v=="CrearPreguntas":
        st.subheader("● LISTA DE ÁREAS - Crear preguntas y respuestas")
        with st.form("crear_preg_v36"):
            areas=list(set([c.get("Área","") for c in st.session_state.areas]))
            area_sel=st.selectbox("Área *", areas if areas else ["Contabilidad"])
            cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
            cargo_sel=st.selectbox("Cargo *", cargos if cargos else [c.get("Cargo","") for c in st.session_state.areas])
            pregunta=st.text_area("Pregunta *")
            correcta=st.text_input("Respuesta Correcta *")
            opB=st.text_input("Opción B")
            opC=st.text_input("Opción C")
            if st.form_submit_button("➕ Crear pregunta", type="primary"):
                if pregunta and correcta:
                    st.session_state.preguntas.append({"ID":len(st.session_state.preguntas)+1,"Área":area_sel,"Cargo":cargo_sel,"Pregunta":pregunta,"Respuesta Correcta":correcta,"Opción B":opB,"Opción C":opC})
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper():
                            v["preguntas"].append({"q":pregunta,"opts":[correcta,opB,opC],"ok":0}); break
                    st.success("Pregunta creada")
        if st.session_state.preguntas:
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.preguntas), "Preguntas")

    elif v=="HojaVidaIA":
        st.subheader("● LISTA DE ÁREAS - Análisis hoja de vida")
        st.write("Opcional")
        with st.form("hv_ia_v36"):
            ced=st.text_input("Cédula (opcional)")
            area_sel=st.selectbox("Área", list(set([c.get("Área","") for c in st.session_state.areas])) if st.session_state.areas else ["Contabilidad"])
            cargo_sel=st.selectbox("Cargo a evaluar", [c.get("Cargo","") for c in st.session_state.areas] if st.session_state.areas else ["AUXILIAR CONTABLE"])
            archivo=st.file_uploader("Cargar Hoja de Vida", type=["pdf","docx","txt"])
            texto_manual=st.text_area("Texto HV - Opcional")
            if st.form_submit_button("🧠 Analizar", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo"
                if texto_manual: texto+= " " + texto_manual
                if not texto: texto="Sin HV"
                score, concepto, mejora = analizar_hv_ia(texto, cargo_sel)
                st.session_state.hojas_vida.append({"cedula":ced or "Opcional","área":area_sel,"cargo":cargo_sel,"score_ia":score,"concepto":concepto,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"✅ {score}% - {concepto}")
        if st.session_state.hojas_vida:
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.hojas_vida), "Hoja_Vida")

    elif v=="CrearEntrevista":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Crear entrevista")
        with st.form("crear_ent_v36"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula *")
                nom=st.text_input("Nombre *")
                fecha_ent=st.date_input("Fecha *", value=date.today())
                hora_ent=st.time_input("Hora")
            with c2:
                areas=list(set([c.get("Área","") for c in st.session_state.areas]))
                area_sel=st.selectbox("Área *", areas if areas else ["Contabilidad"])
                cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
                cargo_sel=st.selectbox("Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
                st.write("Pruebas psicológicas (chuleta):")
                pruebas_sel=[]
                for nombre in [p.get("Nombre","") for p in st.session_state.pruebas_psicologicas]:
                    if st.checkbox(nombre, key=f"chk_v36_{nombre}"):
                        pruebas_sel.append(nombre)
            if st.form_submit_button("📌 Crear entrevista", type="primary", use_container_width=True):
                if ced and nom:
                    cargo_key=list(st.session_state.cargos_db.keys())[0]
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper() or cargo_sel.upper() in v.get("nombre","").upper(): cargo_key=k; break
                    if not pruebas_sel: pruebas_sel=["DISC"]
                    st.session_state.asignaciones.append({
                        "cedula":ced,"nombre":nom,"área":area_sel,"cargo_key":cargo_key,"cargo_nombre":cargo_sel,
                        "pruebas_asignadas":", ".join(pruebas_sel),"fecha_entrevista":str(fecha_ent),"hora":str(hora_ent),
                        "fecha_creacion":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success(f"Entrevista creada: {nom} - {area_sel} - {cargo_sel}")

    elif v=="ListaEntrevistas":
        st.subheader("● ASIGNACIÓN DE ENTREVISTA - Entrevistas creadas")
        if st.session_state.asignaciones:
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.asignaciones), "Entrevistas_Creadas")
        else: st.info("Sin entrevistas")

    elif v=="CrearPruebaPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Crear prueba psicológica")
        with st.form("crear_psi_v36"):
            areas=list(set([c.get("Área","") for c in st.session_state.areas]))
            area_sel=st.selectbox("Área *", areas if areas else ["Contabilidad"])
            cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
            cargo_sel=st.selectbox("Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
            st.write("**Tipo de prueba - Chuleta:**")
            check_16pf = st.checkbox("16PF - Cattell")
            check_disc = st.checkbox("DISC")
            check_wartegg = st.checkbox("Wartegg")
            check_icf = st.checkbox("ICF IE")
            check_zavic = st.checkbox("Zavic Valores")
            check_ipv = st.checkbox("IPV Ventas")
            nombre_pers=st.text_input("Otra prueba personalizada")
            desc=st.text_area("Descripción")
            if st.form_submit_button("➕ Crear prueba", type="primary"):
                pruebas_creadas=[]
                if check_16pf: pruebas_creadas.append("16PF")
                if check_disc: pruebas_creadas.append("DISC")
                if check_wartegg: pruebas_creadas.append("Wartegg")
                if check_icf: pruebas_creadas.append("ICF IE")
                if check_zavic: pruebas_creadas.append("Zavic")
                if check_ipv: pruebas_creadas.append("IPV")
                if nombre_pers: pruebas_creadas.append(nombre_pers.upper())
                if not pruebas_creadas: pruebas_creadas=["DISC"]
                for prueba in pruebas_creadas:
                    new_id=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":new_id,"Nombre":prueba,"Área":area_sel,"Cargo":cargo_sel,"Descripción":desc})
                st.success(f"Pruebas {', '.join(pruebas_creadas)} para {area_sel} - {cargo_sel}")

    elif v=="ResultadosPsi":
        st.subheader("● ÁREA PSICOLÓGICA - Resultado de prueba psicológica")
        st.write("Nombre del paciente, cédula, área que se presentó y fecha - como pediste en video 3")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            # Mostrar solo columnas que pediste
            cols_mostrar=[]
            for col in ["nombre","cedula","área","area","cargo_nombre","cargo","fecha_entrevista","fecha"]:
                if col in df.columns: cols_mostrar.append(col)
            if cols_mostrar:
                df_simple=df[cols_mostrar].copy()
                st.write("**Usuarios que realizaron las pruebas:**")
                # Chuleta para seleccionar
                cedulas=df["cedula"].unique().tolist() if "cedula" in df.columns else []
                seleccionados=[]
                ccols=st.columns(3)
                for i, ced in enumerate(cedulas):
                    with ccols[i%3]:
                        nom=df[df["cedula"]==ced]["nombre"].iloc[0] if "nombre" in df.columns and len(df[df["cedula"]==ced])>0 else ced
                        if st.checkbox(f"{nom} - {ced}", key=f"user_v36_{ced}", value=True):
                            seleccionados.append(ced)
                if seleccionados:
                    df_filtrado=df[df["cedula"].isin(seleccionados)] if "cedula" in df.columns else df
                    df_filtrado_simple=df_filtrado[cols_mostrar] if cols_mostrar else df_filtrado
                    st.dataframe(df_filtrado_simple, use_container_width=True, hide_index=True)
                    csv_buffer = io.StringIO()
                    df_filtrado_simple.to_csv(csv_buffer, index=False)
                    st.download_button(label="📥 Descargar como CSV", data=csv_buffer.getvalue(), file_name="Resultado_Pruebas.csv", mime="text/csv")
                st.divider()
                st.write("**Todos los resultados:**")
                tabla_con_descarga_limpia(df_simple, "Resultado_Pruebas_Todos")
        else:
            st.info("Sin usuarios que hayan realizado pruebas")
        if st.session_state.pruebas_psicologicas:
            st.subheader("Pruebas psicológicas disponibles")
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.pruebas_psicologicas), "Pruebas_Disponibles")

    elif v=="PlanTrabajo":
        st.subheader("● INFORMES - Plan de trabajo")
        if st.session_state.asignaciones:
            df=pd.DataFrame(st.session_state.asignaciones)
            # Mostrar solo columnas útiles
            tabla_con_descarga_limpia(df, "Plan_Trabajo")
        else: st.info("Sin programadas")

    elif v=="ReporteRealizadas":
        st.subheader("● INFORMES - Entrevistas programadas")
        if st.session_state.resultados:
            tabla_con_descarga_limpia(pd.DataFrame(st.session_state.resultados), "Entrevistas_Programadas")
        else: st.info("Sin datos")

    elif v=="ReporteRechazadas":
        st.subheader("● INFORMES - Entrevistas rechazadas")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            rech=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not rech.empty: tabla_con_descarga_limpia(rech, "Entrevistas_Rechazadas")
            else: st.success("No hay rechazadas")
        else: st.info("Sin datos")

    elif v=="Historicos":
        st.subheader("● INFORMES - Históricos")
        if st.session_state.resultados: tabla_con_descarga_limpia(pd.DataFrame(st.session_state.resultados), "Historicos")
        else: st.info("Sin históricos")

    elif v=="PersonalApto":
        st.subheader("● PERSONAL APTO")
        st.write("Calificación de las pruebas y recomendaciones del personal que paso la entrevista con el 90% y que debe mejorar")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            aptos=df[df["score_num"]>=90] if "score_num" in df.columns else df
            if aptos.empty: aptos=df[df["score_num"]>=70] if "score_num" in df.columns else df
            if not aptos.empty:
                aptos["Recomendación"]=aptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                aptos["Debe Mejorar"]="Liderazgo, gestión tiempo, conocimientos avanzados"
                tabla_con_descarga_limpia(aptos, "Personal_APTO")
        else: st.info("Sin datos")

    elif v=="NoAptos":
        st.subheader("● NO APTOS")
        st.write("Personal que no paso por debajo de 70% y recomendación si se debe o no contratar y recomendaciones a mejorar")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            noaptos=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not noaptos.empty:
                noaptos["Recomendación"]=noaptos["score_num"].apply(lambda x: recomendacion_por_score(x))
                noaptos["Debe Mejorar"]="Capacitación técnica, experiencia, comprensión rol"
                tabla_con_descarga_limpia(noaptos, "Personal_NO_APTO")
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
            st.subheader(f"Entrevista - {ced} - {cargo['nombre']} - Área: {asig.get('área','')} - Fecha: {asig.get('fecha_entrevista','')}")
            hv_file=st.file_uploader("Cargar HV - OPCIONAL", type=["pdf","txt","docx"], key=f"hv_{idx}")
            hv_txt=st.text_area("Texto HV opcional", key=f"hvtxt_{idx}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"{i+1}. {pr['q']}")
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                st.write(f"**Pruebas: {asig.get('pruebas_asignadas','')}**")
                chk_dom=st.checkbox("Dominante", key=f"dom_{idx}")
                chk_inf=st.checkbox("Influyente", key=f"inf_{idx}")
                chk_est=st.checkbox("Estable", key=f"est_{idx}")
                chk_con=st.checkbox("Concienzudo", key=f"con_{idx}")
                if st.form_submit_button("🚀 FINALIZAR ENTREVISTA", type="primary", use_container_width=True):
                    texto_hv=""
                    if hv_file:
                        try: texto_hv=str(hv_file.read().decode('utf-8', errors='ignore'))[:3000]
                        except: texto_hv="Archivo HV"
                    if hv_txt: texto_hv+= " " + hv_txt
                    score_hv=0
                    if texto_hv:
                        score_hv, _, _ = analizar_hv_ia(texto_hv, cargo["nombre"])
                        st.session_state.hojas_vida.append({"cedula":ced,"cargo":cargo["nombre"],"score_ia":score_hv,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
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
                        "cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],"área":asig.get("área",""),"area":asig.get("área",""),
                        "score":f"{total_sc}%","score_num":total_sc,"psicologica":psi_str,
                        "pruebas_realizadas":asig.get("pruebas_asignadas",""),"fecha_entrevista":asig.get("fecha_entrevista",""),
                        "recomendacion":recomendacion_por_score(total_sc),"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success(f"✅ {total_sc}% - Finalizado")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
