#!/usr/bin/env python3
# Generates the multi-page site for michalbartech.com (static HTML, shared /assets/site.css).
# Each page: unique <title>/description/H1, canonical, breadcrumbs, FAQ + JSON-LD schema.
# The homepage (index.html) is maintained separately; this builds the inner pages.
# Run:  python build_pages.py

import json, os, pathlib

SITE = "https://michalbartech.com"
GA = "G-ZF50CS11HZ"
BIZ = SITE + "/#business"

def j(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)

# ---------- shared partials ----------
def head(title, desc, path, schemas):
    canonical = SITE + path
    ld = ""
    if schemas:
        graph = {"@context": "https://schema.org", "@graph": schemas}
        ld = '<script type="application/ld+json">\n' + j(graph) + '\n</script>\n'
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:locale" content="he_IL" />
<meta property="og:image" content="{SITE}/og-image.jpg" />
<meta property="og:site_name" content="מיכל בר · פתרונות טכנולוגיים" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{SITE}/og-image.jpg" />
<link rel="icon" href="/logo.png" type="image/png">
<link rel="apple-touch-icon" href="/logo.png">
{ld}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header id="hdr">
  <div class="wrap">
    <nav>
      <a class="brand" href="/">
        <img class="logo" src="/logo.png" alt="מיכל בר" />
        <div><b>מיכל בר</b><small>פיתוח · אוטומציה · סוכני AI</small></div>
      </a>
      <div class="nav-links" id="navlinks">
        <a href="/services">שירותים</a>
        <a href="/about">עליי</a>
        <a href="/projects">פרויקטים</a>
        <a href="/faq">שאלות נפוצות</a>
        <a href="/blog">בלוג</a>
        <a class="nav-cta" href="/contact">צרו קשר</a>
      </div>
      <button class="burger" id="burger" aria-label="תפריט"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>
'''

FOOTER = '''<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-brand">
      <div class="brand">
        <img class="logo" src="/logo.png" alt="מיכל בר" />
        <div><b>מיכל בר</b><small>פיתוח · אוטומציה · סוכני AI</small></div>
      </div>
      <p>פיתוח מערכות ואתרים, אוטומציה וסוכני AI – לעסקים, לעצמאים וליזמים. מהבנת הצורך ועד המימוש.</p>
    </div>
    <div class="footer-col">
      <h4>ניווט</h4>
      <a href="/services">שירותים</a>
      <a href="/about">עליי</a>
      <a href="/projects">פרויקטים</a>
      <a href="/faq">שאלות נפוצות</a>
      <a href="/blog">בלוג</a>
      <a href="/contact">צרו קשר</a>
      <a href="/accessibility">הצהרת נגישות</a>
      <a href="/privacy">מדיניות פרטיות</a>
    </div>
    <div class="footer-col">
      <h4>שירותים</h4>
      <a href="/services/product-development">פיתוח מוצרים ואתרים</a>
      <a href="/services/automation">אוטומציה וסוכני AI</a>
      <a href="/services/consulting">ייעוץ ואפיון טכנולוגי</a>
      <div class="footer-icons">
        <a href="https://wa.me/972547105176" target="_blank" rel="noopener" aria-label="וואטסאפ"><svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.04 4C9.93 4 4.98 8.95 4.98 15.06c0 2.05.56 4.05 1.62 5.8L4 28l7.3-2.55a11.04 11.04 0 0 0 4.74 1.07h.01c6.11 0 11.06-4.95 11.06-11.06C27.1 8.95 22.15 4 16.04 4zm0 20.2c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-4.33 1.51 1.45-4.22-.2-.32a9.16 9.16 0 0 1-1.4-4.87c0-5.06 4.12-9.18 9.19-9.18 2.45 0 4.76.96 6.49 2.69a9.13 9.13 0 0 1 2.69 6.5c0 5.06-4.12 9.18-9.18 9.18z"/></svg></a>
        <a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg></a>
      </div>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span class="mono">2026</span> מיכל בר · כל הזכויות שמורות</span>
    <span>פיתוח · אוטומציה · סוכני AI</span>
  </div>
</footer>
<script>
  var hdr=document.getElementById('hdr');
  addEventListener('scroll',function(){hdr.classList.toggle('scrolled',scrollY>10);});
  var burger=document.getElementById('burger'),navlinks=document.getElementById('navlinks');
  if(burger){burger.addEventListener('click',function(){burger.classList.toggle('open');navlinks.classList.toggle('open');});
    navlinks.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){burger.classList.remove('open');navlinks.classList.remove('open');});});}
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a||!window.gtag)return;var h=a.getAttribute('href')||'';
    if(h.indexOf('wa.me')!==-1) gtag('event','contact_click',{method:'whatsapp'});
    else if(h.indexOf('tel:')===0) gtag('event','contact_click',{method:'phone'});
    else if(h.indexOf('linkedin.com')!==-1) gtag('event','contact_click',{method:'linkedin'});});
</script>
</body>
</html>'''

def crumbs(trail):
    # trail: list of (name, url_or_None)
    parts, items = [], []
    for i,(name,url) in enumerate(trail):
        if url:
            parts.append(f'<a href="{url}">{name}</a>')
        else:
            parts.append(f'<span>{name}</span>')
        items.append({"@type":"ListItem","position":i+1,"name":name,
                      **({"item":SITE+url} if url else {})})
    sep = ' <span class="sep">›</span> '
    html = '<nav class="breadcrumb" aria-label="breadcrumb">' + sep.join(parts) + '</nav>'
    schema = {"@type":"BreadcrumbList","itemListElement":items}
    return html, schema

def faq_block(pairs):
    rows = "\n".join(
        f'    <details><summary>{q}</summary><p class="a">{a}</p></details>' for q,a in pairs)
    html = f'''  <section class="wrap" style="padding-top:14px;padding-bottom:20px;">
    <h2 class="s-head" style="font-size:clamp(26px,4vw,38px);">שאלות נפוצות</h2>
    <div class="faq">
{rows}
    </div>
  </section>'''
    schema = {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}
    return html, schema

# Shared contact grid (WhatsApp + LinkedIn panel + lead form + EmailJS) — used both
# on the /contact page (with an H1 hero) and at the bottom of every inner page (as CTA, with an H2).
CONTACT_GRID = '''  <section class="wrap">
    <div class="contact-grid">
      <div class="contact-side">
        <a class="wa-circle" href="https://wa.me/972547105176" target="_blank" rel="noopener" aria-label="וואטסאפ">
          <svg viewBox="0 0 32 32" fill="#fff" aria-hidden="true"><path d="M16.04 4C9.93 4 4.98 8.95 4.98 15.06c0 2.05.56 4.05 1.62 5.8L4 28l7.3-2.55a11.04 11.04 0 0 0 4.74 1.07h.01c6.11 0 11.06-4.95 11.06-11.06C27.1 8.95 22.15 4 16.04 4zm0 20.2c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-4.33 1.51 1.45-4.22-.2-.32a9.16 9.16 0 0 1-1.4-4.87c0-5.06 4.12-9.18 9.19-9.18 2.45 0 4.76.96 6.49 2.69a9.13 9.13 0 0 1 2.69 6.5c0 5.06-4.12 9.18-9.18 9.18zm5.04-6.87c-.28-.14-1.63-.8-1.88-.9-.25-.09-.43-.14-.61.14-.18.28-.7.9-.86 1.08-.16.18-.32.2-.6.07-.28-.14-1.17-.43-2.22-1.37-.82-.73-1.37-1.63-1.53-1.91-.16-.28-.02-.43.12-.57.13-.13.28-.32.42-.48.14-.16.18-.28.28-.46.09-.18.05-.35-.02-.49-.07-.14-.61-1.47-.84-2.01-.22-.53-.44-.46-.61-.46l-.52-.01c-.18 0-.46.07-.7.35-.25.28-.94.92-.94 2.24 0 1.32.96 2.6 1.1 2.78.14.18 1.9 2.9 4.6 4.06.64.28 1.14.44 1.53.57.64.2 1.23.18 1.69.11.52-.08 1.63-.66 1.86-1.31.23-.64.23-1.19.16-1.31-.07-.12-.25-.19-.53-.33z"/></svg>
        </a>
        <p class="wa-cta">דברו איתי ישירות בוואטסאפ</p>
        <a class="wa-phone" href="tel:+972547105176" dir="ltr">054-710-5176</a>
        <p class="li-cta">ובואו להתחבר אליי בלינקדאין</p>
        <div class="social-row">
          <a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg></a>
        </div>
      </div>
      <form class="contact-form" id="contactForm" novalidate autocomplete="on">
        <h3>השאירו פרטים</h3>
        <p class="form-sub">אחזור אליכם תוך 24 שעות</p>
        <div class="field"><label for="name">שם <span class="req">*</span></label>
          <input type="text" id="name" name="name" required maxlength="80" autocomplete="name" placeholder="איך נכון לפנות אליכם?" dir="rtl" /></div>
        <div class="field"><label for="phone">טלפון <span class="req">*</span></label>
          <input type="tel" id="phone" name="phone" maxlength="20" autocomplete="tel" inputmode="tel" placeholder="050-0000000" dir="ltr" /></div>
        <div class="field"><label for="email">דוא״ל <span class="opt">(לא חובה)</span></label>
          <input type="email" id="email" name="email" maxlength="120" autocomplete="email" inputmode="email" placeholder="name@example.com" dir="ltr" /></div>
        <div class="field"><label for="message">ההודעה <span class="opt">(לא חובה)</span></label>
          <textarea id="message" name="message" maxlength="2000" placeholder="ספרו מה אתם מחפשים – אתגר, רעיון, פרויקט..." dir="rtl"></textarea></div>
        <div class="hp-field" aria-hidden="true"><label for="website">Website</label>
          <input type="text" id="website" name="website" tabindex="-1" autocomplete="off" /></div>
        <button type="submit" class="btn1 form-submit">שליחה – ואחזור אליכם</button>
        <p class="form-trust">הפרטים שלכם נשמרים אצלי בלבד · ללא ספאם</p>
        <div class="form-status" id="formStatus" aria-live="polite"></div>
      </form>
    </div>
  </section>
  <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js" defer></script>
  <script>
  document.addEventListener('DOMContentLoaded',function(){
    var form=document.getElementById('contactForm');
    if(!form||typeof emailjs==='undefined')return;
    emailjs.init({publicKey:"v98_thsqHFYtMxHPD"});
    var status=document.getElementById('formStatus');
    var btn=form.querySelector('.form-submit');
    function msg(cls,t){status.className='form-status '+cls;status.textContent=t;}
    function showDone(){status.className='form-status ok';
      status.innerHTML='<div class="status-card"><div class="status-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 12 10 18 20 6"/></svg></div><h4>תודה!</h4><p>ההודעה התקבלה – אחזור אליכם בהקדם</p><button type="button" class="status-action">שליחת הודעה נוספת</button></div>';
      form.classList.add('is-done');
      var again=status.querySelector('.status-action');
      if(again){again.addEventListener('click',function(){form.classList.remove('is-done');status.className='form-status';status.innerHTML='';form.reset();});}}
    form.addEventListener('submit',function(e){e.preventDefault();
      if(form.website.value){return;}
      var name=(form.name.value||'').trim(),phone=(form.phone.value||'').trim(),email=(form.email.value||'').trim();
      if(name.length<2){msg('err','אנא הזינו שם');return;}
      if(!phone){msg('err','אנא הזינו מספר טלפון');return;}
      var digits=phone.replace(/\\D/g,'');
      var validPhone=/^[\\d\\s\\-+()]+$/.test(phone)&&(/^0\\d{8,9}$/.test(digits)||/^972\\d{9}$/.test(digits));
      if(!validPhone){msg('err','מספר טלפון לא תקין');return;}

      if(email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)){msg('err','כתובת מייל לא תקינה');return;}
      var orig=btn.textContent;btn.textContent='שולח…';btn.disabled=true;msg('','');
      emailjs.sendForm('service_y3jd01l','template_mo4oe7j',form)
        .then(function(){showDone();if(window.gtag)gtag('event','generate_lead',{method:'contact_form'});})
        .catch(function(err){console.error('EmailJS error:',err);msg('err','שגיאה בשליחה – נסו שוב או דברו איתי בוואטסאפ');})
        .finally(function(){btn.textContent=orig;btn.disabled=false;});
    });
  });
  </script>
