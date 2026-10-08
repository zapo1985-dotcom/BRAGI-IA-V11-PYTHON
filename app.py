import streamlit as st
import random, pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io

st.set_page_config(page_title="BRAGI-IA V12 COMPLETA", layout="wide", page_icon="🧠")
st.markdown("""
<style>
.stApp{background:#F2F3F4}
.card{background:white;padding:22px;border-radius:20px;margin:10px 0;box-shadow:0 8px 18px rgba(0,0,0,0.06);z-index:1;position:relative}
.verde{background:#2D5A4A;color:white;padding:14px;border-radius:14px;text-align:center;font-weight:900}
.watermark{position:fixed;top:28%;left:-12%;transform:rotate(-24deg);font-size:26px;color:rgba(45,90,74,0.07);font-weight:900;pointer-events:none;z-index:0;width:250%;line-height:90px}
.small{font-size:12px;color:#6B7280}
</style>
<div class="watermark">TALENTO INTELIGENTE • BRAGI-IA V12 • TALENTO INTELIGENTE • BRAGI-IA</div>
""", unsafe_allow_html=True)
st.markdown('<div class="verde">BRAGI-IA V12 COMPLETA - 22 CARGOS - TALENTO INTELIGENTE</div>', unsafe_allow_html=True)

if "asignaciones" not in st.session_state: st.session_state.asignaciones=[]
if "resultados" not in st.session_state: st.session_state.resultados=[]
if "rol" not in st.session_state: st.session_state.rol=None
if "cargos_db" not in st.session_state:
    st.session_state.cargos_db = {
        "aux_contable": {"nombre":"Auxiliar Contable","preguntas":[
            {"q":"¿Qué es el PUC en Colombia?","opts":["Plan Único de Cuentas","Pago Único","Presupuesto"],"ok":0},
            {"q":"¿Cuenta por pagar es?","opts":["Deuda con terceros","Ingreso","Activo fijo"],"ok":0},
            {"q":"¿Retención en la fuente?","opts":["Anticipo impuesto","Multa","Descuento"],"ok":0},
            {"q":"¿IVA?","opts":["Impuesto Valor Agregado","Impuesto vivienda","Interés"],"ok":0},
            {"q":"¿Balance general?","opts":["Situación financiera fecha","Solo ingresos","Solo gastos"],"ok":0},
            {"q":"¿Conciliación bancaria?","opts":["Comparar libros vs banco","Cerrar banco","Abrir cuenta"],"ok":0},
            {"q":"¿NIIF?","opts":["Normas Internacionales Info Financiera","Normas internas"],"ok":0},
            {"q":"¿Causación?","opts":["Registrar cuando ocurre hecho","Solo cuando paga","Anual"],"ok":0},
            {"q":"¿Activo corriente?","opts":["Se convierte efectivo <1 año","Edificio","Maquinaria 10 años"],"ok":0},
            {"q":"¿Libro obligatorio?","opts":["Libro diario","Agenda","Cuaderno"],"ok":0},
            {"q":"¿Provisión?","opts":["Gasto futuro probable","Ingreso seguro","Préstamo"],"ok":0},
            {"q":"¿Auxiliar con facturas?","opts":["Revisar, causar y archivar","Solo imprimir","Borrar"],"ok":0},
            {"q":"¿Cierre contable?","opts":["Cerrar periodo y utilidad","Cerrar oficina","Cerrar caja"],"ok":0},
            {"q":"¿Software contable?","opts":["Siigo/Alegra/World Office","Excel solo","Photoshop"],"ok":0},
            {"q":"¿Cuenta 1105?","opts":["Caja","Bancos","Clientes"],"ok":0},
        ]},
        "aux_admin": {"nombre":"Auxiliar Administrativa","preguntas":[
            {"q":"¿Archivo gestión?","opts":["Organizar docs activos","Botar papeles","Guardar fotos"],"ok":0},
            {"q":"¿BUSCARV?","opts":["Busca datos tabla","Dibujos","Correos"],"ok":0},
            {"q":"¿PQRS?","opts":["Petición Queja Reclamo Sugerencia","Pago rápido","Paquete"],"ok":0},
            {"q":"¿Prioridad atención cliente?","opts":["Cordialidad y solución","Ignorar","Demorar"],"ok":0},
            {"q":"¿Acta?","opts":["Constancia reunión","Factura","Chiste"],"ok":0},
            {"q":"¿Google Calendar?","opts":["Agendar coordinar","Jugar","Editar fotos"],"ok":0},
            {"q":"¿Confidencialidad?","opts":["No divulgar info interna","Contar todo","Publicar"],"ok":0},
            {"q":"¿Aux admin con proveedores?","opts":["Solicitar cotizaciones","Solo saludar"],"ok":0},
            {"q":"¿Orden compra?","opts":["Solicita compra","Carta amor"],"ok":0},
            {"q":"¿Excel filtrar?","opts":["Filtros y dinámicas","Solo colores"],"ok":0},
            {"q":"¿Inventario papelería?","opts":["Controlar stock oficina","Inventar papeles"],"ok":0},
            {"q":"¿Comunicación asertiva?","opts":["Clara respetuosa directa","Gritar","No hablar"],"ok":0},
            {"q":"¿Archivo muerto?","opts":["Docs no frecuente","Basura"],"ok":0},
            {"q":"¿Recepción?","opts":["Atender visitas y llamadas","Mirar celular"],"ok":0},
            {"q":"¿Base datos clientes?","opts":["Registro contactos","Lista compras"],"ok":0},
        ]},
        "aux_rrhh": {"nombre":"Auxiliar RRHH","preguntas":[
            {"q":"¿Contrato fijo?","opts":["Inicio y fin definida","Sin fin","Verbal"],"ok":0},
            {"q":"¿Afiliación seguridad?","opts":["EPS ARL Pensión Caja","Solo EPS"],"ok":0},
            {"q":"¿Nómina?","opts":["Liquidación salarios","Lista compras"],"ok":0},
            {"q":"¿Entrevista competencias?","opts":["Evaluar comportamientos pasados","Solo edad"],"ok":0},
            {"q":"¿Onboarding?","opts":["Inducción nuevo","Despedir"],"ok":0},
            {"q":"¿Acoso laboral?","opts":["Ley 1010 2006","Ley 80","Ley 100"],"ok":0},
            {"q":"¿Dotación?","opts":["Ropa cada 4 meses","Regalo navidad"],"ok":0},
            {"q":"¿Profesiograma?","opts":["Perfil cargo requisitos","Examen médico solo"],"ok":0},
            {"q":"¿RRHH con incapacidades?","opts":["Tramitar EPS","Ignorarlas"],"ok":0},
            {"q":"¿Evaluación desempeño?","opts":["Medir objetivos","Castigar"],"ok":0},
            {"q":"¿Clima laboral?","opts":["Ambiente percibido","Temperatura"],"ok":0},
            {"q":"¿Retención HV?","opts":["Custodiar confidencial","Botarlas"],"ok":0},
            {"q":"¿Sanción disciplinaria?","opts":["Proceso con debido proceso","Gritar"],"ok":0},
            {"q":"¿Preaviso?","opts":["Avisar tiempo terminación","No avisar"],"ok":0},
            {"q":"¿Base candidatos?","opts":["Registro talentos","Lista amigos"],"ok":0},
        ]},
        "aux_farmacia": {"nombre":"Auxiliar Farmacia","preguntas":[
            {"q":"¿Dispensación?","opts":["Entregar con info","Solo vender"],"ok":0},
            {"q":"¿Vencimiento?","opts":["Límite uso seguro","Fabricación"],"ok":0},
            {"q":"¿FIFO?","opts":["Primero entra primero sale","Último entra"],"ok":0},
            {"q":"¿LASA?","opts":["Se parecen y confunden","Caros"],"ok":0},
            {"q":"¿Cadena frío?","opts":["Mantener 2-8°C","Congelar -50"],"ok":0},
            {"q":"¿Receta?","opts":["Orden escrita médico","Nota cualquiera"],"ok":0},
            {"q":"¿Principio activo?","opts":["Sustancia efecto terapéutico","Color"],"ok":0},
            {"q":"¿Dosis?","opts":["Cantidad administrar","Peso caja"],"ok":0},
            {"q":"¿Contraindicación?","opts":["No debe usarse","Indicación extra"],"ok":0},
            {"q":"¿Inventario ciego?","opts":["Contar sin ver sistema","No contar"],"ok":0},
            {"q":"¿Kardex?","opts":["Registro movimientos","Medicamento"],"ok":0},
            {"q":"¿BPM farmacia?","opts":["Buenas Prácticas Almacenamiento","Buen pago"],"ok":0},
            {"q":"¿Vencido?","opts":["Separar y reportar destrucción","Vender rápido"],"ok":0},
            {"q":"¿Posología?","opts":["Como tomar: dosis frecuencia","Precio"],"ok":0},
            {"q":"¿Farmacia hospitalaria?","opts":["Gestiona medicamentos clínica","Barrio"],"ok":0},
        ]},
        "serv_generales": {"nombre":"Servicios Generales","preguntas":[
            {"q":"¿Limpieza y desinfección?","opts":["Eliminar suciedad y microbios","Solo barrer"],"ok":0},
            {"q":"¿EPP?","opts":["Elemento Protección Personal","Equipo Pintar"],"ok":0},
            {"q":"¿Manejo residuos?","opts":["Separar según color y riesgo","Todo junto"],"ok":0},
            {"q":"¿Dilución?","opts":["Mezclar según ficha","Puro siempre"],"ok":0},
            {"q":"¿Orden puesto?","opts":["Todo en su lugar limpio","Desorden"],"ok":0},
            {"q":"¿Derrame químico?","opts":["Avisar y protocolo","Mano"],"ok":0},
            {"q":"¿Bioseguridad?","opts":["Normas evitar contagios","Tapabocas a veces"],"ok":0},
            {"q":"¿Checklist aseo?","opts":["Lista verificación","Lista compras"],"ok":0},
            {"q":"¿Mantenimiento preventivo?","opts":["Evitar daños revisando","Arreglar cuando daña"],"ok":0},
            {"q":"¿Señalización?","opts":["Avisos seguridad","Adornos"],"ok":0},
            {"q":"¿Uso eficiente agua?","opts":["No desperdiciar","Mucha"],"ok":0},
            {"q":"¿Objeto perdido?","opts":["Entregar supervisor","Quedárselo"],"ok":0},
            {"q":"¿Trabajo alturas?","opts":[">1.5m con arnés permiso","Silla"],"ok":0},
            {"q":"¿Amabilidad?","opts":["Trato respetuoso","Ignorar"],"ok":0},
            {"q":"¿Horario?","opts":["Puntual y cumplir turnos","Cuando quiera"],"ok":0},
        ]},
        "conductor": {"nombre":"Conductor Carro","preguntas":[
            {"q":"¿Licencia C1?","opts":["Automóviles camionetas","Motos","Mula"],"ok":0},
            {"q":"¿Revisar antes salir?","opts":["Frenos llantas aceite luces","Solo gasolina"],"ok":0},
            {"q":"¿SOAT?","opts":["Seguro obligatorio accidentes","Impuesto"],"ok":0},
            {"q":"¿Accidente?","opts":["Señalizar auxiliar llamar","Irse"],"ok":0},
            {"q":"¿Límite urbana?","opts":["30-50 km/h","100 km/h"],"ok":0},
            {"q":"¿Manejo defensivo?","opts":["Anticipar riesgos","Correr mucho"],"ok":0},
            {"q":"¿Kit carretera?","opts":["Extintor botiquín repuesto","Solo llanta"],"ok":0},
            {"q":"¿Pico y placa?","opts":["Restricción por placa","Prohibición total"],"ok":0},
            {"q":"¿Mant preventivo?","opts":["Aceite frenos sincronización","Solo lavar"],"ok":0},
            {"q":"¿Vehículo falla?","opts":["Parquear seguro avisar","Mitad vía"],"ok":0},
            {"q":"¿Normas tránsito?","opts":["No semáforo rojo ni celular","Pasar rápido"],"ok":0},
            {"q":"¿Planilla viaje?","opts":["Registro origen destino km","Dibujo"],"ok":0},
            {"q":"¿Bajo lluvia?","opts":["Reducir velocidad distancia","Acelerar"],"ok":0},
            {"q":"¿Documentación?","opts":["Licencia SOAT tecno tarjeta","Solo cédula"],"ok":0},
            {"q":"¿Trato pasajero?","opts":["Cordial seguro equipaje","Gritar"],"ok":0},
        ]},
        "mensajero_moto": {"nombre":"Mensajero Moto","preguntas":[
            {"q":"¿Licencia moto?","opts":["A2","B1","C1"],"ok":0},
            {"q":"¿EPP moto?","opts":["Casco guantes chaqueta rodilleras","Solo casco a veces"],"ok":0},
            {"q":"¿Paquete frágil?","opts":["Cuidado y asegurar","Tirarlo"],"ok":0},
            {"q":"¿Entrega certificada?","opts":["Con firma evidencia","Tirado"],"ok":0},
            {"q":"¿Ruta óptima?","opts":["Rápido y seguro","Largo"],"ok":0},
            {"q":"¿Cliente no está?","opts":["Llamar esperar reportar","Calle"],"ok":0},
            {"q":"¿Defensivo moto?","opts":["Evitar puntos ciegos distancia","Zigzag"],"ok":0},
            {"q":"¿Mant moto?","opts":["Frenos cadena llantas aceite","Gasolina"],"ok":0},
            {"q":"¿SOAT moto?","opts":["Seguro obligatorio","Opcional"],"ok":0},
            {"q":"¿Dinero recaudado?","opts":["Entregar con soporte","Gastarlo"],"ok":0},
            {"q":"¿App rutas?","opts":["Waze Maps optimizar","Juego"],"ok":0},
            {"q":"¿Confidencialidad?","opts":["No abrir divulgar","Leer todo"],"ok":0},
            {"q":"¿Límite moto ciudad?","opts":["50 km/h","120 km/h"],"ok":0},
            {"q":"¿Reporte novedad?","opts":["Informar inmediato incidente","Ocultar"],"ok":0},
            {"q":"¿Servicio cliente?","opts":["Amable puntual","Grosero"],"ok":0},
        ]},
        "logistica": {"nombre":"Logística Transporte","preguntas":[
            {"q":"¿WMS?","opts":["Sistema gestión bodega","WhatsApp"],"ok":0},
            {"q":"¿Picking?","opts":["Alistar pedido","Empacar sin lista"],"ok":0},
            {"q":"¿Cross docking?","opts":["Pasa directo sin almacenar mucho","Guardar 1 año"],"ok":0},
            {"q":"¿Última milla?","opts":["Entrega final cliente","Primer km"],"ok":0},
            {"q":"¿Flete?","opts":["Costo transporte","Impuesto"],"ok":0},
            {"q":"¿Guía transporte?","opts":["Documento ampara carga","Carta amor"],"ok":0},
            {"q":"¿OTIF?","opts":["On Time In Full","Solo a tiempo"],"ok":0},
            {"q":"¿Ruteo?","opts":["Planificar rutas eficientes","Sin plan"],"ok":0},
            {"q":"¿Cubicaje?","opts":["Calcular espacio carga","Pesar solo"],"ok":0},
            {"q":"¿Inventario cíclico?","opts":["Conteo parcial frecuente","Cada 5 años"],"ok":0},
            {"q":"¿Logística inversa?","opts":["Vuelve cliente a bodega","Se bota"],"ok":0},
            {"q":"¿TMS?","opts":["Sistema gestión transporte","TV"],"ok":0},
            {"q":"¿Consolidación?","opts":["Unir pedidos vehículo","Separar todo"],"ok":0},
            {"q":"¿Trazabilidad?","opts":["Seguir recorrido producto","Perderlo"],"ok":0},
            {"q":"¿KPI logístico?","opts":["Indicador desempeño entregas tiempo","Chisme"],"ok":0},
        ]},
        "contador": {"nombre":"Contador Público","preguntas":[
            {"q":"¿Declaración renta?","opts":["Informe anual ingresos impuestos","Solo empresas"],"ok":0},
            {"q":"¿NIIF PYMES?","opts":["Normas pequeñas empresas","Solo grandes"],"ok":0},
            {"q":"¿Revisoría obligatoria?","opts":["Según topes ingresos/activos","Todas"],"ok":0},
            {"q":"¿IVA descontable?","opts":["IVA pagado cruzar","Se pierde"],"ok":0},
            {"q":"¿Exógena?","opts":["Info reporta DIAN","Interna solo"],"ok":0},
            {"q":"¿Flujo efectivo?","opts":["Entradas salidas efectivo","Solo ventas"],"ok":0},
            {"q":"¿Patrimonio?","opts":["Activos - Pasivos","Solo deudas"],"ok":0},
            {"q":"¿Auditoría interna?","opts":["Revisar procesos mejorar","Buscar culpables"],"ok":0},
            {"q":"¿ICA?","opts":["Industria Comercio municipal","Nacional"],"ok":0},
            {"q":"¿Factura electrónica?","opts":["Factura válida DIAN digital","Excel"],"ok":0},
            {"q":"¿Costo vs gasto?","opts":["Costo produce ingreso gasto administra","Igual"],"ok":0},
            {"q":"¿Provisión cartera?","opts":["Reserva posible no pago","Ingreso extra"],"ok":0},
            {"q":"¿Cierre fiscal?","opts":["Determinar impuestos utilidad real","Imprimir"],"ok":0},
            {"q":"¿Dictamen?","opts":["Opinión sobre estados financieros","Multa"],"ok":0},
            {"q":"¿Ética contable?","opts":["Confidencialidad objetividad integridad","Contar secretos"],"ok":0},
        ]},
        "revisor_fiscal": {"nombre":"Revisor Fiscal","preguntas":[
            {"q":"¿Función?","opts":["Fe pública y controlar","Solo firmar"],"ok":0},
            {"q":"¿Dictamen salvedad?","opts":["Hallazgos pero razonables","Todo perfecto"],"ok":0},
            {"q":"¿Control interno?","opts":["Procesos riesgos cumplimiento","Solo caja menor"],"ok":0},
            {"q":"¿NIA?","opts":["Normas Internacionales Auditoría","Internas"],"ok":0},
            {"q":"¿Fraude?","opts":["Acto intencional engaño","Error sin intención"],"ok":0},
            {"q":"¿Independencia?","opts":["Sin conflicto interés","Amigo gerente"],"ok":0},
            {"q":"¿Informe asamblea?","opts":["Reportar hallazgos socios","No reportar"],"ok":0},
            {"q":"¿Materialidad?","opts":["Importancia error","Peso material"],"ok":0},
            {"q":"¿Pruebas sustantivas?","opts":["Verificar saldos transacciones","Preguntar"],"ok":0},
            {"q":"¿Riesgo auditoría?","opts":["No detecte error material","Llueva"],"ok":0},
            {"q":"¿Código comercio?","opts":["Art 203-213","No existe"],"ok":0},
            {"q":"¿Lavado activos?","opts":["Reportar UIAF","Ignorar"],"ok":0},
            {"q":"¿Circularización?","opts":["Confirmar saldos terceros","Carta interna"],"ok":0},
            {"q":"¿Papeles trabajo?","opts":["Evidencia auditoría","Reciclaje"],"ok":0},
            {"q":"¿Ética revisor?","opts":["Fe pública independencia reserva","Chisme"],"ok":0},
        ]},
        "aud_medica": {"nombre":"Auditoría Médica","preguntas":[
            {"q":"¿Pertinencia?","opts":["Si procedimiento necesario","Si bonito"],"ok":0},
            {"q":"¿Glosa?","opts":["Objeción factura inconsistencia","Pago extra"],"ok":0},
            {"q":"¿RIPS?","opts":["Registro Individual Prestación Servicios Salud","Reporte Interno"],"ok":0},
            {"q":"¿Autorización?","opts":["Aval prestar servicio","Factura"],"ok":0},
            {"q":"¿Aud concurrente?","opts":["Revisar paciente hospitalizado","Después 1 año"],"ok":0},
            {"q":"¿CUPS?","opts":["Codificación procedimientos salud","Postal"],"ok":0},
            {"q":"¿CIE-10?","opts":["Clasificación diagnósticos","Facturas"],"ok":0},
            {"q":"¿Glosa tarifa?","opts":["Cobro encima pactado","Barata"],"ok":0},
            {"q":"¿Glosa pertinencia?","opts":["No justificado clínicamente","Barato"],"ok":0},
            {"q":"¿Facturación salud?","opts":["Liquidar según manual tarifario","Inventar precios"],"ok":0},
            {"q":"¿SOAT auditoría?","opts":["Atención accidente con topes","Seguro carro"],"ok":0},
            {"q":"¿Junta médica?","opts":["Varios médicos deciden","Reunión social"],"ok":0},
            {"q":"¿Habilitación?","opts":["Requisitos prestar servicio salud","Celular"],"ok":0},
            {"q":"¿Calidad atención?","opts":["Oportuna segura pertinente continua","Rápida"],"ok":0},
            {"q":"¿Resol 3047?","opts":["Regula glosas tiempos","Tránsito"],"ok":0},
        ]},
        "facturacion_rips": {"nombre":"Facturación RIPS Glosas","preguntas":[
            {"q":"¿Archivos RIPS?","opts":["US AF AC AP AH AM","Solo uno"],"ok":0},
            {"q":"¿Glosa soportes?","opts":["Falta documento soporte cobro","Soporte bueno"],"ok":0},
            {"q":"¿FURIPS?","opts":["Formato reclamación SOAT","Factura"],"ok":0},
            {"q":"¿Manual tarifario?","opts":["Lista precios pactados","Lista compras"],"ok":0},
            {"q":"¿Devolución?","opts":["No cumple requisitos devuelve completa","Paga igual"],"ok":0},
            {"q":"¿Tiempo responder glosa?","opts":["15 días hábiles","1 año"],"ok":0},
            {"q":"¿Factura electrónica salud?","opts":["Validada DIAN con RIPS","A mano"],"ok":0},
            {"q":"¿Auditoría cuentas médicas?","opts":["Revisar facturas vs soportes contratos","Sumar"],"ok":0},
            {"q":"¿Glosa cobertura?","opts":["No incluido plan","Incluido"],"ok":0},
            {"q":"¿Recobro?","opts":["Cobro ADRES no PBS","Doble"],"ok":0},
            {"q":"¿Conciliación glosas?","opts":["Acuerdo prestador pagador","Pelear"],"ok":0},
            {"q":"¿Codificación correcta?","opts":["CUPS CIE10 correctos","Inventar"],"ok":0},
            {"q":"¿Facturado vs radicado?","opts":["Facturado total radicado entregado EPS","Igual siempre"],"ok":0},
            {"q":"¿Nota crédito salud?","opts":["Ajuste disminuye factura","Aumenta"],"ok":0},
            {"q":"¿Indicador glosa?","opts":["% glosado sobre facturado","Número facturas"],"ok":0},
        ]},
        "ing_ambiental": {"nombre":"Ing Ambiental","preguntas":[
            {"q":"¿PMA?","opts":["Plan Manejo Ambiental","Mantenimiento"],"ok":0},
            {"q":"¿Licencia ambiental?","opts":["Permiso autoridad proyecto","Conducir"],"ok":0},
            {"q":"¿Vertimiento?","opts":["Descarga agua residual","Basura sólida"],"ok":0},
            {"q":"¿ISO 14001?","opts":["Gestión ambiental","Calidad 9001"],"ok":0},
            {"q":"¿Huella carbono?","opts":["Emisiones GEI","Huella pie"],"ok":0},
            {"q":"¿PGIRS?","opts":["Plan Gestión Residuos Sólidos","Gimnasio"],"ok":0},
            {"q":"¿Impacto ambiental?","opts":["Alteración positiva o negativa ambiente","Solo negativo"],"ok":0},
            {"q":"¿EIA?","opts":["Estudio Impacto Ambiental","Evaluación Interna"],"ok":0},
            {"q":"¿Monitoreo agua?","opts":["Medir calidad periódicamente","Mirar agua"],"ok":0},
            {"q":"¿Economía circular?","opts":["Reusar reciclar reducir","Comprar botar"],"ok":0},
            {"q":"¿Compensación?","opts":["Acción compensar impacto","Multa solo"],"ok":0},
            {"q":"¿Riesgo ambiental?","opts":["Posibilidad daño ambiente","Financiero solo"],"ok":0},
            {"q":"¿CAR?","opts":["Corporación Autónoma Regional","Carro"],"ok":0},
            {"q":"¿Matriz legal?","opts":["Listado normas aplican","Matemática"],"ok":0},
            {"q":"¿Sostenibilidad?","opts":["Usar sin comprometer futuro","Usar todo hoy"],"ok":0},
        ]},
        "ing_sistemas": {"nombre":"Ing Sistemas","preguntas":[
            {"q":"¿Algoritmo?","opts":["Pasos ordenados resolver problema","Virus"],"ok":0},
            {"q":"¿Base datos?","opts":["Datos organizados","Carpeta fotos"],"ok":0},
            {"q":"¿API?","opts":["Interfaz conecta sistemas","Café"],"ok":0},
            {"q":"¿Cloud?","opts":["Servicios internet nube","Lluvia"],"ok":0},
            {"q":"¿Scrum?","opts":["Metodología ágil","Deporte"],"ok":0},
            {"q":"¿Backup?","opts":["Copia seguridad","Borrar datos"],"ok":0},
            {"q":"¿LAN?","opts":["Red área local","Mundial"],"ok":0},
            {"q":"¿Ciberseguridad?","opts":["Proteger de ataques","Solo antivirus"],"ok":0},
            {"q":"¿Frontend?","opts":["Visual usuario","Base datos"],"ok":0},
            {"q":"¿Backend?","opts":["Lógica servidor","Colores"],"ok":0},
            {"q":"¿Git?","opts":["Control versiones","Chat"],"ok":0},
            {"q":"¿Ticket soporte?","opts":["Solicitud ayuda","Boleto cine"],"ok":0},
            {"q":"¿SLA?","opts":["Acuerdo nivel servicio","Salario"],"ok":0},
            {"q":"¿Virtualización?","opts":["Crear versión virtual servidor","Juego"],"ok":0},
            {"q":"¿Proyecto TI?","opts":["Planificar ejecutar controlar implementación","Comprar pc"],"ok":0},
        ]},
        "tec_sistemas": {"nombre":"Técnico Sistemas","preguntas":[
            {"q":"¿PC no enciende?","opts":["Revisar energía cables fuente","Formatear de una"],"ok":0},
            {"q":"¿Formateo?","opts":["Borrar reinstalar SO","Limpiar pantalla"],"ok":0},
            {"q":"¿Driver?","opts":["Programa hace funcionar hardware","Conductor"],"ok":0},
            {"q":"¿IP?","opts":["Identificador red","App"],"ok":0},
            {"q":"¿Antivirus?","opts":["Detecta malware","Virus"],"ok":0},
            {"q":"¿Mant preventivo pc?","opts":["Limpiar polvo actualizar backup","Solo usar"],"ok":0},
            {"q":"¿UTP?","opts":["Cable red","Cable luz"],"ok":0},
            {"q":"¿Impresora red?","opts":["Compartida varios usuarios","Una pc"],"ok":0},
            {"q":"¿Soporte remoto?","opts":["Ayudar distancia TeamViewer","Presencial siempre"],"ok":0},
            {"q":"¿Office 365?","opts":["Suite ofimática nube","SO"],"ok":0},
            {"q":"¿SSD vs HDD?","opts":["SSD más rápido sin partes móviles","Iguales"],"ok":0},
            {"q":"¿Clonación disco?","opts":["Copiar todo a otro disco","Fotocopiar"],"ok":0},
            {"q":"¿BIOS?","opts":["Inicia hardware","Virus"],"ok":0},
            {"q":"¿Ticket cerrado?","opts":["Resuelta","Ignorada"],"ok":0},
            {"q":"¿Inventario TI?","opts":["Lista equipos licencias estados","Compras personales"],"ok":0},
        ]},
        "ing_software": {"nombre":"Ing Software","preguntas":[
            {"q":"¿Ciclo vida?","opts":["Requisitos diseño desarrollo pruebas despliegue","Solo programar"],"ok":0},
            {"q":"¿POO?","opts":["Orientada Objetos","Fotos"],"ok":0},
            {"q":"¿Framework?","opts":["Marco agiliza desarrollo","Lenguaje solo"],"ok":0},
            {"q":"¿Testing?","opts":["Probar funciona bien","Probar comida"],"ok":0},
            {"q":"¿Deploy?","opts":["Poner producción","Borrar código"],"ok":0},
            {"q":"¿Microservicios?","opts":["Dividir en servicios pequeños","App gigante"],"ok":0},
            {"q":"¿BD relacional?","opts":["Tablas relacionadas SQL","Carpeta fotos"],"ok":0},
            {"q":"¿Control versiones?","opts":["Git historial","USB"],"ok":0},
            {"q":"¿Código limpio?","opts":["Legible mantenible buenas prácticas","Largo"],"ok":0},
            {"q":"¿Arquitectura?","opts":["Estructura base sistema","Colores"],"ok":0},
            {"q":"¿API REST?","opts":["GET POST PUT DELETE","Archivo"],"ok":0},
            {"q":"¿CI/CD?","opts":["Integración despliegue continuo","Programar"],"ok":0},
            {"q":"¿Debugging?","opts":["Encontrar corregir errores","Crear errores"],"ok":0},
            {"q":"¿Requisito funcional?","opts":["Qué debe hacer sistema","Color botón"],"ok":0},
            {"q":"¿Liderazgo desarrollo?","opts":["Coordinar equipo asegurar entrega","Solo mandar"],"ok":0},
        ]},
        "ing_bd_seg": {"nombre":"Ing BD y Ciberseguridad Lider","preguntas":[
            {"q":"¿SQL?","opts":["Lenguaje consulta BD","SO"],"ok":0},
            {"q":"¿Inyección SQL?","opts":["Ataque inserta código malicioso","Vacuna"],"ok":0},
            {"q":"¿Backup 3-2-1?","opts":["3 copias 2 medios 1 fuera sitio","3 copias mismo pc"],"ok":0},
            {"q":"¿Firewall?","opts":["Barrera filtra tráfico","Pared física"],"ok":0},
            {"q":"¿Encriptación?","opts":["Convertir ilegible sin clave","Borrar"],"ok":0},
            {"q":"¿Índice BD?","opts":["Acelera búsquedas","Hace lenta"],"ok":0},
            {"q":"¿Pentesting?","opts":["Simular ataque encontrar vulnerabilidades","Antivirus"],"ok":0},
            {"q":"¿Gestión proyectos TI?","opts":["Planear liderar coordinar entregar tiempo","Programar"],"ok":0},
            {"q":"¿ISO 27001?","opts":["Seguridad información","Calidad 9001"],"ok":0},
            {"q":"¿Phishing?","opts":["Engaño robar credenciales","Pescar"],"ok":0},
            {"q":"¿Normalización BD?","opts":["Organizar evitar redundancia","Más grande"],"ok":0},
            {"q":"¿Rol DBA?","opts":["Administrar optimizar asegurar BD","Crear tablas"],"ok":0},
            {"q":"¿Incidente seguridad?","opts":["Compromete confidencialidad","Error pequeño"],"ok":0},
            {"q":"¿Liderazgo ciberseg?","opts":["Coordinar definir políticas capacitar","Antivirus"],"ok":0},
            {"q":"¿SOC?","opts":["Centro operaciones seguridad 24/7","Centro comercial"],"ok":0},
        ]},
        "fullstack": {"nombre":"Desarrollador Fullstack","preguntas":[
            {"q":"¿Fullstack?","opts":["Frontend y backend","Solo frontend"],"ok":0},
            {"q":"¿React?","opts":["Librería frontend JS","BD"],"ok":0},
            {"q":"¿Node.js?","opts":["Entorno backend JS","Navegador"],"ok":0},
            {"q":"¿JWT?","opts":["Token autenticación","Virus"],"ok":0},
            {"q":"¿Responsive?","opts":["Adapta celular pc","Solo pc"],"ok":0},
            {"q":"¿CRUD?","opts":["Create Read Update Delete","Framework"],"ok":0},
            {"q":"¿GitHub?","opts":["Alojar código","Fotos"],"ok":0},
            {"q":"¿Docker?","opts":["Conteneriza app desplegar","Animal"],"ok":0},
            {"q":"¿NoSQL?","opts":["MongoDB no relacional","Solo SQL"],"ok":0},
            {"q":"¿Testing fullstack?","opts":["Probar front back integración","Solo front"],"ok":0},
            {"q":"¿Deploy Vercel/Render?","opts":["Subir nube producción","USB"],"ok":0},
            {"q":"¿Performance web?","opts":["Optimizar velocidad carga","Diseño"],"ok":0},
            {"q":"¿Estado React?","opts":["Datos cambian actualizan UI","Color fijo"],"ok":0},
            {"q":"¿Liderazgo técnico?","opts":["Guiar equipo revisar código definir arquitectura","Programar solo"],"ok":0},
            {"q":"¿Coordinación proyecto?","opts":["Dividir tareas seguimiento entrega","Todo último día"],"ok":0},
        ]},
        "abogado": {"nombre":"Abogado Tutelas PQR Contratación Penal Civil","preguntas":[
            {"q":"¿Término tutela?","opts":["10 días fallo primera","1 año","6 meses"],"ok":0},
            {"q":"¿PQRSD?","opts":["Petición Queja Reclamo Sugerencia Denuncia","Pago rápido"],"ok":0},
            {"q":"¿Sanción disciplinaria abogado?","opts":["Falta ética Consejo Superior","Multa tránsito"],"ok":0},
            {"q":"¿Principio contratación estatal?","opts":["Transparencia economía responsabilidad","Solo precio"],"ok":0},
            {"q":"¿Contrato prestación servicios estatal?","opts":["Sin subordinación actividad específica","Laboral fijo"],"ok":0},
            {"q":"¿Contrato debe tener?","opts":["Objeto plazo valor obligaciones garantías","Solo firma"],"ok":0},
            {"q":"¿Cláusula penal?","opts":["Sanción incumplimiento","Premio"],"ok":0},
            {"q":"¿Acción penal?","opts":["Inicia proceso delito","Civil"],"ok":0},
            {"q":"¿Demanda civil?","opts":["Pretensión juez reconocer derecho","Denuncia penal"],"ok":0},
            {"q":"¿SECOP?","opts":["Sistema Electrónico Contratación Pública","Red social"],"ok":0},
            {"q":"Caso tutela niegan medicamento vital ¿falla?","opts":["No amparó salud vida falta medida provisional","No pasa nada"],"ok":0},
            {"q":"Caso contrato sin pólizas ¿falta?","opts":["Garantías cumplimiento calidad salarios","Firma"],"ok":0},
            {"q":"Redacta ¿qué falta si no hay forma pago?","opts":["Forma pago plazo lugar","Solo objeto"],"ok":0},
            {"q":"¿Caducidad estatal?","opts":["Sanción incumplimiento grave impide continuar","Vencimiento"],"ok":0},
            {"q":"¿Debido proceso sanción contratista?","opts":["Citar escuchar descargos pruebas decisión","Sancionar directo"],"ok":0},
        ]},
        "rrhh_prof": {"nombre":"Profesional RRHH","preguntas":[
            {"q":"¿Plan estratégico talento?","opts":["Alinear talento objetivos","Solo contratar"],"ok":0},
            {"q":"¿Rotación?","opts":["% se va vs promedio","Solo contratados"],"ok":0},
            {"q":"¿Escala salarial?","opts":["Rangos sueldos cargo","Igual todos"],"ok":0},
            {"q":"¿Ley 1010 acoso?","opts":["Prevenir sancionar acoso","Contratación"],"ok":0},
            {"q":"¿Formación desarrollo?","opts":["Capacitar mejorar competencias","Solo inducción"],"ok":0},
            {"q":"¿Compensación beneficios?","opts":["Salario + extras bienestar","Solo salario"],"ok":0},
            {"q":"¿Cultura organizacional?","opts":["Valores comportamientos compartidos","Fiesta fin año"],"ok":0},
            {"q":"¿Reclutamiento 4.0?","opts":["Tecnología redes IA","Periódico"],"ok":0},
            {"q":"¿Entrevista STAR?","opts":["Situación Tarea Acción Resultado","Solo nombre"],"ok":0},
            {"q":"¿Manejo conflicto?","opts":["Mediar comunicación acuerdos","Ignorar"],"ok":0},
            {"q":"¿Bienestar laboral?","opts":["Salud mental familiar crecimiento","Solo salario"],"ok":0},
            {"q":"¿Análisis cargo?","opts":["Funciones requisitos riesgos competencias","Nombre"],"ok":0},
            {"q":"¿Desvinculación respeto?","opts":["Proceso humano legal terminación","Gritar sacar"],"ok":0},
            {"q":"¿Métrica tiempo contratación?","opts":["Días vacante hasta contratación","No medir"],"ok":0},
            {"q":"¿Liderazgo RRHH?","opts":["Influir coordinar equipo objetivos humanos","Mandar"],"ok":0},
        ]},
        "bodeguero": {"nombre":"Bodeguero Almacenamiento","preguntas":[
            {"q":"¿FIFO?","opts":["Primero entra primero sale","Último primero"],"ok":0},
            {"q":"¿Ubicación?","opts":["Pasillo estante nivel encontrar","Tirar donde caiga"],"ok":0},
            {"q":"¿Picking y packing?","opts":["Alistar y empacar","Solo guardar"],"ok":0},
            {"q":"¿Inventario?","opts":["Contar físico vs sistema","No contar"],"ok":0},
            {"q":"¿Estiba?","opts":["Agrupar en pallet","Piso"],"ok":0},
            {"q":"¿Montacargas?","opts":["Equipo mover pallets licencia","Carretilla"],"ok":0},
            {"q":"¿5S bodega?","opts":["Clasificar ordenar limpiar estandarizar disciplina","Limpiar"],"ok":0},
            {"q":"¿Averiada?","opts":["Separar reportar no despachar","Despachar igual"],"ok":0},
            {"q":"¿Kardex?","opts":["Movimientos entrada salida","Producto"],"ok":0},
            {"q":"¿Seguridad bodega?","opts":["Casco botas chaleco normas","Sin EPP"],"ok":0},
            {"q":"¿Recepción mercancía?","opts":["Verificar cantidad estado vs orden","Sin revisar"],"ok":0},
            {"q":"¿Almacenamiento altura?","opts":["Estantería montacargas seguridad","Piso alto"],"ok":0},
            {"q":"¿Despacho?","opts":["Entregar verificado transportador","Sin verificar"],"ok":0},
            {"q":"¿Orden y aseo?","opts":["Limpio señalizado","Sucio"],"ok":0},
            {"q":"¿Reporte diferencia?","opts":["Informar faltante sobrante","Ocultar"],"ok":0},
        ]},
        "quimico_farma": {"nombre":"Químico Farmacéutico","preguntas":[
            {"q":"¿Decreto 677 1995?","opts":["Registro sanitario medicamentos Colombia","Tránsito"],"ok":0},
            {"q":"¿BPM INVIMA?","opts":["Buenas Prácticas Manufactura","Buen pago"],"ok":0},
            {"q":"¿Estabilidad?","opts":["Mantiene calidad tiempo condiciones","Se daña rápido"],"ok":0},
            {"q":"¿Validación?","opts":["Demostrar proceso confiable reproducible","Limpiar"],"ok":0},
            {"q":"¿Farmacia hospitalaria rol QF?","opts":["Gestionar dispensar vigilar uso seguro","Vender"],"ok":0},
            {"q":"¿Farmacovigilancia?","opts":["Detectar prevenir efectos adversos","Vender más"],"ok":0},
            {"q":"¿DCI?","opts":["Denominación Común Internacional principio activo","Marca"],"ok":0},
            {"q":"¿Posología dosis?","opts":["Cómo cuánto administrar","Precio"],"ok":0},
            {"q":"¿Interacción?","opts":["Fármaco altera efecto otro","No pasa nada"],"ok":0},
            {"q":"¿Cadena frío QF?","opts":["Mantener 2-8°C monitorear","Congelar todo"],"ok":0},
            {"q":"¿Resol 1403 2007?","opts":["Modelo gestión servicio farmacéutico Colombia","Tránsito"],"ok":0},
            {"q":"¿Lote trazabilidad?","opts":["Identificar seguir fabricación hasta dispensación","Número"],"ok":0},
            {"q":"¿Formulación magistral?","opts":["Preparación personalizada QF prescripción","Industrial"],"ok":0},
            {"q":"¿Auditoría QF?","opts":["Revisar procesos cumplimiento seguridad paciente","Contar cajas"],"ok":0},
            {"q":"¿Liderazgo QF?","opts":["Coordinar garantizar calidad normativa","Dispensar"],"ok":0},
        ]},
    }

