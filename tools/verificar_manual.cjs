const fs=require("fs"),path=require("path"),http=require("http"),crypto=require("crypto"),cp=require("child_process");
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||"playwright");
const root=path.resolve(__dirname,".."),qa=process.env.ISC_QA_DIR||path.join(require("os").tmpdir(),"isc-branding-autonomia-qa-20261118");
fs.mkdirSync(qa,{recursive:true});
const old=cp.execFileSync("git",["show","dfe8806f801172a59809f0204bfa9f8f7acc4094:brand-book.html"],{cwd:root,encoding:"utf8",maxBuffer:3000000}).replace("<head>","<head><base href=\"/\">");
const types={".html":"text/html; charset=utf-8",".css":"text/css",".js":"application/javascript",".svg":"image/svg+xml",".png":"image/png",".jpg":"image/jpeg",".woff2":"font/woff2"};
const server=http.createServer((req,res)=>{let pathname=decodeURIComponent(new URL(req.url,"http://localhost").pathname);if(pathname==="/__original.html"){res.writeHead(200,{"Content-Type":"text/html; charset=utf-8"});res.end(old);return;}
if(pathname.endsWith("/"))pathname+="index.html";const p=path.resolve(root,"."+pathname);
if(!p.startsWith(root+path.sep)||pathname.includes("/.git")){res.writeHead(403);res.end();return;}
fs.readFile(p,(err,b)=>{if(err){res.writeHead(404);res.end("missing");return;}res.writeHead(200,{"Content-Type":types[path.extname(p)]||"application/octet-stream"});res.end(b);});});
(async()=>{let browser;try{
await new Promise(ok=>server.listen(0,"127.0.0.1",ok));const base="http://127.0.0.1:"+server.address().port;
browser=await chromium.launch({headless:true});const context=await browser.newContext();const broken=[],errors=[],external=[];
await context.route("https://fonts.googleapis.com/**",r=>r.fulfill({status:200,contentType:"text/css",body:fs.readFileSync(path.join(root,"assets/fontes/isc-fontes.css"),"utf8")}));
const page=await context.newPage();
page.on("pageerror",e=>errors.push(String(e)));page.on("response",r=>{if(r.status()>=400)broken.push({url:r.url(),status:r.status()});});
page.on("request",r=>{if(r.url().startsWith("http")&&!r.url().startsWith(base)&&!r.url().includes("fonts.googleapis.com"))external.push(r.url());});
await page.setViewportSize({width:1440,height:1000});
async function ready(url){await page.goto(url,{waitUntil:"networkidle"});await page.evaluate(async()=>{for(const img of document.images)img.loading="eager";await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});await page.waitForLoadState("networkidle");await page.addStyleTag({content:"*,*::before,*::after{animation:none!important;transition:none!important}"});await page.evaluate(()=>scrollTo(0,0));}
await ready(base+"/__original.html");const baseline=await page.screenshot({path:qa+"/original-desktop.png"});
await ready(base+"/brand-book.html");const current=await page.screenshot({path:qa+"/copia-desktop.png"});
const desktop=await page.evaluate(()=>({title:document.title,sections:document.querySelectorAll('section[id^="s-"]').length,images:document.images.length,brokenImages:[...document.images].filter(i=>i.currentSrc&&i.complete&&i.naturalWidth===0).map(i=>i.currentSrc),fonts:[document.fonts.check('400 28px "Gilda Display"'),document.fonts.check('500 18px "EB Garamond"'),document.fonts.check('600 18px Montserrat')],scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth}));
await page.setViewportSize({width:390,height:844});await ready(base+"/brand-book.html");await page.screenshot({path:qa+"/copia-mobile.png"});
const mobile=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth,sections:document.querySelectorAll('section[id^="s-"]').length}));
const report={desktop,mobile,desktopPixelsIdentical:baseline.equals(current),baselineSha256:crypto.createHash("sha256").update(baseline).digest("hex"),copySha256:crypto.createHash("sha256").update(current).digest("hex"),brokenResponses:broken,pageErrors:errors,externalRequests:[...new Set(external)]};
fs.writeFileSync(qa+"/verificacao-local.json",JSON.stringify(report,null,2));console.log(JSON.stringify(report));
if(broken.length||errors.length||external.length||desktop.brokenImages.length||desktop.sections!==24||!desktop.fonts.every(Boolean)||mobile.scrollWidth>mobile.viewport||!report.desktopPixelsIdentical)process.exitCode=1;
}finally{if(browser)await browser.close();await new Promise(ok=>server.close(ok));}})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
