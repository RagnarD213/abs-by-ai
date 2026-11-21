const preview = document.getElementById('player');
const positionControl = document.getElementById('preview-position');
const clock = document.getElementById('preview-clock');
const statusLine = document.getElementById('player-status');
const playButton = document.getElementById('toggle-play');
const soundControl = document.getElementById('sound');
let loadSequence = 0;

function formatTime(value) {
  const seconds = Math.max(0, Math.floor(Number(value) || 0));
  return Math.floor(seconds / 60) + ':' + String(seconds % 60).padStart(2, '0');
}
function setPlayerStatus(message, error = false) {
  statusLine.textContent = message;
  statusLine.classList.toggle('error', error);
}
function updateControls() {
  const duration = Number.isFinite(preview.duration) ? preview.duration : 0;
  positionControl.max = duration;
  positionControl.disabled = !duration;
  positionControl.value = preview.currentTime || 0;
  clock.textContent = formatTime(preview.currentTime) + ' / ' + formatTime(duration);
  playButton.textContent = preview.paused ? 'Play' : 'Pause';
  soundControl.checked = !preview.muted;
  document.getElementById('sound-note').hidden = !preview.muted;
}
function setAudioEnabled(enabled) {
  preview.muted = !enabled;
  updateControls();
}
function seekBy(seconds) {
  if (Number.isFinite(preview.duration)) preview.currentTime = Math.max(0, Math.min(preview.duration, preview.currentTime + seconds));
}
function scrubTo(value) {
  if (Number.isFinite(preview.duration)) preview.currentTime = Math.max(0, Math.min(preview.duration, Number(value)));
}
async function startPlayback(sequence) {
  try {
    await preview.play();
    if (sequence === loadSequence) setPlayerStatus('Playing narrated still preview.');
  } catch (error) {
    if (sequence !== loadSequence || error.name === 'AbortError') return;
    setPlayerStatus(error.name === 'NotAllowedError' ? 'Press Play to start this preview.' : 'Could not play this preview. Try the full-quality link.', true);
  }
  updateControls();
}
function togglePlayback() {
  if (preview.paused) startPlayback(loadSequence);
  else preview.pause();
}
function play(src, title) {
  loadSequence += 1;
  preview.pause();
  preview.src = src;
  const audioOnly = /\.m4a$/i.test(src);
  preview.classList.toggle('audio-mode', audioOnly);
  const item = audioOnly ? src[0] + '01' : src.split('/').pop().split('-')[0];
  document.getElementById('playing').textContent = title;
  setPlayerStatus('Loading preview...');
  preview.load();
  startPlayback(loadSequence);
}
['loadedmetadata', 'durationchange', 'timeupdate', 'pause', 'play', 'seeked', 'volumechange'].forEach(name => preview.addEventListener(name, updateControls));
preview.addEventListener('loadedmetadata', () => { preview.playbackRate = Number(document.getElementById('preview-speed').value); });
preview.addEventListener('pause', () => { if (preview.paused && preview.readyState >= 2 && !preview.ended) setPlayerStatus('Preview paused.'); });
preview.addEventListener('ended', () => setPlayerStatus('Preview finished. Choose another clip or press Play.'));
preview.addEventListener('error', () => setPlayerStatus('This preview could not load. Try the full-quality link.', true));
document.querySelectorAll('.decision').forEach(control => {
  try { control.value = localStorage.getItem('sl08-r4-' + control.dataset.id) || 'pending'; } catch (_) {}
  control.onchange = () => { try { localStorage.setItem('sl08-r4-' + control.dataset.id, control.value); } catch (_) {} };
});
function saveDecisions() {
  const data = { stage: 'round4-revised-frame-pairs', date: new Date().toISOString(), notes: document.getElementById('reply').value,
    items: ITEMS.map(item => ({ ...item, verdict: document.querySelector('[data-id="' + item.id + '"]').value })) };
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
  link.download = 'Calories-Shorts-R4-frame-decisions.json';
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
}
updateControls();
