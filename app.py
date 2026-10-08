import streamlit as st, os, base64, io
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

LOGO_PATH = "logo.png"
def get_logo_b64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None
b64 = get_logo_b64()
logo_html = f'<img src="data:image/png;base64,{b64}" style="width:54px;height:54px;border-radius:14px;background:white;padding:3px;object-fit:contain">' if b64 else "🛡️"
page_icon = LOGO_PATH if os.path.exists(LOGO_PATH) else "🛡️"

st.set_page_config(page_title="BRAGI-IA - Talento Inteligente", page_icon=page_icon, layout="wide")

st.markdown(f"""
<style>
.stApp{{background:#F2F3F4}}
.header{{background:#2D5A4A;padding:14px 28px;display:flex;align-items:center;gap:14px;margin:-60px -80px 20px -80px}}
.header h1{{color:white;font-size:26px;font-weight:900;margin:0}}
.card{{background:white;padding:22px;border-radius:20px;box-shadow:0 8px 20px rgba(0,0,0,0.06);margin:10px 0;position:relative;z-index:1}}
.card-login{{background:white;padding:28px;border-radius:22px;box-shadow:0 12px 30px rgba(0,0,0,0.08)}}
.watermark{{position:fixed;top:30%;left:-10%;transform:rotate(-24deg);font-size:22px;color:rgba(45,90,74,0.07);font-weight:900;pointer-events:none;width:250%;z-index:0}}
.progress-bar{{background:#E5E7EB;height:10px;border-radius:10px;overflow:hidden}}
.progress-fill{{background:#2D5A4A;height:10px}}
</style>
<div class="watermark">TALENTO INTELIGENTE • RR.HH • BRAGI-IA • TALENTO INTELIGENTE</div>
<div class="header">{logo_html}<h1>BRAGI-IA - TALENTO INTELIGENTE</h1></div>
""", unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db = {
        "aux_contable": {"nombre":"Auxiliar Contable","preguntas":[
            {"q":"¿Qué es PUC?","opts":["Plan Único de Cuentas","Pago Único Contable","Presupuesto"],"ok":0,"img":None},
            {"q":"Imagen: ¿Cuenta 1105 Caja?","opts":["Caja","Bancos","Clientes"],"ok":0,"img":"💰"},
            {"q":"¿Qué es retención en la fuente?","opts":["Anticipo de impuesto","Multa","Descuento comercial"],"ok":0,"img":None},
            {"q":"¿IVA?","opts":["Impuesto Valor Agregado","Impuesto Vivienda"],"ok":0,"img":None},
            {"q":"¿Balance general refleja?","opts":["Situación financiera a una fecha","Solo ingresos"],"ok":0,"img":None},
        ]},
        "abogado": {"nombre":"Abogado Tutelas PQR Contratación","preguntas":[
            {"q":"¿Término para fallar tutela?","opts":["10 días","1 año","6 meses"],"ok":0,"img":None},
            {"q":"Imagen contrato sin pólizas ¿Qué falta?","opts":["Garantías","Solo firma"],"ok":0,"img":"📄❌"},
            {"q":"Cláusula forma de pago debe tener","opts":["Objeto, plazo, valor, forma pago, garantías","Solo firma"],"ok":0,"img":None},
            {"q":"¿SECOP II?","opts":["Sistema Electrónico Contratación Pública","Red social"],"ok":0,"img":None},
            {"q":"Debido proceso sanción contratista","opts":["Citar, descargos, pruebas, decisión","Sanción directa"],"ok":0,"img":None},
        ]},
        "quimico_farma": {"nombre":"Químico Farmacéutico","preguntas":[
            {"q":"¿BPM según INVIMA?","opts":["Buenas Prácticas Manufactura","Buen Pago Mensual"],"ok":0,"img":None},
            {"q":"Imagen cadena frío 2-8°C","opts":["Mantener 2-8°C y monitorear","Congelar todo"],"ok":0,"img":"🧊🌡️"},
            {"q":"¿Farmacovigilancia?","opts":["Detectar efectos adversos","Vender más"],"ok":0,"img":None},
            {"q":"¿Decreto 677?","opts":["Registro sanitario","Tránsito"],"ok":0,"img":None},
            {"q":"¿Trazabilidad por lote?","opts":["Seguir desde fabricación hasta dispensación","Solo número"],"ok":0,"img":None},
        ]},
    }

PSICO = [
    {"q":"Cuando ves esta imagen ¿qué percibes primero?","img":"🌳👄🌱","opts":["Labios - percibes realidad tal cual","Árboles - ambiciosa, ve adelante","Raíces - progresiva, mejora situación"]},
    {"q":"Elige la forma que más te atrae","img":"🔺 ⭕ ⬜","opts":["Triángulo - liderazgo y ambición","Círculo - amable, armonía","Cuadrado - orden, disciplina"]},
    {"q":"¿Qué ves en esta imagen abstracta?","img":"🐺 / 👤","opts":["Lobo - oportunista, trabaja en equipo","Rostro - observador, líder, analiza entorno"]},
    {"q":"Bajo presión ¿cómo reaccionas?","img":"😰","opts":["Mantengo calma y busco solución","Me bloqueo","Actúo rápido aunque con errores"]},
    {"q":"¿Prefieres trabajar?","img":"👥","opts":["En equipo colaborativo","Solo con autonomía","Liderando equipo"]},
]

def gen_pdf(dato):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=letter)
    if os.path.exists(LOGO_PATH):
        try: c.drawImage(LOGO_PATH, 35, 730, width=45, height=45, mask='auto')
        except: pass
    c.setFont("Helvetica-Bold", 11); c.setFillColor(HexColor("#2D5A4A"))
    c.drawString(90,750,"BRAGI-IA - TALENTO INTELIGENTE • RR.HH - CONFIDENCIAL SOLO RRHH")
    c.setFillColor(HexColor("#2D5A4A"), alpha=0.08); c.setFont("Helvetica-Bold", 22)
    c.saveState(); c.translate(140,300); c.rotate(-24); c.drawString(0,0,"TALENTO INTELIGENTE • RR.HH • BRAGI-IA"); c.restoreState()
    c.setFillColor(HexColor("#000000")); c.setFont("Helvetica", 10)
    y=700
    for k,v in dato.items():
        if y<80: c.showPage(); y=700
        if k not in ["hv_text","score_num"]:
            c.drawString(40,y,f"{k}: {str(v)[:110]}"); y-=16
    y-=12; c.setFont("Helvetica-Bold", 11)
    score=dato.get("score_num",0)
    rec="90% CONTRATAR - Altamente confiable" if score>=90 else "80% CONTRATAR CON MEJORAS" if score>=80 else "60-79% REGULAR - Segunda entrevista" if score>=60 else "0-59% NO CONTRATAR"
    c.drawString(40,y,rec)
    if dato.get("hv_text"):
        c.setFont("Helvetica",8); c.drawString(40,y-18,f"HV IA: {dato.get('hv_text')[:200]}")
    c.setFont("Helvetica",7); c.drawString(40,50,"Confidencial - Solo RRHH - BRAGI-IA V13 - Logo: Talento Inteligente RR.HH Bragi-IA")
    c.showPage(); c.save(); buf.seek(0); return buf