'''

# Bottom-of-page contact section for inner pages: same grid as /contact, but with an H2
# (so each page keeps a single H1) and a "צרו קשר" eyebrow instead of the page hero.
CTA = '''  <section class="wrap page-hero" style="text-align:center;">
    <span class="eyebrow" style="justify-content:center;"><span class="idx">//</span> <span class="ttl">צרו קשר</span></span>
    <h2 class="s-head" style="margin-inline:auto;">יש לכם אתגר, רעיון או פרויקט?</h2>
    <p class="s-lead" style="margin-inline:auto;">שיחת ייעוץ חינם, ללא התחייבות – אחזור אליכם תוך 24 שעות.</p>
  </section>
''' + CONTACT_GRID

def service_schema(name, desc, path):
    return {"@type":"Service","name":name,"description":desc,"serviceType":name,
            "url":SITE+path,"provider":{"@id":BIZ},"areaServed":{"@type":"Country","name":"Israel"}}

def write(path_rel, html):
    fp = pathlib.Path(path_rel)
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(html, encoding="utf-8")
    print("wrote", path_rel)

def page(path, filename, title, desc, trail, body_html, schemas):
    cr_html, cr_schema = crumbs(trail)
    all_schemas = [cr_schema] + schemas
    html = head(title, desc, path, all_schemas)
    html += '<main>\n<div class="wrap">' + cr_html + '</div>\n' + body_html + '\n</main>\n' + FOOTER
    write(filename, html)

# ================= PAGES =================

# ---- /services (hub) ----
svc_cards = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">שירותים</span></span>
    <h1 class="s-head">פיתוח, אוטומציה וסוכני AI – מקצה לקצה</h1>
    <p class="s-lead">משלבת אסטרטגיה, אפיון מדויק, פיתוח, אוטומציה וסוכני AI בליווי אישי מההתחלה ועד התוצאה. שלושה תחומי שירות, גישה אחת: להבין את הצורך השורשי ולבנות את הפתרון הנכון.</p>
    <div class="prose" style="max-width:72ch;margin-top:14px;">
      <p>השירותים מיועדים לעסקים, לעצמאים, ליזמים ולסטארט-אפים – ואפשר להתחיל מכל נקודה: <a href="/services/product-development">פיתוח מוצרים, אתרים ואפליקציות</a>, <a href="/services/automation">אוטומציה וסוכני AI</a>, או <a href="/services/consulting">ייעוץ ואפיון טכנולוגי</a>. מעל 20 שנה בעולמות ההייטק ואינטואיציה מוצרית חדה <a href="/about">מלוות כל פרויקט</a>, מהבנת הצורך ועד המימוש.</p>
    </div>
  </section>
  <section class="wrap">
    <div class="cards">
      <a class="card" href="/services/product-development">
        <div class="ic mono">&lt;/&gt;</div>
        <h3>פיתוח מוצרים, אתרים ואפליקציות</h3>
        <p>מאפיון ראשוני ועד מוצר חי – עיצוב ופיתוח מקצה לקצה של מוצרים, מערכות, אתרים ואפליקציות.</p>
        <ul><li>אתרים ומערכות ווב</li><li>אפליקציות</li><li>MVP ופיתוח מלא</li></ul>
        <span class="go">לפרטים ←</span>
      </a>
      <a class="card" href="/services/automation">
        <div class="ic">⚙</div>
        <h3>אוטומציה וסוכני AI</h3>
        <p>תהליכים ידניים שהופכים אוטומטיים – בשילוב סוכני AI שחוסכים שעות עבודה ועובדים בשביל העסק.</p>
        <ul><li>אוטומציה עסקית</li><li>סוכני AI</li><li>חיבור מערכות ו-API</li></ul>
        <span class="go">לפרטים ←</span>
      </a>
      <a class="card" href="/services/consulting">
        <div class="ic">◆</div>
        <h3>ייעוץ ואפיון טכנולוגי</h3>
        <p>להבין מה באמת לבנות ואיך לתעדף – מיפוי הצורך, אסטרטגיה ואפיון פתרון מדויק.</p>
        <ul><li>מיפוי צרכים וכאבים</li><li>אסטרטגיה טכנולוגית</li><li>ליווי קבלת החלטות</li></ul>
        <span class="go">לפרטים ←</span>
      </a>
    </div>
  </section>
  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">התהליך</span></span>
    <h2 class="s-head">תהליך פשוט, שקוף, בלי הפתעות</h2>
    <div class="steps">
      <div class="step"><b class="n">01</b><h4>שיחת היכרות</h4><p>מבינים את הצורך, היעדים והאתגרים</p></div>
      <div class="step"><b class="n">02</b><h4>אפיון ותכנון</h4><p>בונים אפיון ופתרון מותאם</p></div>
      <div class="step"><b class="n">03</b><h4>פיתוח ויישום</h4><p>מבצעים, עם עדכון שוטף ושקיפות</p></div>
      <div class="step"><b class="n">04</b><h4>השקה והתאמות</h4><p>עולים לאוויר ומתאימים עד שביעות רצון מלאה</p></div>
      <div class="step"><b class="n">05</b><h4>תמיכה שוטפת</h4><p>אופציונלי – תחזוקה, שיפורים והמשך פיתוח, כחבילה חודשית לפי הצורך</p></div>
    </div>
  </section>
'''
faq_html, faq_s = faq_block([
    ("עם אילו לקוחות את עובדת?", "עם עסקים, יזמים וארגונים שצריכים לתרגם צורך לפתרון טכנולוגי – מסטארט-אפ בתחילת הדרך ועד חברות מבוססות."),
    ("כמה זמן לוקח פרויקט?", "תלוי בהיקף. אפיון קצר יכול לקחת שבועות, ומוצר מלא – חודשים. אני חרוצה מאוד ועובדת מהר – אבל בלי להתפשר על איכות. אחרי שיחת ההיכרות והאפיון נוכל לתת לוח זמנים מדויק."),
    ("איך מתמחרים?", "לפי היקף ואופי הפרויקט. אחרי שיחת היכרות קצרה תקבלו הצעת מחיר ברורה, מחולקת לאבני דרך."),
    ("כמה מהר מקבלים הצעת מחיר?", "אחרי שיחת היכרות קצרה (ולעיתים אפיון קצר) תקבלו הצעת מחיר ברורה, מחולקת לאבני דרך – בדרך כלל תוך כמה ימים."),
    ("אפשר לעבוד מרחוק / מכל הארץ?", "כן. אני עובדת עם לקוחות מכל הארץ, ורוב התהליך מתנהל מרחוק – שיחות, אפיון ועדכונים שוטפים אונליין, עם פגישות פרונטליות לפי הצורך."),
])
page("/services","services.html",
     "שירותים · פיתוח, אוטומציה וסוכני AI | מיכל בר",
     "שלושה תחומי שירות – פיתוח מוצרים, אתרים ואפליקציות; אוטומציה וסוכני AI; וייעוץ ואפיון טכנולוגי. מקצה לקצה, בליווי אישי.",
     [("דף הבית","/"),("שירותים",None)],
     svc_cards + faq_html + CTA,
     [{"@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":1,"url":SITE+"/services/product-development","name":"פיתוח מוצרים, אתרים ואפליקציות"},
        {"@type":"ListItem","position":2,"url":SITE+"/services/automation","name":"אוטומציה וסוכני AI"},
        {"@type":"ListItem","position":3,"url":SITE+"/services/consulting","name":"ייעוץ ואפיון טכנולוגי"}]}, faq_s])

