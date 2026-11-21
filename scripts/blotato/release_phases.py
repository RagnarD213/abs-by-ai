"""Dated release phases for organic videos (Dan approved 2026-10-28; plan: Docs/LONGFORM_RELEASE_CALENDAR.md).

One place that says which weekdays carry a long-form, which days carry Shorts and at what local time, and what
content a phase may hold. video_topup.py and longform_queue.py import it; change the plan here, not in them.

Weekdays: Mon=0 ... Sun=6. All times America/Chicago.

  phase 0  before Oct 29 2026   long-form Sun+Wed; Shorts Mon/Tue/Thu/Fri/Sat 9 AM (the Oct 17 rule)
  phase 1  Oct 29 - Nov 25      long-form Sun+Wed; Shorts Mon/Tue/Thu/Fri/Sat 9 AM; NO kitchen footage
  phase 2  Nov 26 - Dec 25      long-form Sun+Wed+Fri (none Dec 25); Shorts 9 AM + 6 PM on every day without a long-form
  phase 3  Dec 26 - Jan 31      long-form Sun+Wed+Fri; Shorts 9 AM + 6 PM Mon/Tue/Thu/Sat; no kitchen
  phase 4  from Feb 1           long-form Sunday; Shorts Mon-Sat 9 AM; kitchen Shorts allowed

A Short on a long-form day goes to Blotato only when that day has no film booked (the film's slot falls back to a Short).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

NO_LONGFORM_DATES = {date(2026, 12, 25)}  # Christmas Day: Shorts only
# Kitchen material that may air in phase 1 (Dan, 2026-10-28): How I Make My Daily Salad and its six Shorts.
KITCHEN_EXEMPT_PREFIXES = ("ro05-daily-salad", "sl03-short")
SALAD_PARENT = "ro05-daily-salad"


@dataclass(frozen=True)
class Phase:
    name: str
    start: date
    end: date
    longform_days: tuple
    short_days: tuple
    short_times: tuple          # local "HH:MM"
    allow_kitchen: bool
    extra_short_times_on_longform_days: tuple = ()  # phase 3 test only (see rule in AGENTS.md); empty by default


PHASES = (
    Phase("0", date(2000, 1, 1), date(2026, 10, 28), (6, 2), (0, 1, 3, 4, 5), ("09:00",), True),
    Phase("1", date(2026, 10, 29), date(2026, 11, 25), (6, 2), (0, 1, 3, 4, 5), ("09:00",), False),
    Phase("2", date(2026, 11, 26), date(2026, 12, 25), (6, 2, 4), (0, 1, 2, 3, 4, 5, 6), ("09:00", "18:00"), True),
    Phase("3", date(2026, 12, 26), date(2027, 1, 31), (6, 2, 4), (0, 1, 3, 5), ("09:00", "18:00"), False),
    Phase("4", date(2027, 2, 1), date(2100, 1, 1), (6,), (0, 1, 2, 3, 4, 5), ("09:00",), True),
)


def phase_for(day: date) -> Phase:
    for p in PHASES:
        if p.start <= day <= p.end:
            return p
    return PHASES[-1]


def longform_allowed(day: date) -> bool:
    return day.weekday() in phase_for(day).longform_days and day not in NO_LONGFORM_DATES


def short_times(day: date, longform_booked: bool = False) -> tuple:
    """Local Short slot times on a day. A booked long-form day carries no Short at 9 AM."""
    p = phase_for(day)
    if p.name == "2":
        # Every day without a long-form is a two-Short day; Sun/Wed/Fri are long-form days unless the film is absent.
        if longform_booked and longform_allowed(day):
            return ()
        return p.short_times
    if day.weekday() in p.short_days:
        return p.short_times
    if day.weekday() in p.longform_days and not longform_booked:
        return p.short_times[:1]  # a long-form day without a film becomes a Short day (one 9 AM slot)
    return ()


def is_short_slot(day: date, hhmm: str, longform_booked: bool = False) -> bool:
    return hhmm in short_times(day, longform_booked)


def is_kitchen_exempt(slug: str) -> bool:
    return slug.startswith(KITCHEN_EXEMPT_PREFIXES)


def blocked_by_content(day: date, entry: dict, slug: str) -> bool:
    """True when this entry's content may not air on this day (phase 1 and 3 hold kitchen; gym Shorts wait for January)."""
    p = phase_for(day)
    if entry.get("kitchen") and not p.allow_kitchen and not is_kitchen_exempt(slug):
        return True
    if entry.get("gym") and not entry.get("phase1_test") and day < date(2026, 12, 26):
        return True
    return False


def next_longform_day(after: date, taken: set, reserved: set = frozenset()) -> date:
    day = after + timedelta(days=1)
    while not longform_allowed(day) or day in taken or day in reserved:
        day += timedelta(days=1)
    return day


def next_short_slot(after_day: date, taken: set, entry: dict, slug: str):
    """First (day, 'HH:MM') strictly after `after_day` that is a Short slot, not in `taken` and allowed for the entry.

    Automatic re-slotting never uses a day that is a long-form day: a film may still be booked there. A film-less
    long-form day gets its Short only by an explicit date in the plan (the config's own "main")."""
    day = after_day + timedelta(days=1)
    while True:
        if not longform_allowed(day):
            for hhmm in short_times(day):
                if (day, hhmm) not in taken and not blocked_by_content(day, entry, slug):
                    return day, hhmm
        day += timedelta(days=1)
