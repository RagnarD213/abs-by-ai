'use strict';
document.getElementById('publish-form').addEventListener('submit',async event => {
  event.preventDefault();
  const status = document.getElementById('publish-status'), button = document.getElementById('publish-button');
  const file = document.getElementById('edition-file').files[0];
  if (!file || file.size > 512000) { status.textContent = 'Choose a prepared brief file smaller than 512 KB.'; return; }
  button.disabled = true;
  try {
    const document = JSON.parse(await file.text());
    const response = await fetch('/api/brief/publish',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-Brief-Action':'publish'},body:JSON.stringify(document)});
    if (response.status === 401) { location.replace('/brief-login'); return; }
    if (!response.ok) throw new Error('Publication unavailable');
    const receipt = await response.json();
    if (receipt.ok !== true || receipt.forDate !== document.forDate || receipt.routineEnabled !== document.routineEnabled) throw new Error('Unverified receipt');
    status.textContent = `Published your ${receipt.forDate} edition privately. ${receipt.routineEnabled ? 'Daily updates are enabled.' : 'No enabled daily schedule is recorded for this edition.'} Publication does not change scheduling.`;
  } catch { status.textContent = 'Publication could not be verified. Check the prepared file and your session, then try again.'; }
  finally { button.disabled = false; }
});
