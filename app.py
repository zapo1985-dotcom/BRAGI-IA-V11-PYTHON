import streamlit as st
import random, pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

st.set_page_config(page_title="BRAGI-IA V11 FINAL", layout="wide", page_icon="🧠")

# --- ESTILOS TALENTO INTELIGENTE ---
st.markdown("""
<style>
.stApp{background:#F2F3F4}
.card{background:white;padding:22px;border-radius:20px;margin:12px 0;box-shadow:0 8px 20px rgba(0,0,0,0.06);position:relative;z-index:1}
.verde{background:#2D5A4A;color:white;padding:14px;border-radius:14px;text-align:center;font-weight:900;letter-spacing:0.5px}
.watermark{position:fixed;top:30%;left:-15%;transform:rotate(-24deg);font-size:26px;color:rgba(45,90,74,0.07);font-weight:900;pointer-events:none;z-index:0;width:250%;line-height:90px}
.badge-excel{background:#D1FAE5;color:#065F46;padding:6px 12px;border-radius:20px;font-weight:800}
.badge-abog{background:#DBEAFE;color:#1E40AF;padding:6px 12px;border-radius:20px;font-weight:800}
.badge-quim{background:#FEF3C7;color:#92400E;padding:6px 12px;border-radius:20px;font-weight:800}
</style>
<div class="watermark">TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE • BRAGI-IA • TALENTO INTELIGENTE • BRAGI-IA</div>
""", unsafe_allow_html=True)

st.markdown('<div class="verde">BRAGI-IA V11 FINAL - TALENTO INTELIGENTE - PYTHON STREAMLIT</div>', unsafe_allow_html=True)

# --- MEMORIA ---
if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None

# --- BANCOS COMPLETOS ---
BANCOS={
"excel":[
{"q":"¿Qué hace BUSCARV?","opts":["Busca valor en tabla","Suma valores","Borra celdas","Crea gráfico"],"ok":0},
{"q":"¿Para qué sirve TABLA DINÁMICA?","opts":["Resumir y analizar datos","Escribir texto","Cambiar color","Enviar correo"],"ok":0},
{"q":"¿Función para sumar con condición?","opts":["SUMAR.SI","SUMA","PROMEDIO","CONTAR"],"ok":0},
{"q":"¿Atajo para fijar celdas $A$1?","opts":["F4","F2","F5","F11"],"ok":0},
{"q":"¿Qué hace CONCATENAR?","opts":["Une textos","Divide","Suma","Filtra"],"ok":0},
{"q":"¿Función que cuenta celdas no vacías?","opts":["CONTARA","CONTAR","CONTAR.SI","SUMA"],"ok":0},
{"q":"¿Validación de datos sirve para?","opts":["Crear lista desplegable","Cambiar fuente","Imprimir","Borrar"],"ok":0},
{"q":"¿Qué es un Dashboard en Excel?","opts":["Panel visual de indicadores","Un tipo de letra","Una fórmula","Un error"],"ok":0},
{"q":"¿INDICE + COINCIDIR reemplaza a?","opts":["BUSCARV más potente","SUMA","PROMEDIO","HOY"],"ok":0},
{"q":"¿Para qué sirve Power Query?","opts":["Limpiar y transformar datos","Jugar","Dibujar","Navegar"],"ok":0},
],
"abogados":[
{"q":"¿Qué es Acción de Tutela?","opts":["Mecanismo protección derechos fundamentales","Demanda laboral","Contrato","Testamento"],"ok":0},
{"q":"Ley 80 de 1993 regula:","opts":["Contratación estatal","Tránsito","Familia","Penal"],"ok":0},
{"q":"¿Término para contestar demanda?","opts":["Según el proceso, ej 10 días","1 año","No hay término","1 hora"],"ok":0},
{"q":"¿Qué es Debido Proceso?","opts":["Garantía constitucional art 29","Solo demora","Un impuesto","Una multa"],"ok":0},
{"q":"¿Recurso contra fallo de primera instancia?","opts":["Apelación","Tutela","Derecho petición","Queja"],"ok":0},
{"q":"¿Qué es SECOP II?","opts":["Plataforma contratación pública","Red social","Juego","Banco"],"ok":0},
{"q":"¿Cláusula penal en contratos?","opts":["Sanción por incumplimiento","Premio","Saludo","Descuento"],"ok":0},
{"q":"¿Qué es Liquidación de contrato estatal?","opts":["Balance final de ejecución","Solo pago","Anulación","Prórroga"],"ok":0},
{"q":"¿Derecho de petición plazo?","opts":["15 días hábiles","1 día","6 meses","No tiene"],"ok":0},
{"q":"¿Qué es Caducidad en contratación?","opts":["Sanción máxima por incumplimiento grave","Vencimiento plazo","Pago","Inicio contrato"],"ok":0},
],
"quimico":[
{"q":"¿Qué son BPM?","opts":["Buenas Prácticas de Manufactura","Buen Pago Mensual","Baja Producción","Buena Práctica Médica"],"ok":0},
{"q":"¿Qué es Farmacovigilancia?","opts":["Vigilar efectos adversos medicamentos","Vender más","Comprar","Publicitar"],"ok":0},
{"q":"¿INVIMA qué regula?","opts":["Medicamentos y alimentos en Colombia","Tránsito","Construcción","Telecom"],"ok":0},
{"q":"¿Qué es estabilidad de un fármaco?","opts":["Que mantiene propiedades en el tiempo","Que es caro","Que es líquido","Que es sólido"],"ok":0},
{"q":"¿Qué es un Lote en producción?","opts":["Cantidad producida en un ciclo","Un terreno","Una persona","Un impuesto"],"ok":0},
{"q":"¿Qué es validación de método analítico?","opts":["Demostrar que método es confiable","Solo limpiar","Solo pesar","Solo vender"],"ok":0},
{"q":"¿Temperatura de cadena de frío típica?","opts":["2-8°C","50°C","100°C","-100°C"],"ok":0},
{"q":"¿Qué es CAPA?","opts":["Corrective and Preventive Action","Capa de ropa","Tapa","Carpeta"],"ok":0},
{"q":"¿Qué es Registro Sanitario?","opts":["Autorización INVIMA para comercializar","Un libro","Una factura","Una foto"],"ok":0},
{"q":"¿Qué es Dossier?","opts":["Expediente técnico del producto","Un bolso","Una caja","Un frasco"],"ok":0},
]
}

