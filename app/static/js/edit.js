const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 900; canvas.height = 600;
const bg = new Image();
bg.onload = ()=> ctx.drawImage(bg,0,0,canvas.width,canvas.height);
if(window.BASE_IMG){ bg.src = window.BASE_IMG; }
function addSun(){ ctx.beginPath(); ctx.arc(120,120,50,0,Math.PI*2); ctx.fillStyle = '#ffd54f'; ctx.fill(); }
function addCloud(){ ctx.beginPath(); ctx.fillStyle = '#e0e0e0'; ctx.arc(500,120,30,0,Math.PI*2); ctx.arc(530,120,25,0,Math.PI*2); ctx.arc(515,105,25,0,Math.PI*2); ctx.fill(); }
function changeBg(){ ctx.fillStyle = `hsl(${Math.floor(Math.random()*360)},60%,90%)`; ctx.fillRect(0,0,canvas.width,canvas.height); if(bg.src) ctx.drawImage(bg,0,0,canvas.width,canvas.height); }
function saveImage(){ const url = canvas.toDataURL('image/png'); const a = document.createElement('a'); a.href=url; a.download='edited_art.png'; a.click(); }