# canonical service list (used for the "related services" cross-links on each sub-page)
SERVICES = [
    ("/services/product-development", "פיתוח מוצרים, אתרים ואפליקציות"),
    ("/services/automation", "אוטומציה וסוכני AI"),
    ("/services/consulting", "ייעוץ ואפיון טכנולוגי"),
]

# ---- generic service sub-page builder ----
def service_page(path, filename, title, desc, h1, lead, intro_paras, includes, forwhom, faq_pairs, svc_name, svc_desc):
    inc = "".join(f"<li>{x}</li>" for x in includes)
    who = "".join(f"<li>{x}</li>" for x in forwhom)
    paras = "".join(f"<p>{p}</p>" for p in intro_paras)
    body = f'''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">שירות</span></span>
    <h1 class="s-head">{h1}</h1>
    <p class="s-lead">{lead}</p>
  </section>
  <section class="wrap">
    <div class="prose">{paras}</div>
    <div class="cards svc-pair" style="margin-top:32px;">
      <div class="card"><h3>מה זה כולל</h3><ul class="svc-list">{inc}</ul></div>
      <div class="card"><h3>למי זה מתאים</h3><ul class="svc-list">{who}</ul></div>
    </div>
  </section>
'''
    fh, fs = faq_block(faq_pairs)
    others = [(p, n) for p, n in SERVICES if p != path]
    rel = "".join(f'<a href="{p}"><span>{n}</span> <span class="ar">&#8592;</span></a>' for p, n in others)
    related = f'''  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">שירותים קשורים</span></span>
    <div class="related">{rel}</div>
  </section>
'''
    page(path, filename, title, desc,
         [("דף הבית","/"),("שירותים","/services"),(h1,None)],
         body + fh + related + CTA,
         [service_schema(svc_name, svc_desc, path), fs])

service_page("/services/product-development","services/product-development.html",
    "פיתוח מוצר דיגיטלי ו-MVP לעסקים | מיכל בר",
    "אפיון, עיצוב ופיתוח של מוצרים, מערכות, אתרים ואפליקציות – מרעיון ל-MVP ועד מוצר מלא, מקצה לקצה.",
    "פיתוח מוצרים, אתרים ואפליקציות",
    "מרעיון ל-MVP ועד מוצר מלא – אפיון, עיצוב ופיתוח מקצה לקצה, כשהדגש הוא על מה נכון לבנות ואיך הוא צריך להיראות.",
    ["הקושי האמיתי בפיתוח מוצר הוא לא הבנייה עצמה – אלא לדעת <strong>מה</strong> באמת נכון לבנות עבור העסק שלך, ו<strong>איך</strong> זה צריך לעבוד ולהיראות. אני מתרגמת צורך עסקי למוצר: מאפיון חד ומדויק, דרך עיצוב חוויית משתמש, ועד פיתוח מלא ועלייה לאוויר.",
     "היום השוק מוצף בפתרונות שנבנים מהר וזול בעזרת כלי AI – בלי ניסיון ובלי חשיבה עסקית. התוצאה כמעט תמיד גנרית: מוצר שנראה כמו כל האחרים, בלי ייחודיות ובלי מה שבאמת גורם לו לעבוד עבור העסק שלך. <strong>כאן ההבדל שלי</strong> – מעל 20 שנה של ניסיון בהייטק והסתכלות עסקית עמוקה, שמייצרות מוצר מותאם בדיוק אליך, מבדל אותך ומביא ערך אמיתי, לא עוד תבנית.",
     "ואתם שותפים לכל אורך הדרך: אני בונה את המוצר במלואו, אבל משתפת אתכם תוך כדי – מראה את המוצר בהתהוותו, עושים יישור קו ומתקדמים יחד, כך שמה שעולה לאוויר הוא בדיוק מה שצריך, בלי הפתעות."],
    ["אפיון מוצר מתוך חשיבה עסקית","עיצוב חוויית משתמש וממשק (UX/UI)","פיתוח אתרים ואפליקציות – עם מסרים נכונים ובידול","פיתוח מערכות פנימיות ו-CRM המותאמים בדיוק לעסק שלך","מערכי תשלום, ניהול ודשבורדים","פיתוח Full-stack מקצה לקצה","בניית MVP – גרסה ראשונה ממוקדת לפי הצורך","ליווי ושיתוף לאורך כל הדרך"],
    ["עצמאים ועסקים שרוצים לצמוח מהר ולבנות נכון","מי שצריך מערכת, כלי פנימי או אתר שבאמת עובדים עבורו","מי שיש לו מוצר וצריך להרחיב או לשפר אותו","מי שקיבל מוצר גנרי או זול – ורוצה משהו שבאמת עובד ומבדל אותו","סטארט-אפים שצריכים MVP ממוקד ומדויק","יזמים עם רעיון שצריך להפוך למוצר"],
    [("כמה עולה לפתח MVP?","העלות תלויה בהיקף הפיצ׳רים. MVP ממוקד עולה משמעותית פחות ממוצר מלא – ואנחנו מגדירים יחד את ההיקף הנכון שיביא ערך מהר. אחרי אפיון תקבלו הצעת מחיר מדויקת מחולקת לאבני דרך."),
     ("איך בוחרים מפתח או חברת פיתוח? מה חשוב לבדוק?","מעבר למחיר, בדקו ארבעה דברים: (1) ניסיון ורקורד אמיתי – לא רק כתיבת קוד, אלא הבנה של מה נכון לבנות; (2) ראייה עסקית – שמבינים את הצורך שלכם ולא רק מבצעים הוראות; (3) אבטחת מידע – שהמוצר נבנה מאובטח מהיסוד ולא חשוף לתקיפה; (4) ליווי מקצה לקצה – אפיון, עיצוב, פיתוח והשקה במקום אחד. בדיוק השילוב הזה – 20+ שנה בהייטק ובסייבר, ראש של מוצר וליווי אישי – הוא היתרון שלי על פני בנייה גנרית וזולה."),
     ("אתר לעסק – מה באמת חשוב מעבר לאיך שהוא נראה?","אתר יפה זה לא מספיק – אתר צריך לעבוד ולהמיר. אני בונה עם ראייה מוצרית: המסרים הנכונים שמדברים בדיוק ללקוח שלכם, flow שמוביל את הגולש צעד-צעד עד לפעולה (ליד, פנייה או רכישה), וחוש עיצובי שמביא רמת מקצועיות שמייצרת אמון – וגם אבטחת מידע, שהאתר בנוי מאובטח מהיסוד (מהניסיון שלי בעולם הסייבר). התוצאה היא לא עוד אתר – אלא כלי שמביא לקוחות."),
     ("האם האתר שאתם בונים מאובטח? וכמה זה חשוב?","מאוד – וזה בדיוק מה שאתרים מהירים וזולים מפספסים. מערכת שנבנית בלי אבטחה חשופה לתקיפה, ואם נדלפים פרטי לקוחות רגישים או פרטי תשלום – העסק חשוף לתביעות ולנזק תדמיתי כבד. מהרקע שלי בעולם הסייבר – היחידה הטכנולוגית של חיל המודיעין וסטארט-אפ סייבר – אבטחת מידע נבנית אצלי מהיסוד, לא נספחת בדיעבד."),
     ("כמה זמן לוקח לפתח מוצר?","MVP: בדרך כלל שבועות עד חודשים ספורים. מוצר מלא: לפי היקף. אני חרוצה מאוד ועובדת מהר – אבל בלי להתפשר על איכות. לוח זמנים מדויק נקבע אחרי אפיון."),
     ("באילו טכנולוגיות את עובדת?","בוחרים את הכלים לפי הצורך של המוצר – פיתוח Full-stack לאתרים, אפליקציות ומערכות. הטכנולוגיה משרתת את המוצר, לא להפך."),
     ("מה ההבדל בין MVP למוצר מלא?","MVP הוא גרסה ראשונה ממוקדת: מוצר שלם ומלוטש שכולל בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך, בלי פיצ׳רים מיותרים. מוצר מלא הוא היקף רחב יותר – ובשני המקרים בונים את המוצר במלואו ומשתפים אתכם לאורך הדרך.")],
    "פיתוח מוצרים, אתרים ואפליקציות",
    "אפיון, עיצוב ופיתוח מוצרים, אתרים ואפליקציות מקצה לקצה – מ-MVP ועד מוצר מלא.")