def generar_pdf(dato, tipo):
    buffer=io.BytesIO()
    c=canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor("#2D5A4A"))
    c.drawString(30,750,f"TALENTO INTELIGENTE - BRAGI-IA V11 - {tipo.upper()} - CONFIDENCIAL")
    c.setFillColor(HexColor("#2D5A4A"), alpha=0.07)
    c.setFont("Helvetica-Bold", 28)
    c.saveState(); c.translate(200,300); c.rotate(-24); c.drawString(0,0,"TALENTO INTELIGENTE"); c.restoreState()
    c.setFillColor(HexColor("#000000"))
    c.setFont("Helvetica", 11)
    y=700
    for k,v in dato.items():
        c.drawString(40,y,f"{k}: {v}"); y-=20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40,100,"Documento confidencial - Uso exclusivo RRHH - BRAGI-IA V11 - TALENTO INTELIGENTE")
    c.showPage(); c.save(); buffer.seek(0); return buffer

# --- LOGIN ---
if st.session_state.rol is None:
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>🧑‍💼 Candidato</h3><p>Entra solo con tu cédula (sin clave)</p></div>', unsafe_allow_html=True)
        ced=st.text_input("Tu cédula", key="ced")
        if st.button("Ver mis pruebas asignadas", use_container_width=True):
            if ced:
                st.session_state.ced=ced; st.session_state.rol="candidato"; st.rerun()
    with col2:
        st.markdown('<div class="card"><h3>👩‍💼 RRHH - Admin</h3></div>', unsafe_allow_html=True)
        u=st.text_input("Usuario", value="admin"); p=st.text_input("Clave", type="password", value="admin123")
        if st.button("Entrar RRHH", type="primary", use_container_width=True):
            if u=="admin" and p=="admin123":
                st.session_state.rol="rrhh"; st.rerun()
            else: st.error("Error")
    st.stop()

