import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

st.set_page_config(page_title="BRAGI-IA V38 SIN VIDA UTIL", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

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
        {"ID":1,"Área":"Contabilidad","Cargo":"AUXILIAR CONTABLE"},
        {"ID":2,"Área":"Jurídica","Cargo":"ABOGADO TUTELAS PQR"},
        {"ID":3,"Área":"Farmacia","Cargo":"QUÍMICO FARMACÉUTICO"},
        {"ID":4,"Área":"Farmacia","Cargo":"REGENTE DE FARMACIA"},
    ]
if "preguntas" not in st.session_state: st.session_state.preguntas=[]
if "pruebas_psicologicas" not in st.session_state:
    st.session_state.pruebas_psicologicas=[
        {"ID":1,"Nombre":"16PF - Cattell","Tipo":"Personalidad","Área":"Jurídica","Cargo":"ABOGADO","Descripción":"16 factores"},
        {"ID":2,"Nombre":"DISC","Tipo":"Comportamiento","Área":"Contabilidad","Cargo":"AUXILIAR","Descripción":"DISC"},
        {"ID":3,"Nombre":"Wartegg","Tipo":"Proyectiva","Área":"Farmacia","Cargo":"REGENTE","Descripción":"Wartegg"},
        {"ID":4,"Nombre":"ICF IE","Tipo":"Emocional","Área":"Farmacia","Cargo":"QUÍMICO","Descripción":"IE"},
        {"ID":5,"Nombre":"Zavic","Tipo":"Valores","Área":"Jurídica","Cargo":"ABOGADO","Descripción":"Valores"},
        {"ID":6,"Nombre":"IPV","Tipo":"Comercial","Área":"Contabilidad","Cargo":"AUXILIAR","Descripción":"Ventas"},
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
    for kw in ["contabilidad","puc","derecho","tutela","farmacia","invima","medicamentos","experiencia"]:
        if kw in texto: score+=15
    return min(score,100)

def tabla_limpia(df, nombre):
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.write(f"Total: {len(df)}")
    buf=io.StringIO(); df.to_csv(buf, index=False)
    st.download_button(label="📥 Descargar como CSV", data=buf.getvalue(), file_name=f"{nombre}.csv", mime="text/csv", key=f"dl_{nombre}_{datetime.now().microsecond}")

if st.session_state.rol is None:
    st.markdown("<h2 style='text-align:center;color:black'>BRAGI-IA V38 - SIN VIDA ÚTIL</h2>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        org=st.selectbox("Organización", ["RRHH","INVITADO A PRUEBA"])
        if org=="RRHH":
            u=st.text_input("Usuario", placeholder="admin")
            p=st.text_input("Contraseña", type="password", placeholder="admin123")
            if st.button("LOG IN", type="primary", use_container_width=True):
                if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
                else: st.error("admin / admin123")
        else:
            ced=st.text_input("Cédula")
            if st.button("LOG IN Invitado", type="primary", use_container_width=True):
                if ced:
                    if not any(a.get("cedula")==ced for a in st.session_state.asignaciones):
                        st.session_state.asignaciones.append({"cedula":ced,"nombre":f"Invitado {ced}","cargo_key":"aux_contable","cargo_nombre":"Auxiliar Contable","area":"Contabilidad","pruebas_asignadas":"DISC","fecha_entrevista":str(date.today())})
                    st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with c2: st.success("V38 - Eliminado Vida Útil - Solo Área + Cargo")
    st.stop()

with st.sidebar:
    st.markdown("<h3 style='color:white!important'>BRAGI-IA V38</h3>", unsafe_allow_html=True)
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
        st.subheader("Dashboard")
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Entrevistas", len(st.session_state.asignaciones))
        c2.metric("Realizadas", len(st.session_state.resultados))
        c3.metric("Aptos", len([r for r in st.session_state.resultados if r.get("score_num",0)>=70]))
        c4.metric("No Aptos", len([r for r in st.session_state.resultados if r.get("score_num",0)<70]))
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            # Solo columnas que pediste
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área"] if c in df.columns]
            tabla_limpia(df[cols] if cols else df, "Dashboard")

    elif v=="CrearAreas":
        st.subheader("Lista de áreas - Crear áreas")
        st.write("**ELIMINADO Vida Útil - Solo dejamos Área + Cargo como pediste**")
        # Tabla existente sin Vida Util
        df_show=pd.DataFrame([{"ID":a.get("ID"),"Área":a.get("Área"),"Cargo":a.get("Cargo")} for a in st.session_state.areas])
        st.dataframe(df_show, use_container_width=True, hide_index=True)
        st.divider()
        with st.form("crear_areas_v38"):
            st.write("Nombre del submenú es crear áreas")
            area=st.text_input("Área *", placeholder="Ej: Contabilidad, Jurídica, Farmacia")
            cargo=st.text_input("Cargo *", placeholder="Ej: AUXILIAR CONTABLE")
            # VIDA UTIL ELIMINADO
            if st.form_submit_button("➕ Crear área", type="primary"):
                if area and cargo:
                    new_id=max([c.get("ID",0) for c in st.session_state.areas], default=0)+1
                    st.session_state.areas.append({"ID":new_id,"Área":area.upper(),"Cargo":cargo.upper()})
                    nid=cargo.lower().replace(" ","_")[:20]
                    st.session_state.cargos_db[nid]={"nombre":cargo,"area":area,"preguntas":[]}
                    st.success(f"Área {area.upper()} - Cargo {cargo.upper()} creado"); st.rerun()

    elif v=="CrearPreguntas":
        st.subheader("Crear preguntas y respuestas")
        st.write("Esto está bien - como dijiste en video")
        with st.form("preg_v38"):
            areas=list(set([c.get("Área","") for c in st.session_state.areas]))
            area_sel=st.selectbox("Área *", areas if areas else ["Contabilidad"])
            cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
            cargo_sel=st.selectbox("Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
            pregunta=st.text_area("Pregunta *")
            correcta=st.text_input("Respuesta Correcta *")
            opB=st.text_input("Opción B")
            opC=st.text_input("Opción C")
            if st.form_submit_button("➕ Crear pregunta", type="primary"):
                if pregunta and correcta:
                    st.session_state.preguntas.append({"ID":len(st.session_state.preguntas)+1,"Área":area_sel,"Cargo":cargo_sel,"Pregunta":pregunta,"Correcta":correcta})
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper(): v["preguntas"].append({"q":pregunta,"opts":[correcta,opB,opC],"ok":0}); break
                    st.success("Pregunta creada")
        if st.session_state.preguntas: tabla_limpia(pd.DataFrame(st.session_state.preguntas), "Preguntas")

    elif v=="HojaVidaIA":
        st.subheader("Análisis hoja de vida")
        with st.form("hv_v38"):
            ced=st.text_input("Cédula")
            area_sel=st.selectbox("Área", list(set([c.get("Área","") for c in st.session_state.areas])) if st.session_state.areas else ["Contabilidad"])
            cargo_sel=st.selectbox("Cargo", [c.get("Cargo","") for c in st.session_state.areas] if st.session_state.areas else ["AUXILIAR CONTABLE"])
            archivo=st.file_uploader("Cargar Hoja de Vida", type=["pdf","docx","txt"])
            texto_manual=st.text_area("Texto HV - Opcional")
            if st.form_submit_button("🧠 Analizar", type="primary"):
                texto=""
                if archivo:
                    try: texto=str(archivo.read().decode('utf-8', errors='ignore'))[:5000]
                    except: texto="Archivo"
                if texto_manual: texto+= " " + texto_manual
                score=analizar_hv_ia(texto or "Sin HV", cargo_sel)
                st.session_state.hojas_vida.append({"cedula":ced or "Opcional","área":area_sel,"cargo":cargo_sel,"score":score,"fecha":datetime.now().strftime("%Y-%m-%d")})
                st.success(f"{score}%")
        if st.session_state.hojas_vida: tabla_limpia(pd.DataFrame(st.session_state.hojas_vida), "Hoja_Vida")

    elif v=="CrearEntrevista":
        st.subheader("Crear entrevista")
        st.write("Asignación de entrevistas - Gran entrevista - como está")
        with st.form("ent_v38"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula *")
                nom=st.text_input("Nombre *")
                fecha_ent=st.date_input("Fecha *", value=date.today())
                hora=st.time_input("Hora")
            with c2:
                areas=list(set([c.get("Área","") for c in st.session_state.areas]))
                area_sel=st.selectbox("Área *", areas if areas else ["Contabilidad"])
                cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
                cargo_sel=st.selectbox("Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
                st.write("Pruebas psicológicas (chuleta):")
                sel=[]
                for n in [p.get("Nombre","") for p in st.session_state.pruebas_psicologicas]:
                    if st.checkbox(n, key=f"chk_{n}"): sel.append(n)
            if st.form_submit_button("📌 Crear entrevista", type="primary", use_container_width=True):
                if ced and nom:
                    cargo_key=list(st.session_state.cargos_db.keys())[0]
                    for k,v in st.session_state.cargos_db.items():
                        if v.get("nombre","").upper() in cargo_sel.upper(): cargo_key=k; break
                    if not sel: sel=["DISC"]
                    st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"área":area_sel,"cargo_nombre":cargo_sel,"cargo_key":cargo_key,"pruebas":", ".join(sel),"fecha_entrevista":str(fecha_ent),"hora":str(hora),"fecha_creacion":str(fecha_ent)})
                    st.success(f"Entrevista {nom} - {area_sel} - {cargo_sel}")

    elif v=="ListaEntrevistas":
        st.subheader("Asignación de entrevista - Entrevistas creadas")
        if st.session_state.asignaciones:
            df=pd.DataFrame(st.session_state.asignaciones)
            cols=[c for c in ["nombre","cedula","área","cargo_nombre","fecha_entrevista"] if c in df.columns]
            tabla_limpia(df[cols] if cols else df, "Entrevistas_Creadas")
        else: st.info("Sin entrevistas")

    elif v=="CrearPruebaPsi":
        st.subheader("Área psicológica - Crear prueba psicológica")
        st.write("Área jurídica, el cargo la descripción - como pediste")
        with st.form("psi_v38"):
            areas=list(set([c.get("Área","") for c in st.session_state.areas]))
            area_sel=st.selectbox("Área *", areas if areas else ["Jurídica"], help="Ej: Jurídica")
            cargos=[c.get("Cargo","") for c in st.session_state.areas if c.get("Área","")==area_sel]
            cargo_sel=st.selectbox("Cargo *", cargos if cargos else ["AUXILIAR CONTABLE"])
            st.write("Tipo de prueba - Chuleta:")
            sel=[]
            if st.checkbox("16PF - Cattell"): sel.append("16PF")
            if st.checkbox("DISC"): sel.append("DISC")
            if st.checkbox("Wartegg"): sel.append("Wartegg")
            if st.checkbox("ICF IE"): sel.append("ICF IE")
            if st.checkbox("Zavic Valores"): sel.append("Zavic")
            if st.checkbox("IPV Ventas"): sel.append("IPV")
            otro=st.text_input("Otra")
            if otro: sel.append(otro.upper())
            desc=st.text_area("Descripción")
            if st.form_submit_button("➕ Crear prueba psicológica", type="primary"):
                if not sel: sel=["DISC"]
                for pr in sel:
                    nid=max([p.get("ID",0) for p in st.session_state.pruebas_psicologicas], default=0)+1
                    st.session_state.pruebas_psicologicas.append({"ID":nid,"Nombre":pr,"Área":area_sel,"Cargo":cargo_sel,"Descripción":desc})
                st.success(f"Pruebas {', '.join(sel)} para Área {area_sel} - Cargo {cargo_sel}")

    elif v=="ResultadosPsi":
        st.subheader("Resultado de prueba psicológica")
        st.write("**Nombre de la persona, cédula, fecha, y cargo al que se presentó - como pediste video 3**")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            # Columnas exactas que pediste
            cols_pedidas=[]
            for c in ["nombre","cedula","fecha","cargo_nombre","área","area","fecha_entrevista"]:
                if c in df.columns: cols_pedidas.append(c)
            # Orden: nombre, cedula, fecha, cargo
            orden=["nombre","cedula","fecha","cargo_nombre","área"]
            cols_orden=[c for c in orden if c in cols_pedidas]
            df_simple=df[cols_orden] if cols_orden else df
            st.write("Usuarios que realizaron pruebas:")
            cedulas=df["cedula"].unique().tolist() if "cedula" in df.columns else []
            sel_ceds=[]
            ccols=st.columns(3)
            for i, ced in enumerate(cedulas):
                with ccols[i%3]:
                    nom=df[df["cedula"]==ced]["nombre"].iloc[0] if "nombre" in df.columns else ced
                    if st.checkbox(f"{nom} - {ced}", key=f"u_{ced}", value=True): sel_ceds.append(ced)
            if sel_ceds:
                df_f=df[df["cedula"].isin(sel_ceds)] if "cedula" in df.columns else df
                df_fs=df_f[cols_orden] if cols_orden else df_f
                st.dataframe(df_fs, use_container_width=True, hide_index=True)
                buf=io.StringIO(); df_fs.to_csv(buf, index=False)
                st.download_button(label="📥 Descargar como CSV", data=buf.getvalue(), file_name="Resultado_Pruebas.csv", mime="text/csv")
            st.divider()
            st.write("Pruebas psicológicas disponibles")
            tabla_limpia(pd.DataFrame(st.session_state.pruebas_psicologicas)[["ID","Nombre","Área","Cargo"]], "Pruebas_Disponibles")
        else:
            st.info("Sin usuarios que hayan realizado pruebas")
            st.write("Pruebas psicológicas disponibles")
            tabla_limpia(pd.DataFrame(st.session_state.pruebas_psicologicas)[["ID","Nombre","Tipo"]], "Pruebas_Disponibles")

    elif v=="PlanTrabajo":
        st.subheader("Plan de trabajo")
        if st.session_state.asignaciones:
            df=pd.DataFrame(st.session_state.asignaciones)
            cols=[c for c in ["nombre","cedula","área","cargo_nombre","fecha_entrevista"] if c in df.columns]
            tabla_limpia(df[cols] if cols else df, "Plan_Trabajo")
        else: st.info("Sin programadas")

    elif v=="ReporteRealizadas":
        st.subheader("Entrevistas programadas")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área"] if c in df.columns]
            tabla_limpia(df[cols] if cols else df, "Entrevistas_Programadas")
        else: st.info("Sin datos")

    elif v=="ReporteRechazadas":
        st.subheader("Entrevistas rechazadas")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área"] if c in df.columns]
            rech=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not rech.empty: tabla_limpia(rech[cols] if cols else rech, "Entrevistas_Rechazadas")
            else: st.info("Sin rechazadas")
        else: st.info("Sin datos")

    elif v=="Historicos":
        st.subheader("Históricos")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área"] if c in df.columns]
            tabla_limpia(df[cols] if cols else df, "Historicos")
        else: st.info("Sin históricos")

    elif v=="PersonalApto":
        st.subheader("Personal apto")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área","score"] if c in df.columns]
            aptos=df[df["score_num"]>=70] if "score_num" in df.columns else df
            if not aptos.empty: tabla_limpia(aptos[cols] if cols else aptos, "Personal_APTO")
        else: st.info("Sin datos")

    elif v=="NoAptos":
        st.subheader("No aptos")
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            cols=[c for c in ["nombre","cedula","fecha","cargo_nombre","área","score"] if c in df.columns]
            noa=df[df["score_num"]<70] if "score_num" in df.columns else pd.DataFrame()
            if not noa.empty: tabla_limpia(noa[cols] if cols else noa, "Personal_NO_APTO")
            else: st.success("No hay No Aptos")
        else: st.info("Sin datos")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a.get("cedula")==ced]
    if not mis: st.error("Sin entrevistas asignadas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig.get("cargo_key"))
            if not cargo: continue
            st.subheader(f"{ced} - {cargo['nombre']} - Área: {asig.get('área','')} - Fecha: {asig.get('fecha_entrevista','')}")
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo.get("preguntas",[])):
                    st.write(f"{i+1}. {pr['q']}")
                    r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}")
                    resps.append(r)
                st.write(f"Pruebas: {asig.get('pruebas','')}")
                if st.form_submit_button("🚀 FINALIZAR", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]) if cargo.get("preguntas") else 0
                    tot=len(cargo.get("preguntas",[])) or 1
                    sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig.get("nombre",ced),"cargo_nombre":cargo["nombre"],"área":asig.get("área",""),"area":asig.get("área",""),"score":f"{sc}%","score_num":sc,"fecha":asig.get("fecha_entrevista",""),"fecha_entrevista":asig.get("fecha_entrevista","")})
                    st.balloons(); st.success(f"✅ {sc}% - Finalizado")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