if st.session_state.rol is None:
    c1,c2=st.columns(2, gap="large")
    with c1:
        st.markdown(f'<div class="card-login"><div style="display:flex;gap:12px;align-items:center">{logo_html}<h2>👤 Candidato</h2></div><p style="color:#6B7280">Ingresa con cédula</p>', unsafe_allow_html=True)
        ced=st.text_input("Cédula", placeholder="Ingrese su cédula", label_visibility="collapsed", key="ced_final")
        hv_file=st.file_uploader("Subir Hoja de Vida (opcional) para análisis IA", type=["pdf"], key="hv_final")
        hv_text=""
        if hv_file:
            try:
                import fitz
                doc=fitz.open(stream=hv_file.read(), filetype="pdf")
                hv_text=" ".join([p.get_text() for p in doc])[:1000]
                st.success("HV cargada, IA la analizará")
            except:
                hv_text="HV cargada"; st.success("HV cargada")
        if st.button("Iniciar Sesión", type="primary", use_container_width=True):
            if ced:
                st.session_state.ced_actual=ced; st.session_state.hv_actual=hv_text; st.session_state.rol="candidato"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card-login"><div style="display:flex;gap:12px;align-items:center">{logo_html}<h2>💼 RRHH Admin</h2></div><p style="color:#6B7280">Solo RRHH ve PDF</p>', unsafe_allow_html=True)
        u=st.text_input("Usuario", placeholder="admin", label_visibility="collapsed", key="user_final")
        p=st.text_input("Clave", type="password", placeholder="••••••••", label_visibility="collapsed", key="pass_final")
        if st.button("Acceder", type="primary", use_container_width=True):
            if u=="admin" and p=="admin123": st.session_state.rol="rrhh"; st.rerun()
            else: st.error("Credenciales incorrectas")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#6B7280;font-size:11px;margin-top:18px">v13 • Inspirado en personality.co - 3 pasos: Prepárate / Completa 100 preguntas / Recibe insights • Logo TALENTO INTELIGENTE RR.HH BRAGI-IA dentro de runas</div>', unsafe_allow_html=True)
    st.stop()