service_page("/services/consulting","services/consulting.html",
    "ייעוץ ואפיון טכנולוגי לעסקים | מיכל בר",
    "ייעוץ שמחבר בין עסק לטכנולוגיה – מיפוי הצורך השורשי, אסטרטגיה, ותכנון פתרון מדויק לפני שבונים.",
    "ייעוץ ואפיון טכנולוגי",
    "מחברת בין הבנה עסקית לטכנולוגיה – מזהה איפה הבעיה האמיתית ובונה את הדרך הנכונה לפתור, לפני שכותבים שורת קוד אחת.",
    ["הרבה פרויקטים נכשלים לא בגלל הפיתוח, אלא בגלל שבנו את הדבר הלא נכון. ייעוץ טוב חוסך את זה: מיפוי מדויק של הצורך והכאב, הבנה של הביזנס והמשתמשים, וגיבוש פתרון ואסטרטגיה – עד להחלטה מושכלת ותוכנית פעולה ברורה.",
     "היתרון שלי הוא שילוב נדיר של שלושה עולמות – הלקוח, הביזנס והטכנולוגיה. אני יודעת גם לזהות את הצורך האמיתי, גם להבין מה אפשרי טכנולוגית, וגם לתעדף נכון כדי להביא ערך מהר."],
    ["מיפוי צרכים, כאבים והזדמנויות","הבנת הביזנס והמשתמשים","אפיון מוצר/מערכת מפורט","גיבוש אסטרטגיה ותהליכים","תכנון פתרון ותיעדוף","ליווי קבלת החלטות טכנולוגיות"],
    ["עצמאים ועסקים שלא בטוחים מה בדיוק לבנות","מי ששוקל פרויקט טכנולוגי וצריך כיוון","מי שרוצה לוודא שהוא בונה את הדבר הנכון – לפני שמשקיע בפיתוח","ארגונים שרוצים לייעל תהליך או מוצר קיים","יזמים שצריכים לתעדף ולמקד"],
    [("מה כולל תהליך ייעוץ?","מיפוי הצורך והכאב, הבנת הביזנס והמשתמשים, וגיבוש פתרון ואסטרטגיה – עד להחלטה מושכלת ותוכנית פעולה."),
     ("מתי כדאי לפנות לייעוץ ולא ישר לפיתוח?","כשלא בטוחים מה בדיוק לבנות, איך לתעדף, או איזו גישה נכונה. ייעוץ טוב חוסך פיתוח מיותר וכסף רב."),
     ("כמה זמן לוקח תהליך ייעוץ?","תלוי בהיקף – משיחה ממוקדת אחת ועד תהליך של מספר שבועות. נגדיר יחד את ההיקף הנכון בשיחת ההיכרות.")],
    "ייעוץ ואפיון טכנולוגי",
    "ייעוץ שמחבר בין עסק לטכנולוגיה – מיפוי צורך, אסטרטגיה ואפיון פתרון מדויק.")

service_page("/services/automation","services/automation.html",
    "אוטומציה עסקית וסוכני AI לעסקים | מיכל בר",
    "אוטומציה של תהליכים עסקיים בשילוב סוכני AI (AI Agents) – חיבור מערכות וכלים כך שפעולות ידניות חוזרות קורות מעצמן וחוסכות שעות עבודה.",
    "אוטומציה וסוכני AI",
    "תהליכים ידניים שהופכים אוטומטיים – חיבור בין הכלים והמערכות שלכם, בשילוב סוכני AI שעושים את העבודה החוזרת בשבילכם.",
    ["כל שעה שאתם או הצוות מבזבזים על פעולות ידניות חוזרות היא שעה שאפשר להחזיר. אבל אוטומציה טובה היא לא רק ‘לחבר מערכות’ – היא מתחילה בהבנת התהליך הקיים, ממשיכה בייעול שלו, ורק אז מממשת פתרון טכנולוגי שמבצע אותו אוטומטית בצורה היעילה ביותר לעסק – בלי טעויות ובלי לגזול זמן.",
     "היום אפשר להרחיק לכת עוד יותר: <strong>סוכני AI</strong> שמבינים הקשר, מקבלים החלטות פשוטות ומבצעים משימות שלמות – מענה לפניות, סיווג וניתוב מידע, סיכומים והפקת תוכן – ולא רק מריצים חוקים קבועים.",
     "מתחילים במיפוי: איפה נשרף הכי הרבה זמן ידני, ומה ההזדמנויות הגדולות. משם בונים אוטומציות וסוכני AI ממוקדים שמשתלבים בכלים שכבר יש לכם."],
    ["אוטומציית תהליכים עסקיים מקצה לקצה","סוכני AI (AI Agents) למשימות ותהליכים","צ'אטבוטים ועוזרים חכמים לעסק","חיבור בין כלים ומערכות (אינטגרציות ו-API)","דוחות, טפסים ועדכונים אוטומטיים","מיפוי תהליכים וזיהוי הזדמנויות לחיסכון"],
    ["עצמאים ועסקים שנשרף להם זמן על עבודה ידנית חוזרת","צוותים שעובדים עם כמה מערכות שלא מדברות זו עם זו","מי שרוצה לשלב סוכני AI בעבודה – אבל לא יודע מאיפה להתחיל","עסקים ועצמאים שרוצים לגדול בלי לגדול בכוח אדם"],
    [("מה זה אוטומציה עסקית?","אוטומציה עסקית מתחילה בהבנת התהליכים הקיימים ואיך הם מתבצעים, ממשיכה בייעול מקסימלי שלהם, ומסתיימת במימוש פתרון טכנולוגי שמבצע אותם אוטומטית – בצורה היעילה ביותר לעסק. זה לא רק חיבור מערכות, אלא חשיבה מחדש על התהליך עצמו."),
     ("מה זה סוכני AI ואיך הם עוזרים לעסק?","סוכני AI (AI Agents) הם עוזרים חכמים שמבינים הקשר ומבצעים משימות שלמות בשבילכם – מענה לפניות, סיווג וניתוב מידע, סיכומים, הפקת תוכן ועוד. בניגוד לאוטומציה שמריצה חוקים קבועים, סוכן AI יודע להתמודד גם עם מצבים לא צפויים."),
     ("מה ההבדל בין אוטומציה לבין סוכן AI?","אוטומציה מריצה חוקים קבועים (‘אם X אז Y’) ומצוינת לתהליכים חוזרים וברורים. סוכן AI הוא צעד קדימה: מבין הקשר, מקבל החלטות ומתמודד גם עם מצבים לא צפויים. בפועל משלבים את השניים – אוטומציה למה שקבוע, וסוכני AI למה שדורש הבנה."),
     ("מה אפשר לאטמט?","כמעט כל תהליך חוזר: העברת נתונים בין מערכות, שליחת מיילים ועדכונים, יצירת דוחות, טפסים, גבייה ועוד – ובעזרת AI גם משימות שדורשות הבנה והחלטה."),
     ("עם אילו כלים את עובדת לאוטומציה?","בוחרים את הכלי לפי הצורך – מכלי אוטומציה מובילים (כמו Make/Zapier) ועד פיתוח מותאם ואינטגרציות API כשצריך משהו ייחודי. הכלי משרת את התהליך, לא להפך."),
     ("האם AI יחליף את הצורך במומחה?","לא. AI הוא כלי חזק – אבל עושה טעויות ולא יודע מה נכון לעסק שלכם. הערך האמיתי הוא בשילוב: מישהו עם ניסיון וראייה עסקית שיודע מה לבנות, איך לשלב AI נכון, ומתי לא. הכלי חוסך זמן; ההחלטות והבידול נשארים אנושיים."),
     ("כמה זמן חוסכים?","תלוי בתהליך – לקוחות חסכו מאות שעות עבודה בשנה. אחרי מיפוי נדע להצביע על ההזדמנויות הגדולות ביותר.")],
    "אוטומציה וסוכני AI",
    "אוטומציה של תהליכים עסקיים בשילוב סוכני AI (AI Agents) – חיבור מערכות וייעול שחוסך שעות עבודה.")

# ---- /about ----
about_body = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">עליי</span></span>
    <h1 class="s-head">היי, אני מיכל בר</h1>
  </section>
  <section class="wrap">
    <div class="about-grid">
      <div class="portrait"><img src="/michal.jpg" alt="מיכל בר" /></div>
      <div>
        <p>במהותי, יש לי יכולת נדירה להבין סיטואציות מורכבות – מהר ולעומק. לזהות איפה הבעיה האמיתית, למה היא קורה ומה התהליכים שמאחוריה, ומשם לבנות את הדרך הנכונה לשפר ולהביא ערך.</p>
        <p>לצד זה יש לי אינטואיציה מוצרית נדירה: מתארים לי בעיה – ואני כבר רואה איך הפתרון צריך להיראות, ומאפיינת אותו במהירות ובדיוק. כי הקושי האמיתי הוא לא הבנייה – אלא לדעת <em>מה</em> נכון לבנות ו<em>איך</em> הוא צריך להיראות.</p>
        <p>אני חושבת בצורה יצירתית, ולכן הפתרונות שלי מדויקים, מקוריים ונכונים – כאלה שמזיזים את המחט. ומכיוון שאני מחוברת לעיצוב ולאסתטיקה, גם המסר וגם הנראות חשובים לי לא פחות מהתוכן.</p>
        <p>היום, כשכל אחד יכול לבנות מוצר עם AI בכמה קליקים, קל לקבל תוצאה גנרית שנראית כמו כל האחרים ולא באמת עובדת לעסק. מה שמבדל הוא ניסיון וראייה עסקית – היכולת לבנות מוצר, אתר או אוטומציה שמותאמים בדיוק לצורך, מבדלים אותך, ומביאים ערך אמיתי.</p>
        <p>מעל 20 שנה בעולמות ההייטק והטכנולוגיה – מהיחידה הטכנולוגית של חיל המודיעין בתחום הסייבר, דרך ייעוץ וניהול לקוחות, ועד תפקידי ניהול בכירים בסטארט-אפ סייבר, שם הובלתי את מערך ה-<span dir="ltr">Customer Success</span> והשירותים המקצועיים – באחריות מלאה על כלל הלקוחות והפרויקטים. היום אני מפתחת מוצרים, אתרים ומערכות, בונה אוטומציות וסוכני AI, ומלווה עסקים, עצמאים ויזמים – מהבנת הצורך ועד המימוש.</p>
        <p class="about-note">ומעל הכל – חיבור אמיתי לאנשים והקשבה לצורך שמאחורי המילים. אנגלית ברמת שפת אם · יכולות הצגה ופרזנטציה גבוהות.</p>
        <div class="sig">מיכל בר<small>פיתוח · אוטומציה · סוכני AI</small></div>
      </div>
    </div>
    <div class="timeline">
      <div class="tl-head"><span class="tl-num">20+</span> שנות ניסיון <span class="sep">·</span> <span class="tl-num">100+</span> פרויקטים</div>
      <ol class="tl">
        <li><span class="tl-dot"></span><b>חיל המודיעין</b><small>יחידה טכנולוגית · סייבר</small></li>
        <li><span class="tl-dot"></span><b>ייעוץ וניהול לקוחות</b><small>עולם הסייבר</small></li>
        <li><span class="tl-dot"></span><b>ניהול בכיר בסטארטאפ</b><small><span dir="ltr">Customer Success</span> · סייבר</small></li>
        <li><span class="tl-dot tl-now"></span><b>היום</b><small>פיתוח, אוטומציה וסוכני AI לעסקים ולעצמאים</small></li>
      </ol>
    </div>
  </section>
  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">לקוחות ממליצים</span></span>
    <h2 class="s-head">מה אומרים עליי</h2>
    <div class="quotes">
      <div class="quote"><div class="stars">★★★★★</div><p>"מיכל פיתחה עבורנו כלי שחסך לנו מאות שעות עבודה, וייעל תהליך בצורה פשוטה עם ממשק נוח ויעיל למשתמש. לעבוד עם מיכל זו זכייה – היא מצליחה להבין את הצורך העסקי עד הסוף ויותר מזה, מייצרת התקדמות מהירה ואיכותית, מחויבות למשימה, וידעה לייצר פתרון טוב הרבה יותר ממה שציפיתי."</p><div class="who"><div class="av">ל</div><div><b>ליאת פלקסין</b><small dir="ltr">Co-founder · FaaS</small></div></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"למיכל יש יכולת נדירה לקחת פרויקט מא׳ עד ת׳ – ומהר. יש לה הבנה עמוקה של הצרכים, יכולת לזהות את מה שעוד חסר, ובעיקר אבחנה טובה בין עיקר לתפל ואיך בונים פרויקט מעולה עם כל היכולות ובלי להסתבך. מעבר למקצועיות הגבוהה, מה שבלט במיוחד אצל מיכל הוא היחס האנושי והזמינות – תמיד קשובה, נגישה וזמינה לכל שאלה. שירות וליווי ברמה אחרת."</p><div class="who"><div class="av">א</div><div><b>איריס שור</b><small>יזמת סדרתית · מנהלת מרכז הפיתוח של LinkedIn לשעבר</small></div></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"למיכל יש את היכולת הנדירה לחבר בין הבנה עסקית לטכנולוגיה, וזה בדיוק מה שחיפשנו. אפיינה ובנתה לנו פתרון עם מסרים מדויקים, יצירתיות ומענה על הצורך – מעל הציפיות."</p><div class="who"><div class="av">א</div><div><b>אלון</b><small>מנכ״ל</small></div></div></div>
    </div>
  </section>
