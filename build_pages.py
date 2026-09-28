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
FONTS_HE = '<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'
FONTS_EN = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Assistant:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">'

BRAND_NAME = {"he": "מיכל בר", "en": "Michal Bar"}
BRAND_SUB  = {"he": "פיתוח · אוטומציה · סוכני AI", "en": "Development · Automation · AI Agents"}
BURGER_LABEL = {"he": "תפריט", "en": "Menu"}
NAV_LINKS = {
    "he": [("/services", "שירותים"), ("/about", "עליי"), ("/projects", "פרויקטים"), ("/faq", "שאלות נפוצות"), ("/blog", "בלוג")],
    "en": [("/services", "Services"), ("/about", "About"), ("/projects", "Projects"), ("/faq", "FAQ"), ("/blog", "Blog")],
}
NAV_CTA = {"he": "צרו קשר", "en": "Contact"}

def _en_url(path):
    return "/en" if path == "/" else "/en" + path

def nav_html(lang, path):
    pfx = "" if lang == "he" else "/en"
    links = "".join('<a href="%s%s">%s</a>\n        ' % (pfx, u, label) for u, label in NAV_LINKS[lang])
    if lang == "he":
        switch = '<a class="lang-switch" href="%s" hreflang="en" aria-label="English">EN</a>' % _en_url(path)
    else:
        switch = '<a class="lang-switch" href="%s" hreflang="he" aria-label="Hebrew">HE</a>' % path
    return (
'<header id="hdr">\n'
'  <div class="wrap">\n'
'    <nav>\n'
'      <a class="brand" href="%s">\n' % (pfx or "/") +
'        <img class="logo" src="/logo.png" alt="%s" />\n' % BRAND_NAME[lang] +
'        <div><b>%s</b><small>%s</small></div>\n' % (BRAND_NAME[lang], BRAND_SUB[lang]) +
'      </a>\n'
'      <div class="nav-links" id="navlinks">\n'
'        ' + links +
'<a class="nav-cta" href="%s/contact">%s</a>\n' % (pfx, NAV_CTA[lang]) +
'      </div>\n'
'      ' + switch + '\n'
'      <button class="burger" id="burger" aria-label="%s"><span></span><span></span><span></span></button>\n' % BURGER_LABEL[lang] +
'    </nav>\n'
'  </div>\n'
'</header>\n'
    )

def head(title, desc, path, schemas, lang="he"):
    he_href = SITE + path
    en_href = SITE + _en_url(path)
    canonical = he_href if lang == "he" else en_href
    html_attr = 'lang="he" dir="rtl"' if lang == "he" else 'lang="en" dir="ltr"'
    og_locale = "he_IL" if lang == "he" else "en_US"
    site_name = "מיכל בר · פתרונות טכנולוגיים" if lang == "he" else "Michal Bar · Technology Solutions"
    fonts = FONTS_HE if lang == "he" else FONTS_EN
    hreflangs = ('<link rel="alternate" hreflang="he" href="%s">\n' % he_href +
                 '<link rel="alternate" hreflang="en" href="%s">\n' % en_href +
                 '<link rel="alternate" hreflang="x-default" href="%s">\n' % he_href)
    nav = nav_html(lang, path)
    ld = ""
    if schemas:
        graph = {"@context": "https://schema.org", "@graph": schemas}
        ld = '<script type="application/ld+json">\n' + j(graph) + '\n</script>\n'
    return f'''<!DOCTYPE html>
<html {html_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
{hreflangs}<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:locale" content="{og_locale}" />
<meta property="og:image" content="{SITE}/og-image.jpg" />
<meta property="og:site_name" content="{site_name}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{SITE}/og-image.jpg" />
<link rel="icon" href="/logo.png" type="image/png">
<link rel="apple-touch-icon" href="/logo.png">
{ld}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
{nav}'''

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

FOOTER_EN = '''<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-brand">
      <div class="brand">
        <img class="logo" src="/logo.png" alt="Michal Bar" />
        <div><b>Michal Bar</b><small>Development · Automation · AI Agents</small></div>
      </div>
      <p>Product, web & app development, automation and AI agents - for businesses, startups and independent professionals. From understanding the need to shipping the solution.</p>
    </div>
    <div class="footer-col">
      <h4>Navigation</h4>
      <a href="/en/services">Services</a>
      <a href="/en/about">About</a>
      <a href="/en/projects">Projects</a>
      <a href="/en/faq">FAQ</a>
      <a href="/en/blog">Blog</a>
      <a href="/en/contact">Contact</a>
      <a href="/en/accessibility">Accessibility</a>
      <a href="/en/privacy">Privacy Policy</a>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      <a href="/en/services/product-development">Product & Web Development</a>
      <a href="/en/services/automation">Automation & AI Agents</a>
      <a href="/en/services/consulting">Tech Consulting</a>
      <div class="footer-icons">
        <a href="https://wa.me/972547105176" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.04 4C9.93 4 4.98 8.95 4.98 15.06c0 2.05.56 4.05 1.62 5.8L4 28l7.3-2.55a11.04 11.04 0 0 0 4.74 1.07h.01c6.11 0 11.06-4.95 11.06-11.06C27.1 8.95 22.15 4 16.04 4zm0 20.2c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-4.33 1.51 1.45-4.22-.2-.32a9.16 9.16 0 0 1-1.4-4.87c0-5.06 4.12-9.18 9.19-9.18 2.45 0 4.76.96 6.49 2.69a9.13 9.13 0 0 1 2.69 6.5c0 5.06-4.12 9.18-9.18 9.18z"/></svg></a>
        <a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg></a>
      </div>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span class="mono">2026</span> Michal Bar · All rights reserved</span>
    <span>Development · Automation · AI Agents</span>
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

def crumbs(trail, lang="he"):
    # trail: list of (name, url_or_None)
    pfx = "" if lang == "he" else "/en"
    parts, items = [], []
    for i,(name,url) in enumerate(trail):
        if url:
            u = (pfx or "/") if url == "/" else pfx + url
            parts.append(f'<a href="{u}">{name}</a>')
        else:
            parts.append(f'<span>{name}</span>')
        items.append({"@type":"ListItem","position":i+1,"name":name,
                      **({"item":SITE+u} if url else {})})
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

def write(path_rel, html, lang="he"):
    if lang == "en":
        path_rel = "en/" + path_rel
    fp = pathlib.Path(path_rel)
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(html, encoding="utf-8")
    print("wrote", path_rel)

def page(path, filename, title, desc, trail, body_html, schemas, lang="he"):
    cr_html, cr_schema = crumbs(trail, lang)
    all_schemas = [cr_schema] + schemas
    html = head(title, desc, path, all_schemas, lang)
    foot = FOOTER_EN if lang == "en" else FOOTER
    html += '<main>\n<div class="wrap">' + cr_html + '</div>\n' + body_html + '\n</main>\n' + foot
    write(filename, html, lang)

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
SVC_LABELS = {
    "he": {"svc":"שירות","inc":"מה זה כולל","who":"למי זה מתאים","rel":"שירותים קשורים","home":"דף הבית","services":"שירותים"},
    "en": {"svc":"Service","inc":"What's included","who":"Who it's for","rel":"Related services","home":"Home","services":"Services"},
}

def service_page(path, filename, title, desc, h1, lead, intro_paras, includes, forwhom, faq_pairs, svc_name, svc_desc, lang="he"):
    L = SVC_LABELS[lang]
    pfx = "/en" if lang == "en" else ""
    svc_list = SERVICES_EN if lang == "en" else SERVICES
    cta = CTA_EN if lang == "en" else CTA
    inc = "".join(f"<li>{x}</li>" for x in includes)
    who = "".join(f"<li>{x}</li>" for x in forwhom)
    paras = "".join(f"<p>{p}</p>" for p in intro_paras)
    body = f'''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">{L["svc"]}</span></span>
    <h1 class="s-head">{h1}</h1>
    <p class="s-lead">{lead}</p>
  </section>
  <section class="wrap">
    <div class="prose">{paras}</div>
    <div class="cards svc-pair" style="margin-top:32px;">
      <div class="card"><h3>{L["inc"]}</h3><ul class="svc-list">{inc}</ul></div>
      <div class="card"><h3>{L["who"]}</h3><ul class="svc-list">{who}</ul></div>
    </div>
  </section>
'''
    fh, fs = faq_block(faq_pairs)
    others = [(p, n) for p, n in svc_list if p != path]
    rel = "".join(f'<a href="{pfx}{p}"><span>{n}</span> <span class="ar">&#8592;</span></a>' for p, n in others)
    related = f'''  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">{L["rel"]}</span></span>
    <div class="related">{rel}</div>
  </section>
