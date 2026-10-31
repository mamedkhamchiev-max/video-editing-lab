const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:process.argv[3],format:'A4',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});
await p.setViewportSize({width:794,height:1123});

const over=await p.$$eval('.page',ps=>ps.map((pg,i)=>[i,pg.scrollHeight>pg.clientHeight+1]).filter(x=>x[1]).map(x=>x[0]));console.log('overflow pages',over);
await b.close()})();
