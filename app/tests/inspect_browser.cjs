// Opcional: npm install --no-save playwright; requer Microsoft Edge instalado.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({headless: true, channel: 'msedge'});
  const page = await browser.newPage({viewport: {width: 1440, height: 1100}});
  async function navigate(name) {
    await page.locator('label').filter({has: page.getByRole('radio',{name,exact:true})}).click();
  }
  async function capture(name) {
    const viewport = page.viewportSize();
    const main = page.locator('[data-testid="stMain"]');
    const height = await main.evaluate(el => el.scrollHeight + 100);
    await page.setViewportSize({width: viewport.width, height});
    await main.evaluate(el => el.scrollTop = 0);
    assert(await main.evaluate(el => el.scrollWidth <= el.clientWidth + 1));
    await page.screenshot({path: 'docs/' + name, fullPage:true});
    await page.setViewportSize(viewport);
  }
  await page.goto('http://127.0.0.1:8501');
  await page.getByRole('button', {name: 'Fechar válvula', exact:true}).waitFor();
  await page.locator('.js-plotly-plot .main-svg').first().waitFor();
  await capture('overview-desktop.png');
  await page.getByText('Demonstração', {exact:true}).click();
  async function scenario(name) {
    await page.getByRole('combobox').click();
    await page.getByRole('option', {name, exact:true}).click();
  }
  await scenario('Consumo elevado');
  await page.getByText(/Consumo elevado no cenário demonstrativo/).waitFor();
  await scenario('Vazamento simulado');
  await page.getByText(/Comando: Pendente/).waitFor();
  await page.getByText(/Comando: Confirmado/).waitFor();
  await page.waitForFunction(() => document.body.innerText.includes('Fechada'));
  assert(await page.getByRole('button',{name:'Abrir válvula',exact:true}).isDisabled());
  await navigate('Alertas e controle');
  await page.getByRole('button',{name:'Reconhecer alerta',exact:true}).click();
  await page.getByText(/Situação: reconhecido/).first().waitFor();
  await capture('alerts-desktop.png');
  await scenario('Operação normal');
  await page.getByRole('button',{name:'Abrir válvula',exact:true}).click();
  await page.getByText(/Comando: Pendente/).waitFor();
  await page.getByText(/Comando: Confirmado/).waitFor();
  await page.waitForFunction(() => (document.body.innerText.match(/Aberta/g) || []).length >= 2);
  await scenario('Comunicação indisponível');
  await page.getByText(/Sem comunicação • leitura desatualizada/).waitFor({timeout:20000});
  assert(await page.getByRole('button',{name:'Abrir válvula',exact:true}).isDisabled());
  await capture('offline-desktop.png');
  await navigate('Histórico');
  await page.getByRole('button',{name:'Baixar CSV do intervalo'}).waitFor();
  await capture('history-desktop.png');
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button',{name:'Baixar CSV do intervalo'}).click();
  const download = await downloadPromise;
  assert.equal(download.suggestedFilename(),'guardiao_historico_exemplo.csv');
  await page.setViewportSize({width:390,height:844});
  await capture('history-narrow.png');
  await scenario('Operação normal');
  await navigate('Visão geral');
  await page.getByRole('button',{name:'Fechar válvula',exact:true}).waitFor();
  await capture('overview-narrow.png');
  await navigate('Alertas e controle');
  await page.getByRole('heading',{name:'Alertas e controle',exact:true}).waitFor();
  await capture('alerts-narrow.png');
  assert.equal(await page.locator('[data-testid="stException"]').count(),0);
  console.log('PASS: três telas, cenários, pendente/confirmado, reconhecimento, reabertura, offline, CSV e capturas desktop/390px.');
  await browser.close();
})();