'''
    page(path, filename, title, desc,
         [(L["home"],"/"),(L["services"],"/services"),(h1,None)],
         body + fh + related + cta,
         [service_schema(svc_name, svc_desc, path), fs], lang=lang)

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
BLOG_IMAGES = ["/assets/blog-1.svg","/assets/blog-2.svg","/assets/blog-3.svg"]
HE_MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]
def he_date(iso):
    y,m,d = iso.split("-"); return "%d ב%s %s" % (int(d), HE_MONTHS[int(m)-1], y)
AUTHOR_BOX = ('<div class="author-box"><img class="av" src="/michal.jpg" alt="מיכל בר" loading="lazy" />'
  '<div><h4>מיכל בר</h4><p>מפתחת ויועצת פתרונות טכנולוגיים – מעל 20 שנה בהייטק ובסייבר (היחידה הטכנולוגית של חיל המודיעין וסטארט-אפ סייבר). מפתחת מוצרים, אתרים ומערכות, בונה אוטומציות וסוכני AI, ומלווה עסקים, עצמאים ויזמים.</p>'
  '<div class="ab-links"><a href="/about">עוד עליי ←</a><a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener">LinkedIn</a></div></div></div>')

AUTHOR_BOX_EN = ('<div class="author-box"><img class="av" src="/michal.jpg" alt="Michal Bar" loading="lazy" />'
  '<div><h4>Michal Bar</h4><p>Technology solutions developer and consultant - 20+ years in hi-tech and cybersecurity (the IDF Intelligence Corps technological unit and a cyber startup). Builds products, websites and systems, automations and AI agents, and partners with businesses, independents and entrepreneurs.</p>'
  '<div class="ab-links"><a href="/en/about">More about me &#8594;</a><a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener">LinkedIn</a></div></div></div>')

EN_MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def fmt_date(iso, lang="he"):
    if lang == "en":
        y,m,d = iso.split("-"); return "%s %d, %s" % (EN_MONTHS[int(m)-1], int(d), y)
    return he_date(iso)

BLOG_LABELS = {
    "he": {"share":"שיתוף","brief":"בקצרה","toc":"במאמר הזה","related":"מאמרים קשורים","byline":"מיכל בר","alt":"מיכל בר","suffix":" | הבלוג של מיכל בר","home":"דף הבית","blog":"בלוג","readmore":"לקרוא עוד ←","all":"הכל"},
    "en": {"share":"Share","brief":"In brief","toc":"In this article","related":"Related articles","byline":"Michal Bar","alt":"Michal Bar","suffix":" | Michal Bar's Blog","home":"Home","blog":"Blog","readmore":"Read more &#8594;","all":"All"},
}

POSTS = [
  {
    "slug":"cost-to-develop-website-or-app",
    "title":"כמה עולה לפתח אתר או אפליקציה – ומאיפה מתחילים",
    "desc":"כמה עולה לפתח אתר, מערכת או אפליקציה? מה קובע את המחיר, איך מתחילים נכון, ולמה ‘זול’ יוצא לרוב ביוקר – מדריך לעסקים, לעצמאים וליזמים.",
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

POSTS += [
  {
    "slug":"automation-and-ai-agents-getting-started",
    "title":"אוטומציה עסקית וסוכני AI לעסקים – מאיפה מתחילים",
    "desc":"אוטומציה עסקית וסוכני AI לעסקים קטנים: מה ההבדל ביניהם, מאיפה מתחילים, מה אפשר לאטמט, ואיך עושים את זה נכון בלי גימיקים.",
    "cat":"אוטומציה וסוכני AI","date":"2026-09-21","modified":"2026-09-21","read":"6 דק׳ קריאה",
    "excerpt":"אוטומציה וסוכני AI יכולים לחסוך לעסק מאות שעות – אם מתחילים מהמקום הנכון. מה ההבדל ביניהם, מאיפה מתחילים, ואיך לא ליפול לגימיקים.",
    "takeaways":[
      "אוטומציה מריצה חוקים קבועים; סוכן AI מבין הקשר ומקבל החלטות – ומשלבים ביניהם.",
      "מתחילים ממיפוי: איפה נשרף הכי הרבה זמן ידני, לא מ‘איפה לדחוף AI’.",
      "הערך הוא בזיהוי התהליכים הנכונים לאטמט – עם ראייה עסקית, לא גימיק.",
    ],
    "sections":[
      ("אוטומציה עסקית – למה זה הזמן להתחיל", '<p>כמעט כל עסק מבזבז שעות על פעולות ידניות חוזרות – העברת נתונים בין מערכות, מיילים, דוחות וטפסים. היום, בעזרת אוטומציה וסוכני AI, אפשר להחזיר את השעות האלה. הכלים בשלים והמחירים נגישים – אבל ההצלחה תלויה פחות בטכנולוגיה ויותר ב<strong>בחירה נכונה של מה לאטמט</strong>.</p>'),
      ("אוטומציה מול סוכני AI – מה ההבדל", '<p><strong>אוטומציה</strong> מריצה חוקים קבועים: ‘אם קורה X, בצע Y’. היא מצוינת לתהליכים חוזרים וברורים. <strong>סוכן AI</strong> הוא צעד קדימה – מבין הקשר, מקבל החלטות ומתמודד גם עם מצבים לא צפויים: מענה לפניות, סיווג וניתוב מידע, סיכומים והפקת תוכן. בפועל <a href="/services/automation">משלבים את השניים</a> – אוטומציה למה שקבוע, וסוכני AI למה שדורש הבנה.</p>'),
      ("מאיפה מתחילים – מיפוי לפני הכל", '<p>הטעות הנפוצה היא להתחיל מ‘בואו נכניס AI’. ההתחלה הנכונה הפוכה: <strong>מיפוי</strong>. רושמים את המשימות החוזרות, מזהים איפה נשרף הכי הרבה זמן ואיפה קורות הכי הרבה טעויות – ומשם בוחרים את ההזדמנויות בעלות הערך הגבוה ביותר. אוטומציה של התהליך הלא נכון רק מבזבזת זמן; אוטומציה של הצוואר-בקבוק האמיתי משנה את העסק.</p>'),
      ("מה אפשר לאטמט", '<p>כמעט כל תהליך חוזר: סנכרון נתונים בין מערכות, שליחת מיילים ועדכונים, הפקת דוחות, טפסים וגבייה, מענה ראשוני ללקוחות, וסיווג לידים וניתובם. עם סוכני AI מוסיפים גם משימות שדורשות הבנה והחלטה – סיכום שיחות, מענה חכם לפניות, או הפקת תוכן ראשוני.</p>'),
      ("איך עושים את זה נכון (ולא גימיק)", '<p>ההבדל בין אוטומציה שמשנה עסק לבין גימיק שנזנח אחרי חודש הוא <strong>ראייה עסקית</strong>: להבין את התהליך, לייעל אותו, ורק אז לאטמט – בכלים שמשתלבים במה שכבר יש לכם. עם רקע של מעל 20 שנה בהייטק, אני מתחילה מהצורך העסקי ולא מהכלי, ובונה פתרון שבאמת עובד לאורך זמן.</p>'),
      ("סיכום", '<p>אוטומציה וסוכני AI הם מנוף אמיתי לעסק – אבל רק כשמתחילים מהמקום הנכון. רוצים לדעת מה שווה לאטמט אצלכם? <a href="/contact">דברו איתי</a> לשיחת היכרות קצרה, ונמפה יחד את ההזדמנויות.</p>'),
    ],
    "faq":[
      ("מה אפשר לאטמט בעסק?","כמעט כל תהליך חוזר: העברת נתונים בין מערכות, מיילים ועדכונים, דוחות, טפסים, גבייה, מענה וסיווג לידים – ובעזרת AI גם משימות שדורשות הבנה והחלטה."),
      ("כמה זמן אוטומציה חוסכת?","תלוי בתהליך – לקוחות חסכו מאות שעות עבודה בשנה. אחרי מיפוי אפשר להצביע על ההזדמנויות הגדולות ביותר."),
      ("צריך לדעת לתכנת כדי להשתמש בזה?","לא. אני בונה ומטמיעה את הפתרון, ואתם נהנים מהתוצאה – תהליך שרץ מעצמו, בלי לגעת בקוד."),
    ],
  },
  {
    "slug":"when-to-consult-before-building",
    "title":"ייעוץ טכנולוגי ואפיון – מתי לפנות לפני שמפתחים",
    "desc":"ייעוץ טכנולוגי ואפיון לעסקים: רוב הפרויקטים נכשלים כי בנו את הדבר הלא נכון. מתי כדאי לייעץ ולאפיין לפני שמשקיעים בפיתוח – וכמה כסף זה חוסך.",
    "cat":"ייעוץ","date":"2026-09-18","modified":"2026-09-18","read":"5 דק׳ קריאה",
    "excerpt":"הרבה פרויקטים נכשלים לא בגלל הפיתוח, אלא כי בנו את הדבר הלא נכון. מתי כדאי לעצור, לייעץ ולאפיין – לפני שמשקיעים בפיתוח.",
    "takeaways":[
      "רוב הכישלונות הם לא טכניים – בונים את המוצר הלא נכון.",
      "ייעוץ ואפיון בתחילת הדרך חוסכים פיתוח מיותר וכסף רב.",
      "היתרון: חיבור בין הבנה עסקית, המשתמשים והטכנולוגיה.",
    ],
    "sections":[
      ("למה פרויקטים נכשלים", '<p>הרבה פרויקטים טכנולוגיים לא נכשלים בגלל הקוד – אלא כי בנו את הדבר הלא נכון. פיצ׳רים שאף אחד לא צריך, תהליך שלא פותר את הכאב האמיתי, או מוצר שלא מתאים לקהל. הכל תקין טכנית, אבל לא מזיז את העסק.</p>'),
      ("מתי כדאי לעצור ולייעץ", '<p>שווה לפנות לייעוץ לפני פיתוח כשלא בטוחים מה בדיוק לבנות, איך לתעדף, או איזו גישה נכונה; כשעומדים לפני השקעה משמעותית ורוצים לוודא שבונים את הדבר הנכון; או כשיש מוצר קיים שצריך לשפר או להרחיב. במקרים האלה, כמה שעות ייעוץ חוסכות חודשי פיתוח מיותר.</p>'),
      ("מה כולל תהליך ייעוץ ואפיון", '<p>מיפוי הצורך והכאב האמיתי, הבנה של הביזנס והמשתמשים, גיבוש אסטרטגיה ותיעדוף, ותכנון פתרון מדויק – עד <a href="/services/consulting">החלטה מושכלת ותוכנית פעולה ברורה</a>. התוצאה: אתם יודעים בדיוק מה לבנות, למה, ובאיזה סדר.</p>'),
      ("הבידול – שלושה עולמות במקום אחד", '<p>היתרון שלי הוא שילוב נדיר: הבנה של הלקוח, של הביזנס ושל הטכנולוגיה. אני יודעת גם לזהות את הצורך האמיתי, גם להבין מה אפשרי טכנולוגית, וגם לתעדף נכון כדי להביא ערך מהר – מעל 20 שנה של ניסיון שמונעות טעויות יקרות.</p>'),
      ("סיכום", '<p>ייעוץ טוב הוא לא הוצאה – הוא חיסכון. לפני שמשקיעים בפיתוח, שווה לוודא שבונים את הדבר הנכון. <a href="/contact">דברו איתי</a> ונבין יחד מה באמת צריך.</p>'),
    ],
    "faq":[
      ("מתי כדאי לפנות לייעוץ ולא ישר לפיתוח?","כשלא בטוחים מה בדיוק לבנות, איך לתעדף, או איזו גישה נכונה – ובמיוחד לפני השקעה גדולה. ייעוץ טוב חוסך פיתוח מיותר וכסף רב."),
      ("כמה זמן לוקח תהליך ייעוץ?","תלוי בהיקף – משיחה ממוקדת אחת ועד תהליך של מספר שבועות. מגדירים יחד את ההיקף הנכון בשיחת ההיכרות."),
      ("אני כבר יודע מה לבנות – עדיין צריך ייעוץ?","לא בהכרח. אם הצורך ברור ומאופיין, אפשר לגשת ישר לפיתוח. הייעוץ נועד למי שרוצה לוודא שהכיוון נכון לפני שמשקיע."),
    ],
  },
  {
    "slug":"mvp-vs-full-product",
    "title":"MVP או מוצר מלא – מה זה, ואיך מחליטים",
    "desc":"מה זה MVP (פיתוח מוצר ראשוני), מתי לבחור גרסה ראשונה ממוקדת ומתי מוצר מלא, ואיך מגדירים את הליבה הנכונה שתביא ערך מהר.",
    "cat":"פיתוח מוצר","date":"2026-09-15","modified":"2026-09-15","read":"6 דק׳ קריאה",
    "excerpt":"MVP הוא לא ‘מוצר חצי אפוי’ – הוא גרסה ראשונה ממוקדת. מתי לבחור בו, מתי ללכת על מוצר מלא, ואיך מגדירים את הליבה הנכונה.",
    "takeaways":[
      "MVP הוא גרסה ראשונה ממוקדת ומלוטשת – לא מוצר חצי-גמור.",
      "הוא מוריד עלות וסיכון ומאפשר ללמוד מהשוק מהר.",
      "המפתח: להגדיר נכון את הליבה שתביא ערך – ולבנות אותה במלואה.",
    ],
    "sections":[
      ("מה זה MVP באמת", '<p>MVP (Minimum Viable Product) נתפס לפעמים בטעות כ‘מוצר חצי אפוי’. הוא לא. MVP הוא <strong>גרסה ראשונה ממוקדת</strong>: מוצר שלם ומלוטש שכולל בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך – בלי פיצ׳רים מיותרים שמנפחים עלות וזמן.</p>'),
      ("מתי לבחור MVP", '<p>MVP מתאים כשרוצים לצאת לשוק מהר, לבדוק רעיון מול משתמשים אמיתיים, או להשקיע בזהירות לפני התחייבות גדולה. הוא מוריד סיכון: במקום להמר על מוצר ענק, בונים את הליבה, לומדים מה עובד, ומרחיבים לפי הצורך האמיתי.</p>'),
      ("מתי ללכת על מוצר מלא", '<p>לפעמים הצורך ברור ובשל ודורש היקף רחב מלכתחילה – מערכת פנימית שחייבת לכסות תהליך שלם, או מוצר בשוק תחרותי שבו גרסה חלקית לא תספיק. גם אז אני בונה בשלבים ומשתפת אתכם לאורך הדרך.</p>'),
      ("איך מגדירים את הליבה הנכונה", '<p>זה הלב של ההחלטה – ולכן מתחילים ב<a href="/services/consulting">אפיון</a>. שואלים: מה הערך המרכזי שהמוצר חייב לספק? מה חייב להיות בגרסה הראשונה ומה יכול לחכות? אפיון חד מונע ‘זחילת פיצ׳רים’ ומבטיח שכל שקל מושקע במה שבאמת מזיז.</p>'),
      ("הטעות הנפוצה", '<p>הטעות הגדולה היא לבנות יותר מדי, מוקדם מדי. מוצר עמוס שנבנה חודשים לפני שראה משתמש אמיתי – מסוכן ויקר. גישה ממוקדת, עם <a href="/services/product-development">ראייה מוצרית</a>, מביאה אתכם לשוק מהר ובחוכמה.</p>'),
      ("סיכום", '<p>MVP או מוצר מלא – התשובה תלויה בצורך, בסיכון ובשוק. מה שקבוע: מתחילים מהגדרת הליבה הנכונה. <a href="/contact">דברו איתי</a> ונחליט יחד מה נכון לכם.</p>'),
    ],
    "faq":[
      ("מה ההבדל בין MVP למוצר מלא?","MVP הוא גרסה ראשונה ממוקדת שכוללת בדיוק את מה שצריך כדי לצאת לשוק ולהוכיח ערך; מוצר מלא הוא היקף רחב יותר. בשני המקרים בונים את המוצר במלואו ומשתפים אתכם לאורך הדרך."),
      ("כמה עולה לפתח MVP?","העלות תלויה בהיקף הפיצ׳רים. MVP ממוקד עולה משמעותית פחות ממוצר מלא. אחרי אפיון תקבלו הצעת מחיר מדויקת מחולקת לאבני דרך."),
      ("אפשר להרחיב MVP למוצר מלא בהמשך?","בהחלט – זו כל הנקודה. יוצאים עם ליבה ממוקדת, לומדים מהשוק, ומרחיבים בהדרגה למה שבאמת עובד."),
    ],
  },
]

POSTS += [
  {
    "slug":"wix-vs-custom-website",
    "title":"למה לבנות אתר בוויקס (Wix) לא מתאים לכל אחד",
    "desc":"אתר בוויקס (Wix) מצוין לחלק מהעסקים – ולא מתאים לאחרים. מתי וויקס עובד, מתי כדאי פיתוח אתר מותאם אישית, ומה ההבדל ב-SEO, בביצועים ובבידול.",
    "cat":"פיתוח מוצר","date":"2026-09-27","modified":"2026-09-27","read":"6 דק׳ קריאה",
    "excerpt":"וויקס זול, מהיר להקמה ומצוין להתחלה – אבל לא מתאים לכל עסק. מתי וויקס עונה על הצורך, ומתי כדאי פיתוח אתר מותאם אישית.",
    "takeaways":[
      "וויקס מצוינת לאתר תדמית בסיסי, בתקציב נמוך, בגישת עשה-זאת-בעצמך.",
      "המגבלות: שליטה ב-SEO ובמהירות, אינטגרציות מורכבות, התאמה אישית, גדילה ואבטחה.",
      "כשצריך פונקציונליות ייחודית, ביצועים, או אתר שבאמת ממיר ומבדל – פיתוח מותאם עדיף.",
    ],
    "sections":[
      ("מתי אתר בוויקס דווקא כן מתאים", '<p>נתחיל בהוגנות: <strong>וויקס (Wix) היא כלי מצוין</strong> לחלק גדול מהעסקים. אם צריך אתר תדמית פשוט, בתקציב נמוך, שאפשר לתחזק לבד – וויקס נותנת עצמאות, אירוח, דומיין וכלים נוחים בגרירה, בלי לגעת בקוד. להתחלה או לנוכחות בסיסית, זו נקודת פתיחה הגיונית לגמרי.</p>'),
      ("המגבלות של וויקס שחשוב להכיר", '<p>אבל וויקס בנויה כפלטפורמת תבניות – וזה מגיע עם תקרה. המגבלות המרכזיות:</p><ul><li><strong>SEO ומהירות</strong> – שליטה מוגבלת בקוד ובביצועים; מהירות האתר, שקריטית לדירוג בגוגל, לרוב פחות טובה מאתר מותאם.</li><li><strong>אינטגרציות ופונקציונליות</strong> – חיבור למערכות עסקיות, לוגיקה מותאמת או פיצ׳רים ייחודיים – מוגבלים או בלתי אפשריים.</li><li><strong>התאמה ובידול</strong> – קל להיתקע במראה תבניתי שנראה כמו הרבה אתרים אחרים.</li><li><strong>גדילה ונעילה</strong> – קשה להרחיב, וקשה לצאת מהפלטפורמה בהמשך.</li><li><strong>אבטחה ושליטה</strong> – פחות שליטה על הסביבה ועל אבטחת המידע.</li></ul>'),
      ("וויקס מול פיתוח אתר מותאם – מה ההבדל", '<p>ההבדל המהותי: בוויקס אתם מתאימים את העסק לפלטפורמה; ב<a href="/services/product-development">פיתוח מותאם אישית</a> הפלטפורמה מותאמת לעסק. אתר מותאם נותן שליטה מלאה בביצועים, ב-SEO, בעיצוב, באינטגרציות ובאבטחה – ונבנה בדיוק סביב הצורך והמסרים שלכם.</p>'),
      ("מתי כדאי לבחור פיתוח מותאם", '<p>שווה לעבור לפיתוח מותאם כשהאתר הוא נכס עסקי מרכזי ולא רק כרטיס ביקור: כשצריך פונקציונליות ייחודית או אינטגרציות; כשה-SEO והמהירות קריטיים; כשרוצים אתר ש<strong>ממיר לקוחות</strong> ומבדל אתכם, לא עוד תבנית; וכשיש נתונים רגישים שדורשים <strong>אבטחה אמיתית מהיסוד</strong> (רקע שאני מביאה מעולם הסייבר).</p>'),
      ("אז מה מתאים לכם?", '<p>השאלה היא לא ‘וויקס טובה או רעה’ – אלא ‘מה נכון לעסק שלכם, עכשיו ובהמשך’. אם לא בטוחים, שווה <a href="/services/consulting">לאפיין את הצורך</a> לפני שמתחייבים. <a href="/contact">דברו איתי</a> ונבין יחד מה הפתרון הנכון בשבילכם.</p>'),
    ],
    "faq":[
      ("האם וויקס טובה ל-SEO?","וויקס השתפרה מאוד, אבל עדיין יש מגבלות בשליטה בקוד ובמהירות מול אתר מותאם – ומהירות היא גורם דירוג חשוב. לאתר שה-SEO קריטי לו, פיתוח מותאם נותן יתרון."),
      ("וויקס או פיתוח מותאם – מה עדיף?","תלוי בצורך. וויקס מצוינת לאתר בסיסי בתקציב נמוך שמתחזקים לבד; פיתוח מותאם עדיף כשצריך פונקציונליות ייחודית, ביצועים, אינטגרציות, בידול או אבטחה."),
      ("אפשר לעבור מוויקס לאתר מותאם בהמשך?","כן. הרבה עסקים מתחילים בוויקס ועוברים לאתר מותאם כשהם גדלים. אפשר לתכנן את המעבר כך שישמור על התוכן והדירוג הקיימים."),
    ],
  },
]

def blog_card(p, lang="he"):
    pfx = "/en" if lang == "en" else ""
    img = p.get("img", BLOG_IMAGES[0])
    return ('<a class="blog-card" data-cat="%s" href="%s/blog/%s"><div class="banner" style="background-image:url(%s)"></div>'
      '<div class="bc-body"><span class="cat">%s</span><h3>%s</h3><p>%s</p>'
      '<span class="meta">%s · %s</span></div></a>') % (p["cat"], pfx, p["slug"], img, p["cat"], p["title"], p["excerpt"], fmt_date(p["date"], lang), p["read"])

def blog_post(p, all_posts, lang="he"):
    L = BLOG_LABELS[lang]
    pfx = "/en" if lang == "en" else ""
    cta = CTA_EN if lang == "en" else CTA
    author = AUTHOR_BOX_EN if lang == "en" else AUTHOR_BOX
    slug=p["slug"]; path="/blog/"+slug; full=SITE+pfx+path
    img = p.get("img", BLOG_IMAGES[0])
    toc=[]; body=[]
    for i,(h2,html) in enumerate(p["sections"]):
        sid="s%d" % (i+1)
        toc.append('<li><a href="#%s">%s</a></li>' % (sid,h2))
        body.append('<h2 id="%s">%s</h2>%s' % (sid,h2,html))
    et=quote(p["title"]); eu=quote(full)
    share=('<div class="share"><span class="lbl">%s</span><div class="share-icons">'
      '<a href="https://wa.me/?text=%s%%20%s" target="_blank" rel="noopener" aria-label="WhatsApp">%s</a>'
      '<a href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener" aria-label="LinkedIn">%s</a>'
      '<a href="https://twitter.com/intent/tweet?url=%s&text=%s" target="_blank" rel="noopener" aria-label="X">%s</a>'
      '<a href="https://mail.google.com/mail/?view=cm&fs=1&su=%s&body=%s" target="_blank" rel="noopener" aria-label="Email">%s</a>'
      '<button type="button" class="copy-link" data-url="%s" aria-label="Copy link">%s</button></div></div>') % (L["share"],et,eu,SVG_WA,eu,SVG_LI,eu,et,SVG_X,et,eu,SVG_MAIL,full,SVG_LINK)
    tldr='<div class="tldr"><b>%s</b><ul>%s</ul></div>' % (L["brief"], "".join("<li>%s</li>" % t for t in p["takeaways"]))
    toc_html='<nav class="toc"><b>%s</b><ol>%s</ol></nav>' % (L["toc"], "".join(toc))
    cp='<script>document.querySelectorAll(".copy-link").forEach(function(b){b.addEventListener("click",function(){try{navigator.clipboard.writeText(b.dataset.url);}catch(e){}b.classList.add("copied");setTimeout(function(){b.classList.remove("copied");},1600);});});</script>'
    body_html=('  <section class="wrap"><article class="post">'
      '<div class="post-head">'
      '<span class="eyebrow"><span class="idx">//</span> <span class="ttl">%s</span></span>'
      '<h1 class="s-head">%s</h1>'
      '<div class="byline"><img class="av" src="/michal.jpg" alt="%s" /> <b>%s</b> <span class="dot">·</span> <time datetime="%s">%s</time> <span class="dot">·</span> %s</div>'
      '</div>'
      '<div class="post-banner" style="background-image:url(%s)"></div>'
      '<div class="post-layout">'
      '<aside class="post-side">%s%s</aside>'
      '<div class="post-main">%s<div class="prose post-body">%s</div>%s</div>'
      '</div>%s'
      '</article></section>') % (p["cat"], p["title"], L["alt"], L["byline"], p["date"], fmt_date(p["date"], lang), p["read"], img, share, toc_html, tldr, "".join(body), author, cp)
    schemas_extra=[]
    if p.get("faq"):
        fh, fs = faq_block(p["faq"]); body_html += fh; schemas_extra.append(fs)
    others=[q for q in all_posts if q["slug"]!=slug][:3]
    if others:
        cards="".join(blog_card(q, lang) for q in others)
        body_html += '  <section class="wrap"><h2 class="s-head" style="font-size:clamp(24px,3.4vw,32px);">%s</h2><div class="blog-cards">%s</div></section>' % (L["related"], cards)
    body_html += cta
    bp={"@type":"BlogPosting","headline":p["title"],"description":p["desc"],
        "datePublished":p["date"],"dateModified":p["modified"],
        "image":SITE+"/og-image.jpg","url":full,"mainEntityOfPage":full,
        "author":{"@type":"Person","name":L["byline"],"url":SITE+pfx+"/about"},"publisher":{"@id":BIZ}}
    page(path, "blog/"+slug+".html", p["title"]+L["suffix"],
         p["desc"], [(L["home"],"/"),(L["blog"],"/blog"),(p["title"],None)],
         body_html, [bp]+schemas_extra, lang=lang)

BLOG_IMG_BY_SLUG = {
    "cost-to-develop-website-or-app":"/assets/blog-1.svg",
    "automation-and-ai-agents-getting-started":"/assets/blog-2.svg",
    "when-to-consult-before-building":"/assets/blog-3.svg",
    "mvp-vs-full-product":"/assets/blog-1.svg",
    "wix-vs-custom-website":"/assets/blog-3.svg",
}
for _p in POSTS:
    if _p["slug"] in BLOG_IMG_BY_SLUG: _p["img"] = BLOG_IMG_BY_SLUG[_p["slug"]]
for _p in POSTS:
    blog_post(_p, POSTS)

_feat = POSTS[0]
featured_html = ('  <section class="wrap"><a class="blog-featured" href="/blog/%s">'
  '<div class="feat-body"><span class="cat">%s</span><h2>%s</h2><p>%s</p>'
  '<span class="feat-btn">לקרוא עוד ←</span></div>'
  '<div class="feat-media" style="background-image:url(%s)"></div></a></section>') % (
    _feat["slug"], _feat["cat"], _feat["title"], _feat["excerpt"], _feat.get("img", BLOG_IMAGES[0]))
_rest = POSTS[1:]
grid_html = ""
if _rest:
    _cats = []
    for _q in _rest:
        if _q["cat"] not in _cats: _cats.append(_q["cat"])
    _filt = '<button class="bfilter active" data-cat="all">הכל</button>' + "".join('<button class="bfilter" data-cat="%s">%s</button>' % (c,c) for c in _cats)
    _cards = "".join(blog_card(_q) for _q in _rest)
    grid_html = ('  <section class="wrap"><div class="blog-filters">%s</div><hr class="blog-div"><div class="blog-cards" id="bgrid">%s</div></section>'
      '<script>document.querySelectorAll(".bfilter").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".bfilter").forEach(function(x){x.classList.remove("active");});b.classList.add("active");var c=b.dataset.cat;document.querySelectorAll("#bgrid .blog-card").forEach(function(w){w.style.display=(c==="all"||w.dataset.cat===c)?"":"none";});});});</script>') % (_filt, _cards)
blog_index_body = ('  <section class="wrap page-hero" style="padding-bottom:8px;"><span class="eyebrow"><span class="idx">//</span> <span class="ttl">בלוג</span></span>'
  '<div class="blog-head"><h1 class="s-head">הבלוג</h1>'
  '<p class="s-lead">תובנות מעשיות על פיתוח מוצר, אתרים, אוטומציה וסוכני AI – לעסקים, לעצמאים וליזמים.</p></div></section>'
  + featured_html + grid_html)
page("/blog","blog.html","בלוג · תובנות על פיתוח, אוטומציה וסוכני AI | מיכל בר",
     "תובנות מעשיות על פיתוח מוצר ואתרים, אוטומציה וסוכני AI, וייעוץ טכנולוגי – לעסקים, לעצמאים וליזמים.",
     [("דף הבית","/"),("בלוג",None)],
     blog_index_body + CTA,
     [{"@type":"Blog","name":"הבלוג של מיכל בר","url":SITE+"/blog"}])

# ============================================================
# ==================  ENGLISH (/en/) VERSION  ================
# ============================================================

CONTACT_GRID_EN = '''  <section class="wrap">
    <div class="contact-grid">
      <div class="contact-side">
        <a class="wa-circle" href="https://wa.me/972547105176" target="_blank" rel="noopener" aria-label="WhatsApp">
          <svg viewBox="0 0 32 32" fill="#fff" aria-hidden="true"><path d="M16.04 4C9.93 4 4.98 8.95 4.98 15.06c0 2.05.56 4.05 1.62 5.8L4 28l7.3-2.55a11.04 11.04 0 0 0 4.74 1.07h.01c6.11 0 11.06-4.95 11.06-11.06C27.1 8.95 22.15 4 16.04 4zm0 20.2c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-4.33 1.51 1.45-4.22-.2-.32a9.16 9.16 0 0 1-1.4-4.87c0-5.06 4.12-9.18 9.19-9.18 2.45 0 4.76.96 6.49 2.69a9.13 9.13 0 0 1 2.69 6.5c0 5.06-4.12 9.18-9.18 9.18zm5.04-6.87c-.28-.14-1.63-.8-1.88-.9-.25-.09-.43-.14-.61.14-.18.28-.7.9-.86 1.08-.16.18-.32.2-.6.07-.28-.14-1.17-.43-2.22-1.37-.82-.73-1.37-1.63-1.53-1.91-.16-.28-.02-.43.12-.57.13-.13.28-.32.42-.48.14-.16.18-.28.28-.46.09-.18.05-.35-.02-.49-.07-.14-.61-1.47-.84-2.01-.22-.53-.44-.46-.61-.46l-.52-.01c-.18 0-.46.07-.7.35-.25.28-.94.92-.94 2.24 0 1.32.96 2.6 1.1 2.78.14.18 1.9 2.9 4.6 4.06.64.28 1.14.44 1.53.57.64.2 1.23.18 1.69.11.52-.08 1.63-.66 1.86-1.31.23-.64.23-1.19.16-1.31-.07-.12-.25-.19-.53-.33z"/></svg>
        </a>
        <p class="wa-cta">Message me directly on WhatsApp</p>
        <a class="wa-phone" href="tel:+972547105176" dir="ltr">+972-54-710-5176</a>
        <p class="li-cta">Or connect with me on LinkedIn</p>
        <div class="social-row">
          <a href="https://www.linkedin.com/in/michal-bar-9100825b/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.4 8.65 21 11 21 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21H9z"/></svg></a>
        </div>
      </div>
      <form class="contact-form" id="contactForm" novalidate autocomplete="on">
        <h3>Leave your details</h3>
        <p class="form-sub">I'll get back to you within 24 hours</p>
        <div class="field"><label for="name">Name <span class="req">*</span></label>
          <input type="text" id="name" name="name" required maxlength="80" autocomplete="name" placeholder="What should I call you?" dir="ltr" /></div>
        <div class="field"><label for="phone">Phone <span class="req">*</span></label>
          <input type="tel" id="phone" name="phone" maxlength="20" autocomplete="tel" inputmode="tel" placeholder="+1 555 000 0000" dir="ltr" /></div>
        <div class="field"><label for="email">Email <span class="opt">(optional)</span></label>
          <input type="email" id="email" name="email" maxlength="120" autocomplete="email" inputmode="email" placeholder="name@example.com" dir="ltr" /></div>
        <div class="field"><label for="message">Message <span class="opt">(optional)</span></label>
          <textarea id="message" name="message" maxlength="2000" placeholder="Tell me what you're looking for - a challenge, an idea, a project..." dir="ltr"></textarea></div>
        <div class="hp-field" aria-hidden="true"><label for="website">Website</label>
          <input type="text" id="website" name="website" tabindex="-1" autocomplete="off" /></div>
        <button type="submit" class="btn1 form-submit">Send - and I'll be in touch</button>
        <p class="form-trust">Your details stay with me only · no spam</p>
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
      status.innerHTML='<div class="status-card"><div class="status-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 12 10 18 20 6"/></svg></div><h4>Thank you!</h4><p>Your message came through - I'll be in touch soon</p><button type="button" class="status-action">Send another message</button></div>';
      form.classList.add('is-done');
      var again=status.querySelector('.status-action');
      if(again){again.addEventListener('click',function(){form.classList.remove('is-done');status.className='form-status';status.innerHTML='';form.reset();});}}
    form.addEventListener('submit',function(e){e.preventDefault();
      if(form.website.value){return;}
      var name=(form.name.value||'').trim(),phone=(form.phone.value||'').trim(),email=(form.email.value||'').trim();
      if(name.length<2){msg('err','Please enter your name');return;}
      if(!phone){msg('err','Please enter a phone number');return;}
      var digits=phone.replace(/\\D/g,'');
      if(digits.length<7){msg('err','Please enter a valid phone number');return;}
      if(email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)){msg('err','Please enter a valid email address');return;}
      var orig=btn.textContent;btn.textContent='Sending…';btn.disabled=true;msg('','');
      emailjs.sendForm('service_y3jd01l','template_mo4oe7j',form)
        .then(function(){showDone();if(window.gtag)gtag('event','generate_lead',{method:'contact_form'});})
        .catch(function(err){console.error('EmailJS error:',err);msg('err','Something went wrong - please try again or message me on WhatsApp');})
        .finally(function(){btn.textContent=orig;btn.disabled=false;});
    });
  });
  </script>