'''
page("/about","about.html",
     "עליי · מיכל בר – יועצת ומפתחת פתרונות טכנולוגיים",
     "מעל 20 שנה בהייטק ובסייבר – מחיל המודיעין ועד ניהול בכיר בסטארט-אפ. היום מפתחת מוצרים, אתרים ומערכות, אוטומציות וסוכני AI לעסקים, לעצמאים וליזמים – מהבנת הצורך ועד המימוש.",
     [("דף הבית","/"),("עליי",None)],
     about_body + CTA,
     [{"@id":BIZ+"-michal","@type":"Person","name":"מיכל בר","url":SITE+"/about",
       "jobTitle":"מפתחת ויועצת פתרונות טכנולוגיים",
       "description":"מעל 20 שנה בהייטק ובסייבר. מפתחת מוצרים, אתרים ומערכות, בונה אוטומציות וסוכני AI, ומלווה עסקים, עצמאים ויזמים.",
       "knowsAbout":["פיתוח מוצר","פיתוח אתרים","פיתוח אפליקציות","אוטומציה עסקית","סוכני AI","ייעוץ טכנולוגי"]}])

# ---- /projects ----
projects_body = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">פרויקטים</span></span>
    <h1 class="s-head">פרויקטים נבחרים</h1>
    <p class="s-lead" style="max-width:none;">כל אחד נבנה מתוך הבנת הצורך העסקי – מוצרים, אתרים ומערכות שבאמת עובדים.</p>
  </section>
  <section class="wrap">
    <div class="proj">
      <div class="pcard">
        <div class="thumb"><img src="/proj-deskday.jpg" alt="deskday – מרקטפלייס לעמדות עבודה" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">מוצר</span><span class="tag">אפיון</span><span class="tag">עיצוב</span><span class="tag">פיתוח</span><span class="tag" dir="ltr">Full-Stack</span></div>
          <h4>מרקטפלייס לעמדות עבודה</h4>
          <p>מרקטפלייס מקצה לקצה להשכרת עמדות עבודה יומיות: חיפוש חללים לפי מיקום ותאריך, דפי חלל עם תמונות ומועדפים, ממשק נפרד לבעלי חללים ולשוכרים, ומערך תשלומים מלא – גבייה, קבלות וחשבוניות, לוח ניהול והודעות. מוצר עצמאי שאפיינתי, עיצבתי ופיתחתי.</p>
        </div>
      </div>
      <a class="pcard" href="https://makombateva.com" target="_blank" rel="noopener">
        <div class="thumb"><img src="/proj-makombateva.jpg" alt="מקום בטבע – אתר תדמית" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">אפיון</span><span class="tag">עיצוב</span><span class="tag">פיתוח</span><span class="tag">אתר תדמית</span></div>
          <h4>מקום בטבע</h4>
          <p>אתר תדמית מלא לעסק אירוח בטבע – אפיון, עיצוב ופיתוח מקצה לקצה: דף נחיתה, גלריית תמונות וסרטונים, עמוד מדריך אורחים מאובטח וטופס פנייה חכם.</p>
          <span class="visit">צפו באתר ↗</span>
        </div>
      </a>
      <div class="pcard">
        <div class="thumb"><img src="/proj-instagram.jpg" alt="מערכת לניתוח תוכן באינסטגרם" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">מוצר</span><span class="tag">אפיון</span><span class="tag">פיתוח</span><span class="tag" dir="ltr">Data Analytics</span><span class="tag" dir="ltr">AI</span></div>
          <h4>ניתוח תוכן לאינסטגרם</h4>
          <p>מערכת לניתוח ביצועי תוכן באינסטגרם – מגדירים חשבונות לניתוח, והמערכת אוספת נתונים מעמיקים מכל פוסט (חשיפות, מעורבות, סוג תוכן ועוד), מנתחת ומפיקה אינסייטס: אילו פוסטים עובדים, למה, ומה אפשר לשפר כדי להגיע לביצועים טובים יותר. <strong>התוצאה:</strong> חיסכון של מאות שעות עבודה ידנית בחודש, ותובנות שניתוח ידני לא הצליח להגיע אליהן – שהביאו מכירות חדשות רבות לעסק.</p>
        </div>
      </div>
    </div>
  </section>
'''
page("/projects","projects.html",
     "פרויקטים נבחרים | מיכל בר",
     "פרויקטים נבחרים שאפיינתי, עיצבתי ופיתחתי – מרקטפלייס לעמדות עבודה, אתר תדמית למקום בטבע, ומערכת לניתוח תוכן באינסטגרם.",
     [("דף הבית","/"),("פרויקטים",None)],
     projects_body + CTA, [])

# ---- /contact ----
contact_body = '''  <section class="wrap page-hero" style="text-align:center;">
    <span class="eyebrow" style="justify-content:center;"><span class="idx">//</span> <span class="ttl">צרו קשר</span></span>
    <h1 class="s-head" style="margin-inline:auto;">יש לכם אתגר, רעיון או פרויקט?</h1>
    <p class="s-lead" style="margin-inline:auto;">שיחת ייעוץ חינם, ללא התחייבות – אחזור אליכם תוך 24 שעות.</p>
  </section>
''' + CONTACT_GRID
page("/contact","contact.html",
     "צרו קשר | מיכל בר · פתרונות טכנולוגיים",
     "בואו נדבר – שיחת היכרות ללא התחייבות. וואטסאפ, טלפון, לינקדאין או טופס. אחזור אליכם תוך 24 שעות.",
     [("דף הבית","/"),("צרו קשר",None)],
     contact_body,
     [{"@type":"ContactPage","name":"צרו קשר · מיכל בר","url":SITE+"/contact"}])

# ---- /privacy ----
privacy_body = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">משפטי</span></span>
    <h1 class="s-head">מדיניות פרטיות</h1>
    <p class="s-lead">עודכן לאחרונה: ספטמבר 2026</p>
  </section>
  <section class="wrap"><div class="prose">
    <p>אני, מיכל בר ("אני"/"האתר"), מכבדת את פרטיותכם. מדיניות זו מסבירה איזה מידע נאסף באתר michalbartech.com, כיצד נעשה בו שימוש, ומהן זכויותיכם.</p>
    <h2>איזה מידע נאסף</h2>
    <ul>
      <li><strong>מידע שאתם מוסרים ביוזמתכם</strong> – בעת מילוי טופס יצירת הקשר: שם, טלפון, דוא״ל ותוכן ההודעה.</li>
      <li><strong>מידע סטטיסטי אנונימי</strong> – נתוני שימוש ותנועה הנאספים באמצעות Google Analytics (עמודים שנצפו, מקור הגעה, סוג מכשיר וכד׳), ללא זיהוי אישי.</li>
    </ul>
    <p>מסירת הפרטים בטופס היא <strong>וולונטרית ואינה מחויבת על-פי חוק</strong> – אך ללא הפרטים לא אוכל לחזור אליכם. הפרטים משמשים אך ורק למטרות המפורטות להלן.</p>
    <h2>למה משמש המידע</h2>
    <ul>
      <li>ליצירת קשר ומענה לפניות.</li>
      <li>לשיפור האתר והבנת אופן השימוש בו.</li>
    </ul>
    <h2>שירותי צד שלישי</h2>
    <p>האתר עושה שימוש בשירותים חיצוניים לצורך תפעולו: <strong>Google Analytics</strong> (ניתוח תנועה), <strong>EmailJS</strong> (העברת פניות מהטופס לתיבת הדוא״ל שלי), ו-<strong>Vercel</strong> (אחסון האתר). לכל אחד מהם מדיניות פרטיות משלו.</p>
    <h2>עוגיות (Cookies)</h2>
    <p>האתר עשוי לעשות שימוש בעוגיות לצרכים סטטיסטיים ותפעוליים. ניתן לחסום עוגיות בהגדרות הדפדפן.</p>
    <h2>שמירת מידע ואבטחה</h2>
    <p>המידע נשמר כל עוד הוא נדרש למטרות שלשמן נאסף, ומאובטח באמצעים סבירים. פניות מהטופס נשמרות בתיבת הדוא״ל שלי.</p>
    <h2>הזכויות שלכם</h2>
    <p>אתם רשאים לפנות אליי בכל עת בבקשה לעיין במידע שנאסף עליכם, לתקנו או למחקו, בכתובת <a href="/contact">צרו קשר</a> או בדוא״ל barmichal100@gmail.com.</p>
    <h2>שינויים במדיניות</h2>
    <p>מדיניות זו עשויה להתעדכן מעת לעת. המועד המעודכן יופיע בראש העמוד.</p>
  </div></section>
