const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const errors = [];
  page.on('pageerror', err => errors.push(err.message));
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });

  console.log('Navigating to http://localhost:5173/parent/children ...');
  await page.goto('http://localhost:5173/parent/children', { waitUntil: 'networkidle' });
  
  const content = await page.content();
  if (content.includes('Something went wrong!')) {
    console.error('ERROR: Error boundary is still visible!');
  } else {
    console.log('SUCCESS: Error boundary is NOT visible.');
  }
  
  if (errors.length > 0) {
    console.log('Found errors:');
    errors.forEach(e => console.log(e));
  } else {
    console.log('No console or page errors found.');
  }
  
  await browser.close();
})();