'''

CTA_EN = '''  <section class="wrap page-hero" style="text-align:center;">
    <span class="eyebrow" style="justify-content:center;"><span class="idx">//</span> <span class="ttl">Contact</span></span>
    <h2 class="s-head" style="margin-inline:auto;">Have a challenge, an idea, or a project?</h2>
    <p class="s-lead" style="margin-inline:auto;">A free, no-obligation consultation - I'll get back to you within 24 hours.</p>
  </section>
''' + CONTACT_GRID_EN

# ---- /en/about ----
about_body_en = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">About</span></span>
    <h1 class="s-head">Hi, I'm Michal Bar</h1>
  </section>
  <section class="wrap">
    <div class="about-grid">
      <div class="portrait"><img src="/michal.jpg" alt="Michal Bar" /></div>
      <div>
        <p>At my core, I have a rare ability to understand complex situations - quickly and deeply. To pinpoint where the real problem is, why it's happening and the processes behind it, and from there to build the right path to improve things and create value.</p>
        <p>Alongside that, I have a rare product intuition: describe a problem to me, and I already see how the solution should look - and I can spec it quickly and precisely. Because the real difficulty was never the building - it's knowing <em>what</em> is right to build, and <em>how</em> it should look.</p>
        <p>I think creatively, so my solutions are precise, original and on point - the kind that move the needle. And because I'm deeply connected to design and aesthetics, the message and the look matter to me just as much as the content.</p>
        <p>Today, when anyone can build a product with AI in a few clicks, it's easy to end up with a generic result that looks like everyone else's and doesn't actually work for the business. What sets you apart is experience and business sense - the ability to build a product, website or automation that fits the need exactly, differentiates you, and delivers real value.</p>
        <p>More than 20 years in hi-tech and technology - from the technological unit of the IDF Intelligence Corps in the cyber field, through consulting and client management, to senior management roles at a cybersecurity startup, where I led the <span dir="ltr">Customer Success</span> and professional-services organization, with full responsibility for all clients and projects. Today I develop products, websites and systems, build automations and AI agents, and partner with businesses, independent professionals and entrepreneurs - from understanding the need to delivery.</p>
        <p class="about-note">And above all - a genuine connection with people, and listening to the need behind the words. Native-level English · strong presentation and communication skills.</p>
        <div class="sig">Michal Bar<small>Development · Automation · AI Agents</small></div>
      </div>
    </div>
    <div class="timeline">
      <div class="tl-head"><span class="tl-num">20+</span> years of experience <span class="sep">·</span> <span class="tl-num">100+</span> projects</div>
      <ol class="tl">
        <li><span class="tl-dot"></span><b>IDF Intelligence Corps</b><small>Technological unit · Cyber</small></li>
        <li><span class="tl-dot"></span><b>Consulting & client management</b><small>Cybersecurity</small></li>
        <li><span class="tl-dot"></span><b>Senior management at a startup</b><small><span dir="ltr">Customer Success</span> · Cyber</small></li>
        <li><span class="tl-dot tl-now"></span><b>Today</b><small>Development, automation & AI agents for businesses and independents</small></li>
      </ol>
    </div>
  </section>
  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">Testimonials</span></span>
    <h2 class="s-head">What people say</h2>
    <div class="quotes">
      <div class="quote"><div class="stars">★★★★★</div><p>"Michal built us a tool that saved hundreds of work hours and streamlined a whole process, with a simple, intuitive and efficient interface. Working with Michal is a win - she fully grasps the business need and then some, drives fast, high-quality progress with real commitment, and delivered a solution far better than I expected."</p><div class="who"><div class="av">L</div><div><b>Liat Plaksin</b><small dir="ltr">Co-founder · FaaS</small></div></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"Michal has a rare ability to take a project from A to Z - and fast. She deeply understands the needs, spots what's still missing, and above all knows how to separate the essential from the noise and build an excellent project with everything it needs and without over-complicating. Beyond the high level of professionalism, what really stood out was the human touch and availability - always attentive, accessible and there for every question. Service and support on a whole other level."</p><div class="who"><div class="av">I</div><div><b>Iris Shoor</b><small>Serial entrepreneur · former head of LinkedIn's Tel Aviv R&D center</small></div></div></div>
      <div class="quote"><div class="stars">★★★★★</div><p>"Michal has the rare ability to connect business understanding with technology, and that's exactly what we were looking for. She spec'd and built us a solution with precise messaging, creativity and a real answer to the need - beyond expectations."</p><div class="who"><div class="av">A</div><div><b>Alon</b><small>CEO</small></div></div></div>
    </div>
  </section>
'''
page("/about","about.html",
     "About · Michal Bar - Technology Consultant & Developer",
     "20+ years in hi-tech and cybersecurity - from the IDF Intelligence Corps to senior startup management. Today I build products, websites and systems, automations and AI agents for businesses, independent professionals and entrepreneurs - from understanding the need to delivery.",
     [("Home","/"),("About",None)],
     about_body_en + CTA_EN,
     [{"@id":BIZ+"-michal","@type":"Person","name":"Michal Bar","url":SITE+"/en/about",
       "jobTitle":"Technology Solutions Developer & Consultant",
       "description":"20+ years in hi-tech and cybersecurity. Develops products, websites and systems, builds automations and AI agents, and works with businesses, independent professionals and entrepreneurs.",
       "knowsAbout":["Product development","Web development","App development","Business automation","AI agents","Technology consulting"]}],
     lang="en")