'''
page("/privacy","privacy.html",
     "מדיניות פרטיות | מיכל בר",
     "מדיניות הפרטיות של אתר michalbartech.com – איזה מידע נאסף, כיצד הוא משמש, ומהן זכויותיכם.",
     [("דף הבית","/"),("מדיניות פרטיות",None)],
     privacy_body, [])

# ---- /accessibility ----
access_body = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">נגישות</span></span>
    <h1 class="s-head">הצהרת נגישות</h1>
    <p class="s-lead">עודכן לאחרונה: ספטמבר 2026</p>
  </section>
  <section class="wrap"><div class="prose">
    <p>אני רואה חשיבות רבה במתן שירות שוויוני ונגיש לכלל הגולשים, כולל אנשים עם מוגבלות. אתר זה נבנה במאמץ להתאימו להנחיות הנגישות המקובלות.</p>
    <h2>רמת הנגישות באתר</h2>
    <p>האתר נבנה בהתאם לעקרונות תקן הנגישות הישראלי (ת״י 5568) ולהנחיות <span dir="ltr">WCAG 2.0</span> ברמה AA, ככל שניתן. בין היתר:</p>
    <ul>
      <li>מבנה סמנטי ותקין המאפשר ניווט בקורא מסך.</li>
      <li>ניגודיות צבעים מספקת בין טקסט לרקע.</li>
      <li>טקסט חלופי לתמונות משמעותיות.</li>
      <li>אפשרות ניווט וגלישה במקלדת.</li>
      <li>תמיכה בהגדלת טקסט בדפדפן.</li>
    </ul>
    <h2>הסתייגות</h2>
    <p>ייתכן שחלקים מסוימים באתר טרם הונגשו במלואם, או שנמצא רכיב שאינו נגיש דיו. אני פועלת לשיפור מתמיד של נגישות האתר.</p>
    <h2>יצירת קשר בנושא נגישות</h2>
    <p>אחראית הנגישות באתר היא <strong>מיכל בר</strong>. נתקלתם בבעיה או בקושי בנגישות האתר? אשמח לשמוע ולתקן, ואפשר לפנות אליי:</p>
    <ul>
      <li>דוא״ל: <a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=barmichal100@gmail.com&amp;su=נגישות+-+michalbartech" target="_blank" rel="noopener">barmichal100@gmail.com</a></li>
      <li>טלפון: <a href="tel:+972547105176" dir="ltr">054-710-5176</a></li>
    </ul>
    <p>אשתדל לטפל בפנייה בהקדם.</p>
  </div></section>
'''
page("/accessibility","accessibility.html",
     "הצהרת נגישות | מיכל בר",
     "הצהרת הנגישות של אתר michalbartech.com – רמת הנגישות, ההתאמות שבוצעו, ודרכי פנייה בנושא נגישות.",
     [("דף הבית","/"),("הצהרת נגישות",None)],
     access_body, [])

# ---- /faq (aggregated) ----
faq_groups = [
    ("כללי", [
        ("למה לבנות אצלך ולא פשוט לבנות לבד עם AI או בזול?", "היום כל אחד יכול לבנות משהו בכמה פקודות ל-AI – אבל בדרך כלל מקבלים מוצר גנרי שנראה כמו כל האחרים ולא באמת עובד לעסק. ההבדל הוא ניסיון וראייה עסקית: מעל 20 שנה בהייטק, הבנה של מה באמת צריך להיבנות ואיך, ומוצר שמותאם בדיוק אליכם, מבדל אתכם ומביא ערך אמיתי – לא עוד תבנית."),
        ("עם אילו לקוחות את עובדת?", "עם עסקים, יזמים וארגונים שצריכים לתרגם צורך לפתרון טכנולוגי – מסטארט-אפ בתחילת הדרך ועד חברות מבוססות."),
        ("אפשר לעבוד מרחוק / מכל הארץ?", "כן. אני עובדת עם לקוחות מכל הארץ, ורוב התהליך מתנהל מרחוק – שיחות, אפיון ועדכונים שוטפים אונליין, עם פגישות פרונטליות לפי הצורך."),
        ("כמה זמן לוקח פרויקט?", "תלוי בהיקף. אפיון קצר יכול לקחת שבועות, ומוצר מלא – חודשים. אני חרוצה מאוד ועובדת מהר – אבל בלי להתפשר על איכות. אחרי שיחת ההיכרות והאפיון נוכל לתת לוח זמנים מדויק."),
        ("איך מתמחרים?", "לפי היקף ואופי הפרויקט. אחרי שיחת היכרות קצרה תקבלו הצעת מחיר ברורה, מחולקת לאבני דרך."),
        ("מה קורה אחרי ההשקה? יש תמיכה?", "לא נעלמים אחרי העלייה לאוויר. יש אפשרות לתמיכה וליווי שוטף – תחזוקה, שיפורים והמשך פיתוח – כחבילה חודשית לפי הצורך."),
        ("איך מתחילים לעבוד יחד?", "פשוט: שיחת היכרות קצרה וללא התחייבות. מבינים את הצורך והמטרות, ואם זה מתאים – מקבלים אפיון והצעת מחיר ברורה. אפשר לפנות בטופס, בוואטסאפ או בטלפון."),
    ]),
    ("פיתוח מוצר", [
        ("כמה עולה לפתח אתר או אפליקציה?", "העלות תלויה בהיקף ובמורכבות – אתר תדמית, מערכת או אפליקציה מלאה הם טווחים שונים לגמרי. במקום ‘הכי זול’, אני ממוקדת ב‘הכי נכון’: מוצר בנוי טוב שמחזיר את ההשקעה. אחרי שיחת היכרות קצרה תקבלו הצעת מחיר ברורה, מחולקת לאבני דרך – בלי הפתעות."),
        ("כמה עולה לפתח MVP?", "העלות תלויה בהיקף הפיצ׳רים. MVP ממוקד עולה משמעותית פחות ממוצר מלא – ואנחנו מגדירים יחד את ההיקף הנכון שיביא ערך מהר. אחרי אפיון תקבלו הצעת מחיר מדויקת מחולקת לאבני דרך."),
        ("איך בוחרים מפתח או חברת פיתוח? מה חשוב לבדוק?", "מעבר למחיר, בדקו ארבעה דברים: (1) ניסיון ורקורד אמיתי – לא רק כתיבת קוד, אלא הבנה של מה נכון לבנות; (2) ראייה עסקית – שמבינים את הצורך שלכם ולא רק מבצעים הוראות; (3) אבטחת מידע – שהמוצר נבנה מאובטח מהיסוד ולא חשוף לתקיפה; (4) ליווי מקצה לקצה – אפיון, עיצוב, פיתוח והשקה במקום אחד. בדיוק השילוב הזה – 20+ שנה בהייטק ובסייבר, ראש של מוצר וליווי אישי – הוא היתרון שלי על פני בנייה גנרית וזולה."),
        ("אתר לעסק – מה באמת חשוב מעבר לאיך שהוא נראה?", "אתר יפה זה לא מספיק – אתר צריך לעבוד ולהמיר. אני בונה עם ראייה מוצרית: המסרים הנכונים שמדברים בדיוק ללקוח שלכם, flow שמוביל את הגולש צעד-צעד עד לפעולה (ליד, פנייה או רכישה), וחוש עיצובי שמביא רמת מקצועיות שמייצרת אמון – וגם אבטחת מידע, שהאתר בנוי מאובטח מהיסוד (מהניסיון שלי בעולם הסייבר). התוצאה היא לא עוד אתר – אלא כלי שמביא לקוחות."),
        ("האם האתר שאתם בונים מאובטח? וכמה זה חשוב?", "מאוד – וזה בדיוק מה שאתרים מהירים וזולים מפספסים. מערכת שנבנית בלי אבטחה חשופה לתקיפה, ואם נדלפים פרטי לקוחות רגישים או פרטי תשלום – העסק חשוף לתביעות ולנזק תדמיתי כבד. מהרקע שלי בעולם הסייבר – היחידה הטכנולוגית של חיל המודיעין וסטארט-אפ סייבר – אבטחת מידע נבנית אצלי מהיסוד, לא נספחת בדיעבד."),
        ("כמה זמן לוקח לפתח מוצר?", "MVP: בדרך כלל שבועות עד חודשים ספורים. מוצר מלא: לפי היקף. אני חרוצה מאוד ועובדת מהר – אבל בלי להתפשר על איכות. לוח זמנים מדויק נקבע אחרי אפיון."),
        ("באילו טכנולוגיות את עובדת?", "בוחרים את הכלים לפי הצורך של המוצר – פיתוח Full-stack לאתרים, אפליקציות ומערכות. הטכנולוגיה משרתת את המוצר, לא להפך."),
        ("מה ההבדל בין MVP למוצר מלא?", "MVP הוא גרסה ראשונה ממוקדת: מוצר שלם ומלוטש שכולל בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך, בלי פיצ׳רים מיותרים. מוצר מלא הוא היקף רחב יותר – ובשני המקרים בונים את המוצר במלואו ומשתפים אתכם לאורך הדרך."),
    ]),
    ("ייעוץ", [
        ("מה כולל תהליך ייעוץ?", "מיפוי הצורך והכאב, הבנת הביזנס והמשתמשים, וגיבוש פתרון ואסטרטגיה – עד להחלטה מושכלת ותוכנית פעולה."),
        ("מתי כדאי לפנות לייעוץ ולא ישר לפיתוח?", "כשלא בטוחים מה בדיוק לבנות, איך לתעדף, או איזו גישה נכונה. ייעוץ טוב חוסך פיתוח מיותר וכסף רב."),
        ("כמה זמן לוקח תהליך ייעוץ?", "תלוי בהיקף – משיחה ממוקדת אחת ועד תהליך של מספר שבועות. נגדיר יחד את ההיקף הנכון בשיחת ההיכרות."),
    ]),
    ("אוטומציה וסוכני AI", [
        ("מה זה אוטומציה עסקית?", "אוטומציה עסקית מתחילה בהבנת התהליכים הקיימים ואיך הם מתבצעים, ממשיכה בייעול מקסימלי שלהם, ומסתיימת במימוש פתרון טכנולוגי שמבצע אותם אוטומטית – בצורה היעילה ביותר לעסק. זה לא רק חיבור מערכות, אלא חשיבה מחדש על התהליך עצמו."),
        ("מה זה סוכני AI ואיך הם עוזרים לעסק?", "סוכני AI (AI Agents) הם עוזרים חכמים שמבינים הקשר ומבצעים משימות שלמות בשבילכם – מענה לפניות, סיווג וניתוב מידע, סיכומים, הפקת תוכן ועוד. בניגוד לאוטומציה שמריצה חוקים קבועים, סוכן AI יודע להתמודד גם עם מצבים לא צפויים."),
        ("מה ההבדל בין אוטומציה לבין סוכן AI?", "אוטומציה מריצה חוקים קבועים (‘אם X אז Y’) ומצוינת לתהליכים חוזרים וברורים. סוכן AI הוא צעד קדימה: מבין הקשר, מקבל החלטות ומתמודד גם עם מצבים לא צפויים. בפועל משלבים את השניים – אוטומציה למה שקבוע, וסוכני AI למה שדורש הבנה."),
        ("מה אפשר לאטמט?", "כמעט כל תהליך חוזר: העברת נתונים בין מערכות, שליחת מיילים ועדכונים, יצירת דוחות, טפסים, גבייה ועוד – ובעזרת AI גם משימות שדורשות הבנה והחלטה."),
        ("עם אילו כלים את עובדת לאוטומציה?", "בוחרים את הכלי לפי הצורך – מכלי אוטומציה מובילים (כמו Make/Zapier) ועד פיתוח מותאם ואינטגרציות API כשצריך משהו ייחודי. הכלי משרת את התהליך, לא להפך."),
        ("האם AI יחליף את הצורך במומחה?", "לא. AI הוא כלי חזק – אבל עושה טעויות ולא יודע מה נכון לעסק שלכם. הערך האמיתי הוא בשילוב: מישהו עם ניסיון וראייה עסקית שיודע מה לבנות, איך לשלב AI נכון, ומתי לא. הכלי חוסך זמן; ההחלטות והבידול נשארים אנושיים."),
        ("כמה זמן חוסכים?", "תלוי בתהליך – לקוחות חסכו מאות שעות עבודה בשנה. אחרי מיפוי נדע להצביע על ההזדמנויות הגדולות ביותר."),
    ]),
]
faq_all = []
faq_sections = ['''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">שאלות נפוצות</span></span>
    <h1 class="s-head">שאלות נפוצות</h1>
    <p class="s-lead">כל מה שכדאי לדעת לפני שמתחילים – שירותים, לוחות זמנים, תמחור ותהליך העבודה. לא מצאתם תשובה? <a href="/contact" style="color:var(--accent);">דברו איתי</a>.</p>
  </section>''']
