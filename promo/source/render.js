const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const mode = process.argv[2]; const dir = __dirname;
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('page:', m.text())); page.on('pageerror', e => console.log('ERR', e.message));
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.evaluate(() => window.ready);
  if (mode === 'preview') {
    const times = process.argv.slice(3).map(Number);
    for (const t of times) { await page.evaluate(t => render(t), t); await page.screenshot({ path: path.join(dir, process.env.PREV||'prev', `f_${t.toFixed(2)}.png`) }); }
  } else {
    const fps = 30, N = 900;
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', String(fps), path.join(dir, 'video_silent.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < N; f++) {
      await page.evaluate(t => render(t), f / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 90 === 0) console.log('frame', f);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