# ---- English service list (related-services cross-links) ----
SERVICES_EN = [
    ("/services/product-development", "Product, Web & App Development"),
    ("/services/automation", "Automation & AI Agents"),
    ("/services/consulting", "Tech Consulting"),
]

# ---- /en/services (hub) ----
svc_cards_en = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">Services</span></span>
    <h1 class="s-head">Development, automation & AI agents - end to end</h1>
    <p class="s-lead">Combining strategy, precise spec, development, automation and AI agents with personal guidance from start to result. Three service areas, one approach: understand the root need and build the right solution.</p>
    <div class="prose" style="max-width:72ch;margin-top:14px;">
      <p>The services are for businesses, independent professionals, entrepreneurs and startups - and you can start from any point: <a href="/en/services/product-development">product, web & app development</a>, <a href="/en/services/automation">automation & AI agents</a>, or <a href="/en/services/consulting">tech consulting</a>. 20+ years in hi-tech and a sharp product intuition <a href="/en/about">accompany every project</a>, from understanding the need to delivery.</p>
    </div>
  </section>
  <section class="wrap">
    <div class="cards">
      <a class="card" href="/en/services/product-development">
        <div class="ic mono">&lt;/&gt;</div>
        <h3>Product, Web & App Development</h3>
        <p>From an initial spec to a live product - end-to-end design and development of products, systems, websites and apps.</p>
        <ul><li>Websites & web systems</li><li>Apps</li><li>MVP & full development</li></ul>
        <span class="go">Details &#8594;</span>
      </a>
      <a class="card" href="/en/services/automation">
        <div class="ic">⚙</div>
        <h3>Automation & AI Agents</h3>
        <p>Manual processes that become automatic - with AI agents that save work hours and work for your business.</p>
        <ul><li>Business automation</li><li>AI agents</li><li>System & API integration</li></ul>
        <span class="go">Details &#8594;</span>
      </a>
      <a class="card" href="/en/services/consulting">
        <div class="ic">◆</div>
        <h3>Tech Consulting</h3>
        <p>Understand what's really worth building and how to prioritize - need mapping, strategy and a precise solution spec.</p>
        <ul><li>Mapping needs & pains</li><li>Technology strategy</li><li>Decision guidance</li></ul>
        <span class="go">Details &#8594;</span>
      </a>
    </div>
  </section>
  <section class="wrap">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">The process</span></span>
    <h2 class="s-head">A simple, transparent process - no surprises</h2>
    <div class="steps">
      <div class="step"><b class="n">01</b><h4>Intro call</h4><p>We understand the need, the goals and the challenges</p></div>
      <div class="step"><b class="n">02</b><h4>Spec & planning</h4><p>We build a spec and a tailored solution</p></div>
      <div class="step"><b class="n">03</b><h4>Development & implementation</h4><p>We execute, with ongoing updates and transparency</p></div>
      <div class="step"><b class="n">04</b><h4>Launch & tuning</h4><p>We go live and refine until you're fully satisfied</p></div>
      <div class="step"><b class="n">05</b><h4>Ongoing support</h4><p>Optional - maintenance, improvements and continued development, as a monthly package as needed</p></div>
    </div>
  </section>
