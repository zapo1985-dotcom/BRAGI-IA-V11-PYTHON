from flask import Flask, render_template_string, request
import json, os, random
app = Flask(__name__)
DB="bragi_db.json"
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump({"a":[],"r":[]},f)
def load():
    with open(DB) as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f)

HTML="""
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--v:#2D5A4A;--c:#F2F3F4;--o:#2B2F32}
body{margin:0;font-family:sans-serif;background:var(--c);position:relative}
body::before{content:"TALENTO INTELIGENTE • BRAGI-IA • ";position:fixed;top:-30%;left:-60%;width:300%;height:250%;font-size:22px;color:rgba(45,90,74,0.07);font-weight:900;transform:rotate(-24deg);white-space:nowrap;pointer-events:none;line-height:100px}
header{background:var(--o);color:white;padding:12px 20px}
.card{background:white;border-radius:20px;padding:20px;margin:16px;position:relative;z-index:1}
.btn{padding:12px 22px;border-radius:30px;border:none;font-weight:800}
.btnV{background:var(--v);color:white}
</style></head><body>
<header><h2>BRAGI-IA V11 PYTHON - TALENTO INTELIGENTE</h2></header>
<div>{{c|safe}}</div></body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, c='<div class="card"><h2>Login</h2><form method="POST" action="/login"><input name="cedula" placeholder="Cedula candidato 123" style="width:100%;padding:12px;border-radius:12px"><button class="btn btnV">Entrar Candidato</button></form><hr><form method="POST" action="/login"><input name="user" value="admin" style="width:100%;padding:12px;border-radius:12px"><input name="pass" value="admin123" type="password" style="width:100%;padding:12px;border-radius:12px"><button class="btn btnV">Entrar RRHH</button></form></div>')

@app.route("/login", methods=["POST"])
def login():
    db=load(); ced=request.form.get("cedula",""); user=request.form.get("user","")
    if user=="admin":
        rows="".join([f"<tr><td>{x['ced']}</td><td>{x['nom']}</td><td>{x['mod']}</td><td>{x['asig']}</td><td>{x['sc']}%</td></tr>" for x in db["r"]])
        return render_template_string(HTML, c=f'<div class="card"><h2>Asignar</h2><form method="POST" action="/asignar"><input name="ced" placeholder="Cedula"><input name="nom" placeholder="Nombre"><select name="mod"><option value="excel">Excel</option><option value="abogados">Abogados</option><option value="quimico">Quimico</option></select><input name="asig" value="RRHH"><button class="btn btnV">Asignar</button></form></div><div class="card"><table border=1 width=100%><tr><th>Ced</th><th>Nombre</th><th>Modulo</th><th>Asignado por</th><th>Result</th></tr>{rows}</table></div>')
    if ced:
        return render_template_string(HTML, c=f'<div class="card"><h2>Modulo para {ced}</h2><form method="POST" action="/fin/{ced}"><p>1. Que hace BUSCARV?<br><input type="radio" name="q0"> Busca</p><button class="btn btnV" style="width:100%">FINALIZAR - Envio auto a RRHH</button></form></div>')
    return "Error"

@app.route("/asignar", methods=["POST"])
def asig():
    db=load(); db["a"].append({"ced":request.form["ced"],"nom":request.form["nom"],"mod":request.form["mod"],"asig":request.form["asig"]}); save(db); return "Asignado <a href=/>Volver</a>"

@app.route("/fin/<ced>", methods=["POST"])
def fin(ced):
    db=load(); a=[x for x in db["a"] if x["ced"]==ced]; sc=random.randint(85,96); db["r"].append({"ced":ced,"nom":a[0]["nom"] if a else ced,"mod":a[0]["mod"] if a else "excel","asig":a[0]["asig"] if a else "RRHH","sc":sc}); save(db); return render_template_string(HTML, c=f'<div class="card"><h1>✅ {sc}% Guardado automatico en RRHH</h1><a href="/">Volver</a></div>')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
