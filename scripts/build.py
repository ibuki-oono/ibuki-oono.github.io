#!/usr/bin/env python3
"""Build the dependency-free GitHub Pages site: python3 scripts/build.py."""
import json
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = json.loads((ROOT / 'data/projects.json').read_text())
X = 'https://x.com/ibuntu_robot'


def url(value):
    return escape(quote(value, safe=':/%?#=&'), quote=True)


def page(path, title, description, content, active='', crumbs=()):
    depth = len(Path(path).parts) - 1
    prefix = '../' * depth if depth else './'
    links = ''.join(f'<a href="{prefix}{slug}/"' + (' aria-current="page"' if active == slug else '') + f'>{label}</a>' for slug, label in [('about', '自己紹介'), ('works', '制作物'), ('contact', '仕事依頼')])
    breadcrumb = ''
    if crumbs:
        items = f'<li><a href="{prefix}">ホーム</a></li>'
        for label, target in crumbs:
            items += f'<li><a href="{prefix}{target}">{escape(label)}</a></li>' if target else f'<li aria-current="page">{escape(label)}</li>'
        breadcrumb = f'<nav class="breadcrumbs container" aria-label="パンくず"><ol>{items}</ol></nav>'
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#f5f5f7">
  <title>{escape(title)} — ibuki's blog</title>
  <link rel="icon" href="{prefix}image/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}css/style.css">
  <script src="{prefix}js/main.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">本文へスキップ</a>
  <header class="site-header">
    <div class="nav-inner"><a class="brand" href="{prefix}" aria-label="ibuki's blog ホーム">ibuki<span>.</span></a><nav aria-label="メインナビゲーション">{links}</nav></div>
    <div class="scroll-progress" aria-hidden="true"></div>
  </header>
  <main id="main">{breadcrumb}{content}</main>
  <footer class="site-footer container"><a class="brand" href="{prefix}" aria-label="ibuki's blog ホーム">ibuki<span>.</span></a><p>ロボットと、好奇心と、サメさんと。</p><a href="{X}">X / @ibuntu_robot <span aria-hidden="true">↗</span></a></footer>
</body>
</html>
'''
    output = ROOT / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding='utf-8')


def image_source(project, prefix='./', original=False):
    edited = project.get('display_image') if not original else None
    if edited:
        return url(edited if edited.startswith('https://') else prefix + edited)
    local = f'image/projects/{project["slug"]}.jpg'
    return url(prefix + local if (ROOT / local).is_file() else (prefix + project['image'] if not project['image'].startswith('https://') else project['image']))


def image(project, css='', eager=False, prefix='./', original=False):
    priority = ' fetchpriority="high"' if eager else ''
    presentation = ' is-cutout' if project.get('display_image') and not original else ''
    return f'''<div class="project-image {css}{presentation}"><img src="{image_source(project, prefix, original=original)}" alt="{escape(project['image_alt'])}" loading="{'eager' if eager else 'lazy'}" decoding="async" referrerpolicy="no-referrer"{priority}><span class="image-fallback">写真は原記事でご覧いただけます</span></div>'''


def card(project, prefix, asset_prefix='./'):
    return f'''<a class="project-card reveal" href="{prefix}{project['slug']}/">{image(project, prefix=asset_prefix)}<div class="project-card-copy"><div class="project-meta"><span>{escape(project['category'])}</span><time datetime="{project['date']}">{project['date'].replace('-', '.')}</time></div><h3>{escape(project['title'])}<span aria-hidden="true">↗</span></h3><p>{escape(project['summary'])}</p></div></a>'''


def heading(kicker, title, lead):
    return f'<section class="page-heading container"><p class="eyebrow hero-enter">{kicker}</p><h1 class="hero-enter enter-delay-1">{title}</h1><p class="page-lead hero-enter enter-delay-2">{lead}</p></section>'


def next_page(href, kicker, title):
    return f'<a class="next-page container reveal" href="{href}"><span><small>{kicker}</small><strong>{title}</strong></span><span class="next-arrow" aria-hidden="true">↗</span></a>'


home = '''
<section class="home-hero container" aria-labelledby="hero-title">
  <p class="eyebrow hero-enter">IBUKI’S BLOG / ROBOTICS & CURIOSITY</p>
  <h1 id="hero-title" class="hero-enter enter-delay-1">つくる。ためす。<br><span class="gradient-text">夢中になる。</span></h1>
  <p class="hero-description hero-enter enter-delay-2">ロボットづくりと、日々の好奇心。</p>
  <div class="hero-actions hero-enter enter-delay-3"><a class="button button-primary" href="./works/">制作物を見る <span aria-hidden="true">↗</span></a><a class="text-link" href="./about/">ibukiについて <span aria-hidden="true">↗</span></a></div>
