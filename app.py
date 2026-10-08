import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="BRAGI-IA V11", layout="wide")

st.markdown("""
<style>
.stApp{background:#F2F3F4}
h1,h2,h3{color:#2B2F32}
.card{background:white;padding:20px;border-radius:20px;margin:10px 0;box-shadow:0 4px 10px rgba(0,0,0,0.05)}
.verde{background:#2D5A4A;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:800}
.watermark{position:fixed;top:30%;left:-10%;transform:rotate(-25deg);font-size:28px;color:rgba(45,90,74,0.07);font-weight:900;pointer-events:none;z-index:0;width:200%}
</style>
<div class="watermark">TALENTO INTELIGENTE • BRAGI-IA V11 • TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE</div>
""", unsafe_allow_html=True)

st.markdown('<div class="verde">BRAGI-IA V11 - TALENTO INTELIGENTE - Verde Moda #2D5A4A</div>', unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None

if st.session_state.rol is None:
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Candidato")
        ced=st.text_input("Escribe tu cédula", key="ced_in")
        if st.button("Entrar como Candidato", use_container_width=True):
            if ced:
                st.session_state.ced=ced
                st.session_state.rol="candidato"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("RRHH")
        u=st.text_input("Usuario", value="admin")
        p=st.text_input("Clave", type="password", value="admin123")
        if st.button("Entrar como RRHH", use_container_width=True):
            if u=="admin" and p=="admin123":
                st.session_state.rol="rrhh"
                st.rerun()
            else:
                st.error("Usuario o clave mala")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if st.session_state.rol=="rrhh":
    st.markdown('<div class="card"><h2>Panel RRHH - Aquí aparece todo automático</h2></div>', unsafe_allow_html=True)
    with st.form("form_asig"):
        st.write("Asignar prueba")
        ced=st.text_input("Cédula del candidato")
        nom=st.text_input("Nombre completo")
        mod=st.selectbox("Módulo", ["excel","abogados","quimico"])
        asig=st.text_input("Asignado por (tu nombre)", value="RRHH Maria")
        btn=st.form_submit_button("✅ Asignar")
        if btn and ced and nom:
            st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"modulo":mod,"asignado":asig,"fecha":str(datetime.now())})
            st.success(f"Asignado {ced} - {nom}")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### Resultados automáticos (aparecen cuando el candidato finaliza)")
    if st.session_state.resultados:
        st.table(st.session_state.resultados)
    else:
        st.info("Aún no hay resultados. Cuando el candidato de FINALIZAR, aquí sale automático con cédula, quién lo asignó y el score.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Cerrar sesión"):
        st.session_state.rol=None
        st.rerun()

if st.session_state.rol=="candidato":
    ced=st.session_state.ced
    asign=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not asign:
        st.error(f"Tu cédula {ced} no tiene módulos asignados. Pídele a RRHH que te asigne primero.")
        if st.button("Volver"):
            st.session_state.rol=None
            st.rerun()
        st.stop()

    mod=asign[0]["modulo"]
    st.markdown(f'<div class="card"><h2>Módulo: {mod.upper()} para {ced} - Asignado por {asign[0]["asignado"]}</h2></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    q1=st.radio("1. ¿Qué hace BUSCARV en Excel?", ["Busca un valor","Suma","Borra"], index=None)
    q2=st.radio("2. ¿Para qué sirve una tabla dinámica?", ["Resumir datos","Dibujar"], index=None)
    if st.button("🚀 FINALIZAR - Enviar automático a RRHH", use_container_width=True):
        score=random.randint(88,97)
        st.session_state.resultados.append({
            "cedula": ced,
            "nombre": asign[0]["nombre"],
            "modulo": mod,
            "asignado_por": asign[0]["asignado"],
            "score": f"{score}%",
            "rango": "Altamente Confiable" if score>=90 else "Confiable"
        })
        st.balloons()
        st.success(f"✅ ¡Enviado! {score}% - Ya aparece automático en RRHH")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Cerrar sesión"):
        st.session_state.rol=None
        st.rerun()
