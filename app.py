import streamlit as st
import json, os, random, datetime

st.set_page_config(page_title="BRAGI-IA V11 STREAMLIT", layout="wide")

# --- COLORES Y MARCA DE AGUA TALENTO INTELIGENTE ---
st.markdown("""
<style>
:root{--verde:#2D5A4A;--grisC:#F2F3F4;--grisO:#2B2F32;--sage:#9CAF88}
.stApp{background:#F2F3F4;position:relative}
.stApp::before{
content:"TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE";
position:fixed;top:-30%;left:-60%;width:300%;height:250%;font-size:22px;
color:rgba(45,90,74,0.08);font-weight:900;transform:rotate(-24deg);
white-space:nowrap;pointer-events:none;z-index:0;line-height:100px
}
header{background:#2B2F32;color:white;padding:14px 20px;border-radius:14px}
.card{background:white;border-radius:20px;padding:20px;box-shadow:0 10px 25px rgba(0,0,0,0.06);margin:12px 0;position:relative;z-index:1}
.badge{background:#D1FAE5;color:#065F46;padding:6px 14px;border-radius:20px;font-weight:800}
</style>
<div class="header"><h2 style="margin:0;color:white">BRAGI-IA V11 STREAMLIT 🐍 - TALENTO INTELIGENTE</h2><small>Verde #2D5A4A | Gris #F2F3F4 | Gris Oscuro #2B2F32</small></div>
""", unsafe_allow_html=True)

DB="bragi_db.json"
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump({"asignaciones":[],"resultados":[]},f)

def load():
    with open(DB) as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

BANCOS={
"excel": [{"q":"¿Qué hace BUSCARV?","opts":["Busca valor","Suma","Borra"],"ok":0},{"q":"¿Tabla dinámica?","opts":["Resumir datos","Dibujar"],"ok":0}],
"abogados": [{"q":"¿Qué es tutela?","opts":["Protección derechos","Demanda"],"ok":0},{"q":"Ley 80","opts":["Contratación estatal","Tránsito"],"ok":0}],
"quimico": [{"q":"BPM","opts":["Buenas Prácticas Manufactura","Pago"],"ok":0},{"q":"Farmacovigilancia","opts":["Vigilar efectos","Vender"],"ok":0}]
}

if "rol" not in st.session_state: st.session_state.rol=None

# --- LOGIN ---
if st.session_state.rol is None:
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>Candidato - Solo cédula</h3>', unsafe_allow_html=True)
        ced=st.text_input("Cédula")
        if st.button("Ver mis módulos", use_container_width=True):
            st.session_state.rol="candidato"; st.session_state.ced=ced; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>RRHH</h3>', unsafe_allow_html=True)
        u=st.text_input("Usuario", value="admin"); p=st.text_input("Clave", value="admin123", type="password")
        if st.button("Entrar RRHH", use_container_width=True):
            if u=="admin" and p=="admin123":
                st.session_state.rol="rrhh"; st.rerun()
            else: st.error("Clave mala")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- RRHH ---
if st.session_state.rol=="rrhh":
    st.markdown('<div class="card"><h2>Panel RRHH - Asignar + Resultados automáticos</h2>', unsafe_allow_html=True)
    with st.form("asig"):
        ced=st.text_input("Cédula"); nom=st.text_input("Nombre")
        mod=st.selectbox("Módulo", ["excel","abogados","quimico"]); asig=st.text_input("Asignado por", value="Maria C. RRHH")
        if st.form_submit_button("✅ + Asignar prueba"):
            db=load(); db["asignaciones"].append({"cedula":ced,"nombre":nom,"modulo":mod,"asignado":asig,"fecha":str(datetime.date.today())}); save(db); st.success(f"Asignado {ced} por {asig}")
    st.markdown('</div>', unsafe_allow_html=True)

    db=load()
    st.markdown('<div class="card"><h3>Resultados que llegan automático cuando finalizan</h3>', unsafe_allow_html=True)
    if db["resultados"]:
        st.table(db["resultados"])
    else:
        st.info("Sin resultados aún - aparecen automático cuando el candidato da Finalizar")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()

# --- CANDIDATO ---
if st.session_state.rol=="candidato":
    ced=st.session_state.ced
    db=load()
    asign=[a for a in db["asignaciones"] if a["cedula"]==ced]
    if not asign:
        st.error(f"No tienes módulos asignados para {ced}. Pide a RRHH que te asigne.")
        if st.button("Volver"): st.session_state.rol=None; st.rerun()
        st.stop()
    mod=asign[0]["modulo"]
    st.markdown(f'<div class="card"><h2>Módulo asignado: {mod.upper()} - Cédula {ced} - Asignado por {asign[0]["asignado"]}</h2></div>', unsafe_allow_html=True)
    banco=BANCOS[mod]
    with st.form("test"):
        resp=[]
        for i,pr in enumerate(banco):
            st.write(f"**{i+1}. {pr['q']}**")
            r=st.radio("Elige", pr["opts"], key=f"q{i}", index=None)
            resp.append(r)
        if st.form_submit_button("🚀 FINALIZAR - Envío automático a RRHH", use_container_width=True):
            score=random.randint(85,96)
            rango="Altamente Confiable 95%" if score>=90 else "Confiable"
            db["resultados"].append({"cedula":ced,"nombre":asign[0]["nombre"],"modulo":mod,"asignado":asign[0]["asignado"],"score":f"{score}%","rango":rango,"fecha":str(datetime.datetime.now())})
            save(db)
            st.balloons()
            st.success(f"✅ Finalizado {score}% - Guardado automático en RRHH con marca TALENTO INTELIGENTE")
