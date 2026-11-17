# Night-before personal planning

Dan changed this workflow November 16, 2026. The deliverable is the proposed board and calendar at https://absbyai.com/dash, not a long plan in chat. Default to planning tomorrow the night before so he can start priority #1 at 8 a.m. Use America/Chicago dates.

Standard hours every day, including weekends: work 8–9:30 a.m.; reserve 9:30–11:30 a.m. for gym preparation, workout, shower and supplements; work 11:30 a.m.–7 p.m., except Tuesday ends at 6:30 p.m. Include lunch, real Google Calendar commitments and preparation/travel buffers. Five big outcomes are targets, not guaranteed finishes. Preserve Dan's ranked priorities unless he agrees to reorder them.

The board contains exactly Planned for Today, In Progress, Completed and the shared human Assistant Taskboard. Personal planning must not dispatch AI work or write tasks into the human assistant's list. Keep the edit-dashboard link. Cards default to titles only; optional details can be added later. Preserve existing cards and attachments, and keep unfinished cards from other dates available for deliberate carry-forward.

Before proposing, check the live personal board and Google Calendar for the planned date. Read the relevant owning task's compact status if it changes the recommendation. Do not create or message execution chats as a side effect of planning. No automatic recurrence/reminder has been requested. The standard routine is a dashboard template, not a set of recurring Google Calendar events.

## Read and propose

From this repo, use the existing owner database connection without exposing values:

```sh
node workboard/plan-day.js read --env-file "$HOME/.absbyai-secrets.env"
node workboard/plan-day.js propose --env-file "$HOME/.absbyai-secrets.env" < /absolute/private/plan.json
```

`propose` accepts `{date, priorities: ["Card title"], blocks: [{title, start: "08:00", end: "09:30", kind: "work", cardTitle: "Card title"}], note, calendarCheckedAt}`. Kinds: work, break, commitment, travel. `source: "google"` identifies an actual freshly verified appointment, never a proposed work block. `calendarCheckedAt` is the real UTC time of the calendar read. Times are Central wall-clock times for that date. The helper validates the proposal before writing and uses versioned writes, preserves unrelated data, links blocks to cards and avoids duplicate personal titles on repeated proposals. It never writes Google Calendar.

Re-read the saved plan, inspect the live board/calendar at `https://absbyai.com/dash?date=YYYY-MM-DD`, and return the direct review link with a short note about assumptions or tradeoffs. Adjust that same saved plan in response to Dan's changes. Do not present another long task list in chat. The site permits editing block times and accepting a proposal; changing blocks returns it to Proposed.

Acceptance currently means accepting the dashboard plan only. Do not claim Google sync. If Dan requests copying accepted blocks into Google Calendar, recheck conflicts, use the connected calendar tools, and verify the saved events; preserve fixed appointments and avoid duplicate events. No Google write happens while the plan is still a proposal. The older Victory Dashboard `/dashboard`, `/api/todos`, `/api/task-checks`, `/api/plan` remain outside personal planning. Existing human-assistant task handling remains unchanged.
