'use strict';

const crypto = require('crypto');
const DAY = 86400000;
const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

// A paid event enrolls a member. Access status alone is NOT proof of payment.
// Delivery is durable across deploys; a short lease plus Resend's idempotency
// key handles concurrent sweeps and a crash between sending and recording it.
function createMemberEmails({ db, fetch, apiKey, from, replyTo, siteUrl, secret, optedOut = () => false, now = () => new Date() }) {
  const token = id => crypto.createHmac('sha256', secret).update(`member-email:${id}`).digest('hex');
  const unsubscribeUrl = id => `${siteUrl}/api/member-emails/unsubscribe?id=${id}&token=${token(id)}`;
  async function enroll(userId, reference) {
    if (!db || !reference) return;
    await db.query(`INSERT INTO member_email_enrollments (user_id, payment_reference, next_at)
      VALUES ($1,$2,$3) ON CONFLICT (user_id) DO NOTHING`, [userId, reference, now()]);
  }
  async function unsubscribe(id, suppliedToken) {
    if (!/^\d+$/.test(String(id))) return false;
    const expected = Buffer.from(token(id));
    const actual = Buffer.from(String(suppliedToken || ''));
    if (actual.length !== expected.length || !crypto.timingSafeEqual(actual, expected)) return false;
    await db.query('UPDATE member_email_enrollments SET opted_out = true WHERE user_id = $1', [Number(id)]);
    return true;
  }
  function message(member, step, hasProgram) {
    const link = `${siteUrl}/?login=1`;
    let subject, body;
    if (step === 0) {
      subject = 'Getting started with your Abs By AI membership';
      body = `<p>Thanks for being an Abs By AI member.</p><p>Your membership includes your AI Trainer, AI Nutritionist, meal tracking, Progress Log and transformations.</p><p><strong>Start with your workout program.</strong> Sign in, open AI Trainer and answer the questions about your goal and available equipment. If you already have a program, open it and choose your next workout.</p>`;
    } else if (step === 1) {
      subject = hasProgram ? 'Your next workout in Abs By AI' : 'Have you built your workout program?';
      body = hasProgram
        ? '<p>Your workout program is saved in Abs By AI. Open AI Trainer, choose your next workout and record your completed sets as you go.</p><p>Pick a time for that workout today so you know when it will happen.</p>'
        : '<p>If you have not started yet, open AI Trainer and build your workout program. You can choose the equipment you have, including a home setup.</p><p>You do not need to set up every feature at once. Start with your first workout.</p>';
    } else {
      subject = step === 2 ? 'Your first Abs By AI progress check-in' : 'Your weekly Abs By AI check-in';
      body = '<p>Take a few minutes to check your progress in Abs By AI.</p><p>Open your workout program and review your completed workouts. Use the Progress Log to record a fresh update, then choose the workouts you will do this week.</p><p>If tracking meals has been difficult, start by logging your next meal. Your AI Nutritionist can help you plan what to eat.</p>';
    }
    const unsub = unsubscribeUrl(member.user_id);
    const html = `${body}<p><a href="${escapeHtml(link)}">Open my Abs By AI account</a></p><p>If you need help, reply to this email and tell us where you are stuck.</p><p>Dan<br>Abs By AI</p><hr><p style="font-size:12px;color:#666">You receive these product-use emails as an Abs By AI member. <a href="${escapeHtml(unsub)}">Stop member check-in emails</a>. Account and payment emails will continue.</p>`;
    return { from, to: [member.email], reply_to: replyTo, subject, html,
      headers: { 'List-Unsubscribe': `<${unsub}>`, 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' } };
  }
  async function sweep() {
    if (!db || !apiKey) return { sent: 0 };
    const time = now();
    const { rows } = await db.query(`SELECT e.*, u.email, u.membership_status, u.membership_period_end
      FROM member_email_enrollments e JOIN users u ON u.id = e.user_id
      WHERE e.opted_out = false AND e.next_at <= $1 AND u.membership_status = 'active'
      AND (u.membership_period_end IS NULL OR u.membership_period_end > $1)
      ORDER BY e.next_at LIMIT 100`, [time]);
    let sent = 0;
    for (const member of rows) {
      if (/@example\.(com|net|org)$/i.test(member.email) || optedOut(member.email)) continue;
      const key = `member-checkin/${member.user_id}/${member.step}`;
      const hasProgram = (await db.query('SELECT id FROM programs WHERE user_id = $1 LIMIT 1', [member.user_id])).rows.length > 0;
      const payload = message(member, member.step, hasProgram);
      await db.query(`INSERT INTO member_email_deliveries (send_key,user_id,payload)
        VALUES ($1,$2,$3) ON CONFLICT (send_key) DO NOTHING`, [key, member.user_id, JSON.stringify(payload)]);
      // Freeze the payload for a retry: Resend requires the same key AND body.
      const claim = await db.query(`UPDATE member_email_deliveries SET lease_until = $2,
        first_attempt_at = COALESCE(first_attempt_at,$3)
        WHERE send_key = $1 AND sent_at IS NULL AND blocked = false
        AND (lease_until IS NULL OR lease_until < $3) RETURNING *`, [key, new Date(time.getTime() + 5 * 60000), time]);
      const delivery = claim.rows[0];
      if (!delivery) continue;
      // An unresolved send older than Resend's 24h dedupe window needs review,
      // never a blind resend which could deliver a duplicate.
      if (time - new Date(delivery.first_attempt_at) > 23 * 3600000) {
        await db.query('UPDATE member_email_deliveries SET blocked = true, last_error = $2 WHERE send_key = $1', [key, 'Delivery uncertain beyond idempotency window; inspect provider log']);
        console.error('MEMBER_EMAIL_REVIEW_REQUIRED', key);
        continue;
      }
      try {
        const response = await fetch('https://api.resend.com/emails', { method: 'POST',
          headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json', 'Idempotency-Key': key },
          body: JSON.stringify(delivery.payload), timeout: 20000 });
        if (!response.ok) throw new Error(`Resend ${response.status}: ${(await response.text()).slice(0,200)}`);
        const result = await response.json();
        if (!result.id) throw new Error('Resend response has no email id');
        await db.query('UPDATE member_email_deliveries SET sent_at = $2, provider_id = $3, last_error = NULL WHERE send_key = $1', [key, time, result.id]);
        await advance(member, time);
        sent++;
        console.log('MEMBER_EMAIL_ACCEPTED', key, result.id);
      } catch (error) {
        await db.query('UPDATE member_email_deliveries SET last_error = $2 WHERE send_key = $1', [key, String(error.message).slice(0,300)]);
        console.error('MEMBER_EMAIL_FAILED', key, error.message);
      }
    }
    // Recover a crash after recording delivery but before advancing the sequence.
    const completed = await db.query(`SELECT e.* FROM member_email_enrollments e
      JOIN member_email_deliveries d ON d.user_id = e.user_id
      WHERE d.send_key = 'member-checkin/' || e.user_id::text || '/' || e.step::text AND d.sent_at IS NOT NULL`);
    for (const member of completed.rows) await advance(member, time);
    return { sent };
  }
  async function advance(member, time) {
    const delay = member.step === 0 ? 2 : member.step === 1 ? 5 : 7;
    await db.query(`UPDATE member_email_enrollments SET step = step + 1, next_at = $3
      WHERE user_id = $1 AND step = $2`, [member.user_id, member.step, new Date(time.getTime() + delay * DAY)]);
  }
  return { enroll, sweep, unsubscribe, message, unsubscribeUrl };
}
module.exports = { createMemberEmails };