'''
featured = PROJECTS[0]
home += f'''<figure class="hero-photo reveal"><div class="hero-photo-frame" data-parallax>{image(featured, eager=True)}</div></figure>'''
home += '''
</section>
<section class="home-about container section-space reveal" aria-labelledby="home-about-title">
  <div class="home-about-heading"><p class="eyebrow">ABOUT ME</p><h2 id="home-about-title">はじめまして、<br><span class="gradient-text">ibukiです。</span></h2></div>
  <div class="home-about-copy"><p>ロボットに魅せられ、ものづくりを続けています。機械の設計から回路、制御まで、アイデアを実際に動くかたちにすることが好きです。</p><p>大会への挑戦や、日々の試作で得た発見を、この場所に残しています。</p><a class="text-link" href="./about/">自己紹介を見る <span aria-hidden="true">↗</span></a></div>
</section>
<section class="container section-space" id="selected" aria-labelledby="selected-title"><div class="section-intro reveal"><div><p class="eyebrow">SELECTED WORKS</p><h2 id="selected-title">アイデアを、かたちに。</h2></div><a class="text-link" href="./works/">すべての制作物 <span aria-hidden="true">↗</span></a></div><div class="project-grid">'''
home += ''.join(card(p, './works/') for p in PROJECTS[:6])
home += '''</div></section>
<section class="explore-section section-space" aria-labelledby="explore-title"><div class="container"><div class="section-intro reveal"><div><p class="eyebrow">EXPLORE</p><h2 id="explore-title">ここから、もう少し。</h2></div></div><div class="page-grid">
  <a class="page-card about-card reveal" href="./about/"><div class="card-top"><span class="card-kicker">01 / ABOUT</span><span class="circle-arrow" aria-hidden="true">↗</span></div><div class="card-copy"><h3>自己紹介</h3><p>ロボットに魅せられた、管理人のこと。</p></div></a>
  <a class="page-card works-card reveal" href="./works/"><div class="card-top"><span class="card-kicker">02 / WORKS</span><span class="circle-arrow" aria-hidden="true">↗</span></div><div class="card-copy"><h3>制作物</h3><p>つくったものと、試行錯誤の記録。</p></div></a>
  <a class="page-card contact-card reveal" href="./contact/"><div class="card-top"><span class="card-kicker">03 / LET’S TALK</span><span class="circle-arrow" aria-hidden="true">↗</span></div><div class="card-copy"><h3>仕事依頼</h3><p>一緒に、つくる話を。</p></div></a>