for gtitle, pairs in faq_groups:
    faq_all += pairs
    rows = "\n".join('      <details><summary>%s</summary><p class="a">%s</p></details>' % (q,a) for q,a in pairs)
    faq_sections.append('''  <section class="wrap">
    <h2 class="s-head" style="font-size:clamp(24px,3.4vw,32px);">%s</h2>
    <div class="faq">
%s
    </div>
  </section>''' % (gtitle, rows))
faq_schema = {"@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_all]}
page("/faq","faq.html",
     "שאלות נפוצות | מיכל בר · פתרונות טכנולוגיים",
     "תשובות לשאלות הנפוצות על פיתוח מוצר, ייעוץ טכנולוגי ואוטומציה – לוחות זמנים, תמחור, MVP ותהליך העבודה.",
     [("דף הבית","/"),("שאלות נפוצות",None)],
     "\n".join(faq_sections) + CTA,
     [faq_schema])

# ================= BLOG =================
from urllib.parse import quote
SVG_WA = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.04 4C9.93 4 4.98 8.95 4.98 15.06c0 2.05.56 4.05 1.62 5.8L4 28l7.3-2.55a11.04 11.04 0 0 0 4.74 1.07h.01c6.11 0 11.06-4.95 11.06-11.06C27.1 8.95 22.15 4 16.04 4zm0 20.2c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-4.33 1.51 1.45-4.22-.2-.32a9.16 9.16 0 0 1-1.4-4.87c0-5.06 4.12-9.18 9.19-9.18 2.45 0 4.76.96 6.49 2.69a9.13 9.13 0 0 1 2.69 6.5c0 5.06-4.12 9.18-9.18 9.18z"/></svg>'
SVG_LI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg>'
SVG_X = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-7.3 8.3L23 22h-6.8l-5.3-6.9L4.8 22H1.7l7.8-8.9L1 2h7l4.8 6.3z"/></svg>'
SVG_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
SVG_LINK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>'
BLOG_GRADS = ["linear-gradient(135deg,#E3A45C,#C2683F)","linear-gradient(135deg,#C98A34,#A6543A)","linear-gradient(135deg,#D98E52,#8C4A3A)"]
HE_MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]
def he_date(iso):
    y,m,d = iso.split("-"); return "%d ב%s %s" % (int(d), HE_MONTHS[int(m)-1], y)
AUTHOR_BOX = ('<div class="author-box"><img class="av" src="/michal.jpg" alt="מיכל בר" loading="lazy" />'
  '<div><h4>מיכל בר</h4><p>מפתחת ויועצת פתרונות טכנולוגיים – מעל 20 שנה בהייטק ובסייבר (היחידה הטכנולוגית של חיל המודיעין וסטארט-אפ סייבר). מפתחת מוצרים, אתרים ומערכות, בונה אוטומציות וסוכני AI, ומלווה עסקים, עצמאים ויזמים.</p>'
  '<div class="ab-links"><a href="/about">עוד עליי ←</a><a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener">LinkedIn</a></div></div></div>')