def gen_pdf(dato, tipo="TECNICO"):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=letter)
    c.setFont("Helvetica-Bold", 11); c.setFillColor(HexColor("#2D5A4A"))
    c.drawString(30,750,f"TALENTO INTELIGENTE - BRAGI-IA V12 - {tipo} - CONFIDENCIAL")
    c.setFillColor(HexColor("#2D5A4A"), alpha=0.08); c.setFont("Helvetica-Bold", 30)
    c.saveState(); c.translate(150,300); c.rotate(-24); c.drawString(0,0,"TALENTO INTELIGENTE"); c.restoreState()
    c.setFillColor(HexColor("#000000")); c.setFont("Helvetica", 11)
    y=700
    for k,v in dato.items():
        if y<100: c.showPage(); y=700
        c.drawString(40,y,f"{k}: {str(v)[:95]}"); y-=18
    y-=10; c.setFont("Helvetica-Bold", 11)
    score=int(str(dato.get("score","0%")).replace("%",""))
    if score>=90: rec="RECOMENDACION: CONTRATAR - 90% Excelente altamente confiable"
    elif score>=80: rec="RECOMENDACION: 80% CONTRATAR CON MEJORAS - Bueno plan mejora 30 dias"
    elif score>=60: rec="RECOMENDACION: REGULAR - 60-79% En observacion segunda entrevista"
    else: rec="RECOMENDACION: NO CONTRATAR - 0-59% No cumple minimo"
    c.drawString(40,y,rec)
    c.showPage(); c.save(); buf.seek(0); return buf

