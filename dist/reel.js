/* A projected film loop. No WebGL, remote assets, framework, or animation library. */
(() => {
  'use strict';
  const TAU = Math.PI * 2;
  const COUNT = 10;
  const WIDTH = 900;
  const HEIGHT = 650;
  const names = ['TIDELINE', 'ALPINE', 'AFTER HOURS', 'DUNE STUDY', 'CANOPY'];

  function path(ctx, points, fill) {
    ctx.beginPath();
    points.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
  }
  function gradient(ctx, top, bottom) {
    const g = ctx.createLinearGradient(0, 0, 0, 256);
    g.addColorStop(0, top); g.addColorStop(1, bottom);
    ctx.fillStyle = g; ctx.fillRect(0, 0, 480, 256);
  }
  function circle(ctx, x, y, r, fill) {
    ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fillStyle = fill; ctx.fill();
  }
  function scene(ctx, index) {
    // Deliberately graphic scenery: hard silhouettes, composed light, fine grain.
    const kind = index % 5;
    if (kind === 0) {
      gradient(ctx, '#deb98e', '#f7dcb0');
      circle(ctx, 347, 73, 24, '#fff0ce');
      ctx.fillStyle = '#527c86'; ctx.fillRect(0, 121, 480, 135);
      for (let y = 126; y < 256; y += 9) {
        ctx.strokeStyle = y < 180 ? '#98b4b1' : '#739b9f'; ctx.lineWidth = .8;
        ctx.beginPath();
        for (let x = 0; x <= 480; x += 8) {
          const yy = y + Math.sin(x * .025 + y * .08) * 2;
          x ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
        }
        ctx.stroke();
      }
      path(ctx, [[0,63],[66,105],[119,115],[143,151],[211,172],[178,199],[107,227],[90,256],[0,256]], '#293d42');
      path(ctx, [[0,63],[66,105],[119,115],[143,151],[77,145],[37,123],[0,137]], '#68726a');
      path(ctx, [[480,200],[430,194],[404,223],[358,241],[356,256],[480,256]], '#354d50');
      ctx.strokeStyle = '#e2e6d5'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(157,160);ctx.bezierCurveTo(260,186,96,221,112,256);ctx.stroke();
    } else if (kind === 1) {
      gradient(ctx, '#648eaa', '#d5dde0');
      path(ctx, [[0,188],[90,87],[138,124],[230,14],[334,149],[401,100],[480,186]], '#73899a');
      path(ctx, [[138,124],[230,14],[334,149],[249,100],[223,67],[188,105]], '#edf0e7');
      path(ctx, [[230,14],[249,100],[334,149],[282,108]], '#a8bfce');
      path(ctx, [[0,183],[60,128],[131,173],[160,139],[262,207],[0,256]], '#355866');
      ctx.fillStyle = '#537e8c'; ctx.fillRect(0, 213, 480, 43);
      for (let i = 0; i < 21; i++) {
        const x = 290 + i * 11, h = 14 + Math.sin(i * 8) * 8;
        path(ctx, [[x,216-h],[x-7,222],[x+7,222]], '#264747');
      }
    } else if (kind === 2) {
      gradient(ctx, '#152a45', '#725b79');
      circle(ctx, 373, 49, 16, '#eccbb7');
      for (let i = 0; i < 13; i++) {
        const x = i * 39, y = 48 + ((i * 47) % 91);
        ctx.fillStyle = i % 2 ? '#222f46' : '#303a51';ctx.fillRect(x, y, 34, 256-y);
        for (let wy = y + 13; wy < 236; wy += 18) {
          for (let wx = x + 7; wx < x+30; wx += 11) {
            ctx.fillStyle = (wx + wy) % 3 ? '#be957d' : '#587282';ctx.fillRect(wx,wy,3,6);
          }
        }
      }
      path(ctx, [[201,256],[233,145],[263,145],[305,256]], '#172838');
      ctx.strokeStyle='#d79482';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(243,174);ctx.lineTo(251,256);ctx.stroke();
    } else if (kind === 3) {
      gradient(ctx, '#bfb0aa', '#efd4b6');
      circle(ctx, 126, 65, 29, '#f8e4c6');
      ctx.fillStyle='#dca87a';ctx.beginPath();ctx.moveTo(0,155);ctx.bezierCurveTo(95,82,202,146,480,114);ctx.lineTo(480,256);ctx.lineTo(0,256);ctx.fill();
      ctx.fillStyle='#b96e4e';ctx.beginPath();ctx.moveTo(0,256);ctx.bezierCurveTo(116,127,281,119,480,168);ctx.lineTo(480,256);ctx.fill();
      ctx.fillStyle='#e4b488';ctx.beginPath();ctx.moveTo(0,256);ctx.bezierCurveTo(116,127,281,119,480,168);ctx.bezierCurveTo(226,123,228,200,133,256);ctx.fill();
      for(let i=0;i<9;i++){ctx.strokeStyle='#a25b4133';ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(278+i*13,175);ctx.quadraticCurveTo(230+i*20,220,227+i*25,256);ctx.stroke();}
    } else {
      gradient(ctx, '#b4c8b7', '#718f83');
      for (let layer=0;layer<3;layer++) {
        for(let i=0;i<12;i++) {
          const x=i*47+layer*13, y=32+((i*71+layer*31)%72), h=160+layer*30;
          const color=['#6e9485','#416f66','#204b49'][layer];
          path(ctx, [[x,y],[x-31,y+h*.7],[x-18,y+h*.7],[x-43,y+h],[x+43,y+h],[x+18,y+h*.7],[x+31,y+h*.7]],color);
        }
      }
      path(ctx, [[235,171],[191,256],[267,256],[247,204]],'#a9b8a0');
    }
    // Seeded, static texture avoids per-frame noise work and flicker.
    let seed=91+index;
    for(let i=0;i<3800;i++) {
      seed=(Math.imul(seed,1664525)+1013904223)>>>0; const x=(seed%480);
      seed=(Math.imul(seed,1664525)+1013904223)>>>0; const y=(seed%256);
      ctx.fillStyle=i%2?'#ffffff0a':'#00000008';ctx.fillRect(x,y,1,1);
    }
  }

  function filmTexture(makeCanvas, index) {
    const c=makeCanvas(512,320), ctx=c.getContext('2d');
    ctx.fillStyle='#1d2129';ctx.fillRect(0,0,512,320);
    ctx.save();ctx.translate(16,32);scene(ctx,index);ctx.restore();
    for(let x=18;x<500;x+=30) {
      ctx.fillStyle='#c8c7d0';ctx.fillRect(x,9,13,9);ctx.fillRect(x,302,13,9);
    }
    ctx.fillStyle='#dfd9c7';ctx.font='9px monospace';ctx.fillText(`${String(index+1).padStart(2,'0')}   ${names[index%5]}`,20,27);
    ctx.fillText('MC / 35',442,299);
    ctx.fillStyle='#ffffff25';ctx.fillRect(0,0,512,1);ctx.fillRect(0,319,512,1);
    return c;
  }

  function point(t, v, tilt=0) {
    const x=Math.cos(t)*344, z=Math.sin(t)*220;
    const y=-Math.sin(t)*101+(v-.5)*171;
    const roll=-.27+tilt, scale=1000/(1000+z);
    return {x:455+(x*Math.cos(roll)-y*Math.sin(roll))*scale,
      y:304+(x*Math.sin(roll)+y*Math.cos(roll))*scale,z};
  }
  function createRenderer(canvas,makeCanvas) {
    const ctx=canvas.getContext('2d');
    const textures=Array.from({length:COUNT},(_,i)=>filmTexture(makeCanvas,i));
    function draw(phase=0,tilt=0) {
      ctx.setTransform(canvas.width/WIDTH,0,0,canvas.height/HEIGHT,0,0);
      ctx.clearRect(0,0,WIDTH,HEIGHT);
      // Grounding shadow, entirely procedural and independent of frame count.
      ctx.save();ctx.translate(472,532);ctx.scale(1,.13);
      const shadow=ctx.createRadialGradient(0,0,20,0,0,315);
      shadow.addColorStop(0,'#30244923');shadow.addColorStop(.55,'#3024490d');shadow.addColorStop(1,'#30244900');
      ctx.fillStyle=shadow;ctx.fillRect(-320,-320,640,640);ctx.restore();
      const panels=Array.from({length:COUNT},(_,i)=>({i,t:i*TAU/COUNT+phase-Math.PI/2-TAU/COUNT/2}));
      panels.sort((a,b)=>Math.sin(b.t+TAU/COUNT/2)-Math.sin(a.t+TAU/COUNT/2));
      for(const {i,t} of panels) {
        const texture=textures[i], span=TAU/COUNT-.008;
        const steps=20,spanPixels=512/steps;
        for(let strip=0;strip<steps;strip++) {
          const u=strip/steps,next=(strip+1)/steps,mid=(u+next)/2;
          const left=point(t+u*span,.5,tilt),right=point(t+next*span,.5,tilt);
          const top=point(t+mid*span,0,tilt),bottom=point(t+mid*span,1,tilt);
          // Narrow affine slices follow the curve without clipped triangle seams.
          ctx.save();
          ctx.transform((right.x-left.x)/spanPixels,(right.y-left.y)/spanPixels,
            (bottom.x-top.x)/320,(bottom.y-top.y)/320,left.x,left.y);
          ctx.drawImage(texture,u*512-.7,0,spanPixels+1.4,320,-.7,-160,spanPixels+1.4,320);
          ctx.restore();
        }
        const outline=[];
        for(let s=0;s<=steps;s++){const p=point(t+s/steps*span,0,tilt);outline.push([p.x,p.y]);}
        for(let s=steps;s>=0;s--){const p=point(t+s/steps*span,1,tilt);outline.push([p.x,p.y]);}
        path(ctx,outline,`rgba(16,20,32,${.03+.19*(Math.sin(t+span/2)+1)/2})`);
      }
      // One stationary focus aperture: the library finding a moment in the loop.
      const focus=-Math.PI/2, half=.302;
      ctx.strokeStyle='#5140c6';ctx.lineWidth=3;ctx.lineCap='square';
      for(const [t,v,dt,dv] of [[focus-half,-.045,.065,.10],[focus+half,-.045,-.065,.10],[focus-half,1.045,.065,-.10],[focus+half,1.045,-.065,-.10]]) {
        const a=point(t+dt,v,tilt),b=point(t,v,tilt),c=point(t,v+dv,tilt);
        ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.lineTo(c.x,c.y);ctx.stroke();
      }
    }
    return {draw};
  }

  // A shared renderer lets the build create the exact no-JavaScript poster too.
  if(typeof module!=='undefined' && module.exports) module.exports={createRenderer,WIDTH,HEIGHT};
  if(typeof document==='undefined') return;
  const root=document.querySelector('.reel-art'),canvas=root?.querySelector('canvas');
  if(!canvas || !canvas.getContext('2d')) return;
  const makeCanvas=(w,h)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c;};
  const renderer=createRenderer(canvas,makeCanvas);
  const button=root.querySelector('.reel-control');
  const label=button.querySelector('.reel-control-label');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let paused=reduced.matches, visible=true, phase=0, tilt=0, targetTilt=0, last=0, frame=0;
  const running=()=>!paused && visible && !document.hidden;
  function tick(now) {
    frame=0;
    if(!running()){last=0;return;}
    if(last && now-last<1000/30){frame=requestAnimationFrame(tick);return;}
    if(last)phase+=Math.min((now-last)/1000,.1)*.072;
    last=now;tilt+=(targetTilt-tilt)*.045;renderer.draw(phase,tilt);
    frame=requestAnimationFrame(tick);
  }
  function sync() {
    button.setAttribute('aria-pressed',String(paused));
    button.setAttribute('aria-label',paused?'Play reel animation':'Pause reel animation');
    label.textContent=paused?'Play':'Pause';
    root.dataset.motion=running()?'running':'paused';
    if(running()&&!frame){last=0;frame=requestAnimationFrame(tick);}
    else if(!running()&&frame){cancelAnimationFrame(frame);frame=0;last=0;}
  }
  function resize() {
    const box=root.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,1.5);
    canvas.width=Math.round(box.width*dpr);canvas.height=Math.round(box.height*dpr);
    renderer.draw(phase,tilt);
  }
  resize();root.dataset.ready='true';button.hidden=false;
  new ResizeObserver(resize).observe(root);
  new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;sync();},{threshold:.05}).observe(root);
  document.addEventListener('visibilitychange',sync);
  button.addEventListener('click',()=>{paused=!paused;sync();});
  reduced.addEventListener('change',()=>{paused=reduced.matches;tilt=targetTilt=0;renderer.draw(phase,tilt);sync();});
  root.addEventListener('pointermove',e=>{
    if(e.pointerType!=='mouse'||reduced.matches||paused)return;
    const rect=root.getBoundingClientRect();targetTilt=((e.clientY-rect.top)/rect.height-.5)*.08;
  });
  root.addEventListener('pointerleave',()=>{targetTilt=0;});
  sync();
})();
