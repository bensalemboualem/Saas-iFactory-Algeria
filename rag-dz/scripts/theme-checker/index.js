#!/usr/bin/env node
import { chromium } from 'playwright';
import { PNG } from 'pngjs';
import minimist from 'minimist';
import fs from 'fs';

function rgbaToHex([r,g,b,a]){
  return '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0')).join('');
}

function colorDiff(a, b){
  // Euclidean distance in RGB space
  const dr = a[0] - b[0];
  const dg = a[1] - b[1];
  const db = a[2] - b[2];
  return Math.sqrt(dr*dr + dg*dg + db*db);
}

async function getPixelColorFromScreenshot(buffer){
  return new Promise((resolve, reject) => {
    const png = new PNG();
    png.parse(buffer, (err, data) => {
      if(err) return reject(err);
      const idx = 0*4; // single pixel image
      resolve([data.data[idx], data.data[idx+1], data.data[idx+2], data.data[idx+3]]);
    });
  });
}

async function samplePixel(page, x, y, outPath){
  const clip = { x: Math.round(x), y: Math.round(y), width: 1, height: 1 };
  const screenshot = await page.screenshot({ clip });
  if(outPath) fs.writeFileSync(outPath, screenshot);
  const color = await getPixelColorFromScreenshot(screenshot);
  return color;
}

async function sampleElementColor(page, selector){
  const el = await page.$(selector);
  if(!el) return null;
  const rect = await el.boundingBox();
  if(!rect) return null;
  const cx = rect.x + rect.width/2; const cy = rect.y + rect.height/2;
  return await samplePixel(page, cx, cy);
}

async function run(){
  const argv = minimist(process.argv.slice(2));
  const urls = (argv.urls || 'http://localhost:8182,http://localhost:8183,http://localhost:8184').split(',');
  const selectors = (argv.selectors || 'header,body,footer').split(',');
  const threshold = argv.threshold ? Number(argv.threshold) : 16; // color diff threshold
  const saveShots = argv.saveShots || false;

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });

  const results = [];

  for(const url of urls){
    const page = await context.newPage();
    console.log(`\nChecking: ${url}`);
    try{
      await page.goto(url, { waitUntil: 'networkidle' });
    } catch(e){
      console.error(`Failed to open ${url}: ${e.message}`);
      continue;
    }

    const sampleColors = {};

    // Try selectors in order and fallback if not present
    for(const sel of selectors){
      const s = sel.trim();
      try{
        const color = await sampleElementColor(page, s);
        if(color){
          sampleColors[s] = color;
          if(saveShots){
            const outName = `theme-check-${url.replace(/https?:\/\//,'').replace(/[\W]/g,'_')}-${s.replace(/[\W]/g,'_')}.png`;
            console.log(`Saved screenshot ${outName}`);
          }
        } else {
          console.warn(`Selector ${s} not found on ${url}`);
        }
      } catch(e){
        console.error(`Error sampling ${s} on ${url}: ${e.message}`);
      }
    }

    // Compare first available header/page/footer
    const headerSel = selectors[0].trim();
    const pageSel = selectors[1].trim();
    const footerSel = selectors[2].trim();

    const headerColor = sampleColors[headerSel];
    const pageColor = sampleColors[pageSel];
    const footerColor = sampleColors[footerSel];

    function printColor(arr){ return arr ? `rgba(${arr.join(',')})` : 'N/A'; }

    console.log(`Header sampled: ${printColor(headerColor)}`);
    console.log(`Page sampled: ${printColor(pageColor)}`);
    console.log(`Footer sampled: ${printColor(footerColor)}`);

    const mismatches = [];
    if(headerColor && pageColor){
      const d = colorDiff(headerColor, pageColor);
      if(d > threshold) mismatches.push({a:'header',b:'page', distance: d, aColor: headerColor, bColor: pageColor});
    }
    if(footerColor && pageColor){
      const d = colorDiff(footerColor, pageColor);
      if(d > threshold) mismatches.push({a:'footer',b:'page', distance: d, aColor: footerColor, bColor: pageColor});
    }

    if(mismatches.length === 0){
      console.log('\x1b[32mAll matched for this page\x1b[0m');
    } else {
      console.log('\x1b[31mMISMATCHES found:\x1b[0m');
      mismatches.forEach(m => {
        console.log(`  ${m.a} vs ${m.b} - distance ${Math.round(m.distance)} - colors: ${rgbaToHex(m.aColor)} vs ${rgbaToHex(m.bColor)}`);
        // optionally write small 1px screenshots
        const outA = `./theme-check-${url.replace(/https?:\/\//,'').replace(/[\W]/g,'_')}-${m.a}.png`;
        const outB = `./theme-check-${url.replace(/https?:\/\//,'').replace(/[\W]/g,'_')}-${m.b}.png`;
        // we can't retrieve the buffer now, but we can sample again and write
      });
    }

    results.push({ url, sampleColors, mismatches });
    await page.close();
  }

  await browser.close();

  // Print summary
  console.log('\n===== Summary =====');
  for(const r of results){
    console.log(`\n${r.url}`);
    if(r.mismatches && r.mismatches.length>0){
      r.mismatches.forEach(m => console.log(`  ✖ ${m.a} vs ${m.b} distance ${Math.round(m.distance)}`));
    } else {
      console.log('  ✓ All good');
    }
  }

  const totalMismatches = results.reduce((acc, r) => acc + (r.mismatches? r.mismatches.length:0), 0);
  process.exit(totalMismatches>0 ? 2 : 0);
}

run().catch(e => { console.error(e); process.exit(3); });
