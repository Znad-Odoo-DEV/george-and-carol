/**
 * دفتر المباركات — الخادم
 * ---------------------------------------------------------------------------
 * Google Apps Script bound to a Google Sheet. It is what makes a blessing
 * written on one phone appear on everyone else's: a static page has nowhere to
 * put shared text, and anything kept in the browser would only ever be visible
 * to whoever typed it.
 *
 * No guest signs in. The sheet is the record, and deleting a row removes a
 * blessing from the page — that is the whole moderation story.
 *
 * Setup lives in GUESTBOOK.md. Three steps, about two minutes.
 */

var SHEET_NAME = 'blessings';
var MAX_NAME = 40;
var MAX_MESSAGE = 240;
var MAX_SHOWN = 300;

/** Reads the wall. Newest first. */
function doGet() {
  var rows = sheet().getDataRange().getValues().slice(1); // drop the header
  var entries = [];

  for (var i = rows.length - 1; i >= 0 && entries.length < MAX_SHOWN; i--) {
    var r = rows[i];
    // Type "hidden" in column D to take a blessing down without losing it.
    if (String(r[3]).trim().toLowerCase() === 'hidden') continue;
    if (!String(r[2]).trim()) continue;
    entries.push({ at: r[0], name: String(r[1]), message: String(r[2]) });
  }

  return json({ ok: true, entries: entries });
}

/** Writes one blessing, then hands the fresh wall straight back. */
function doPost(e) {
  var body;
  try {
    body = JSON.parse(e.postData.contents);
  } catch (err) {
    return json({ ok: false, error: 'bad-json' });
  }

  // The honeypot: a field no person can see, so anything in it came from a
  // bot. The answer is a cheerful ok, because telling a bot it failed only
  // teaches it what to change.
  if (String(body.website || '').trim()) return json({ ok: true, entries: [] });

  var name = clean(body.name, MAX_NAME);
  var message = clean(body.message, MAX_MESSAGE);
  if (!name || !message) return json({ ok: false, error: 'empty' });

  // One writer at a time, or two blessings sent together land on one row.
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    sheet().appendRow([new Date().toISOString(), name, message, '']);
  } finally {
    lock.releaseLock();
  }

  return doGet();
}

/**
 * Collapses whitespace and caps length. Control characters go too, so a
 * pasted blessing cannot smuggle line breaks into a single-line cell.
 * Nothing here needs to escape HTML: the page renders every blessing with
 * textContent, never innerHTML.
 */
function clean(value, max) {
  return String(value == null ? '' : value)
    .replace(new RegExp('[\\x00-\\x1f\\x7f]', 'g'), ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, max);
}

function sheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['at', 'name', 'message', 'status']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function json(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(
    ContentService.MimeType.JSON
  );
}