if st.session_state.rol=="rrhh":
    t1,t2,t3,t4=st.tabs(["📌 Asignar Pruebas","⚙️ Tabla Cargos y Preguntas","📊 Dashboard PDF solo RRHH","📚 Psicología con Imágenes"])
    with t1:
        with st.form("asig_final"):
            c1,c2=st.columns(2)
            with c1: ced=st.text_input("Cédula*"); nom=st.text_input("Nombre*")
            with c2:
                cargo=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                asig=st.text_input("Asignado por*", value="Maria C. RRHH")
            if st.form_submit_button("✅ Asignar", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo,"cargo_nombre":st.session_state.cargos_db[cargo]["nombre"],"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Asignado {nom} - {cargo}")
    with t2:
        st.markdown('<div class="card"><h3>Tabla editable - incorpora cargos y preguntas según cargo</h3><p>Agrega filas, edita, borra - como Excel</p></div>', unsafe_allow_html=True)
        df_cargos=pd.DataFrame([{"ID":k,"Nombre":v["nombre"],"Preguntas":len(v["preguntas"])} for k,v in st.session_state.cargos_db.items()])
        ed=st.data_editor(df_cargos, num_rows="dynamic", use_container_width=True, key="ed_cargos_final")
        if st.button("💾 Guardar cargos"):
            for _,r in ed.iterrows():
                if r["ID"] in st.session_state.cargos_db: st.session_state.cargos_db[r["ID"]]["nombre"]=r["Nombre"]
            st.success("Guardado")
        sel=st.selectbox("Cargo para editar preguntas", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"], key="sel_final")
        df_p=pd.DataFrame([{"Pregunta":p["q"],"Correcta":p["opts"][0],"O2":p["opts"][1] if len(p["opts"])>1 else "","O3":p["opts"][2] if len(p["opts"])>2 else "","Imagen/Emoji":p.get("img","")} for p in st.session_state.cargos_db[sel]["preguntas"]])
        ed2=st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key=f"ed_{sel}_final")
        if st.button("💾 Guardar preguntas de este cargo"):
            st.session_state.cargos_db[sel]["preguntas"]=[{"q":r["Pregunta"],"opts":[r["Correcta"],r["O2"],r["O3"]],"ok":0,"img":r["Imagen/Emoji"]} for _,r in ed2.iterrows() if r["Pregunta"]]
            st.success("Guardado"); st.rerun()
        with st.expander("➕ Crear nuevo cargo vacío"):
            nid=st.text_input("ID sin espacios ej: aux_logistica"); nnom=st.text_input("Nombre cargo ej: Auxiliar Logística")
            if st.button("Crear cargo nuevo"):
                if nid and nnom: st.session_state.cargos_db[nid]={"nombre":nnom,"preguntas":[]}; st.success("Creado"); st.rerun()
    with t3:
        st.markdown('<div class="card"><h3>Dashboard - PDF solo lo ve RRHH</h3></div>', unsafe_allow_html=True)
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            c1,c2,c3,c4=st.columns(4)
            with c1: st.metric("Total", len(df))
            with c2: st.metric("Promedio", f"{df['score_num'].mean():.1f}%")
            with c3: st.metric(">=80%", len(df[df["score_num"]>=80]))
            with c4: st.metric(">=90%", len(df[df["score_num"]>=90]))
            st.bar_chart(df["cargo_nombre"].value_counts())
            st.dataframe(df, use_container_width=True)
            for i,r in enumerate(df.to_dict(orient="records")):
                pdf=gen_pdf(r)
                st.download_button(f"🔒 PDF CONFIDENCIAL SOLO RRHH {r['cedula']} {r['cargo_nombre']} {r['score']}", pdf, f"CONFIDENCIAL_RRHH_{r['cedula']}.pdf", "application/pdf", key=f"pdf_{i}")
        else: st.info("Sin resultados aún")
    with t4:
        st.markdown('<div class="card"><h3>📚 Psicología con imágenes estilo personality.co</h3><p>How it works personality.co: 1 Prepárate lugar tranquilo 2 Completa 100 preguntas con imágenes 3 Recibe reporte con fortalezas, retos, certificado</p></div>', unsafe_allow_html=True)
        for ps in PSICO: st.markdown(f'<div class="card"><div style="font-size:36px">{ps["img"]}</div><b>{ps["q"]}</b><br>{ps["opts"]}</div>', unsafe_allow_html=True)
    if st.button("Cerrar sesión RRHH"): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis: st.error(f"Cédula {ced} sin pruebas");
    else:
        st.markdown(f'<div class="card"><h3>Progreso estilo personality.co - {ced}</h3><div class="progress-bar"><div class="progress-fill" style="width:60%"></div></div><p>Paso 2 de 3 - Completa el test</p></div>', unsafe_allow_html=True)
        for idx,asig in enumerate(mis):
            cargo=st.session_state.cargos_db.get(asig["cargo_key"])
            if not cargo: continue
            st.markdown(f'<div class="card"><h3>{cargo["nombre"]} - Asignado por {asig["asignado_por"]}</h3></div>', unsafe_allow_html=True)
            with st.form(f"form_{ced}_{idx}"):
                resps=[]
                for i,pr in enumerate(cargo["preguntas"]):
                    if pr.get("img"): st.markdown(f'<div style="font-size:38px;text-align:center">{pr["img"]}</div>', unsafe_allow_html=True)
                    st.write(f"**{i+1}. {pr['q']}**"); r=st.radio("Elige", pr["opts"], index=None, key=f"r_{ced}_{idx}_{i}"); resps.append(r)
                st.divider(); st.write("**🧠 Psicología con imágenes (estilo personality.co):**")
                rp=[]
                for j,ps in enumerate(PSICO):
                    st.markdown(f'<div style="font-size:30px">{ps["img"]}</div><b>{ps["q"]}</b>', unsafe_allow_html=True)
                    r2=st.radio(f"ps {j}", ps["opts"], index=None, key=f"ps_{ced}_{idx}_{j}"); rp.append(r2)
                caso=st.text_area("Caso práctico / Redacción")
                if st.form_submit_button("🚀 FINALIZAR - Enviar automático a RRHH", type="primary", use_container_width=True):
                    ac=sum(1 for j,rr in enumerate(resps) if rr==cargo["preguntas"][j]["opts"][0]); tot=len(cargo["preguntas"]) or 1; sc=int(ac/tot*100)
                    st.session_state.resultados.append({"cedula":ced,"nombre":asig["nombre"],"cargo_nombre":cargo["nombre"],"asignado_por":asig["asignado_por"],"score":f"{sc}%","score_num":sc,"aciertos":f"{ac}/{tot}","hv_text":st.session_state.get("hv_actual","")[:250],"caso":caso[:200],"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.balloons(); st.success(f"✅ {sc}% Enviado a RRHH - PDF solo lo ve RRHH")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
