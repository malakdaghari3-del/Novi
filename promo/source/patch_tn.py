import sys;p=sys.argv[1];s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a));s=s.replace(a,b)
# ---- head: font + timeline + css ----
R('<style>','<link rel="stylesheet" href="assets/fonts/cairo.css"><script src="tl.js"></script>\n<style>')
R('.big{font-size:156px;','''.ar{font-family:Cairo,Inter,sans-serif;direction:rtl;unicode-bidi:plaintext}
.arh{font-family:Cairo,Inter,sans-serif;font-weight:800;white-space:nowrap;direction:rtl;letter-spacing:0}
.arh .w{padding:0 .06em .2em}
.fcard{width:560px;height:640px;border-radius:24px;background:linear-gradient(170deg,#f8f1e4,#eadfcb);color:#3b2416;padding:34px 36px;box-shadow:0 40px 90px rgba(0,0,0,.6),0 0 60px rgba(255,80,160,.18);font-family:Inter,'IPAGothic','WenQuanYi Zen Hei',sans-serif}
.fcard .t{font-size:40px;font-weight:900;color:#6b2d12;font-family:'IPAGothic','WenQuanYi Zen Hei',sans-serif}
.fcard .st{font-size:20px;font-weight:600;color:#8a5a3c;margin:6px 0 22px}
.fcard .h{font-size:22px;font-weight:900;letter-spacing:.05em;margin-bottom:8px}
.fcard .x{font-size:25px;line-height:1.7;font-weight:500;font-family:'IPAGothic','WenQuanYi Zen Hei',sans-serif}
.fcard .nut{margin-top:22px;border-top:3px solid #3b2416}.fcard .nut div{height:16px;border-bottom:1px solid rgba(59,36,22,.35);margin-top:8px}
.pill{padding:14px 26px;border-radius:999px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.18);font-size:30px;font-weight:700;white-space:nowrap}
.qm{font-family:Cairo,Inter,sans-serif;font-weight:900;color:#ff6fb5;text-shadow:0 0 30px rgba(255,80,170,.9)}
.chem{padding:18px 30px;border-radius:999px;background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.04));border:1.5px solid rgba(255,130,185,.4);font-size:32px;font-weight:700;white-space:nowrap;box-shadow:0 0 30px rgba(255,80,160,.15);position:absolute}
.chem b{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#ff5fb0;margin-left:14px;font-family:Cairo;font-size:26px;vertical-align:middle;box-shadow:0 0 16px rgba(255,80,170,.8)}
.num{font-size:300px;font-weight:900;letter-spacing:-0.05em;line-height:1;white-space:nowrap}
.dot{width:40px;height:40px;border-radius:50%;border:2.5px solid rgba(255,255,255,.25);position:absolute}
.big{font-size:156px;''')
# ---- texts ----
R('<div id="tagl" class="a tagl">Smart label analyser, powered by AI</div>','<div id="tagl" class="a tagl ar" style="font-size:40px;font-weight:700">تطبيقة تخدم بالـ AI</div>')
R('<div id="cta" class="a cta">Try it free<div','<div id="cta" class="a cta ar" style="font-size:42px">جرّبها بلاش<div')
R('<div id="fine" class="a fine">3 free scans &nbsp;·&nbsp; no account needed</div>','<div id="fine" class="a fine ar" style="font-size:26px">3 scans بلاش &nbsp;·&nbsp; من غير compte</div>')
R('<div id="psub" class="a cap">Novi flags them on <b>every scan</b>.</div>','<div id="psub" class="a cap ar" style="font-size:36px">Novi ينبّهك عليهم في <b>كل scan</b></div>')
R('<div id="althead" class="a althead">Better alternatives<small>📍 Sold in 🇺🇸 United States</small></div>','<div id="althead" class="a althead ar" style="text-align:right">بدائل لمنتوجك المفضّل<small>📍 متوفّرين في 🇫🇷 France</small></div>')
R('<div class="thumb">🌻</div><div><div class="aname">Sunflower Cocoa Spread</div><div class="asub">Nut-free · No palm oil</div>','<div class="thumb">🧴</div><div><div class="aname">Gentle Shampoo</div><div class="asub">Sulfate-free · Silicone-free</div>')
R('<div class="thumb">🥣</div><div><div class="aname">Oat Choco Cream</div><div class="asub">Dairy-free · Vegan</div>','<div class="thumb">🫙</div><div><div class="aname">Hydrating Cream</div><div class="asub">Paraben-free · Fragrance-free</div>')
R('<div class="thumb">🍫</div><div><div class="aname">Dark Cocoa Spread</div><div class="asub">No palm oil · Low sugar</div>','<div class="thumb">🌿</div><div><div class="aname">Natural Conditioner</div><div class="asub">Silicone-free · Vegan</div>')
R('<div id="t1" class="a big"></div>\n  <div id="t2" class="a big"></div>','<div id="t1" class="a big arh" style="font-size:118px"></div>\n  <div id="t2" class="a big arh" style="font-size:118px"></div>')
# new scene DOM
R('<!-- S8 -->','''<!-- A: foreign label -->
  <div id="aOrb"></div>
  <div id="aH1" class="a arh line" style="font-size:70px"></div>
  <div id="aChip" class="a pill">📍 東京 · Japan</div>
  <div id="aCard" class="a fcard"><div class="t">ヘーゼルナッツスプレッド</div><div class="st">内容量 400g · ココア入り</div><div class="h">原材料名：</div>
    <div class="x">砂糖、パーム油、ヘーゼルナッツ（13%）、脱脂粉乳、低脂肪ココアパウダー、乳化剤（大豆レシチン）、香料</div><div class="nut"><div></div><div></div><div></div><div></div></div></div>
  <div id="aQ0" class="a qm" style="font-size:150px">?</div><div id="aQ1" class="a qm" style="font-size:110px">?</div><div id="aQ2" class="a qm" style="font-size:90px">?</div><div id="aQ3" class="a qm" style="font-size:130px">?</div>
  <div id="aH2" class="a arh line" style="font-size:66px"></div>
  <!-- B: chemical names -->
  <div id="bH1" class="a arh line" style="font-size:66px"></div>
  <div id="bQ" class="a qm" style="font-size:380px;line-height:1">؟</div>
  <div id="bChems"></div>
  <div id="bH2" class="a arh line" style="font-size:96px"></div>
  <!-- E headline -->
  <div id="eH" class="a" style="text-align:center"><div class="arh grad" style="font-size:120px;line-height:1.1">صوّر</div><div style="font-size:42px;font-weight:700;color:rgba(255,255,255,.85);white-space:nowrap">la liste des ingrédients</div></div>
  <div id="eH2" class="a arh" style="font-size:52px">يترجملك على حسب <span class="grad">احتياجاتك</span></div>
  <!-- H: 12 languages -->
  <div id="hH" class="a arh line" style="font-size:72px"></div>
  <div id="hGlobe" class="a" style="font-size:230px;filter:drop-shadow(0 0 40px rgba(255,90,170,.6))">🌍</div>
  <div id="hNum" class="a num grad">1</div>
  <div id="hLab" class="a" style="font-size:44px;font-weight:700;color:#ff9fcb;white-space:nowrap">languages</div>
  <div id="hDots"></div>
  <!-- S8 -->''')
