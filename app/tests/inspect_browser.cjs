// Opcional: pacote playwright + Microsoft Edge; servidor iniciado separadamente.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');

(async () => {
  const out = 'docs/reformulacao';
  await fs.mkdir(out, {recursive: true});
  const browser = await chromium.launch({headless: true, channel: 'msedge'});
  const page = await browser.newPage({viewport: {width: 1672, height: 941}, reducedMotion: 'reduce'});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  try {
    async function navigate(name) {
      const sidebar = page.getByTestId('stSidebar');
      if (!await sidebar.isVisible() || await sidebar.getAttribute('aria-expanded') === 'false') {
        await page.getByTestId('stExpandSidebarButton').click();
      }
      await sidebar.locator('label').filter({has: page.getByRole('radio', {name, exact: true})}).click();
      await page.getByRole('heading', {name, exact: true}).waitFor();
      if (page.viewportSize().width < 700) {
        await page.getByTestId('stSidebarCollapseButton').click();
      }
    }
    async function capture(name) {
      await page.evaluate(() => document.fonts.ready);
      const viewport = page.viewportSize();
      const main = page.getByTestId('stMain');
      const height = await main.evaluate(el => el.scrollHeight + 60);
      await page.setViewportSize({width: viewport.width, height});
      await main.evaluate(el => el.scrollTop = 0);
      await page.waitForFunction(() => !document.querySelector('[data-stale="true"]'));
      assert(await main.evaluate(el => el.scrollWidth <= el.clientWidth + 1), 'Sem rolagem horizontal');
      await page.screenshot({path: path.join(out, name), fullPage: true, animations:'disabled'});
      await page.setViewportSize(viewport);
    }
    async function demoOpen() {
      const summary = page.locator('summary').filter({hasText:'Configurações da demonstração'});
      if (await summary.getAttribute('aria-expanded') !== 'true') await summary.click();
    }
    async function scenario(name) {
      await demoOpen();
      await page.getByRole('combobox').click();
      await page.getByRole('option', {name, exact:true}).click();
    }
    async function metric(label, value) {
      await page.getByTestId('stMetric').filter({has:page.getByText(label, {exact:true})})
        .getByTestId('stMetricValue').filter({hasText:value}).waitFor();
    }
    await page.goto(process.env.APP_URL || 'http://127.0.0.1:8501');
    await page.getByRole('button', {name:'Fechar válvula', exact:true}).waitFor();
    await page.locator('.js-plotly-plot .main-svg').first().waitFor();
    await capture('overview-desktop.png');
    if (process.argv.includes('--capture-only')) {
      console.log(await page.evaluate(()=>({
        cards:[...document.querySelectorAll('[class*="st-key-gh_metric_"]')].map(n=>({cls:n.className, gap:getComputedStyle(n).gap,padding:getComputedStyle(n).padding,html:n.outerHTML.slice(0,1600)})),
        captions:[...document.querySelectorAll('[data-testid="stCaptionContainer"] p')].slice(0,2).map(n=>({color:getComputedStyle(n).color,font:getComputedStyle(n).fontSize})),
        stale:[...document.querySelectorAll('[data-stale]')].slice(0,2).map(n=>n.outerHTML.slice(0,250))
      })));
      console.log(await page.locator('body').innerText());
      await page.setViewportSize({width:390, height:844});
      await capture('overview-narrow.png');
      console.log(await page.getByRole('button').evaluateAll(nodes=>nodes.map(n=>({label:n.getAttribute('aria-label'),testid:n.getAttribute('data-testid'),text:n.innerText}))));
      return;
    }
    // Atualização automática produz novas leituras sem interação.
    const first = await page.getByText(/Bancada principal · Última leitura:/).innerText();
    await page.waitForFunction(text => !document.body.innerText.includes(text), first, {timeout:8000});
    await scenario('Consumo elevado');
    await page.getByText(/Consumo elevado no cenário demonstrativo/).first().waitFor();
    assert(await page.getByRole('button',{name:'Fechar válvula',exact:true}).isEnabled());
    await scenario('Vazamento simulado');
    await page.getByText(/Comando: Pendente/).waitFor();
    await capture('pending-desktop.png');
    await page.getByText(/Comando: Confirmado/).waitFor();
    await metric('Válvula', 'Fechada');
    assert(await page.getByRole('button',{name:'Abrir válvula',exact:true}).isDisabled());
    await page.getByRole('button',{name:'Ver todos os eventos'}).click();
    await page.getByRole('heading',{name:'Alertas e controle',exact:true}).waitFor();
    await page.getByRole('button',{name:/Reconhecer alerta/}).click();
    await page.getByText(/Crítico · Reconhecido/).waitFor();
    await capture('alerts-desktop.png');
    await scenario('Operação normal');
    await page.getByRole('button',{name:'Abrir válvula',exact:true}).click();
    await page.getByText(/Comando: Pendente/).waitFor();
    await page.getByText(/Comando: Confirmado/).waitFor();
    await page.locator('.gh-status').filter({hasText:'Aberta'}).waitFor();
    await scenario('Comunicação indisponível');
    await page.getByText(/Sem comunicação • leitura desatualizada/).waitFor({timeout:20000});
    assert(await page.getByRole('button',{name:'Abrir válvula',exact:true}).isDisabled());
    assert(await page.getByRole('button',{name:'Fechar válvula',exact:true}).isDisabled());
    await capture('offline-desktop.png');
    await scenario('Operação normal');
    await page.getByRole('button',{name:/Pausar simulação/}).click();
    await page.getByText(/Simulação pausada. Relógio/).waitFor();
    await capture('paused-desktop.png');
    await page.getByRole('button',{name:/Retomar simulação/}).click();
    await navigate('Histórico');
    await page.getByRole('table',{name:'Volumes diários de exemplo'}).waitFor();
    assert.equal(await page.getByRole('row').count(),8);
    await capture('history-desktop.png');
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button',{name:'Baixar CSV do intervalo'}).click();
    const download = await downloadPromise;
    assert.equal(download.suggestedFilename(),'guardiao_historico_exemplo.csv');
    const csv = await fs.readFile(await download.path(), 'utf8');
    assert.equal(csv.trim().split(/\r?\n/).length,8);
    await page.setViewportSize({width:390,height:844});
    await capture('history-narrow.png');
    await navigate('Visão geral');
    await page.getByRole('button',{name:'Fechar válvula',exact:true}).waitFor();
    await capture('overview-narrow.png');
    await navigate('Alertas e controle');
    await capture('alerts-narrow.png');
    await page.setViewportSize({width:1440,height:1000});
    await navigate('Visão geral');
    await capture('overview-1440.png');
    // Foco de teclado e dimensões dos controles principais.
    const close = page.getByRole('button',{name:'Fechar válvula',exact:true});
    await close.focus();
    await page.keyboard.press('Tab');
    const focus = await page.evaluate(()=>({tag:document.activeElement.tagName,
      outline:getComputedStyle(document.activeElement).outlineWidth}));
    assert.notEqual(focus.tag,'BODY');
    assert.notEqual(focus.outline,'0px');
    const targets = await page.getByRole('button').evaluateAll(nodes => nodes.filter(n=>
      /Fechar válvula|Ver todos os eventos|Pausar simulação|Reiniciar demonstração/.test(n.innerText))
      .map(n=>({label:n.innerText,height:n.getBoundingClientRect().height,width:n.getBoundingClientRect().width})));
    console.log({targets, focus});
    assert(targets.filter(t=>t.height>0).every(t=>t.height>=44 && t.width>=44));
    const modeColors = await page.locator('.gh-mode-status').evaluate(n=>({text:getComputedStyle(n).color,background:getComputedStyle(n.parentElement).backgroundColor}));
    await navigate('Alertas e controle');
    const successColors = await page.locator('[data-testid="stAlertContentSuccess"] p').evaluate(n=>({text:getComputedStyle(n).color}));
    assert.equal(await page.getByTestId('stException').count(),0);
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({result:'PASS',targets,focus,modeColors,successColors,checks:[
      'três telas', 'atualização periódica', 'cenários', 'pendente/confirmado/leitura',
      'reconhecimento', 'reabertura', 'offline', 'pausa', 'CSV', 'desktop/390px', 'foco e alvos 44px'
    ]},null,2));
  } catch (error) {
    console.log((await page.locator('body').innerText()).slice(-7000));
    console.log(await page.getByRole('button').evaluateAll(nodes=>nodes.map(n=>({label:n.getAttribute('aria-label'),testid:n.getAttribute('data-testid'),text:n.innerText}))));
    throw error;
  } finally {
    await browser.close();
  }
})();
