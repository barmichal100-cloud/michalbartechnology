#!/usr/bin/env python3
# Builds a self-contained, branded price-quote template (quote-template.html) for
# "מיכל בר · פתרונות טכנולוגיים" — Yarden (serif headings) + Assistant (body) + logo,
# all embedded as base64. Editable in the browser, auto-calculating total, prints to PDF.
# Local tool (quote-template.html is gitignored).

import base64, pathlib

def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode("ascii")

Y_REG  = b64("fonts/yarden-regular.woff2")
Y_BOLD = b64("fonts/yarden-bold.woff2")
A_HE   = b64("fonts/assistant-hebrew.woff2")
A_LAT  = b64("fonts/assistant-latin.woff2")
LOGO   = b64("logo.png")

HTML = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>הצעת מחיר · מיכל בר</title>
<style>
@font-face{font-family:'Yarden';src:url(data:font/woff2;base64,__Y_REG__) format('woff2');font-weight:400;font-display:swap;unicode-range:U+0020-0040,U+005B-0060,U+007B-00FF,U+0590-05FF,U+FB1D-FB4F,U+2000-206F,U+20AA;}
@font-face{font-family:'Yarden';src:url(data:font/woff2;base64,__Y_BOLD__) format('woff2');font-weight:700;font-display:swap;unicode-range:U+0020-0040,U+005B-0060,U+007B-00FF,U+0590-05FF,U+FB1D-FB4F,U+2000-206F,U+20AA;}
@font-face{font-family:'Assistant';src:url(data:font/woff2;base64,__A_HE__) format('woff2');font-weight:400 700;font-display:swap;unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F;}
@font-face{font-family:'Assistant';src:url(data:font/woff2;base64,__A_LAT__) format('woff2');font-weight:400 700;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+2074,U+20AC,U+2122,U+2212;}
:root{
  --paper:#FDFBF8; --paper-2:#F3EDE4; --paper-3:#E6DDD0;
  --ink:#2A2230; --ink-soft:#6E6576; --accent:#C76B45; --accent-soft:#e8c6a3; --amber:#E3A45C;
}
*{box-sizing:border-box;}
body{margin:0;background:#E7E0D6;font-family:'Assistant','Yarden',Arial,sans-serif;color:var(--ink);line-height:1.45;}

.toolbar{position:sticky;top:0;z-index:10;display:flex;gap:.7rem;justify-content:center;align-items:center;
  flex-wrap:wrap;padding:.8rem 1rem;background:var(--ink);}
.toolbar button{font-family:inherit;font-weight:700;font-size:.95rem;border:0;border-radius:999px;padding:.6rem 1.4rem;cursor:pointer;}
.btn-pdf{background:var(--accent);color:#fff;}
.btn-pdf:hover{background:#a9522f;}
.hint{color:#c9bfb4;font-size:.82rem;}

.page{width:210mm;min-height:297mm;margin:1.6rem auto;background:var(--paper);
  box-shadow:0 12px 45px rgba(0,0,0,.22);padding:13mm 16mm;}

[contenteditable]{outline:none;}
[contenteditable]:hover{background:rgba(227,164,92,.12);border-radius:5px;}
[contenteditable]:focus{background:rgba(227,164,92,.22);border-radius:5px;}

.q-head{display:flex;align-items:center;gap:1.1rem;border-bottom:3px solid var(--accent);padding-bottom:.6rem;}
.q-head img{height:64px;width:auto;}
.q-head .brand{flex:1;text-align:center;}
.q-head .brand h1{margin:0;font-family:'Yarden',serif;font-size:1.85rem;color:var(--ink);}
.q-head .brand p{margin:.25rem 0 0;color:var(--ink-soft);font-size:.92rem;}
.q-head .title .label{font-family:'Yarden',serif;font-size:1.65rem;font-weight:700;color:var(--accent);white-space:nowrap;}

.meta{display:flex;flex-wrap:wrap;gap:.3rem 2.2rem;margin:.7rem 0 .2rem;font-size:.96rem;}
.meta .lbl{color:var(--ink-soft);}
.intro{margin:.6rem 0 .7rem;}

table.items{width:100%;border-collapse:collapse;margin:.4rem 0;}
table.items th{background:var(--paper-2);color:var(--ink);text-align:right;padding:.4rem .9rem;font-size:.9rem;font-weight:700;border-bottom:2px solid var(--paper-3);}
table.items td{padding:.4rem .9rem;border-bottom:1px solid var(--paper-3);vertical-align:top;}
.note{font-size:.82rem;color:var(--ink-soft);margin-top:.15rem;line-height:1.45;}
.note:empty::before{content:attr(data-ph);color:var(--accent-soft);}
.col-price{width:150px;text-align:left;white-space:nowrap;font-variant-numeric:tabular-nums;}
.col-x{width:30px;}
.rm{cursor:pointer;color:var(--accent-soft);border:0;background:none;font-size:1.05rem;line-height:1;}
.rm:hover{color:var(--accent);}
tfoot td{padding:.32rem .9rem;font-variant-numeric:tabular-nums;}
.subtotal-row td,.discount-row td{color:var(--ink-soft);}
.discount-val{color:var(--accent);text-align:left;white-space:nowrap;}
.disc-pct{color:var(--accent);font-weight:700;}
.total-row td{border-top:2.5px solid var(--accent);font-weight:700;font-size:1.22rem;padding-top:.5rem;}
.total-val{color:var(--accent);text-align:left;}

.add-row{margin:.3rem 0 .6rem;}
.add-row button{background:var(--paper-2);border:1px dashed var(--amber);color:var(--ink);border-radius:8px;padding:.45rem 1.1rem;cursor:pointer;font-family:inherit;font-size:.9rem;}
.add-row button:hover{background:var(--paper-3);}

.section-h{font-family:'Yarden',serif;font-weight:700;color:var(--accent);margin:.9rem 0 .35rem;font-size:1.12rem;border-bottom:1px solid var(--paper-3);padding-bottom:.25rem;}
ul.incl{margin:.2rem 0;padding-inline-start:1.4rem;}
ul.incl li{margin:.12rem 0;}
.terms{font-size:.88rem;color:var(--ink-soft);}
.terms p{margin:.2rem 0;}

.sign-note{font-size:.86rem;color:var(--ink-soft);margin:.1rem 0 .4rem;}
.signatures{display:flex;gap:3rem;margin:.3rem 0 .2rem;break-inside:avoid;}
.sig{flex:1;max-width:62%;}
.sig-role{font-weight:700;color:var(--ink);margin-bottom:.3rem;font-size:.98rem;}
.sig-field{display:flex;align-items:flex-end;gap:.45rem;margin:.34rem 0;}
.sig-lbl{color:var(--ink-soft);font-size:.9rem;white-space:nowrap;}
.sig-blank{flex:1;border-bottom:1px solid var(--ink-soft);min-height:1.2rem;line-height:1.2rem;color:var(--ink);}

.q-foot{margin-top:.95rem;border-top:1px solid var(--paper-3);padding-top:.6rem;display:flex;
  justify-content:space-between;align-items:flex-end;font-size:.9rem;color:var(--ink-soft);}
.sign{text-align:center;}
.sign .name{font-family:'Yarden',serif;font-weight:700;color:var(--ink);font-size:1.1rem;}
.q-foot a{color:var(--accent);text-decoration:none;}
.li-link{display:inline-flex;align-items:center;gap:.35rem;margin-top:.3rem;color:var(--accent);text-decoration:none;font-weight:700;}
.li-link svg{flex:none;}

@media print{
  @page{size:A4;margin:0;}
  html,body{background:var(--paper) !important;}
  .toolbar{display:none !important;}
  .rm,.add-row{display:none !important;}
  .note:empty{display:none !important;}
  .page{box-shadow:none;margin:0 auto;width:auto;min-height:0;background:var(--paper);padding:6mm 14mm;}
  [contenteditable]:hover,[contenteditable]:focus{background:none !important;}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
}
</style>
</head>
<body>
  <div class="toolbar">
    <button class="btn-pdf" onclick="window.print()">⬇&nbsp; ייצא ל-PDF</button>
    <span class="hint">לחצי על כל טקסט כדי לערוך · הסה״כ מתעדכן לבד · בחלון ההדפסה בחרי "שמירה כ-PDF"</span>
  </div>

  <div class="page">
    <header class="q-head">
      <div class="title"><div class="label">הצעת מחיר</div></div>
      <div class="brand">
        <h1 contenteditable="true">מיכל בר</h1>
        <p contenteditable="true">פתרונות טכנולוגיים · ייעוץ · פיתוח · אוטומציה</p>
      </div>
      <img src="data:image/png;base64,__LOGO__" alt="מיכל בר">
    </header>

    <div class="meta">
      <div><span class="lbl">לכבוד:</span> <span contenteditable="true">______________</span></div>
      <div><span class="lbl">תאריך:</span> <span contenteditable="true" dir="ltr">DD/MM/YYYY</span></div>
      <div><span class="lbl">בתוקף עד:</span> <span contenteditable="true" dir="ltr">DD/MM/YYYY</span></div>
    </div>

    <p class="intro" contenteditable="true">תודה על פנייתכם! להלן הצעת מחיר עבור [שם הפרויקט]. ההצעה מבוססת על הצרכים שעלו בשיחתנו וכוללת אפיון, עיצוב ופיתוח מקצה לקצה. אשמח להתאים את ההצעה לכל שינוי או דגש.</p>

    <table class="items">
      <thead>
        <tr><th>תיאור</th><th class="col-price">מחיר (₪)</th><th class="col-x"></th></tr>
      </thead>
      <tbody id="rows">
        <tr><td><div contenteditable="true">אפיון ואסטרטגיה – מיפוי הצורך, הגדרת הפתרון ותכנון</div><div class="note" contenteditable="true" data-ph="הערה (אופציונלי)"></div></td><td class="col-price price" contenteditable="true">0</td><td class="col-x"><button class="rm" onclick="rm(this)">✕</button></td></tr>
        <tr><td><div contenteditable="true">עיצוב ופיתוח – בניית הפתרון מקצה לקצה</div><div class="note" contenteditable="true" data-ph="הערה (אופציונלי)"></div></td><td class="col-price price" contenteditable="true">0</td><td class="col-x"><button class="rm" onclick="rm(this)">✕</button></td></tr>
      </tbody>
      <tfoot>
        <tr class="subtotal-row" id="subtotalRow"><td>סכום ביניים</td><td class="col-price" id="subtotal">₪0</td><td></td></tr>
        <tr class="discount-row" id="discountRow"><td>הנחה <span class="disc-pct" contenteditable="true">10</span>%</td><td class="col-price discount-val" id="discountVal">−₪0</td><td class="col-x"><button class="rm" onclick="removeDiscount()" title="הסר הנחה">✕</button></td></tr>
        <tr class="total-row"><td>סה״כ לתשלום</td><td class="col-price total-val" id="total">₪0</td><td></td></tr>
      </tfoot>
    </table>
    <div class="add-row">
      <button onclick="addRow()">＋ הוסף שורה</button>
      <button id="addDiscountBtn" onclick="addDiscount()" style="display:none;">＋ הוסף הנחה</button>
    </div>

    <div class="section-h">מה ההצעה כוללת</div>
    <ul class="incl" contenteditable="true">
      <li>אפיון מעמיק והגדרת פתרון מדויק</li>
      <li>עיצוב ופיתוח מותאמים אישית</li>
      <li>בדיקות, התאמות והשקה</li>
      <li>ליווי וזמינות לאורך כל הפרויקט</li>
    </ul>

    <div class="section-h">תנאים</div>
    <div class="terms" contenteditable="true">
      <p>• המחירים אינם כוללים מע״מ.</p>
      <p>• תנאי תשלום: 40% מקדמה לתחילת העבודה, 30% באבן דרך מוסכמת, 30% בסיום ולפני המסירה.</p>
      <p>• לוחות הזמנים יתואמו לאחר השלמת האפיון.</p>
      <p>• זכויות השימוש בתוצר עוברות ללקוח עם השלמת התשלום המלא.</p>
      <p>• תמיכה ותיקון תקלות: עד 30 יום מהמסירה, ללא עלות.</p>
    </div>

    <div class="section-h">אישור וחתימה</div>
    <p class="sign-note">חתימה על הצעה זו מהווה אישור ההזמנה והסכמה לכל התנאים המפורטים בה, ובאה במקום חוזה נפרד.</p>
    <div class="signatures">
      <div class="sig">
        <div class="sig-role">הלקוח/ה</div>
        <div class="sig-field"><span class="sig-lbl">שם:</span><span class="sig-blank" contenteditable="true">&nbsp;</span></div>
        <div class="sig-field"><span class="sig-lbl">חתימה:</span><span class="sig-blank"></span></div>
        <div class="sig-field"><span class="sig-lbl">תאריך:</span><span class="sig-blank" contenteditable="true" dir="ltr">&nbsp;</span></div>
      </div>
    </div>

    <footer class="q-foot">
      <div>
        מיכל בר · פתרונות טכנולוגיים<br>
        <a href="tel:+972547105176">054-710-5176</a> · <a href="https://michalbartech.com">michalbartech.com</a><br>
        <a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=barmichal100@gmail.com&amp;su=הצעת+מחיר+-+מיכל+בר" target="_blank" rel="noopener">barmichal100@gmail.com</a><br>
        <a class="li-link" href="https://www.linkedin.com/in/michal-bar-9100825b/">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg>
          התחברו · <span dir="ltr">LinkedIn</span>
        </a>
      </div>
      <div class="sign">בברכה,<br><span class="name" contenteditable="true">מיכל בר</span></div>
    </footer>
  </div>

  <script>
    function fmt(n){ return '₪' + (Math.round(n)||0).toLocaleString('he-IL'); }
    var hasDiscount = true;
    function recalc(){
      var subtotal=0;
      document.querySelectorAll('#rows .price').forEach(function(c){
        subtotal += parseFloat((c.textContent||'').replace(/[^0-9.]/g,'')) || 0;
      });
      var total=subtotal;
      if(hasDiscount){
        var pct=parseFloat((document.querySelector('.disc-pct').textContent||'').replace(/[^0-9.]/g,'')) || 0;
        var disc=Math.round(subtotal*pct/100);
        total=subtotal-disc;
        document.getElementById('subtotal').textContent=fmt(subtotal);
        document.getElementById('discountVal').textContent='−'+fmt(disc);
      }
      document.getElementById('total').textContent=fmt(total);
    }
    function setDiscount(on){
      hasDiscount=on;
      document.getElementById('subtotalRow').style.display=on?'':'none';
      document.getElementById('discountRow').style.display=on?'':'none';
      document.getElementById('addDiscountBtn').style.display=on?'none':'';
      recalc();
    }
    function removeDiscount(){ setDiscount(false); }
    function addDiscount(){ setDiscount(true); }
    function rm(btn){ btn.closest('tr').remove(); recalc(); }
    function addRow(){
      var tr=document.createElement('tr');
      tr.innerHTML='<td><div contenteditable="true">שורה חדשה</div><div class="note" contenteditable="true" data-ph="הערה (אופציונלי)"></div></td>'+
        '<td class="col-price price" contenteditable="true">0</td>'+
        '<td class="col-x"><button class="rm" onclick="rm(this)">✕</button></td>';
      document.getElementById('rows').appendChild(tr);
      recalc();
    }
    document.addEventListener('input',function(e){
      if(e.target.classList && (e.target.classList.contains('price')||e.target.classList.contains('disc-pct'))) recalc();
    });
    recalc();
  </script>
</body>
</html>
"""

HTML = (HTML.replace("__Y_REG__", Y_REG).replace("__Y_BOLD__", Y_BOLD)
            .replace("__A_HE__", A_HE).replace("__A_LAT__", A_LAT)
            .replace("__LOGO__", LOGO))
pathlib.Path("quote-template.html").write_text(HTML, encoding="utf-8")
print("wrote quote-template.html  (%.0f KB)" % (len(HTML.encode("utf-8")) / 1024))