</div></div></section>
<section class="closing-section container reveal"><p class="eyebrow">STAY CURIOUS. KEEP MAKING.</p><h2>次の「つくりたい」で、<br>また会いましょう。</h2><a class="text-link" href="https://x.com/ibuntu_robot">Xで日々のことを見る <span aria-hidden="true">↗</span></a></section>
'''
page('index.html', 'つくる、その先へ。', 'ibukiのロボットづくり。自己紹介、制作物、仕事のご相談はこちらから。', home)

about = heading('01 / ABOUT ME', 'ロボットに、<br><span class="gradient-text">魅せられて。</span>', 'つくることに夢中な、管理人のこと。')
about += '''<section class="profile-section container"><figure class="profile-photo reveal"><img src="../image/top_same.jpg" alt="管理人の相棒、メガネをかけた青いサメのぬいぐるみ" width="4080" height="2344"><figcaption>MY COMPANION / サメさん</figcaption></figure><div class="profile-copy reveal"><p class="eyebrow">HELLO, I’M</p><h2 class="profile-name">ibuki<span>.</span></h2><p>ロボットに魅せられ、ロボットを作り続ける管理人です。</p><p>機構を考えるところから、回路、制御まで。<br>思い描いたものが動く、その瞬間が好きです。</p><div class="tags"><span>機械設計</span><span>電装・制御</span><span>ロボット</span></div><a class="text-link" href="https://x.com/ibuntu_robot">X / @ibuntu_robot <span aria-hidden="true">↗</span></a></div></section>
<section class="statement-section container reveal"><p class="eyebrow">ABOUT THIS PLACE</p><h2>完成までの時間も、<br>ものづくりの一部。</h2><p>ロボットのこと、つくってみたこと。<br>そんな日々の一片を、ここに残していきます。</p></section>'''
about += next_page('../works/', 'NEXT / WORKS', 'つくったものを見る。')
page('about/index.html', '自己紹介', 'ロボットに魅せられ、機構・回路・制御に取り組むibukiの自己紹介。', about, 'about', [('自己紹介', None)])

works = heading('02 / WORKS', 'アイデアを、<br><span class="gradient-text">かたちに。</span>', 'つくったものと、その記録。')
works += f'<section class="container works-list" aria-labelledby="works-list-title"><div class="works-list-heading reveal"><h2 id="works-list-title">制作物一覧</h2><span>{len(PROJECTS):02d} PROJECTS / {PROJECTS[-1]["date"][:4]}—{PROJECTS[0]["date"][:4]}</span></div><div class="project-grid">'
works += ''.join(card(p, './', asset_prefix='../') for p in PROJECTS)
works += '</div></section>'
works += next_page('../contact/', 'NEXT / LET’S TALK', '一緒につくる話を。')
page('works/index.html', '制作物', 'キャチロボ、つくばチャレンジ、自律型ゴルフロボット。ibukiの制作物を紹介します。', works, 'works', [('制作物', None)])

contact = heading('03 / LET’S TALK', '一緒に、<br><span class="gradient-text">つくる話を。</span>', '仕事のご依頼やご相談は、Xからどうぞ。')
contact += '''<section class="contact-panel container reveal"><div class="contact-panel-copy"><p class="eyebrow">GET IN TOUCH</p><h2>はじまりは、<br>ひとつのメッセージ。</h2><p>「こんなことを相談したい」<br>まずは、お話を聞かせてください。</p><a class="button button-primary" href="https://x.com/ibuntu_robot">Xで相談する <span aria-hidden="true">↗</span></a><span class="contact-handle">@ibuntu_robot</span></div><div class="contact-panel-art" aria-hidden="true">↗</div></section>
<section class="container section-space"><div class="section-intro reveal"><div><p class="eyebrow">A GOOD START</p><h2>ご相談のときに。</h2></div><p>決まっている範囲で教えてください。</p></div><ol class="request-list"><li class="reveal"><span aria-hidden="true">01</span><div><h3>相談したいこと</h3><p>つくりたいものや、ご依頼の概要。</p></div></li><li class="reveal"><span aria-hidden="true">02</span><div><h3>時期・スケジュール</h3><p>ご希望の日程や、納期の目安。</p></div></li><li class="reveal"><span aria-hidden="true">03</span><div><h3>ご予算・条件</h3><p>予算感や、共有しておきたいこと。</p></div></li></ol></section>'''
contact += next_page('../about/', 'MORE / ABOUT ME', '管理人について知る。')
page('contact/index.html', '仕事依頼', 'ibukiへの仕事依頼やご相談。連絡先はXの@ibuntu_robotです。', contact, 'contact', [('仕事依頼', None)])

for i, project in enumerate(PROJECTS):
    content = heading(f'WORKS / {project["date"].replace("-", ".")}', escape(project['title']), escape(project['summary']))
    content += f'<article class="project-detail container"><div class="detail-meta reveal"><span>{escape(project["subtitle"])}</span><div class="tags">' + ''.join(f'<span>{escape(tag)}</span>' for tag in project['tags']) + '</div></div>'
    content += f'<figure class="detail-figure reveal">{image(project, eager=True, prefix="../../")}<figcaption>写真：{escape(project.get("source_kind", "ロボット技術研究会"))} の制作記録</figcaption></figure>'
    content += '<div class="article-layout"><nav class="article-toc reveal" aria-label="この記事の目次"><p class="eyebrow">ON THIS PAGE</p>'
    content += ''.join(f'<a href="#section-{j}">{escape(s["title"])}</a>' for j, s in enumerate(project['sections'], 1))
    content += '</nav><div class="article-body">'
    for j, section in enumerate(project['sections'], 1):
        content += f'<section id="section-{j}" class="article-section reveal"><span class="section-number">0{j}</span><h2>{escape(section["title"])}</h2><p>{escape(section["text"])}</p></section>'
    if project.get('gallery'):
        content += '<section class="article-gallery reveal" aria-label="制作写真"><h2>制作の記録</h2><div class="gallery-grid">'
        for photo in project['gallery']:
            content += f'<figure><img src="{url("../../" + photo["image"])}" alt="{escape(photo["caption"], quote=True)}" loading="lazy" decoding="async"><figcaption>{escape(photo["caption"])}</figcaption></figure>'
        content += '</div></section>'
    if project.get('source', '').startswith('https://'):
        content += f'<aside class="source-note reveal"><p class="eyebrow">SOURCE</p><h2>元の制作記録</h2><p>この記事はロボット技術研究会公式ブログの制作記録をもとにまとめています。</p><a class="text-link" href="{url(project["source"])}">{escape(project["source_title"])} <span aria-hidden="true">↗</span></a></aside>'
    content += '</div></div></article>'
    content += '<div class="detail-bottom container reveal"><a class="text-link" href="../"><span aria-hidden="true">←</span> 制作物一覧に戻る</a>'
    following = PROJECTS[(i + 1) % len(PROJECTS)]
    content += f'<a class="text-link" href="../{following["slug"]}/">次の制作物 <span aria-hidden="true">→</span></a></div>'
    page(f'works/{project["slug"]}/index.html', project['title'], project['summary'], content, 'works', [('制作物', 'works/'), (project['title'], None)])

print(f'Built {len(PROJECTS) + 4} static pages.')
