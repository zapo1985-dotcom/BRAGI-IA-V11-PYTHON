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
logo_html=f'<img src="data:image/png;base64,{bg}" style="width:60px;height:60px;border-radius:14px;background:white;padding:3px;object-fit:contain">' if bg else "🛡️"

st.set_page_config(page_title="BRAGI-IA", page_icon=LOGO if os.path.exists(LOGO) else "🛡️", layout="wide")

st.markdown(f"""
<style>
.stApp{{background:#E8F5E9}}
.header{{background:#2D5A4A;padding:12px 24px;display:flex;align-items:center;gap:12px;margin:-60px -80px 12px -80px;box-shadow:0 4px 12px rgba(0,0,0,0.08)}}
.header h1{{color:white;font-size:19px;font-weight:900;margin:0}}
.card{{background:white;padding:20px;border-radius:18px;box-shadow:0 6px 18px rgba(45,90,74,0.08);margin:8px 0;border:1px solid #E8F5E9}}
.watermark{{position:fixed;top:32%;left:-10%;transform:rotate(-24deg);font-size:20px;color:rgba(45,90,74,0.05);font-weight:900;pointer-events:none;width:250%}}
[data-testid="stSidebar"]{{background:white;border-right:1px solid #D1E7DD;box-shadow:4px 0 20px rgba(0,0,0,0.05)}}
[data-testid="stSidebar"] *{{color:#1F2937}}
div[data-testid="stSidebar"] input{{background:#F6FBF7!important;color:#111!important;border-radius:12px!important;border:1.5px solid #D1E7DD!important}}
div[data-testid="stExpander"]{{background:#F6FBF7!important;border:1px solid #E8F5E9!important;border-radius:12px!important;margin:6px 0}}
div[data-testid="stExpander"] summary{{color:#2D5A4A!important;font-weight:700}}
.sidebar-logo{{display:flex;flex-direction:column;align-items:center;padding:18px 0 12px 0;border-bottom:1.5px solid #E8F5E9;margin-bottom:8px}}
.cat-icon{{background:#D1E7DD;padding:6px;border-radius:8px;color:#2D5A4A}}
</style>
<div class="watermark">TALENTO INTELIGENTE • RR.HH • BRAGI-IA</div>
<div class="header">{logo_html}<h1>BRAGI-IA V18 • TALENTO INTELIGENTE • FONDO CLARO VERDE MODA • RR.HH</h1></div>
""", unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "view" not in st.session_state: st.session_state.view="Asignar"
if "plan_trabajo" not in st.session_state: st.session_state.plan_trabajo=[]
if "procesos" not in st.session_state: st.session_state.procesos=[]
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db={
        "aux_contable":{"nombre":"Auxiliar Contable","preguntas":[{"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0,"img":"💰"}]},
        "abogado":{"nombre":"Abogado Tutelas","preguntas":[{"q":"¿Término tutela?","opts":["10 días","1 año"],"ok":0,"img":"⚖️"}]},
        "quimico":{"nombre":"Químico Farmacéutico","preguntas":[{"q":"¿BPM?","opts":["Buenas Prácticas","Buen Pago"],"ok":0,"img":"🧪"}]},
    }

def gen_pdf(d):
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=letter)
    if os.path.exists(LOGO):
        try: c.drawImage(LOGO,35,730,width=45,height=45,mask='auto')
        except: pass
    c.setFont("Helvetica-Bold",11); c.setFillColor(HexColor("#2D5A4A")); c.drawString(90,750,"BRAGI-IA - TALENTO INTELIGENTE • RR.HH - CONFIDENCIAL")
    c.setFillColor(HexColor("#2D5A4A"),alpha=0.06); c.setFont("Helvetica-Bold",20); c.saveState(); c.translate(130,300); c.rotate(-24); c.drawString(0,0,"TALENTO INTELIGENTE • RR.HH • BRAGI-IA"); c.restoreState()
    c.setFillColor(HexColor("#000000")); c.setFont("Helvetica",10); y=700
    for k,v in d.items():
        if y<80: c.showPage(); y=700
        if k not in ["hv_text","score_num"]: c.drawString(40,y,f"{k}: {str(v)[:110]}"); y-=14
    c.showPage(); c.save(); buf.seek(0); return buf

# LOGIN UNICO CLARO
if st.session_state.rol is None:
    st.markdown(f'<div style="max-width:460px;margin:20px auto;background:white;padding:22px;border-radius:20px;text-align:center;box-shadow:0 10px 30px rgba(45,90,74,0.1);border:1px solid #D1E7DD"><div style="display:flex;justify-content:center">{logo_html}</div><h2 style="color:#2D5A4A;margin:8px 0 2px 0">BRAGI-IA</h2><p style="color:#9CAF88;font-size:12px;margin:0">TALENTO INTELIGENTE • RR.HH • BRAGI-IA</p></div>', unsafe_allow_html=True)
    st.markdown('<div style="max-width:460px;margin:0 auto;background:white;padding:24px;border-radius:20px;box-shadow:0 8px 24px rgba(0,0,0,0.06)">', unsafe_allow_html=True)
    tipo=st.radio("Acceso", ["👤 Candidato","💼 RRHH"], horizontal=True, label_visibility="collapsed")
    st.divider()
    if "Candidato" in tipo:
        ced=st.text_input("Cédula", placeholder="Ingresa tu cédula")
        if st.button("LOG IN", type="primary", use_container_width=True):
            if ced: st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    else:
        u=st.text_input("Usuario", placeholder="admin"); p=st.text_input("Clave", type="password", placeholder="admin123")
        if st.button("LOG IN", type="primary", use_container_width=True):
            if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
            else: st.error("admin / admin123")
    st.markdown('</div>', unsafe_allow_html=True); st.stop()

with st.sidebar:
    st.markdown(f'<div class="sidebar-logo"><div>{logo_html}</div><b style="color:#2D5A4A;margin-top:6px">TALENTO INTELIGENTE</b><span style="color:#6B7280;font-size:11px;letter-spacing:1px">RR.HH • BRAGI-IA</span></div>', unsafe_allow_html=True)
    search=st.text_input("search", placeholder="Buscar en el menú... 🔍", label_visibility="collapsed")
    s=search.lower() if search else ""
    def show(t): return s in t.lower() if s else True

    if show("gestion talento"):
        with st.expander("👥 Gestión de Talento", expanded=True):
            if st.button("📌 Asignar Pruebas", use_container_width=True): st.session_state.view="Asignar"; st.rerun()
            if st.button("👤 Ver Candidatos", use_container_width=True): st.session_state.view="Candidatos"; st.rerun()

    if show("cargos"):
        with st.expander("💼 Cargos", expanded=True):
            if st.button("➕ Adicionar Cargo Nuevo", use_container_width=True): st.session_state.view="AddCargo"; st.rerun()
            if st.button("📋 Ver Cargos", use_container_width=True): st.session_state.view="VerCargos"; st.rerun()

    if show("preguntas"):
        with st.expander("❓ Preguntas por Cargo", expanded=True):
            if st.button("➕ Adicionar Preguntas que se requiera", use_container_width=True): st.session_state.view="AddPreg"; st.rerun()

    if show("asignar"):
        with st.expander("📋 Asignar Pruebas", expanded=False):
            if st.button("📋 Ir a Asignar", use_container_width=True): st.session_state.view="Asignar"; st.rerun()

    if show("plan trabajo"):
        with st.expander("📅 Plan de Trabajo", expanded=True):
            if st.button("📅 Crear Plan", use_container_width=True): st.session_state.view="PlanTrabajo"; st.rerun()
            if st.button("📋 Ver Planes", use_container_width=True): st.session_state.view="VerPlanes"; st.rerun()

    if show("planeacion") or show("procesos"):
        with st.expander("🔄 Planeación de Procesos", expanded=True):
            if st.button("🔄 Nuevo Proceso", use_container_width=True): st.session_state.view="AddProceso"; st.rerun()
            if st.button("🔍 Ver Procesos", use_container_width=True): st.session_state.view="VerProcesos"; st.rerun()

    if show("informes"):
        with st.expander("📈 Informes", expanded=False):
            if st.button("📈 Generar Informes", use_container_width=True): st.session_state.view="Informes"; st.rerun()

    if show("historicos"):
        with st.expander("🕘 Históricos", expanded=False):
            if st.button("🕘 Ver Históricos", use_container_width=True): st.session_state.view="Historicos"; st.rerun()

    if show("dashboard"):
        with st.expander("📊 Dashboard RRHH"):
            if st.button("📊 Dashboard", use_container_width=True): st.session_state.view="Dash"; st.rerun()

    if show("psicologia"):
        with st.expander("🧠 Psicología Imágenes"):
            if st.button("🧠 Ver Tests", use_container_width=True): st.session_state.view="Psico"; st.rerun()

    st.divider()
    if st.button("Cerrar sesión", use_container_width=True): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="rrhh":
    v=st.session_state.view
    if v=="Asignar":
        st.markdown('<div class="card"><h3>📌 Asignar Pruebas</h3></div>', unsafe_allow_html=True)
        with st.form("asig"):
            c1,c2=st.columns(2)
            with c1: ced=st.text_input("Cédula*"); nom=st.text_input("Nombre*")
            with c2: cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"]); asig=st.text_input("Asignado por*", value="RRHH BRAGI-IA")
            if st.form_submit_button("✅ Asignar", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success("Asignado")

    elif v=="AddCargo":
        st.markdown('<div class="card"><h3>💼 Adicionar Cargos - SUB-VENTANA dentro de Cargos</h3></div>', unsafe_allow_html=True)
        with st.form("newc"):
            nid=st.text_input("ID*"); nnom=st.text_input("Nombre*")
            if st.form_submit_button("💾 Crear", type="primary"):
                if nid and nnom: st.session_state.cargos_db[nid]={"nombre":nnom,"preguntas":[]}; st.success("Creado")

    elif v=="AddPreg":
        st.markdown('<div class="card"><h3>❓ Adicionar Preguntas que se requiera - Dentro de Preguntas por Cargo</h3></div>', unsafe_allow_html=True)
        sel=st.selectbox("Cargo", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
        with st.form(f"ap_{sel}"):
            pq=st.text_area("Pregunta*"); o1=st.text_input("Correcta*"); o2=st.text_input("O2"); o3=st.text_input("O3")
            if st.form_submit_button("💾 Adicionar", type="primary"):
                if pq and o1: st.session_state.cargos_db[sel]["preguntas"].append({"q":pq,"opts":[o1,o2 or "B",o3 or "C"],"ok":0}); st.success("Adicionada")

    elif v=="PlanTrabajo":
        st.markdown('<div class="card"><h3>📅 Plan de Trabajo - Nuevo</h3></div>', unsafe_allow_html=True)
        with st.form("plan"):
            c1,c2=st.columns(2)
            with c1: titulo=st.text_input("Título*"); responsable=st.text_input("Responsable*"); ini=st.date_input("Inicio", value=date.today())
            with c2: cargo_rel=st.selectbox("Cargo", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"]); fin=st.date_input("Fin"); pri=st.selectbox("Prioridad", ["Alta","Media","Baja"])
            tareas=st.text_area("Tareas (una por línea)")
            if st.form_submit_button("💾 Guardar Plan", type="primary", use_container_width=True):
                st.session_state.plan_trabajo.append({"titulo":titulo,"responsable":responsable,"cargo_nombre":st.session_state.cargos_db[cargo_rel]["nombre"],"inicio":str(ini),"fin":str(fin),"prioridad":pri,"tareas":tareas,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"estado":"En Curso"}); st.success("Plan creado")

    elif v=="VerPlanes":
        st.markdown('<div class="card"><h3>📋 Planes de Trabajo</h3></div>', unsafe_allow_html=True)
        if st.session_state.plan_trabajo: st.dataframe(pd.DataFrame(st.session_state.plan_trabajo), use_container_width=True)
        else: st.info("Sin planes")

    elif v=="AddProceso":
        st.markdown('<div class="card"><h3>🔄 Planeación de Procesos - Nuevo</h3></div>', unsafe_allow_html=True)
        with st.form("proc"):
            nombre=st.text_input("Nombre Proceso*"); resp=st.text_input("Líder*"); etapas=st.text_area("Etapas*"); tiempo=st.text_input("Tiempo Estimado")
            if st.form_submit_button("💾 Guardar", type="primary", use_container_width=True):
                st.session_state.procesos.append({"nombre":nombre,"responsable":resp,"etapas":etapas,"tiempo":tiempo,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success("Guardado")

    elif v=="VerProcesos":
        st.markdown('<div class="card"><h3>🔍 Planeación de Procesos</h3></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.procesos), use_container_width=True)

    elif v=="Informes":
        st.markdown('<div class="card"><h3>📈 Informes</h3></div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Evaluados", len(st.session_state.resultados))
        with c2: st.metric("Planes", len(st.session_state.plan_trabajo))
        with c3: st.metric("Procesos", len(st.session_state.procesos))
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados); st.bar_chart(df["cargo_nombre"].value_counts()); st.dataframe(df, use_container_width=True)

    elif v=="Historicos":
        st.markdown('<div class="card"><h3>🕘 Históricos</h3></div>', unsafe_allow_html=True)
        t1,t2,t3=st.tabs(["Asignaciones","Resultados","Planes/Procesos"])
        with t1: st.dataframe(pd.DataFrame(st.session_state.asignaciones), use_container_width=True)
        with t2:
            if st.session_state.resultados:
                df=pd.DataFrame(st.session_state.resultados); st.dataframe(df, use_container_width=True)
                for i,r in enumerate(df.to_dict(orient="records")):
                    pdf=gen_pdf(r); st.download_button(f"🔒 PDF {r['cedula']} {r['score']}", pdf, f"HIST_{r['cedula']}.pdf","application/pdf", key=f"h_{i}")
        with t3:
            st.write("Planes"); st.dataframe(pd.DataFrame(st.session_state.plan_trabajo), use_container_width=True)
            st.write("Procesos"); st.dataframe(pd.DataFrame(st.session_state.procesos), use_container_width=True)

    elif v=="Dash":
        st.markdown('<div class="card"><h3>📊 Dashboard</h3></div>', unsafe_allow_html=True)
        if st.session_state.resultados: st.dataframe(pd.DataFrame(st.session_state.resultados), use_container_width=True)
        else: st.info("Sin resultados")

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual; mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis: st.error("Sin pruebas")
    else:
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig["cargo_key"])
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>{cargo["nombre"]}</h3></div>', unsafe_allow_html=True)
            with st.form(f"f{idx}"):
                resps=[]
                for i,pr in enumerate(cargo["preguntas"]):
                    st.write(f"**{i+1}. {pr['q']}**"); r=st.radio("Elige", pr["opts"], index=None, key=f"r{idx}_{i}"); resps.append(r)
                if st.form_submit_button("🚀 FINALIZAR", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]); tot=len(cargo["preguntas"]) or 1; sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig["nombre"],"cargo_nombre":cargo["nombre"],"asignado_por":asig["asignado_por"],"score":f"{sc}%","score_num":sc,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% Enviado")