'''
faq_html_en, faq_s_en = faq_block([
    ("Who do you work with?", "Businesses, entrepreneurs and organizations that need to translate a need into a technological solution - from early-stage startups to established companies."),
    ("How long does a project take?", "It depends on scope. A short spec can take weeks, and a full product - months. I'm extremely hard-working and fast - but without compromising on quality. After the intro call and spec we can give a precise timeline."),
    ("How do you price?", "By the scope and nature of the project. After a short intro call you'll get a clear quote, broken into milestones."),
    ("How fast do I get a quote?", "After a short intro call (and sometimes a brief spec) you'll get a clear quote broken into milestones - usually within a few days."),
    ("Can we work remotely / from anywhere?", "Yes. I work with clients everywhere, and most of the process runs remotely - calls, spec and ongoing updates online, with in-person meetings as needed."),
])
page("/services","services.html",
     "Services · Development, Automation & AI Agents | Michal Bar",
     "Three service areas - product, web & app development; automation & AI agents; and tech consulting. End to end, with personal guidance.",
     [("Home","/"),("Services",None)],
     svc_cards_en + faq_html_en + CTA_EN,
     [{"@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":1,"url":SITE+"/en/services/product-development","name":"Product, Web & App Development"},
        {"@type":"ListItem","position":2,"url":SITE+"/en/services/automation","name":"Automation & AI Agents"},
        {"@type":"ListItem","position":3,"url":SITE+"/en/services/consulting","name":"Tech Consulting"}]}, faq_s_en],
     lang="en")

service_page("/services/product-development","services/product-development.html",
    "Digital Product & MVP Development for Businesses | Michal Bar",
    "Spec, design and development of products, systems, websites and apps - from idea to MVP to a full product, end to end.",
    "Product, Web & App Development",
    "From idea to MVP to a full product - spec, design and development end to end, with the focus on what's right to build and how it should look.",
    ["The real difficulty in building a product was never the building itself - it's knowing <strong>what</strong> is actually right to build for your business, and <strong>how</strong> it should work and look. I translate a business need into a product: from a sharp, precise spec, through UX design, to full development and launch.",
     "Today the market is flooded with solutions built fast and cheap with AI tools - with no experience and no business thinking. The result is almost always generic: a product that looks like everyone else's, with no differentiation and none of what actually makes it work for your business. <strong>That's the difference with me</strong> - 20+ years of hi-tech experience and a deep business perspective, producing a product tailored exactly to you, that sets you apart and delivers real value - not another template.",
     "And you're a partner the whole way: I build the full product, but keep you in the loop as we go - showing you the product as it takes shape, aligning and moving forward together, so what goes live is exactly what's needed, with no surprises."],
    ["Product spec grounded in business thinking","UX/UI design","Website & app development - with the right messaging and differentiation","Internal systems & CRM tailored exactly to your business","Payment flows, admin panels and dashboards","End-to-end full-stack development","MVP - a focused first version built around the need","Guidance and collaboration throughout"],
    ["Independents and businesses that want to grow fast and build right","Anyone who needs a system, internal tool or website that truly works for them","Anyone with a product who needs to expand or improve it","Anyone who got a generic or cheap product - and wants something that actually works and sets them apart","Startups that need a focused, precise MVP","Entrepreneurs with an idea that needs to become a product"],
    [("How much does it cost to build an MVP?","The cost depends on the scope of features. A focused MVP costs significantly less than a full product - and together we define the right scope to deliver value fast. After a spec, you'll get a precise quote broken into milestones."),
     ("How do you choose a developer or dev shop? What should you check?","Beyond price, check four things: (1) real experience and track record - not just writing code, but understanding what's right to build; (2) business perspective - that they understand your need and don't just follow instructions; (3) security - that the product is built secure from the ground up and not exposed to attack; (4) end-to-end support - spec, design, development and launch in one place. That exact combination - 20+ years in hi-tech and cybersecurity, a product mindset and personal guidance - is my advantage over generic, cheap builds."),
     ("A business website - what really matters beyond how it looks?","A pretty website isn't enough - a website needs to work and convert. I build with a product mindset: the right messaging that speaks precisely to your customer, a flow that leads the visitor step by step to an action (a lead, an inquiry or a purchase), and a design sense that conveys the professionalism that builds trust - plus security, so the site is built safe from the ground up (from my background in cybersecurity). The result isn't just another website - it's a tool that brings in customers."),
     ("Is the website you build secure? And how much does it matter?","A lot - and it's exactly what fast, cheap websites miss. A system built without security is exposed to attack, and if sensitive customer or payment details leak, the business faces lawsuits and serious reputational damage. From my background in cybersecurity - the IDF Intelligence Corps technological unit and a cyber startup - security is built in from the ground up, not bolted on afterward."),
     ("How long does it take to build a product?","MVP: usually a few weeks to a few months. Full product: depends on scope. I'm extremely hard-working and fast - but without compromising on quality. A precise timeline is set after the spec."),
     ("What technologies do you work with?","We choose the tools based on the product's needs - full-stack development for websites, apps and systems. The technology serves the product, not the other way around."),
     ("What's the difference between an MVP and a full product?","An MVP is a focused first version: a complete, polished product that includes exactly what's needed to go to market and prove value, without unnecessary features. A full product is broader in scope - and in both cases I build the full product and keep you involved throughout.")],
    "Product, Web & App Development",
    "Spec, design and development of products, websites and apps end to end - from MVP to a full product.",
    lang="en")

service_page("/services/consulting","services/consulting.html",
    "Technology Consulting & Product Spec for Businesses | Michal Bar",
    "Consulting that connects business and technology - mapping the root need, strategy, and precise solution planning before you build.",
    "Tech Consulting",
    "I connect business understanding with technology - identifying where the real problem is and building the right way to solve it, before a single line of code is written.",
    ["Many projects fail not because of the development, but because the wrong thing was built. Good consulting prevents that: a precise mapping of the need and the pain, an understanding of the business and the users, and a solution and strategy - all the way to an informed decision and a clear action plan.",
     "My advantage is a rare combination of three worlds - the client, the business and the technology. I can identify the real need, understand what's technically possible, and prioritize correctly to deliver value fast."],
    ["Mapping needs, pains and opportunities","Understanding the business and the users","Detailed product/system spec","Strategy and process design","Solution planning and prioritization","Guiding technology decisions"],
    ["Independents and businesses unsure what exactly to build","Anyone weighing a tech project who needs direction","Anyone who wants to make sure they build the right thing - before investing in development","Organizations that want to streamline an existing process or product","Entrepreneurs who need to prioritize and focus"],
    [("What does a consulting process include?","Mapping the need and the pain, understanding the business and the users, and forming a solution and strategy - all the way to an informed decision and an action plan."),
     ("When should you get consulting instead of going straight to development?","When you're not sure what exactly to build, how to prioritize, or which approach is right. Good consulting saves unnecessary development and a lot of money."),
     ("How long does a consulting process take?","It depends on scope - from a single focused conversation to a process of several weeks. We'll define the right scope together in the intro call.")],
    "Tech Consulting",
    "Consulting that connects business and technology - need mapping, strategy and a precise solution spec.",
    lang="en")

service_page("/services/automation","services/automation.html",
    "Business Automation & AI Agents for Businesses | Michal Bar",
    "Automating business processes with AI agents - connecting systems and tools so repetitive manual tasks happen on their own and save hours of work.",
    "Automation & AI Agents",
    "Manual processes that become automatic - connecting your tools and systems, with AI agents that do the repetitive work for you.",
    ["Every hour you or your team spend on repetitive manual tasks is an hour you can get back. But good automation isn't just 'connecting systems' - it starts with understanding the existing process, continues by streamlining it, and only then implements a technological solution that runs it automatically in the most efficient way for the business - with no mistakes and no wasted time.",
     "Today you can go even further: <strong>AI agents</strong> that understand context, make simple decisions and carry out whole tasks - answering inquiries, classifying and routing information, summarizing and producing content - rather than just running fixed rules.",
     "We start with mapping: where the most manual time is burned, and where the big opportunities are. From there we build focused automations and AI agents that plug into the tools you already use."],
    ["End-to-end business process automation","AI agents for tasks and processes","Chatbots and smart assistants for your business","Connecting tools and systems (integrations & APIs)","Automated reports, forms and updates","Process mapping and spotting opportunities to save"],
    ["Independents and businesses burning time on repetitive manual work","Teams working across several systems that don't talk to each other","Anyone who wants to bring AI agents into their work - but doesn't know where to start","Businesses and independents that want to grow without growing headcount"],
    [("What is business automation?","Business automation starts with understanding your existing processes and how they run, continues by streamlining them as much as possible, and ends by implementing a technological solution that runs them automatically - in the most efficient way for the business. It's not just connecting systems, but rethinking the process itself."),
     ("What are AI agents and how do they help a business?","AI agents are smart assistants that understand context and carry out whole tasks for you - answering inquiries, classifying and routing information, summarizing, producing content and more. Unlike automation that runs fixed rules, an AI agent can handle unexpected situations too."),
     ("What's the difference between automation and an AI agent?","Automation runs fixed rules ('if X then Y') and is great for clear, repetitive processes. An AI agent is a step further: it understands context, makes decisions and handles unexpected situations too. In practice you combine the two - automation for what's fixed, AI agents for what requires understanding."),
     ("What can be automated?","Almost any repetitive process: moving data between systems, sending emails and updates, generating reports, forms, billing and more - and with AI, tasks that require understanding and judgment too."),
     ("What tools do you use for automation?","We choose the tool based on the need - from leading automation tools (like Make/Zapier) to custom development and API integrations when something unique is required. The tool serves the process, not the other way around."),
     ("Will AI replace the need for an expert?","No. AI is a powerful tool - but it makes mistakes and doesn't know what's right for your business. The real value is in the combination: someone with experience and business perspective who knows what to build, how to bring in AI correctly, and when not to. The tool saves time; the decisions and the differentiation stay human."),
     ("How much time do you save?","It depends on the process - clients have saved hundreds of work hours a year. After mapping, we'll know where the biggest opportunities are.")],
    "Automation & AI Agents",
    "Automating business processes with AI agents - connecting systems and streamlining to save hours of work.",
    lang="en")

# ---- /en/projects ----
projects_body_en = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">Projects</span></span>
    <h1 class="s-head">Selected projects</h1>
    <p class="s-lead" style="max-width:none;">Each one built from understanding the business need - products, websites and systems that truly work.</p>
  </section>
  <section class="wrap">
    <div class="proj">
      <div class="pcard">
        <div class="thumb"><img src="/proj-deskday.jpg" alt="deskday - workspace marketplace" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">Product</span><span class="tag">Spec</span><span class="tag">Design</span><span class="tag">Development</span><span class="tag" dir="ltr">Full-Stack</span></div>
          <h4>Workspace marketplace</h4>
          <p>An end-to-end marketplace for renting daily workspaces: search spaces by location and date, space pages with photos and favorites, separate interfaces for space owners and renters, and a full payments system - billing, receipts and invoices, an admin dashboard and messaging. An independent product I spec'd, designed and built.</p>
        </div>
      </div>
      <a class="pcard" href="https://makombateva.com" target="_blank" rel="noopener">
        <div class="thumb"><img src="/proj-makombateva.jpg" alt="Makom BaTeva - brand website" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">Spec</span><span class="tag">Design</span><span class="tag">Development</span><span class="tag">Brand site</span></div>
          <h4>Makom BaTeva</h4>
          <p>A full brand website for a nature-hospitality business - spec, design and end-to-end development: landing page, photo and video gallery, a secure guest-guide page and a smart inquiry form.</p>
          <span class="visit">Visit site ↗</span>
        </div>
      </a>
      <div class="pcard">
        <div class="thumb"><img src="/proj-instagram.jpg" alt="Instagram content analytics system" loading="lazy"></div>
        <div class="body">
          <div class="tags"><span class="tag">Product</span><span class="tag">Spec</span><span class="tag">Development</span><span class="tag" dir="ltr">Data Analytics</span><span class="tag" dir="ltr">AI</span></div>
          <h4>Instagram content analytics</h4>
          <p>A system for analyzing Instagram content performance - you define accounts to analyze, and the system collects deep data from every post (reach, engagement, content type and more), analyzes it and produces insights: which posts work, why, and what to improve to reach better performance. <strong>The result:</strong> hundreds of manual work hours saved each month, and insights manual analysis couldn't reach - which brought the business many new sales.</p>
        </div>
      </div>
    </div>
  </section>
'''
page("/projects","projects.html",
     "Selected Projects | Michal Bar",
     "Selected projects I spec'd, designed and built - a workspace marketplace, a brand website for Makom BaTeva, and an Instagram content-analytics system.",
     [("Home","/"),("Projects",None)],
     projects_body_en + CTA_EN, [], lang="en")