if st.session_state.rol is None:
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="card"><h3>🧑‍💼 Candidato</h3></div>', unsafe_allow_html=True)
        ced=st.text_input("Tu cédula", key="login_ced_v12_final")
        if st.button("Ver mis pruebas", key="btn_cand_final", use_container_width=True):
            if ced:
                st.session_state.ced_actual=ced; st.session_state.rol="candidato"; st.rerun()
    with c2:
        st.markdown('<div class="card"><h3>👩‍💼 RRHH</h3></div>', unsafe_allow_html=True)
        u=st.text_input("Usuario", value="admin", key="login_user_final")
        p=st.text_input("Clave", type="password", value="admin123", key="login_pass_final")
        if st.button("Entrar RRHH", key="btn_rrhh_final", type="primary", use_container_width=True):
            if u=="admin" and p=="admin123":
                st.session_state.rol="rrhh"; st.rerun()
    st.stop()

if st.session_state.rol=="rrhh":
    tab1,tab2,tab3,tab4=st.tabs(["📌 Asignar","⚙️ Gestionar Cargos","📊 Dashboard","📚 Estudio"])
    with tab1:
        with st.form("asignar_v12_final"):
            c1,c2=st.columns(2)
            with c1:
                ced=st.text_input("Cédula*"); nom=st.text_input("Nombre*")
            with c2:
                cargo_key=st.selectbox("Cargo*", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"])
                asig=st.text_input("Asignado por*", value="Maria C. RRHH")
            if st.form_submit_button("✅ Asignar prueba", type="primary", use_container_width=True):
                st.session_state.asignaciones.append({"cedula":ced,"nombre":nom,"cargo_key":cargo_key,"cargo_nombre":st.session_state.cargos_db[cargo_key]["nombre"],"asignado_por":asig,"fecha":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"Asignado {nom} - {st.session_state.cargos_db[cargo_key]['nombre']} por {asig}")
    with tab2:
        cargo_sel=st.selectbox("Cargo editar", list(st.session_state.cargos_db.keys()), format_func=lambda x: st.session_state.cargos_db[x]["nombre"], key="edit_sel_final")
        st.write(f"Preguntas: {len(st.session_state.cargos_db[cargo_sel]['preguntas'])}")
        st.dataframe(pd.DataFrame([{"#":i+1,"Pregunta":p["q"]} for i,p in enumerate(st.session_state.cargos_db[cargo_sel]["preguntas"])]), use_container_width=True)
        with st.expander("➕ Agregar pregunta"):
            q=st.text_input("Pregunta nueva"); o1=st.text_input("Opción correcta"); o2=st.text_input("Opción 2"); o3=st.text_input("Opción 3")
            if st.button("Agregar"):
                if q and o1:
                    st.session_state.cargos_db[cargo_sel]["preguntas"].append({"q":q,"opts":[o1,o2 or "Opción 2",o3 or "Opción 3"],"ok":0}); st.rerun()
        if st.button("🗑️ Borrar última pregunta"):
            if st.session_state.cargos_db[cargo_sel]["preguntas"]: st.session_state.cargos_db[cargo_sel]["preguntas"].pop(); st.rerun()
    with tab3:
        if st.session_state.resultados:
            df=pd.DataFrame(st.session_state.resultados)
            c1,c2,c3,c4=st.columns(4)
            with c1: st.metric("Entrevistas", len(df))
            with c2: st.metric("Promedio", f"{df['score_num'].mean():.1f}%")
            with c3: st.metric(">=80% Contratables", len(df[df["score_num"]>=80]))
            with c4: st.metric(">=90% Excelentes", len(df[df["score_num"]>=90]))
            st.bar_chart(df["cargo_nombre"].value_counts())
            st.dataframe(df, use_container_width=True)
            for i,r in enumerate(df.to_dict(orient="records")):
                pdf=gen_pdf(r, f"TECNICO {r['cargo_nombre']}")
                st.download_button(f"📄 PDF {r['cedula']} {r['cargo_nombre']} {r['score']}", pdf, f"{r['cedula']}_{r['cargo_nombre']}.pdf", "application/pdf", key=f"pdf_{i}")
        else: st.info("Sin resultados aún")
    with tab4:
        st.write("**Módulo Estudio:** Excel, Psicología DISC, Casos Tutela, Contratos, RIPS, Logística, etc por cargo")
    if st.button("Cerrar sesión", key="close_rrhh_final"): st.session_state.rol=None; st.rerun()

if st.session_state.rol=="candidato":
    ced=st.session_state.ced_actual
    mis=[a for a in st.session_state.asignaciones if a["cedula"]==ced]
    if not mis:
        st.error(f"Tu cédula {ced} sin pruebas");
        if st.button("Volver"): st.session_state.rol=None; st.rerun()
        st.stop()
    for idx,asig in enumerate(mis):
        cargo=st.session_state.cargos_db.get(asig["cargo_key"])
        if not cargo: continue
        st.markdown(f'<div class="card"><h3>{cargo["nombre"]} - Asignado por {asig["asignado_por"]}</h3></div>', unsafe_allow_html=True)
        with st.form(f"form_{asig['cargo_key']}_{ced}_{idx}"):
            respuestas=[]
            for i,preg in enumerate(cargo["preguntas"]):
                st.write(f"**{i+1}. {preg['q']}**")
                r=st.radio("Elige", preg["opts"], index=None, key=f"r_{asig['cargo_key']}_{ced}_{idx}_{i}")
                respuestas.append(r)
            st.text_area("Caso práctico / Redacta contrato / Resuelve tutela (solo abogados obligatorio)", key=f"caso_{ced}_{idx}")
            if st.form_submit_button("🚀 FINALIZAR - Envío automático RRHH", type="primary", use_container_width=True):
                aciertos=sum(1 for j,resp in enumerate(respuestas) if resp==cargo["preguntas"][j]["opts"][cargo["preguntas"][j]["ok"]])
                score=int((aciertos/len(cargo["preguntas"]))*100) if cargo["preguntas"] else 0
                if score>=90: rango="90% CONTRATAR - Positivo"
                elif score>=80: rango="80% CONTRATAR CON MEJORAS"
                elif score>=60: rango="REGULAR - Observación"
                else: rango="NO CONTRATAR"
                st.session_state.resultados.append({"cedula":ced,"nombre":asig["nombre"],"cargo_key":asig["cargo_key"],"cargo_nombre":cargo["nombre"],"asignado_por":asig["asignado_por"],"fecha_asignacion":asig["fecha"],"score":f"{score}%","score_num":score,"rango":rango,"aciertos":f"{aciertos}/{len(cargo['preguntas'])}","fecha_final":datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.balloons(); st.success(f"✅ {score}% {rango} - Enviado a RRHH historial")
    if st.button("Cerrar sesión cand", key="close_cand_final"): st.session_state.rol=None; st.rerun()