# ---- build helpers for new text ----
R("const t1l=letters($('t1'),'Scan smarter.',5);\nconst t2l=letters($('t2'),'Shop safer.',5);",
"""function arWords(el,arr){el.innerHTML=arr.map(([w,c])=>`<span class="${c||''}">${w}</span>`).join(' ');return [...el.children]}
const t1l=arWords($('t1'),[['موش'],['المهم'],['كان'],['شنوّا'],['تشري،','grad']]);
const t2l=arWords($('t2'),[['المهم'],['زادة'],['تعرف'],['شنوّا','grad'],['فيه.','grad']]);
const aH1w=words($('aH1'),[['تخيّل'],['روحك'],['في'],['supermarché'],['في'],['بلاد'],['أخرى…','grad']]);
const aH2w=words($('aH2'),[['أما'],['المكوّنات'],['بلغة'],['ما','grad'],['تفهمهاش','grad']]);
const bH1w=words($('bH1'),[['و'],['حتى'],['كان'],['تفهمها…']]);
const bH2w=words($('bH2'),[['شنوّا'],['معناها؟','grad']]);
const hHw=words($('hH'),[['و'],['أحسن'],['حاجة…','grad']]);
const CHEMS=[['Sodium Laureth Sulfate',500,380],['Methylparaben',1430,360],['Dimethicone',400,560],['Phenoxyethanol',1520,560],['Cyclopentasiloxane',520,745],['Propylparaben',1410,750]];
$('bChems').innerHTML=CHEMS.map(([c],i)=>`<div class="a chem" id="ch${i}">${c}<b>؟</b></div>`).join('');
const AORB=['Zucker','Sucre','Azúcar','Сахар','설탕','Şeker','Cukier','Açúcar','Zucchero','糖','Suiker','Socker'];
$('aOrb').innerHTML=AORB.map((w,i)=>`<div class="a orb" id="ao${i}">${w}</div>`).join('');
$('hDots').innerHTML=Array.from({length:12},(_,i)=>`<div class="a dot" id="hd${i}"></div>`).join('');""")
# prefs: 3 cosmetics nodes
R("const PREFS=[['🥛','Dairy-free'],['🌱','Vegan'],['🥖','Gluten-free'],['🥜','Nut allergy'],['🍬','Low sugar'],['🐟','Shellfish']];\nconst NX=[330,582,834,1086,1338,1590];\nconst NY=NX.map((x,i)=>475-75*Math.sin(Math.PI*(i+.5)/6));",
  "const PREFS=[['🧴','Paraben'],['🫧','Sulfate'],['💧','Silicone']];\nconst NX=[620,960,1300];\nconst NY=[485,450,485];")
