const test = require('node:test');
const assert = require('node:assert/strict');
const { createSpeechController } = require('../listening-audio.js');
class Utterance { constructor(text) { this.text = text; } }
function fake() {
  const spoken = [];
  const synthesis = { speak(u) { spoken.push(u); setImmediate(() => u.onend()); }, cancel() {} };
  return { synthesis, spoken };
}
test('reports unsupported synthesis without claiming playback', async () => {
  const statuses = [];
  const controller = createSpeechController({ onStatus: s => statuses.push(s) });
  assert.equal(controller.isSupported(), false);
  assert.equal(await controller.play([{ text: 'Hello.' }]), false);
  assert.deepEqual(statuses, ['unsupported']);
});
test('plays segments in order with English language and selected rate', async () => {
  const { synthesis, spoken } = fake();
  const controller = createSpeechController({ synthesis, Utterance });
  assert.equal(await controller.play([{ text: 'First.' }, { text: 'Second.' }], 0.75), true);
  assert.deepEqual(spoken.map(x => x.text), ['First.', 'Second.']);
  assert.ok(spoken.every(x => x.lang === 'en-US' && x.rate === 0.75));
});
test('stop cancels current speech and prevents later segments', async () => {
  let utterance; let cancels = 0;
  const synthesis = { speak(u) { utterance = u; }, cancel() { cancels += 1; } };
  const controller = createSpeechController({ synthesis, Utterance });
  const playback = controller.play([{ text: 'First.' }, { text: 'Second.' }]);
  controller.stop(); utterance.onend();
  assert.equal(await playback, false); assert.equal(cancels, 2);
});
test('starting a new playback interrupts and settles the previous playback', async () => {
  const utterances = [];
  const synthesis = { speak(u) { utterances.push(u); if (utterances.length === 2) setImmediate(() => u.onend()); }, cancel() {} };
  const controller = createSpeechController({ synthesis, Utterance });
  const previous = controller.play([{ text: 'Old clip.' }, { text: 'This must not play.' }]);
  const current = controller.play([{ text: 'New clip.' }]);
  assert.equal(await previous, false);
  assert.equal(await current, true);
  assert.deepEqual(utterances.map(x => x.text), ['Old clip.', 'New clip.']);
});
test('speech errors are reported', async () => {
  const synthesis = { speak(u) { setImmediate(() => u.onerror(new Error('voice unavailable'))); }, cancel() {} };
  const statuses = [];
  const controller = createSpeechController({ synthesis, Utterance, onStatus: s => statuses.push(s) });
  assert.equal(await controller.play([{ text: 'Hello.' }]), false);
  assert.deepEqual(statuses, ['playing', 'error']);
});