# ---- /en/contact ----
contact_body_en = '''  <section class="wrap page-hero" style="text-align:center;">
    <span class="eyebrow" style="justify-content:center;"><span class="idx">//</span> <span class="ttl">Contact</span></span>
    <h1 class="s-head" style="margin-inline:auto;">Have a challenge, an idea, or a project?</h1>
    <p class="s-lead" style="margin-inline:auto;">A free, no-obligation consultation - I'll get back to you within 24 hours.</p>
  </section>
''' + CONTACT_GRID_EN
page("/contact","contact.html",
     "Contact | Michal Bar · Technology Solutions",
     "Let's talk - a no-obligation intro call. WhatsApp, phone, LinkedIn or the form. I'll get back to you within 24 hours.",
     [("Home","/"),("Contact",None)],
     contact_body_en,
     [{"@type":"ContactPage","name":"Contact · Michal Bar","url":SITE+"/en/contact"}],
     lang="en")

# ---- /en/privacy ----
privacy_body_en = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">Legal</span></span>
    <h1 class="s-head">Privacy Policy</h1>
    <p class="s-lead">Last updated: September 2026</p>
  </section>
  <section class="wrap"><div class="prose">
    <p>I, Michal Bar ("I"/"the site"), respect your privacy. This policy explains what information is collected on michalbartech.com, how it is used, and what your rights are.</p>
    <h2>What information is collected</h2>
    <ul>
      <li><strong>Information you provide voluntarily</strong> - when filling out the contact form: name, phone, email and the content of your message.</li>
      <li><strong>Anonymous statistical information</strong> - usage and traffic data collected via Google Analytics (pages viewed, referral source, device type, etc.), without personal identification.</li>
    </ul>
    <p>Providing details in the form is <strong>voluntary and not required by law</strong> - but without them I won't be able to get back to you. The details are used only for the purposes described below.</p>
    <h2>How the information is used</h2>
    <ul>
      <li>To get in touch and respond to inquiries.</li>
      <li>To improve the site and understand how it is used.</li>
    </ul>
    <h2>Third-party services</h2>
    <p>The site uses external services to operate: <strong>Google Analytics</strong> (traffic analytics), <strong>EmailJS</strong> (delivering form inquiries to my inbox), and <strong>Vercel</strong> (site hosting). Each has its own privacy policy.</p>
    <h2>Cookies</h2>
    <p>The site may use cookies for statistical and operational purposes. You can block cookies in your browser settings.</p>
    <h2>Data retention and security</h2>
    <p>Information is kept for as long as it is needed for the purposes for which it was collected, and is secured by reasonable means. Form inquiries are stored in my email inbox.</p>
    <h2>Your rights</h2>
    <p>You may contact me at any time to review the information collected about you, correct it or delete it, via <a href="/en/contact">Contact</a> or by email at barmichal100@gmail.com.</p>
    <h2>Changes to this policy</h2>
    <p>This policy may be updated from time to time. The updated date will appear at the top of the page.</p>
  </div></section>
'''
page("/privacy","privacy.html",
     "Privacy Policy | Michal Bar",
     "The privacy policy for michalbartech.com - what information is collected, how it is used, and what your rights are.",
     [("Home","/"),("Privacy Policy",None)],
     privacy_body_en, [], lang="en")

# ---- /en/accessibility ----
access_body_en = '''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">Accessibility</span></span>
    <h1 class="s-head">Accessibility Statement</h1>
    <p class="s-lead">Last updated: September 2026</p>
  </section>
  <section class="wrap"><div class="prose">
    <p>I place great importance on providing an equal, accessible service to all visitors, including people with disabilities. This site was built in an effort to conform to accepted accessibility guidelines.</p>
    <h2>The site's accessibility level</h2>
    <p>The site was built in line with the <span dir="ltr">WCAG 2.0</span> guidelines at level AA, as far as possible. Among other things:</p>
    <ul>
      <li>A valid, semantic structure that enables screen-reader navigation.</li>
      <li>Sufficient color contrast between text and background.</li>
      <li>Alternative text for meaningful images.</li>
      <li>Keyboard navigation and browsing.</li>
      <li>Support for browser text enlargement.</li>
    </ul>
    <h2>Reservation</h2>
    <p>Some parts of the site may not yet be fully accessible, or a component that isn't accessible enough may be found. I work to continuously improve the site's accessibility.</p>
    <h2>Accessibility contact</h2>
    <p>The site's accessibility coordinator is <strong>Michal Bar</strong>. Ran into an accessibility problem or difficulty? I'd be glad to hear and fix it - you can reach me:</p>
    <ul>
      <li>Email: <a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=barmichal100@gmail.com&amp;su=Accessibility+-+michalbartech" target="_blank" rel="noopener">barmichal100@gmail.com</a></li>
      <li>Phone: <a href="tel:+972547105176" dir="ltr">+972-54-710-5176</a></li>
    </ul>
    <p>I'll do my best to handle your inquiry as soon as possible.</p>
  </div></section>