R("const pt=words($('ptitle'),[[\"Set\"],[\"your\"],[\"preferences\"],[\"once.\",\"grad\"]]);","$('ptitle').classList.add('arh');const pt=words($('ptitle'),[['عندك'],['حساسية','grad'],['من…']]);")
R("const tw=[15.35,15.5,15.65,15.92];pt.forEach","const tw=[15.35,15.55,15.8];pt.forEach")
# chat removed from ask scene
R("  // user bubble\n  {","  ['ailab1','bu','ailab2','dots','ba'].forEach(i=>hide($(i)));\n  if(false){")
R("  const hq=te=>eo(P(te,19.75,20.05));trail(P_Q","  const hq=te=>0;if(0)trail(P_Q")
R("  // AI typing + answer\n  {","  if(false){")
R("const h1=P(t,19.75,19.95)*(1-P(t,21.05,21.3)), h2=","const h1=0, h2=")
# tagline: underlines computed from measured widths
R("const P_U1=makePath([[530,575],[960,566],[1390,575]]);\nconst P_U2=makePath([[560,758],[960,749],[1360,758]]);",
  "let P_U1=makePath([[530,585],[960,576],[1390,585]]);\nlet P_U2=makePath([[560,768],[960,759],[1360,768]]);")
R("l.style.transform=`translateY(${(1-e)*90}px) rotate(${(1-e)*8}deg)`;l.style.opacity=cl(p*3);l.style.filter=p<1?`blur(${(1-e)*8}px)`:'none'});\n  T($('t2')",
  "l.style.transform=`translateY(${(1-e)*90}px)`;l.style.opacity=cl(p*3);l.style.filter=p<1?`blur(${(1-e)*8}px)`:'none'});\n  T($('t2')")
R("const p=P(t,23.75+i*.028,23.75+i*.028+.45)","const p=P(t,23.75+i*.09,23.75+i*.09+.45)")
R("l.style.transform=`translateY(${(1-e)*90}px) rotate(${(1-e)*8}deg)`;l.style.opacity=cl(p*3);l.style.filter=p<1?`blur(${(1-e)*8}px)`:'none'});\n  // underlines",
  "l.style.transform=`translateY(${(1-e)*90}px)`;l.style.opacity=cl(p*3);l.style.filter=p<1?`blur(${(1-e)*8}px)`:'none'});\n  // underlines")