POSTS = [
  {
    "slug":"cost-to-develop-website-or-app",
    "title":"כמה עולה לפתח אתר או אפליקציה – ומאיפה מתחילים",
    "desc":"מה באמת קובע את העלות של אתר, מערכת או אפליקציה, איך מתחילים נכון, ולמה ‘זול’ יוצא לרוב ביוקר. מדריך קצר לעסקים, לעצמאים וליזמים.",
    "cat":"פיתוח מוצר",
    "date":"2026-09-23","modified":"2026-09-23","read":"7 דק׳ קריאה",
    "excerpt":"אין מחיר אחד לפיתוח – יש טווח שנקבע לפי היקף, מורכבות, עיצוב ואבטחה. איך להבין את העלות, מאיפה להתחיל, ולמה הזול לרוב עולה ביוקר.",
    "takeaways":[
      "אין ‘מחיר אחד’ – העלות נקבעת לפי היקף, מורכבות, עיצוב, אינטגרציות ואבטחה.",
      "אתר תדמית, מערכת ואפליקציה הם טווחים שונים לגמרי – מתחילים מהגדרת הצורך, לא מהמחיר.",
      "MVP ממוקד מוריד עלות וסיכון ומאפשר לצאת לשוק מהר.",
      "‘זול’ לרוב יוצא ביוקר: מוצר גנרי, בלי חשיבה עסקית ובלי אבטחה, חושף אתכם לתיקונים, לתביעות ולנזק תדמיתי.",
    ],
    "sections":[
      ("למה אין ‘מחיר אחד’ לפיתוח", '<p>אחת השאלות הראשונות של כל עסק היא ‘כמה זה יעלה?’ – וזו שאלה נכונה. אבל בניגוד למוצר מדף, פיתוח הוא לא פריט אחד במחיר קבוע: הוא נבנה בדיוק סביב הצורך שלכם. אתר תדמית, מערכת ניהול פנימית, ואפליקציה עם משתמשים ותשלומים הם שלושה עולמות שונים לחלוטין – ולכן גם טווחי המחיר שונים לגמרי. במקום לחפש ‘את המחיר’, כדאי להבין <strong>מה משפיע עליו</strong> ואיך להוציא את הערך הגבוה ביותר מכל שקל.</p>'),
      ("מה קובע את העלות", '<p>כמה גורמים מרכזיים קובעים את היקף העבודה – ולכן את העלות:</p><ul><li><strong>היקף ומורכבות</strong> – כמה מסכים, תהליכים ומשתמשים, וכמה ‘חכמה’ הלוגיקה מאחורי הקלעים.</li><li><strong>עיצוב וחוויית משתמש</strong> – עיצוב מותאם ומלוטש מול תבנית גנרית.</li><li><strong>אינטגרציות</strong> – חיבור למערכות תשלום, CRM, כלים חיצוניים ו-API.</li><li><strong>אבטחת מידע</strong> – קריטי כשיש פרטי לקוחות או תשלומים. אבטחה נכונה נבנית מהיסוד, לא מתווספת בסוף.</li><li><strong>תחזוקה והמשך</strong> – מוצר חי דורש תמיכה ושיפורים לאורך זמן.</li></ul>'),
      ("אתר תדמית, מערכת או אפליקציה?", '<p>לפני שמדברים על מחיר, כדאי להגדיר מה בעצם צריך. <strong>אתר תדמית</strong> מציג את העסק ומביא פניות – פרויקט ממוקד יחסית. <strong>מערכת פנימית</strong> (כמו CRM או כלי ניהול) בנויה סביב תהליך עבודה וחוסכת זמן יקר. <strong>אפליקציה או מוצר עם משתמשים</strong> הוא העולם הרחב ביותר – חשבונות, תשלומים וניהול שוטף. ככל שהמוצר עושה יותר, הוא דורש יותר – וזה בסדר; העיקר להתאים את ההשקעה למה שבאמת יזיז את העסק. <a href="/services/product-development">כך אני בונה מוצרים, אתרים ומערכות</a>.</p>'),
      ("מאיפה מתחילים נכון", '<p>ההתחלה הנכונה היא לא קוד – אלא <strong>אפיון</strong>. מגדירים מה הצורך העסקי האמיתי, מי המשתמשים, ומה חייב להיות בגרסה הראשונה. גישה טובה היא <strong>MVP</strong> – גרסה ראשונה ממוקדת שכוללת בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך, בלי פיצ׳רים מיותרים שמנפחים עלות וזמן. משם מרחיבים לפי מה שבאמת עובד. <a href="/services/consulting">ייעוץ ואפיון</a> בתחילת הדרך חוסך הרבה כסף בהמשך – כי בונים את הדבר הנכון מהפעם הראשונה.</p>'),
      ("למה ‘זול’ לרוב יוצא ביוקר", '<p>היום קל יותר מתמיד לבנות משהו מהר וזול – עם תבניות מוכנות או כלי AI. הבעיה: לרוב מקבלים מוצר <strong>גנרי</strong> שנראה כמו כל האחרים, בלי חשיבה עסקית שתגרום לו באמת לעבוד, ו<strong>בלי אבטחה</strong>. מערכת לא מאובטחת חשופה לתקיפה – ואם נדלפים פרטי לקוחות או תשלום, העסק חשוף ל<strong>תביעות</strong> ולנזק תדמיתי כבד. ‘זול’ כזה נגמר לרוב בפיתוח מחדש. מוצר שנבנה נכון – עם ראייה מוצרית ואבטחה מהיסוד – עולה יותר מראש, אבל מחזיר את ההשקעה ולא מתפוצץ בפנים.</p>'),
      ("סיכום", '<p>אין תשובה אחת ל‘כמה זה עולה’ – אבל יש דרך נכונה: להגדיר את הצורך, להתחיל ממוקד, ולבחור מי שבונה עם ניסיון, ראייה עסקית ואבטחה. יש לכם רעיון או צורך? <a href="/contact">דברו איתי</a> לשיחת היכרות קצרה, ונבין יחד מה נכון לבנות ובאיזה היקף.</p>'),
    ],
    "faq":[
      ("כמה עולה אתר תדמית לעומת אפליקציה?","אלה שני עולמות שונים: אתר תדמית הוא פרויקט ממוקד יחסית, ואפליקציה עם משתמשים ותשלומים היא היקף רחב בהרבה. הטווח נקבע לפי מה שהמוצר צריך לעשות – ולכן מגדירים קודם את הצורך, ואז נותנים הצעת מחיר מדויקת."),
      ("מה זה MVP וכמה הוא חוסך?","MVP הוא גרסה ראשונה ממוקדת שכוללת בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך. הוא מוריד עלות וסיכון, מקצר זמן, ומאפשר ללמוד מהשוק לפני השקעה גדולה."),
      ("למה פיתוח זול יוצא ביוקר?","כי לרוב מקבלים מוצר גנרי, בלי חשיבה עסקית ובלי אבטחה. מוצר לא מאובטח חושף את העסק לתביעות ולנזק תדמיתי, ומוצר גנרי לרוב נזרק ונבנה מחדש – מה שעולה בסוף הרבה יותר."),
    ],
  },
]

def blog_card(p):
    gi = POSTS.index(p) % len(BLOG_GRADS)
    return ('<a class="blog-card" href="/blog/%s"><div class="banner" style="background:%s"></div>'
      '<div class="bc-body"><span class="cat">%s</span><h3>%s</h3><p>%s</p>'
      '<span class="meta">%s · %s</span></div></a>') % (p["slug"], BLOG_GRADS[gi], p["cat"], p["title"], p["excerpt"], he_date(p["date"]), p["read"])

def blog_post(p, all_posts):
    slug=p["slug"]; path="/blog/"+slug; full=SITE+path
    gi = POSTS.index(p) % len(BLOG_GRADS)
    toc=[]; body=[]
    for i,(h2,html) in enumerate(p["sections"]):
        sid="s%d" % (i+1)
        toc.append('<li><a href="#%s">%s</a></li>' % (sid,h2))
        body.append('<h2 id="%s">%s</h2>%s' % (sid,h2,html))
    et=quote(p["title"]); eu=quote(full)
    share=('<div class="share"><span class="lbl">שיתוף:</span>'
      '<a href="https://wa.me/?text=%s%%20%s" target="_blank" rel="noopener" aria-label="שיתוף בוואטסאפ">%s</a>'
      '<a href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener" aria-label="שיתוף בלינקדאין">%s</a>'
      '<a href="https://twitter.com/intent/tweet?url=%s&text=%s" target="_blank" rel="noopener" aria-label="שיתוף ב-X">%s</a>'
      '<a href="mailto:?subject=%s&body=%s" aria-label="שיתוף במייל">%s</a>'
      '<button type="button" class="copy-link" data-url="%s" aria-label="העתקת קישור">%s</button></div>') % (et,eu,SVG_WA,eu,SVG_LI,eu,et,SVG_X,et,eu,SVG_MAIL,full,SVG_LINK)
    tldr='<div class="tldr"><b>בקצרה</b><ul>%s</ul></div>' % ("".join("<li>%s</li>" % t for t in p["takeaways"]))
    toc_html='<nav class="toc"><b>במאמר הזה</b><ol>%s</ol></nav>' % ("".join(toc))
    cp='<script>document.querySelectorAll(".copy-link").forEach(function(b){b.addEventListener("click",function(){try{navigator.clipboard.writeText(b.dataset.url);}catch(e){}var o=b.getAttribute("aria-label");b.setAttribute("aria-label","הקישור הועתק!");setTimeout(function(){b.setAttribute("aria-label",o);},1500);});});</script>'
    body_html=('  <section class="wrap"><article class="post">'
      '<span class="eyebrow"><span class="idx">//</span> <span class="ttl">%s</span></span>'
      '<h1 class="s-head">%s</h1>'
      '<div class="byline"><span class="av" style="background:%s">מ</span> <b>מיכל בר</b> <span class="dot">·</span> <time datetime="%s">%s</time> <span class="dot">·</span> %s</div>'
      '<div class="post-banner" style="background:%s"><span class="mono">&lt;/&gt;</span></div>'
      '%s%s%s<div class="prose post-body">%s</div>%s%s'
      '</article></section>') % (p["cat"], p["title"], BLOG_GRADS[gi], p["date"], he_date(p["date"]), p["read"], BLOG_GRADS[gi], share, tldr, toc_html, "".join(body), AUTHOR_BOX, cp)
    schemas_extra=[]
    if p.get("faq"):
        fh, fs = faq_block(p["faq"]); body_html += fh; schemas_extra.append(fs)
    others=[q for q in all_posts if q["slug"]!=slug][:3]
    if others:
        cards="".join(blog_card(q) for q in others)
        body_html += '  <section class="wrap"><h2 class="s-head" style="font-size:clamp(24px,3.4vw,32px);">מאמרים קשורים</h2><div class="blog-cards">%s</div></section>' % cards
    body_html += CTA
    bp={"@type":"BlogPosting","headline":p["title"],"description":p["desc"],
        "datePublished":p["date"],"dateModified":p["modified"],
        "image":SITE+"/og-image.jpg","url":full,"mainEntityOfPage":full,
        "author":{"@type":"Person","name":"מיכל בר","url":SITE+"/about"},"publisher":{"@id":BIZ}}
    page(path, "blog/"+slug+".html", p["title"]+" | הבלוג של מיכל בר",
         p["desc"], [("דף הבית","/"),("בלוג","/blog"),(p["title"],None)],
         body_html, [bp]+schemas_extra)

for _p in POSTS:
    blog_post(_p, POSTS)

blog_index_body = ('  <section class="wrap page-hero"><span class="eyebrow"><span class="idx">//</span> <span class="ttl">בלוג</span></span>'
  '<h1 class="s-head">הבלוג</h1>'
  '<p class="s-lead">תובנות מעשיות על פיתוח מוצר, אתרים, אוטומציה וסוכני AI – לעסקים, לעצמאים וליזמים.</p></section>'
  '  <section class="wrap"><div class="blog-cards">%s</div></section>') % ("".join(blog_card(p) for p in POSTS))
page("/blog","blog.html","בלוג · תובנות על פיתוח, אוטומציה וסוכני AI | מיכל בר",
     "תובנות מעשיות על פיתוח מוצר ואתרים, אוטומציה וסוכני AI, וייעוץ טכנולוגי – לעסקים, לעצמאים וליזמים.",
     [("דף הבית","/"),("בלוג",None)],
     blog_index_body + CTA,
     [{"@type":"Blog","name":"הבלוג של מיכל בר","url":SITE+"/blog"}])

print("\\nAll pages generated.")
