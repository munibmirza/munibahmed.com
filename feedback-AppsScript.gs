// Feedback backend for munibahmed.com
// Sheet tab MUST be named "Feedback" with row 1 headers (exact order):
// Timestamp | Name | Designation | LinkedIn | Photo | Message | Approved | Relationship
// A row shows on the website ONLY when its "Approved" cell = Yes

var SHEET_NAME = 'Feedback';

function doGet(e) {
  var cb = e && e.parameter && e.parameter.callback;
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  var rows = [];
  if (sheet && sheet.getLastRow() > 1) {
    var values = sheet.getDataRange().getValues();
    for (var i = 1; i < values.length; i++) {
      var r = values[i];
      if (String(r[6]).trim().toLowerCase() === 'yes') {
        rows.push({
          name: r[1], designation: r[2], linkedin: r[3],
          photo: r[4], message: r[5], relationship: r[7]
        });
      }
    }
  }
  rows.reverse();
  var out = JSON.stringify(rows);
  if (cb) {
    return ContentService.createTextOutput(cb + '(' + out + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(out)
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    if (p.website) return json({ ok: true });

    var name = String(p.name || '').slice(0, 80).trim();
    var message = String(p.message || '').slice(0, 1000).trim();
    if (!name || !message) return json({ ok: false, error: 'missing name/message' });

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    sheet.appendRow([
      new Date(),
      name,
      String(p.designation || '').slice(0, 120).trim(),
      String(p.linkedin || '').slice(0, 200).trim(),
      String(p.photo || '').slice(0, 300).trim(),
      message,
      'No',
      String(p.relationship || '').slice(0, 20).trim()
    ]);
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function json(o) {
  return ContentService.createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}