'''
page("/accessibility","accessibility.html",
     "Accessibility Statement | Michal Bar",
     "The accessibility statement for michalbartech.com - the accessibility level, the adjustments made, and how to get in touch about accessibility.",
     [("Home","/"),("Accessibility",None)],
     access_body_en, [], lang="en")

# ---- /en/faq ----
faq_groups_en = [
    ("General", [
        ("Why build with you instead of just building it myself with AI, or cheaply?", "Today anyone can build something with a few AI prompts - but you usually get a generic product that looks like everyone else's and doesn't really work for the business. The difference is experience and business perspective: 20+ years in hi-tech, an understanding of what actually needs to be built and how, and a product tailored exactly to you that sets you apart and delivers real value - not another template."),
        ("Who do you work with?", "Businesses, entrepreneurs and organizations that need to translate a need into a technological solution - from early-stage startups to established companies."),
        ("Can we work remotely / from anywhere?", "Yes. I work with clients everywhere, and most of the process runs remotely - calls, spec and ongoing updates online, with in-person meetings as needed."),
        ("How long does a project take?", "It depends on scope. A short spec can take weeks, and a full product - months. I'm extremely hard-working and fast - but without compromising on quality. After the intro call and spec we can give a precise timeline."),
        ("How do you price?", "By the scope and nature of the project. After a short intro call you'll get a clear quote, broken into milestones."),
        ("What happens after launch? Is there support?", "I don't disappear after go-live. Ongoing support and guidance is available - maintenance, improvements and continued development - as a monthly package as needed."),
        ("How do we start working together?", "Simple: a short, no-obligation intro call. We understand the need and the goals, and if it's a fit - you get a spec and a clear quote. You can reach out via the form, WhatsApp or phone."),
    ]),
    ("Product development", [
        ("How much does it cost to build a website or an app?", "The cost depends on scope and complexity - a brand website, a system or a full app are completely different ranges. Instead of 'the cheapest', I focus on 'the most right': a well-built product that pays back the investment. After a short intro call you'll get a clear quote, broken into milestones - no surprises."),
        ("How much does it cost to build an MVP?", "The cost depends on the scope of features. A focused MVP costs significantly less than a full product - and together we define the right scope to deliver value fast. After a spec you'll get a precise quote broken into milestones."),
        ("How do you choose a developer or dev shop? What should you check?", "Beyond price, check four things: (1) real experience and track record - not just writing code, but understanding what's right to build; (2) business perspective - that they understand your need and don't just follow instructions; (3) security - that the product is built secure from the ground up and not exposed to attack; (4) end-to-end support - spec, design, development and launch in one place. That exact combination - 20+ years in hi-tech and cybersecurity, a product mindset and personal guidance - is my advantage over generic, cheap builds."),
        ("A business website - what really matters beyond how it looks?", "A pretty website isn't enough - a website needs to work and convert. I build with a product mindset: the right messaging that speaks precisely to your customer, a flow that leads the visitor step by step to an action (a lead, an inquiry or a purchase), and a design sense that conveys the professionalism that builds trust - plus security, so the site is built safe from the ground up (from my background in cybersecurity). The result isn't just another website - it's a tool that brings in customers."),
        ("Is the website you build secure? And how much does it matter?", "A lot - and it's exactly what fast, cheap websites miss. A system built without security is exposed to attack, and if sensitive customer or payment details leak, the business faces lawsuits and serious reputational damage. From my background in cybersecurity - the IDF Intelligence Corps technological unit and a cyber startup - security is built in from the ground up, not bolted on afterward."),
        ("How long does it take to build a product?", "MVP: usually a few weeks to a few months. Full product: depends on scope. I'm extremely hard-working and fast - but without compromising on quality. A precise timeline is set after the spec."),
        ("What technologies do you work with?", "We choose the tools based on the product's needs - full-stack development for websites, apps and systems. The technology serves the product, not the other way around."),
        ("What's the difference between an MVP and a full product?", "An MVP is a focused first version: a complete, polished product that includes exactly what's needed to go to market and prove value, without unnecessary features. A full product is broader in scope - and in both cases I build the full product and keep you involved throughout."),
    ]),
    ("Consulting", [
        ("What does a consulting process include?", "Mapping the need and the pain, understanding the business and the users, and forming a solution and strategy - all the way to an informed decision and an action plan."),
        ("When should you get consulting instead of going straight to development?", "When you're not sure what exactly to build, how to prioritize, or which approach is right. Good consulting saves unnecessary development and a lot of money."),
        ("How long does a consulting process take?", "It depends on scope - from a single focused conversation to a process of several weeks. We'll define the right scope together in the intro call."),
    ]),
    ("Automation & AI Agents", [
        ("What is business automation?", "Business automation starts with understanding your existing processes and how they run, continues by streamlining them as much as possible, and ends by implementing a technological solution that runs them automatically - in the most efficient way for the business. It's not just connecting systems, but rethinking the process itself."),
        ("What are AI agents and how do they help a business?", "AI agents are smart assistants that understand context and carry out whole tasks for you - answering inquiries, classifying and routing information, summarizing, producing content and more. Unlike automation that runs fixed rules, an AI agent can handle unexpected situations too."),
        ("What's the difference between automation and an AI agent?", "Automation runs fixed rules ('if X then Y') and is great for clear, repetitive processes. An AI agent is a step further: it understands context, makes decisions and handles unexpected situations too. In practice you combine the two - automation for what's fixed, AI agents for what requires understanding."),
        ("What can be automated?", "Almost any repetitive process: moving data between systems, sending emails and updates, generating reports, forms, billing and more - and with AI, tasks that require understanding and judgment too."),
        ("What tools do you use for automation?", "We choose the tool based on the need - from leading automation tools (like Make/Zapier) to custom development and API integrations when something unique is required. The tool serves the process, not the other way around."),
        ("Will AI replace the need for an expert?", "No. AI is a powerful tool - but it makes mistakes and doesn't know what's right for your business. The real value is in the combination: someone with experience and business perspective who knows what to build, how to bring in AI correctly, and when not to. The tool saves time; the decisions and the differentiation stay human."),
        ("How much time do you save?", "It depends on the process - clients have saved hundreds of work hours a year. After mapping, we'll know where the biggest opportunities are."),
    ]),
]
faq_all_en = []
faq_sections_en = ['''  <section class="wrap page-hero">
    <span class="eyebrow"><span class="idx">//</span> <span class="ttl">FAQ</span></span>
    <h1 class="s-head">Frequently asked questions</h1>
    <p class="s-lead">Everything worth knowing before you start - services, timelines, pricing and how we work. Didn't find an answer? <a href="/en/contact" style="color:var(--accent);">Talk to me</a>.</p>
  </section>''']
for gtitle, pairs in faq_groups_en:
    faq_all_en += pairs
    rows = "\n".join('      <details><summary>%s</summary><p class="a">%s</p></details>' % (q,a) for q,a in pairs)
    faq_sections_en.append('''  <section class="wrap">
    <h2 class="s-head" style="font-size:clamp(24px,3.4vw,32px);">%s</h2>
    <div class="faq">
