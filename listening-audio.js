'use strict';
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.ListeningAudio = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  function createSpeechController({ synthesis, Utterance, onStatus = () => {} } = {}) {
    let generation = 0;
    let finishCurrent = null;
    const isSupported = () => Boolean(synthesis && typeof synthesis.speak === 'function' && Utterance);
    function cancelCurrent() {
      if (!finishCurrent) return;
      const finish = finishCurrent;
      finishCurrent = null;
      finish(false);
    }
    function stop() {
      generation += 1;
      cancelCurrent();
      if (synthesis && typeof synthesis.cancel === 'function') synthesis.cancel();
      onStatus('stopped');
    }
    async function play(segments, rate = 0.85) {
      if (!isSupported()) { onStatus('unsupported'); return false; }
      const token = ++generation;
      cancelCurrent();
      if (typeof synthesis.cancel === 'function') synthesis.cancel();
      onStatus('playing');
      for (const segment of segments) {
        if (token !== generation) return false;
        const utterance = new Utterance(segment.text);
        utterance.lang = 'en-US'; utterance.rate = rate;
        const finished = await new Promise(resolve => {
          const finish = value => {
            if (finishCurrent === finish) finishCurrent = null;
            resolve(value);
          };
          finishCurrent = finish;
          utterance.onend = () => finish(true);
          utterance.onerror = () => finish(false);
          synthesis.speak(utterance);
        });
        if (!finished) { if (token === generation) onStatus('error'); return false; }
      }
      if (token === generation) onStatus('ended');
      return token === generation;
    }
    return { isSupported, play, stop };
  }
  return { createSpeechController };
});
