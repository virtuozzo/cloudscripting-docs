// Execute the shipped script with a minimal DOM and real loopback HTTP fetch.
// Browser layout/keyboard checks remain a separate acceptance gate.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const [mode, scriptPath, encoded] = process.argv.slice(2);
const input = JSON.parse(encoded);
const script = fs.readFileSync(scriptPath, 'utf8');

async function run() {
  if (mode === 'search') {
    const url = new URL(input.url);
    let replaced;
    const link = {};
    vm.runInNewContext(script.match(/<script>([\s\S]*?)<\/script>/)[1], {
      URL, URLSearchParams,
      document: {getElementById: () => link},
      location: {href: url.href, search: url.search, hash: url.hash, replace: value => replaced = value}
    });
    assert.equal(replaced, input.expected);
    assert.equal(link.href, input.expected);
    console.log(JSON.stringify({destination: replaced}));
  } else if (mode === 'version') {
    const current = new URL(input.url);
    let handler, prevented = false, assigned;
    const requests = [];
    const a = {href: input.target, getAttribute: name => ({'data-vs-from': input.from, 'data-vs-lang': '', 'aria-current': 'false'})[name]};
    const location = {pathname: current.pathname, search: current.search, hash: current.hash, href: current.href};
    let done;
    const finished = new Promise(resolve => done = resolve);
    Object.defineProperty(location, 'href', {get: () => assigned || current.href, set: value => { assigned = value; done(); }});
    const realFetch = async (url, options) => { requests.push([url, options.method]); return fetch(url, options); };
    vm.runInNewContext(script, {URL, location, fetch: realFetch, window: {fetch: realFetch, URL},
      document: {addEventListener: (name, callback) => handler = callback}});
    handler({target: {closest: () => a}, button: 0, ctrlKey: !!input.modified, preventDefault: () => prevented = true});
    if (prevented) {
      let timer;
      await Promise.race([finished, new Promise((_, reject) => timer = setTimeout(() => reject(Error('navigation timed out')), 5000))]);
      clearTimeout(timer);
      assert.equal(assigned, input.expected);
      assert.ok(requests.length);
      assert.ok(requests.every(([, method]) => method === 'HEAD'));
    } else {
      assert.equal(input.modified, true);
      assert.deepEqual(requests, []);
      assert.equal(assigned, undefined);
    }
    console.log(JSON.stringify({destination: assigned, prevented, requests}));
  } else if (mode === 'copy') {
    let handler, copied;
    const button = {dataset: {}, textContent: 'Copy', classList: {add() {}, remove() {}}, closest: () => block};
    const block = {querySelector: () => ({value: input.body})};
    const copyScript = script.match(/\(function initCodeCopyButtons\(\) \{[\s\S]*?\n\}\)\(\);/)[0];
    vm.runInNewContext(copyScript, {
      document: {addEventListener: (name, callback) => handler = callback}, elems: () => [button],
      navigator: {clipboard: {writeText: text => {copied = text; return Promise.resolve();}}}, window: {setTimeout() {}}
    });
    handler({target: {closest: () => button}});
    await Promise.resolve();
    assert.equal(copied, input.expected);
    assert.equal(button.textContent, 'Copied');
    console.log(JSON.stringify({copied}));
  } else throw Error('Unknown mode');
}
run().catch(error => { console.error(error); process.exitCode = 1; });