R("const p=P(t,24.95+i*.03,24.95+i*.03+.45)","const p=P(t,24.95+i*.09,24.95+i*.09+.45)")
# logo: tagline text per use; mascot idle uses real time
R("  const tp=eo(P(d,.6,1.1));","  $('tagl').textContent=t0===26.7?'افهم شنوّا تشري':'تطبيقة تخدم بالـ AI';\n  const tp=eo(P(d,.6,1.1));")
R("const bob=d>.55?Math.sin((d-.55)*3.2)*9:0, br=1+.012*Math.sin(d*2.6);","const bob=d>.55?Math.sin(RT*3.2)*9:0, br=1+.012*Math.sin(RT*2.6);")
R("T(el,{x,y:y+bob+(1-eo(ip))*120,s,sx,r:(flip?-1:1)*2*Math.sin(d*1.9),","T(el,{x,y:y+bob+(1-eo(ip))*120,s,sx,r:(flip?-1:1)*2*Math.sin(RT*1.9),")
# ---- new render ----
a=s.index('function render(t){');b=s.index('window.render=render;')
s=s[:a]+r'''let RT=0;
function mapK(u,K){if(u<=K[0][0])return K[0][1];for(let i=1;i<K.length;i++){if(u<=K[i][0]){const [a0,b0]=K[i-1],[a1,b1]=K[i];return lerp(b0,b1,(u-a0)/Math.max(1e-6,a1-a0))}}return K[K.length-1][1]}
function headIn(ws,u,t0,st=.12){ws.forEach((w,i)=>{const p=eo5(P(u,t0+i*st,t0+i*st+.5));w.style.transform=`translateY(${(1-p)*115}%)`})}
function sceneA(u,d,sp){
  const on=u>=0&&u<d+.05;const ids=['aH1','aChip','aCard','aQ0','aQ1','aQ2','aQ3','aH2'];
  if(!on){ids.forEach(i=>hide($(i)));AORB.forEach((_,i)=>hide($('ao'+i)));return}
  const x=eio(P(u,d-.4,d)),xa=1-x,xb=14*x;
  T($('aH1'),{y:150-20*x,a:xa,blur:xb});headIn(aH1w,u,.15,.1);
  const cp=P(u,.6,1.25),ce=eo(cp);
  T($('aCard'),{y:lerp(1300,555,ce)+8*Math.sin(u*1.6),s:lerp(.8,.82,ce)*(1-.15*x),rx:lerp(40,6,ce),ry:lerp(-30,-10,ce)+5*Math.sin(u*.9),persp:1600,a:cl(cp*3)*xa,blur:xb});
  const chp=P(u,1.1,1.5);T($('aChip'),{x:1460,y:300,s:lerp(.5,1,eb(chp)),a:cl(chp*3)*xa,blur:xb});
  glowAt(960,560,520,.16*ce*xa);
  const sl=sp-0.0;
  [[1290,430,-12],[650,380,10],[700,760,-8],[1260,780,14]].forEach(([qx,qy,r],i)=>{const p=P(u,sl+.15+i*.16,sl+.55+i*.16);
    T($('aQ'+i),{x:qx,y:qy+6*Math.sin(u*3+i),r:r+6*Math.sin(u*2+i),s:lerp(.2,1,eb(p)),a:cl(p*3)*xa,blur:xb})});
  T($('aH2'),{y:955+20*x,a:(u>sl-.05?1:0)*xa,blur:xb});headIn(aH2w,u,sl,.12);
  AORB.forEach((w,i)=>{const ang=i/AORB.length*6.283+u*.15;const z=Math.sin(ang);T($('ao'+i),{x:960+760*Math.cos(ang),y:540+380*z*.85,s:.7+.25*(z+1)/2,a:P(u,.2+i*.04,.7+i*.04)*(.08+.12*(z+1)/2)*xa,blur:(1-z)*2+xb})});
}
function sceneB(u,d){
  const on=u>=0&&u<d+.05;
  if(!on){['bH1','bQ','bH2'].forEach(i=>hide($(i)));CHEMS.forEach((_,i)=>hide($('ch'+i)));return}
  const x=eio(P(u,d-.45,d-.05)),xa=1-x;
  T($('bH1'),{y:170-20*x,a:xa,blur:14*x});headIn(bH1w,u,.05,.1);
  const qp=P(u,.25,.7);T($('bQ'),{y:520+10*Math.sin(u*2.5),s:lerp(.3,1,eb(qp))*(1-.5*x),r:6*Math.sin(u*2),a:cl(qp*3)*xa,blur:14*x});
  glowAt(960,520,420,.25*eo(qp)*xa);
  CHEMS.forEach(([c,cx,cy],i)=>{const p=P(u,.2+i*.13,.6+i*.13);const dx=(960-cx)*eio(P(u,d-.5,d-.1));const dy=(500-cy)*eio(P(u,d-.5,d-.1));
    T($('ch'+i),{x:cx+dx,y:cy+dy+7*Math.sin(u*2.2+i),s:lerp(.3,1,eb(p))*(1-.6*x),a:cl(p*3)*xa,blur:10*x})});
  const sp=Math.min(1.2,d*.45);T($('bH2'),{y:930+20*x,a:(u>sp-.05?1:0)*xa,blur:14*x});headIn(bH2w,u,sp,.15);
  // converge into the logo burst
  const h=te=>ei(P(te,d-.6,d));if(u>d-.6){trail(P_S1b,h(u)-.55,h(u),{width:1.2});sparks(P_S1b,h,u,9)}
}
function sceneEHead(u,d,K){
  if(u<0||u>d){hide($('eH'));hide($('eH2'));return}
  const r=K[1][0];
  const p=eo(P(u,.5,.95)),x=eio(P(u,r-.4,r-.05));T($('eH'),{x:430,y:520+30*(1-p),a:p*(1-x),blur:8*(1-p)+12*x});
  const p2=eo(P(u,r+.3,r+.75)),x2=eio(P(u,d-.5,d-.1));T($('eH2'),{x:1330,y:160+20*(1-p2),a:p2*(1-x2),blur:8*(1-p2)+12*x2});
}
function sceneH(u,d){
  const ids=['hH','hGlobe','hNum','hLab'];
  if(u<0||u>d+.05){ids.forEach(i=>hide($(i)));for(let i=0;i<12;i++)hide($('hd'+i));return 0}
  const x=eio(P(u,d-.4,d)),xa=1-x,xb=14*x;
  T($('hH'),{y:200-20*x,a:xa,blur:xb});headIn(hHw,u,.05,.12);
  const gp=P(u,.25,.7);T($('hGlobe'),{x:700,y:520,s:lerp(.3,1,eb(gp))*(1+.03*Math.sin(u*3)),r:8*Math.sin(u*1.5),a:cl(gp*3)*xa,blur:xb});
  const c0=.5,c1=Math.min(1.9,d-.9);const k=Math.max(1,Math.min(12,1+Math.floor(11*eo(P(u,c0,c1))+1e-6)));
  const hit=P(u,c1,c1+.45);
  $('hNum').textContent=k;T($('hNum'),{x:1130,y:480,s:(1+.25*Math.exp(-Math.max(0,u-c1)*6)*(u>c1?1:0)),a:P(u,.3,.5)*xa,blur:xb});
  T($('hLab'),{x:1130,y:650,a:P(u,.45,.7)*xa,blur:xb});
  for(let i=0;i<12;i++){const el=$('hd'+i);const xx=960-11*29+i*58;T(el,{x:xx,y:770,s:lerp(.3,1,eb(P(u,.3+i*.025,.6+i*.025))),a:P(u,.3+i*.025,.45+i*.025)*xa,blur:xb});
    const f=i<k;el.style.background=f?'linear-gradient(135deg,#fb55b0,#ff888d)':'transparent';el.style.borderColor=f?'#ff8fc4':'rgba(255,255,255,.25)';el.style.boxShadow=f?'0 0 18px rgba(255,80,170,.8)':'none'}
  glowAt(1130,480,420,.2*P(u,.3,.6)*xa+.3*(u>c1?Math.exp(-(u-c1)*3):0)*xa);
  // orbit words reuse
  AORB.forEach((w,i)=>{const ang=i/AORB.length*6.283+u*.2;const z=Math.sin(ang);T($('ao'+i),{x:960+800*Math.cos(ang),y:520+380*z*.85,s:.7+.25*(z+1)/2,a:P(u,.2,.6)*(.08+.12*(z+1)/2)*xa,blur:(1-z)*2+xb})});
  return c1;
}
function render(t){
  RT=t;
  const S=TL.scenes;let k=S.findIndex(q=>t>=q.s&&t<q.e);if(k<0)k=S.length-1;const sc=S[k];const u=t-sc.s,d=sc.e-sc.s;
  const oldT=sc.knots?mapK(u,sc.knots):-10;
  let sh=0;
  if(sc.id==='C'||sc.id==='J'){for(const [tb,amt] of [[2.7,14],[26.7,12]]){const dd=oldT-tb;if(dd>=0&&dd<.45)sh+=Math.pow(1-dd/.45,2)*amt}}
  const sx=Math.sin(t*93)*sh,sy=Math.cos(t*71)*sh;
  $('stage').style.transform=`translate(${sx}px,${sy}px)`;
  drawBG(t);
  fx.setTransform(1,0,0,1,0,0);fx.clearRect(0,0,1920,1080);fx.setTransform(1,0,0,1,sx,sy);
  hide($('q1'));hide($('q2'));
  const ls=sceneLogo(oldT);sceneMascot(oldT,ls);scenePhone(oldT);sceneResult(oldT);sceneLang(-10);scenePrefs(oldT);sceneAsk(oldT);sceneTag(oldT);
  if(sc.id!=='H')AORB.forEach((_,i)=>hide($('ao'+i)));
  sceneA(sc.id==='A'?u:-1,d,sc.split||d*.55);sceneB(sc.id==='B'?u:-1,d);sceneEHead(sc.id==='E'?u:-1,d,sc.knots||[[0,0],[0,0]]);
  const c1=sceneH(sc.id==='H'?u:-1,d);
  if(sc.id==='C')burst(960,400,2.7,oldT,{seed:2,n:110});
  if(sc.id==='H'&&c1){burst(1130,480,c1,u,{seed:12,n:80,speed:1200,ring:600,flash:.6});const dd=u-c1;if(dd>=0&&dd<.4){const a=Math.pow(1-dd/.4,2)*6;$('stage').style.transform=`translate(${Math.sin(t*93)*a}px,${Math.cos(t*71)*a}px)`}}
  if(sc.id==='J'&&oldT>=26.7){burst(1210,330,26.7,oldT,{seed:8,n:90,speed:1200,ring:650});burst(600,540,26.7,oldT,{seed:9,n:90,speed:1300,ring:750,flash:.7})}
  post.clearRect(0,0,1920,1080);post.drawImage(vign,0,0);
  post.globalAlpha=.055;post.globalCompositeOperation='overlay';post.drawImage(grains[Math.floor(t*30)%6],0,0,1920,1080);post.globalAlpha=1;post.globalCompositeOperation='source-over';
  $('black').style.opacity=Math.max(1-P(t,0,.25),P(t,TL.total-.45,TL.total));
}
function initPaths(){
  // underline paths sized to the measured Arabic lines
  const w1=$('t1').offsetWidth,w2=$('t2').offsetWidth;
  P_U1=makePath([[960-w1/2,585],[960,576],[960+w1/2,585]]);P_U2=makePath([[960-w2/2,768],[960,759],[960+w2/2,768]]);
}
'''+s[b:]
R("window.ready=Promise.all([document.fonts.ready,...[...document.images].map(i=>i.decode())]);",
  "window.ready=Promise.all([document.fonts.load('800 60px Cairo','عربي'),document.fonts.load('900 60px Cairo','عربي'),document.fonts.load('700 60px Cairo','عربي'),document.fonts.ready,...[...document.images].map(i=>i.decode())]).then(()=>{initPaths();render(0)});")
R("render(0);\n</script>","</script>")
open(p,'w').write(s);print('patched')
