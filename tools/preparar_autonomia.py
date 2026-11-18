#!/usr/bin/env python3
"""Prepara hospedagem ISC na conta do titular sem alterar conteúdo editorial.
Uso: python3 tools/preparar_autonomia.py. Python padrão; sem instalação nem rede.
A versão original permanece no histórico Git e no manifesto de preservação.
"""
from pathlib import Path
import base64,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent.parent
OWNER="sharbocasagrande-ai"
SITE=f"https://{OWNER}.github.io/branding-isc/"
OLD_SITE="https://rafaelnasch.github.io/branding-isc/"
OLD_REPO="https://github.com/rafaelnasch/branding-isc"
DATE="2026-11-18"
BT=chr(96)

def main():
    manifest=ROOT/"preservation"/f"original-{DATE}.json"
    if not manifest.exists():
        entries=[]
        raw=subprocess.check_output(["git","ls-tree","-rz","HEAD"],cwd=ROOT)
        for item in raw.split(b"\0"):
            if not item:continue
            info,name=item.split(b"\t",1)
            mode,typ,sha=info.decode().split()
            if typ!="blob":continue
            rel=name.decode();b=(ROOT/rel).read_bytes()
            gitsha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
            if gitsha!=sha:raise RuntimeError("Arquivo original divergente: "+rel)
            entries.append({"path":rel,"mode":mode,"git_blob":sha,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
        record={"date":DATE,"source_repository":"rafaelnasch/branding-isc","owner_repository":f"{OWNER}/branding-isc",
                "original_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
                "original_tree":subprocess.check_output(["git","rev-parse","HEAD^{tree}"],cwd=ROOT,text=True).strip(),
                "original_files":entries,"scope":"Cópia exata original no commit/tag; hospedagem posterior altera só dependências e instruções de distribuição."}
        manifest.parent.mkdir(exist_ok=True);manifest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    css=(ROOT/"assets/fontes/google-6956886754.css").read_text()
    faces=[]
    for alphabet,body in re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})",css):
        if alphabet not in ("latin","latin-ext"):continue
        def embed(m):
            p=ROOT/"assets/fontes"/m.group(1).rsplit("/",1)[-1]
            if not p.is_file():raise RuntimeError("Fonte original ausente: "+p.name)
            return "url(data:font/woff2;base64,"+base64.b64encode(p.read_bytes()).decode()+")"
        faces.append("/* "+alphabet+" */\n"+re.sub(r"url\((https://fonts\.gstatic\.com/[^)]+)\)",embed,body))
    if len(faces)!=12:raise RuntimeError("Cobertura inesperada das fontes: "+str(len(faces)))
    localcss="/* Mesmas fontes do manual original; cópia local sob licença SIL OFL. */\n"+"\n".join(faces)+"\n"
    (ROOT/"assets/fontes/isc-fontes.css").write_text(localcss)
    for name in ("brand-book.html","deck-template.html","lockup.html"):
        p=ROOT/name;s=p.read_text()
        s=re.sub(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>\n?',"",s)
        s=re.sub(r'<link\b[^>]*href="https://fonts\.googleapis\.com/[^"]+"[^>]*>',
                 '<link href="assets/fontes/isc-fontes.css" rel="stylesheet">',s)
        p.write_text(s)
    p=ROOT/"autocontido.py";s=p.read_text()
    marker="    # 0. fontes do Google embutidas na própria <style> (continua uma <style> só)"
    addition='''    # Fonte local da cópia ISC: mantém a exportação independente da rede.
    local_link = '<link href="assets/fontes/isc-fontes.css" rel="stylesheet">'
    if local_link in html:
        local_css = open(os.path.join(FONTES, "isc-fontes.css"), encoding="utf-8").read()
        html = html.replace(local_link, "")
        html = html.replace("<style>", "<style>\\n" + local_css, 1)
'''
    if "# Fonte local da cópia ISC" not in s:
        if marker not in s:raise RuntimeError("Exportador mudou: revisar antes de adaptar")
        s=s.replace(marker,addition+marker);p.write_text(s)
    p=ROOT/"tools/empacotar_skill.py";s=p.read_text().replace(OLD_SITE,SITE)
    s=s.replace('("fontes", "*.css")):', '("fontes", "*.css"), ("fontes", "*.txt")):')
    p.write_text(s)
    p=ROOT/"SKILL.md";s=p.read_text().replace(OLD_SITE,SITE)
    s=s.replace("do Releases (execução de código ligada)","da pasta downloads do manual (execução de código ligada)")
    s=s.replace("4. **Fontes:** continuam pelo link do Google Fonts.",
        "4. **Fontes:** use a cópia local em "+BT+"assets/fontes/isc-fontes.css"+BT+"; para arquivo único, embuta o CSS.")
    s=s.replace('<link href="https://fonts.googleapis.com/css2?family=Gilda+Display&family=EB+Garamond:ital,wght@1,400;1,500&family=Montserrat:wght@400;500;600&display=swap" rel="stylesheet">',
        '<link href="assets/fontes/isc-fontes.css" rel="stylesheet">')
    p.write_text(s)
    p=ROOT/"README.md";s=p.read_text().replace(OLD_SITE,SITE).replace(OLD_REPO,f"https://github.com/{OWNER}/branding-isc")
    s=s.replace(f"https://github.com/{OWNER}/branding-isc/releases/latest/download/branding-isc.zip",SITE+"downloads/branding-isc.zip")
    s=s.replace(f"https://github.com/{OWNER}/branding-isc/releases/latest",SITE+"downloads/")
    s=s.replace(f"https://github.com/{OWNER}/branding-isc/releases",SITE+"downloads/")
    s=s.replace("[rafaelnasch.github.io/branding-isc]",f"[{OWNER}.github.io/branding-isc]")
    s=s.replace("do Releases","de Downloads").replace("[Releases]","[Downloads]").replace("página de **Releases**","página de **Downloads**")
    heading="# branding-isc · a identidade visual do Instituto ISC como skill\n"
    note=f"\n> **Cópia administrada por SHARBO CASAGRANDE.** Manual, recursos, fontes e pacote de instalação hospedados na conta {BT}sharbocasagrande-ai{BT}. Conteúdo e créditos originais preservados; detalhes da preservação em [AUTONOMIA.md](AUTONOMIA.md).\n"
    if "Cópia administrada por SHARBO CASAGRANDE" not in s:s=s.replace(heading,heading+note,1)
    p.write_text(s)
    (ROOT/".nojekyll").touch()
    p=ROOT/".gitignore";s=p.read_text()
    if "!downloads/branding-isc.zip" not in s:s+="\n!downloads/branding-isc.zip\n"
    p.write_text(s)
    d=ROOT/"downloads";d.mkdir(exist_ok=True)
    (d/"index.html").write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Downloads ISC</title><style>body{background:#121314;color:#F5F0E6;font:18px system-ui;max-width:700px;margin:12vh auto;padding:24px}a{color:#E6C28A;line-height:2}</style><h1>Arquivos do Instituto ISC</h1><p>Cópia administrada por SHARBO CASAGRANDE.</p><p><a href="branding-isc.zip" download>Baixar a skill completa para instalação</a></p><p><a href="../brand-book.html">Abrir o manual de marca</a></p><p><a href="https://github.com/sharbocasagrande-ai/branding-isc/archive/refs/heads/main.zip">Baixar todos os arquivos do repositório</a></p></html>\n''')
    print(json.dumps({"source_files_preserved":len(json.loads(manifest.read_text())["original_files"]),"font_faces":len(faces),"site":SITE},ensure_ascii=False))
if __name__=="__main__":main()