# --- PANEL RRHH ---
if st.session_state.rol=="rrhh":
    st.markdown('<div class="card"><h2>Panel RRHH - Asignaciones y Resultados Automáticos</h2><p>Cuando el candidato da FINALIZAR, aquí aparece automático con cédula, nombre, módulo y quién lo asignó.</p></div>', unsafe_allow_html=True)
    with st.form("asignar_form"):
        c1,c2,c3=st.columns(3)
        with c1: ced=st.text_input("Cédula*"); nom=st.text_input("Nombre completo*")
        with c2: mod=st.selectbox("Módulo*", ["excel","abogados","quimico"]); asig=st.text_input("Asignado por*", value="Maria C. - RRHH")
        with c3: st.write(""); st.write(""); ok=st.form_submit_button("✅ + ASIGNAR PRUEBA", use_container_width=True, type="primary")
        if ok and ced and nom:
            st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"modulo":mod,"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
            st.success(f"✅ Asignado {nom} ({ced}) módulo {mod} por {asig}")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Resultados que llegan automático")
    if st.session_state.resultados:
        df=pd.DataFrame(st.session_state.resultados)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df["modulo"].value_counts())
        # PDFs
        for i, r in enumerate(st.session_state.resultados):
            colA,colB=st.columns(2)
            with colA:
                pdf1=generar_pdf(r, "TECNICO HV")
                st.download_button(f"📄 PDF Técnico {r['cedula']}", pdf1, f"Tecnico_{r['cedula']}.pdf", "application/pdf", key=f"t{i}")
            with colB:
                pdf2=generar_pdf(r, "PSICOLOGICO CONFIDENCIAL")
                st.download_button(f"🔒 PDF Confidencial {r['cedula']}", pdf2, f"Confidencial_{r['cedula']}.pdf", "application/pdf", key=f"c{i}")
    else:
        st.info("Sin resultados aún. Asigna una cédula, entra como candidato y dale FINALIZAR. Verás como aparece aquí automático.")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()

# --- PANEL CANDIDATO ---
if st.session_state.rol=="candidato":
    ced=st.session_state.ced
    mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis:
        st.error(f"❌ Tu cédula {ced} no tiene pruebas asignadas. Pídele a RRHH que te asigne en el panel.")
        if st.button("Volver"): st.session_state.rol=None; st.rerun()
        st.stop()
    for asig in mis:
        mod=asig["modulo"]
        badge=f"badge-{mod}" if mod!="abogados" else "badge-abog"
        st.markdown(f'<div class="card"><span class="{badge}">{mod.upper()}</span> <h3>Prueba para {asig["nombre"]} - Cédula {ced}</h3><small>Asignado por: {asig["asignado_por"]} el {asig["fecha"]}</small></div>', unsafe_allow_html=True)
        banco=BANCOS[mod]
        with st.form(f"form_{mod}_{ced}"):
            respuestas=[]
            for i,preg in enumerate(banco):
                st.write(f"**{i+1}. {preg['q']}**")
                r=st.radio("Selecciona:", preg["opts"], index=None, key=f"{mod}_{ced}_{i}")
                respuestas.append(r)
            final=st.form_submit_button("🚀 FINALIZAR PRUEBA - Envío automático a RRHH", type="primary", use_container_width=True)
            if final:
                aciertos=sum(1 for idx,resp in enumerate(respuestas) if resp==banco[idx]["opts"][banco[idx]["ok"]])
                score=int((aciertos/len(banco))*100)
                if score>=90: rango="Altamente Confiable - 95%"; color="#065F46"
                elif score>=75: rango="Confiable"; color="#2D5A4A"
                elif score>=60: rango="Riesgo Moderado"; color="#92400E"
                else: rango="No Recomendado"; color="#991B1B"
                resultado={"cedula":ced,"nombre":asig["nombre"],"modulo":mod,"asignado_por":asig["asignado_por"],"score":f"{score}%","rango":rango,"aciertos":f"{aciertos}/{len(banco)}","fecha":datetime.now().strftime("%Y-%m-%d %H:%M")}
                st.session_state.resultados.append(resultado)
                st.balloons()
                st.success(f"✅ FINALIZADO {score}% - {rango} - Guardado automático en RRHH. Ya no tienes que hacer nada más.")
    if st.button("Cerrar sesión"): st.session_state.rol=None; st.rerun()