%s
    </div>
  </section>''' % (gtitle, rows))
faq_schema_en = {"@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_all_en]}
page("/faq","faq.html",
     "FAQ | Michal Bar · Technology Solutions",
     "Answers to the common questions about product development, tech consulting and automation - timelines, pricing, MVP and how we work.",
     [("Home","/"),("FAQ",None)],
     "\n".join(faq_sections_en) + CTA_EN,
     [faq_schema_en], lang="en")

# ---- English blog ----
POSTS_EN = [
  {
    "slug":"cost-to-develop-website-or-app",
    "title":"How much does it cost to build a website or app - and where to start",
    "desc":"How much does it cost to build a website, system or app? What determines the price, how to start right, and why 'cheap' usually costs more - a guide for businesses, independents and entrepreneurs.",
    "cat":"Product development","date":"2026-09-23","modified":"2026-09-23","read":"7 min read",
    "excerpt":"There's no single price for development - there's a range set by scope, complexity, design and security. How to understand the cost, where to start, and why cheap usually costs more.",
    "takeaways":[
      "There's no 'single price' - cost is set by scope, complexity, design, integrations and security.",
      "A brand site, a system and an app are completely different ranges - start by defining the need, not the price.",
      "A focused MVP lowers cost and risk and gets you to market fast.",
      "'Cheap' usually costs more: a generic product with no business thinking and no security exposes you to rework, lawsuits and reputational damage.",
    ],
    "sections":[
      ("Why there's no 'single price' for development", '<p>One of the first questions any business asks is "how much will it cost?" - and it\'s a fair question. But unlike an off-the-shelf product, development isn\'t one item at a fixed price: it\'s built precisely around your need. A brand website, an internal management system, and an app with users and payments are three completely different worlds - so their price ranges differ completely too. Instead of hunting for "the price", it\'s better to understand <strong>what drives it</strong> and how to get the most value out of every dollar.</p>'),
      ("What determines the cost", '<p>A few key factors determine the scope of work - and therefore the cost:</p><ul><li><strong>Scope and complexity</strong> - how many screens, processes and users, and how "smart" the logic behind the scenes.</li><li><strong>Design and UX</strong> - a custom, polished design vs. a generic template.</li><li><strong>Integrations</strong> - connecting to payment systems, a CRM, external tools and APIs.</li><li><strong>Security</strong> - critical when there are customer details or payments. Proper security is built in from the ground up, not added at the end.</li><li><strong>Maintenance and continuity</strong> - a live product needs ongoing support and improvements.</li></ul>'),
      ("A brand site, a system, or an app?", '<p>Before talking price, it helps to define what you actually need. A <strong>brand website</strong> presents the business and brings in inquiries - a relatively focused project. An <strong>internal system</strong> (like a CRM or a management tool) is built around a workflow and saves valuable time. An <strong>app or product with users</strong> is the broadest world - accounts, payments and ongoing management. The more the product does, the more it requires - and that\'s fine; the point is to match the investment to what will really move the business. <a href="/en/services/product-development">This is how I build products, websites and systems</a>.</p>'),
      ("Where to start, the right way", '<p>The right start isn\'t code - it\'s a <strong>spec</strong>. You define the real business need, who the users are, and what must be in the first version. A good approach is an <strong>MVP</strong> - a focused first version that includes exactly what\'s needed to go to market and prove value, without unnecessary features that inflate cost and time. From there you expand based on what actually works. <a href="/en/services/consulting">Consulting and a spec</a> at the start save a lot of money later - because you build the right thing the first time.</p>'),
      ("Why 'cheap' usually costs more", '<p>Today it\'s easier than ever to build something fast and cheap - with ready-made templates or AI tools. The problem: you usually get a <strong>generic</strong> product that looks like everyone else\'s, with no business thinking to actually make it work, and <strong>no security</strong>. An unsecured system is exposed to attack - and if customer or payment details leak, the business is exposed to <strong>lawsuits</strong> and serious reputational damage. That kind of "cheap" usually ends in a rebuild. A product built right - with a product mindset and security from the ground up - costs more upfront, but pays back the investment and doesn\'t blow up in your face.</p>'),
      ("Summary", '<p>There\'s no single answer to "how much does it cost" - but there is a right way: define the need, start focused, and choose someone who builds with experience, business sense and security. Have an idea or a need? <a href="/en/contact">Talk to me</a> for a short intro call, and we\'ll figure out together what\'s right to build and at what scope.</p>'),
    ],
    "faq":[
      ("How much does a brand website cost vs. an app?","These are two different worlds: a brand website is a relatively focused project, and an app with users and payments is a much broader scope. The range is set by what the product needs to do - so we define the need first, then give a precise quote."),
      ("What is an MVP and how much does it save?","An MVP is a focused first version that includes exactly what's needed to go to market and prove value. It lowers cost and risk, shortens time, and lets you learn from the market before a big investment."),
      ("Why does cheap development cost more?","Because you usually get a generic product, with no business thinking and no security. An unsecured product exposes the business to lawsuits and reputational damage, and a generic product usually gets thrown out and rebuilt - which costs far more in the end."),
    ],
  },
  {
    "slug":"automation-and-ai-agents-getting-started",
    "title":"Business automation and AI agents - where to start",
    "desc":"Business automation and AI agents for small businesses: the difference between them, where to start, what can be automated, and how to do it right without gimmicks.",
    "cat":"Automation & AI Agents","date":"2026-09-21","modified":"2026-09-21","read":"6 min read",
    "excerpt":"Automation and AI agents can save a business hundreds of hours - if you start in the right place. What the difference is, where to start, and how not to fall for gimmicks.",
    "takeaways":[
      "Automation runs fixed rules; an AI agent understands context and makes decisions - and you combine them.",
      "Start with mapping: where the most manual time is burned, not with 'where to push AI'.",
      "The value is in identifying the right processes to automate - with business sense, not a gimmick.",
    ],
    "sections":[
      ("Business automation - why now is the time to start", '<p>Almost every business wastes hours on repetitive manual tasks - moving data between systems, emails, reports and forms. Today, with automation and AI agents, you can get those hours back. The tools are mature and the prices are accessible - but success depends less on the technology and more on <strong>choosing the right thing to automate</strong>.</p>'),
      ("Automation vs. AI agents - what's the difference", '<p><strong>Automation</strong> runs fixed rules: "if X happens, do Y." It\'s great for clear, repetitive processes. An <strong>AI agent</strong> is a step further - it understands context, makes decisions and handles unexpected situations too: answering inquiries, classifying and routing information, summarizing and producing content. In practice you <a href="/en/services/automation">combine the two</a> - automation for what\'s fixed, AI agents for what requires understanding.</p>'),
      ("Where to start - mapping before anything", '<p>The common mistake is to start with "let\'s add AI." The right start is the opposite: <strong>mapping</strong>. You list the repetitive tasks, identify where the most time is burned and where the most mistakes happen - and from there you pick the highest-value opportunities. Automating the wrong process just wastes time; automating the real bottleneck changes the business.</p>'),
      ("What can be automated", '<p>Almost any repetitive process: syncing data between systems, sending emails and updates, generating reports, forms and billing, first-line customer responses, and classifying and routing leads. With AI agents you add tasks that require understanding and judgment too - summarizing calls, smart responses to inquiries, or producing first-draft content.</p>'),
      ("How to do it right (and not a gimmick)", '<p>The difference between automation that changes a business and a gimmick abandoned after a month is <strong>business sense</strong>: understand the process, streamline it, and only then automate - with tools that fit into what you already use. With 20+ years of hi-tech background, I start from the business need, not the tool, and build a solution that actually works over time.</p>'),
      ("Summary", '<p>Automation and AI agents are a real lever for a business - but only when you start in the right place. Want to know what\'s worth automating for you? <a href="/en/contact">Talk to me</a> for a short intro call, and we\'ll map the opportunities together.</p>'),
    ],
    "faq":[
      ("What can be automated in a business?","Almost any repetitive process: moving data between systems, emails and updates, reports, forms, billing, responses and lead classification - and with AI, tasks that require understanding and judgment too."),
      ("How much time does automation save?","It depends on the process - clients have saved hundreds of work hours a year. After mapping, we can point to the biggest opportunities."),
      ("Do I need to know how to code to use this?","No. I build and deploy the solution, and you enjoy the result - a process that runs on its own, without touching code."),
    ],
  },
  {
    "slug":"when-to-consult-before-building",
    "title":"Tech consulting and specs - when to reach out before you build",
    "desc":"Tech consulting and specs for businesses: most projects fail because the wrong thing was built. When to consult and spec before investing in development - and how much money it saves.",
    "cat":"Consulting","date":"2026-09-18","modified":"2026-09-18","read":"5 min read",
    "excerpt":"Many projects fail not because of the development, but because the wrong thing was built. When to stop, consult and spec - before you invest in development.",
    "takeaways":[
      "Most failures aren't technical - the wrong product gets built.",
      "Consulting and a spec at the start save unnecessary development and a lot of money.",
      "The advantage: connecting business understanding, the users and the technology.",
    ],
    "sections":[
      ("Why projects fail", '<p>Many tech projects don\'t fail because of the code - but because the wrong thing was built. Features no one needs, a process that doesn\'t solve the real pain, or a product that doesn\'t fit the audience. Everything is technically fine, but it doesn\'t move the business.</p>'),
      ("When it's worth stopping to consult", '<p>It\'s worth getting consulting before development when you\'re not sure what exactly to build, how to prioritize, or which approach is right; when you\'re facing a significant investment and want to make sure you\'re building the right thing; or when there\'s an existing product that needs improving or expanding. In these cases, a few hours of consulting save months of unnecessary development.</p>'),
      ("What a consulting and spec process includes", '<p>Mapping the real need and pain, understanding the business and the users, forming a strategy and priorities, and planning a precise solution - all the way to <a href="/en/services/consulting">an informed decision and a clear action plan</a>. The result: you know exactly what to build, why, and in what order.</p>'),
      ("The differentiator - three worlds in one", '<p>My advantage is a rare combination: an understanding of the client, the business and the technology. I can identify the real need, understand what\'s technically possible, and prioritize correctly to deliver value fast - 20+ years of experience that prevent costly mistakes.</p>'),
      ("Summary", '<p>Good consulting isn\'t an expense - it\'s a saving. Before investing in development, it\'s worth making sure you\'re building the right thing. <a href="/en/contact">Talk to me</a> and we\'ll figure out together what\'s really needed.</p>'),
    ],
    "faq":[
      ("When should you get consulting instead of going straight to development?","When you're not sure what exactly to build, how to prioritize, or which approach is right - especially before a big investment. Good consulting saves unnecessary development and a lot of money."),
      ("How long does a consulting process take?","It depends on scope - from a single focused conversation to a process of several weeks. We define the right scope together in the intro call."),
      ("I already know what to build - do I still need consulting?","Not necessarily. If the need is clear and spec'd, you can go straight to development. Consulting is for those who want to make sure the direction is right before investing."),
    ],
  },
  {
    "slug":"mvp-vs-full-product",
    "title":"MVP or full product - what it is, and how to decide",
    "desc":"What an MVP (initial product build) is, when to choose a focused first version vs. a full product, and how to define the right core that delivers value fast.",
    "cat":"Product development","date":"2026-09-15","modified":"2026-09-15","read":"6 min read",
    "excerpt":"An MVP isn't a 'half-baked product' - it's a focused first version. When to choose it, when to go for a full product, and how to define the right core.",
    "takeaways":[
      "An MVP is a focused, polished first version - not a half-finished product.",
      "It lowers cost and risk and lets you learn from the market fast.",
      "The key: define the right core that delivers value - and build it fully.",
    ],
    "sections":[
      ("What an MVP really is", '<p>An MVP (Minimum Viable Product) is sometimes mistakenly seen as a "half-baked product." It isn\'t. An MVP is a <strong>focused first version</strong>: a complete, polished product that includes exactly what\'s needed to go to market and prove value - without unnecessary features that inflate cost and time.</p>'),
      ("When to choose an MVP", '<p>An MVP is a good fit when you want to get to market fast, test an idea against real users, or invest cautiously before a big commitment. It lowers risk: instead of betting on a huge product, you build the core, learn what works, and expand based on the real need.</p>'),
      ("When to go for a full product", '<p>Sometimes the need is clear and mature and requires a broad scope from the start - an internal system that must cover a whole process, or a product in a competitive market where a partial version won\'t be enough. Even then, I build in stages and keep you involved throughout.</p>'),
      ("How to define the right core", '<p>This is the heart of the decision - so we start with a <a href="/en/services/consulting">spec</a>. We ask: what\'s the core value the product must deliver? What must be in the first version and what can wait? A sharp spec prevents "feature creep" and ensures every dollar is invested in what really moves the needle.</p>'),
      ("The common mistake", '<p>The big mistake is building too much, too early. An overloaded product built for months before it ever saw a real user is risky and expensive. A focused approach, with a <a href="/en/services/product-development">product mindset</a>, gets you to market fast and smart.</p>'),
      ("Summary", '<p>MVP or full product - the answer depends on the need, the risk and the market. What\'s constant: you start by defining the right core. <a href="/en/contact">Talk to me</a> and we\'ll decide together what\'s right for you.</p>'),
    ],
    "faq":[
      ("What's the difference between an MVP and a full product?","An MVP is a focused first version that includes exactly what's needed to go to market and prove value; a full product is broader in scope. In both cases I build the full product and keep you involved throughout."),
      ("How much does it cost to build an MVP?","The cost depends on the scope of features. A focused MVP costs significantly less than a full product. After a spec you'll get a precise quote broken into milestones."),
      ("Can an MVP be expanded into a full product later?","Absolutely - that's the whole point. You launch with a focused core, learn from the market, and gradually expand into what actually works."),
    ],
  },
  {
    "slug":"wix-vs-custom-website",
    "title":"Why building a website on Wix isn't right for everyone",
    "desc":"A Wix website is great for some businesses - and not right for others. When Wix works, when a custom-built website is worth it, and the difference in SEO, performance and differentiation.",
    "cat":"Product development","date":"2026-09-27","modified":"2026-09-27","read":"6 min read",
    "excerpt":"Wix is cheap, fast to set up and great for starting out - but not right for every business. When Wix meets the need, and when a custom-built website is worth it.",
    "takeaways":[
      "Wix is great for a basic brand site, on a low budget, DIY.",
      "The limits: control over SEO and speed, complex integrations, customization, scaling and security.",
      "When you need unique functionality, performance, or a site that truly converts and differentiates - custom is better.",
    ],
    "sections":[
      ("When a Wix website actually is a good fit", '<p>Let\'s start fair: <strong>Wix is an excellent tool</strong> for a large share of businesses. If you need a simple brand website, on a low budget, that you can maintain yourself - Wix gives you independence, hosting, a domain and convenient drag-and-drop tools, without touching code. For starting out or a basic presence, it\'s a perfectly reasonable starting point.</p>'),
      ("The Wix limits worth knowing", '<p>But Wix is built as a template platform - and that comes with a ceiling. The main limits:</p><ul><li><strong>SEO and speed</strong> - limited control over code and performance; site speed, which is critical for Google ranking, is usually worse than a custom site.</li><li><strong>Integrations and functionality</strong> - connecting to business systems, custom logic or unique features - limited or impossible.</li><li><strong>Customization and differentiation</strong> - it\'s easy to get stuck with a templated look that resembles many other sites.</li><li><strong>Scaling and lock-in</strong> - hard to expand, and hard to leave the platform later.</li><li><strong>Security and control</strong> - less control over the environment and over data security.</li></ul>'),
      ("Wix vs. a custom-built website - what's the difference", '<p>The fundamental difference: on Wix you adapt the business to the platform; with <a href="/en/services/product-development">custom development</a> the platform is adapted to the business. A custom site gives full control over performance, SEO, design, integrations and security - and is built precisely around your need and messaging.</p>'),
      ("When to choose custom development", '<p>It\'s worth moving to custom development when the website is a core business asset and not just a business card: when you need unique functionality or integrations; when SEO and speed are critical; when you want a site that <strong>converts customers</strong> and sets you apart, not another template; and when there\'s sensitive data that requires <strong>real security from the ground up</strong> (a background I bring from the cyber world).</p>'),
      ("So what's right for you?", '<p>The question isn\'t "is Wix good or bad" - it\'s "what\'s right for your business, now and going forward." If you\'re not sure, it\'s worth <a href="/en/services/consulting">spec\'ing the need</a> before you commit. <a href="/en/contact">Talk to me</a> and we\'ll figure out together what the right solution is for you.</p>'),
    ],
    "faq":[
      ("Is Wix good for SEO?","Wix has improved a lot, but there are still limits on control over code and speed compared to a custom site - and speed is an important ranking factor. For a site where SEO is critical, custom development gives an advantage."),
      ("Wix or custom development - which is better?","It depends on the need. Wix is great for a basic site on a low budget that you maintain yourself; custom development is better when you need unique functionality, performance, integrations, differentiation or security."),
      ("Can I move from Wix to a custom site later?","Yes. Many businesses start on Wix and move to a custom site as they grow. The migration can be planned to preserve existing content and ranking."),
    ],
  },
]
for _pe in POSTS_EN:
    if _pe["slug"] in BLOG_IMG_BY_SLUG: _pe["img"] = BLOG_IMG_BY_SLUG[_pe["slug"]]
for _pe in POSTS_EN:
    blog_post(_pe, POSTS_EN, lang="en")

_feat_en = POSTS_EN[0]
featured_html_en = ('  <section class="wrap"><a class="blog-featured" href="/en/blog/%s">'
  '<div class="feat-body"><span class="cat">%s</span><h2>%s</h2><p>%s</p>'
  '<span class="feat-btn">Read more &#8594;</span></div>'
  '<div class="feat-media" style="background-image:url(%s)"></div></a></section>') % (
    _feat_en["slug"], _feat_en["cat"], _feat_en["title"], _feat_en["excerpt"], _feat_en.get("img", BLOG_IMAGES[0]))
_rest_en = POSTS_EN[1:]
grid_html_en = ""
if _rest_en:
    _cats_en = []
    for _qe in _rest_en:
        if _qe["cat"] not in _cats_en: _cats_en.append(_qe["cat"])
    _filt_en = '<button class="bfilter active" data-cat="all">All</button>' + "".join('<button class="bfilter" data-cat="%s">%s</button>' % (c,c) for c in _cats_en)
    _cards_en = "".join(blog_card(_qe, "en") for _qe in _rest_en)
    grid_html_en = ('  <section class="wrap"><div class="blog-filters">%s</div><hr class="blog-div"><div class="blog-cards" id="bgrid">%s</div></section>'
      '<script>document.querySelectorAll(".bfilter").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".bfilter").forEach(function(x){x.classList.remove("active");});b.classList.add("active");var c=b.dataset.cat;document.querySelectorAll("#bgrid .blog-card").forEach(function(w){w.style.display=(c==="all"||w.dataset.cat===c)?"":"none";});});});</script>') % (_filt_en, _cards_en)
blog_index_body_en = ('  <section class="wrap page-hero" style="padding-bottom:8px;"><span class="eyebrow"><span class="idx">//</span> <span class="ttl">Blog</span></span>'
  '<div class="blog-head"><h1 class="s-head">The Blog</h1>'
  '<p class="s-lead">Practical insights on product, web and app development, automation and AI agents - for businesses, independents and entrepreneurs.</p></div></section>'
  + featured_html_en + grid_html_en)
page("/blog","blog.html","Blog · Insights on Development, Automation & AI Agents | Michal Bar",
     "Practical insights on product and web development, automation and AI agents, and tech consulting - for businesses, independents and entrepreneurs.",
     [("Home","/"),("Blog",None)],
     blog_index_body_en + CTA_EN,
     [{"@type":"Blog","name":"Michal Bar's Blog","url":SITE+"/en/blog"}], lang="en")

print("\\nAll pages generated.")
