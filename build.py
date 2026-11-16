#!/usr/bin/env python3
"""Build the bilingual academic homepage and redirects for retired topic pages."""
import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text())
release_hash = hashlib.sha256()
for source in [ROOT / 'build.py', ROOT / 'content.json', *sorted((ROOT / 'assets').rglob('*'))]:
    if source.is_file() and source.name != '.DS_Store':
        release_hash.update(source.relative_to(ROOT).as_posix().encode())
        release_hash.update(source.read_bytes())
SITE_VERSION = release_hash.hexdigest()[:12]
parser = argparse.ArgumentParser()
parser.add_argument('--out', default='dist')
OUT = ROOT / parser.parse_args().out
OUT.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
E = html.escape
PREVIEW_UPDATES = 3
LEGACY = {'research': 'publications', 'experiences': 'experiences', 'background': 'education', 'mentorship': 'mentorship'}


def render(language):
    zh = language == 'zh'
    t = lambda en, cn: cn if zh else en
    val = lambda values: values[int(zh)]
    base = '../' if zh else './'
    asset = lambda name: base + 'assets/' + name + '?v=' + SITE_VERSION
    home = lambda lang: base + ('zh/' if lang == 'zh' else '') + '?v=' + SITE_VERSION

    def section(heading, id_, body):
        return f'<section class="section" id="{id_}"><h2>{heading}</h2>{body}</section>'

    def update(item, older=False):
        body = E(val(item['text']))
        for name in item.get('people', []):
            body = body.replace(E(name), f'<span class="person-name">{E(name)}</span>')
        for word in ('Champion', 'Oral', '擂主'):
            body = body.replace(word, f'<strong>{word}</strong>')
        papers = ''.join(f'<li>{E(name)}</li>' for name in item.get('papers', []))
        if papers:
            body += f'<ul class="update-papers">{papers}</ul>'
        return f'<article class="update" {"data-older-update" if older else ""}><time>{E(item["date"])}</time><div>{body}</div></article>'

    recent = ''.join(update(item) for item in DATA['updates'][:PREVIEW_UPDATES])
    older = DATA['updates'][PREVIEW_UPDATES:]
    if older:
        recent += f'<details class="updates-more"><summary><span class="when-closed">{t(f"Show more updates ({len(older)})", f"展开更多动态（{len(older)}）")}</span><span class="when-open">{t("Show fewer updates", "收起往期动态")}</span><span class="chevron" aria-hidden="true">⌄</span></summary><div class="older-updates">{"".join(update(item, True) for item in older)}</div></details>'

    papers = []
    for paper in DATA['publications']:
        authors = []
        for author in paper['authors']:
            name = E(author['name'])
            if author['name'] == DATA['name']:
                name = f'<strong>{name}</strong>'
            marker = ('*' if author.get('equal') else '') + ('†' if author.get('corresponding') else '')
            authors.append(name + (f'<sup>{marker}</sup>' if marker else ''))
        width, height = (1216, 556) if paper['id'] == 's3-lora' else (1518, 834)
        figure = f'<a class="paper-figure" href="{asset(paper["figure"])}" target="_blank" rel="noopener"><img src="{asset(paper["figure"])}" alt="{E(val(paper["figure_alt"]))}" width="{width}" height="{height}" loading="lazy"><span>{t("View figure ↗", "查看主图 ↗")}</span></a>'
        abstract = f'<details class="paper-abstract"><summary><span class="when-closed">{t("Show abstract", "展开摘要")}</span><span class="when-open">{t("Hide abstract", "收起摘要")}</span><span class="chevron" aria-hidden="true">⌄</span></summary><p class="abstract" data-full-abstract>{E(val(paper["abstract"]))}</p></details>'
        papers.append(f'<article class="publication" id="{paper["id"]}">{figure}<div class="paper-body"><h3>{E(paper["title"])}</h3><p class="authors">{", ".join(authors)}</p><p class="venue">{E(paper["venue"])}</p>{abstract}</div></article>')
    publications = ''.join(papers) + f'<p class="author-note">{t("* Equal contribution. † Corresponding author.", "* 共同第一作者。† 通讯作者。")}</p>'

    education = []
    for item in DATA['education']:
        school = E(val(item.get('institution', ['Beihang University', '北京航空航天大学'])))
        if item.get('rank'):
            school += f' · <strong>{E(val(item["rank"]))}</strong>'
        education.append(f'<article class="timeline-row mini-edu"><time>{E(val(item["date"]))}</time><div><h3>{E(val(item["degree"]))}</h3><p class="school">{school}</p><p class="detail">{E(val(item["detail"]))}</p></div></article>')

    experience = f'<article class="timeline-row"><time>2026.11 — {t("Present", "至今")}</time><div><h3>{t("Baidu · Agentic Embodied Intelligence", "百度 · Agentic 具身智能")}</h3><p class="detail">{t("Research on VLA post-training for Agentic embodied intelligence.", "围绕 Agentic 具身智能开展 VLA 后训练研究。")}</p></div></article>'
    projects = f'''<details class="project-details"><summary>{t('Selected projects', '代表项目')}<span class="chevron" aria-hidden="true">⌄</span></summary><div class="project-list">
<article><h3>StarOps · {t('Intelligent operations for Kylin', '星维管家')}</h3><p>{t('Built a system-level agent for the Kylin operating system, integrating monitoring, anomaly diagnosis, automated optimisation, MCP-compatible services, and log anomaly detection.', '面向银河麒麟操作系统构建系统级 Agent，集成状态监控、异常诊断与自动调优，开发符合 MCP 协议的系统接口与日志异常检测算法。')}</p><a href="https://github.com/Kylin-StarOps-Team/StarOps">{t('Source code ↗', '项目代码 ↗')}</a></article>
<article><h3>{t('Low-precision adaptation · Huawei Pangu', '低精度模型适配 · 华为盘古')}</h3><p>{t('Reproduced L4Q and adapted MXFP8 training schemes, investigating quantization-aware PEFT under limited compute and memory budgets.', '复现 L4Q，适配 MXFP8 训练方案，在有限算力与显存条件下探索量化感知 PEFT。')}</p></article>
<article><h3>SmartFibers · {t('AI-based industrial inspection', 'AI 工业质检')}</h3><p>{t('High-precision imaging and intelligent inspection of spandex yarn packages, awarded in the Capital Challenge Cup special competition.', '基于 AI 的氨纶丝饼高精度成像与智能检测技术研究及应用，获首都挑战杯“青智未来”专项赛擂主。')}</p><div class="project-links"><a href="https://github.com/MitakeMoca/SmartFibers-frontend">Frontend ↗</a><a href="https://github.com/MitakeMoca/SmartFibers-backend">Backend ↗</a></div></article>
</div></details>'''

    courses = []
    for course in DATA['courses']:
        role = f'<span class="ta-note"> · {t("Head TA", "助教组长")}</span>' if course.get('lead') else ''
        repo = f' <a class="ta-repo" href="{E(course["repo"])}">{t("Repository ↗", "教学仓库 ↗")}</a>' if course.get('repo') else ''
        courses.append(f'<div class="ta-row" data-home-course><time>{E(val(course["term"]))}</time><div>{E(val(course["title"]))}{role}{repo}</div></div>')
    mentorship = f'<p class="ta-heading">{t("Teaching Assistant · Beihang University", "课程助教 · 北京航空航天大学")}</p><div class="ta-list">{"".join(courses)}</div>'
    awards = ''.join(f'<article class="timeline-row award-row"><time>{E(item["year"])}</time><div><h3>{E(val(item["title"]))}</h3><p class="detail">{E(val(item["detail"]))}</p></div></article>' for item in DATA['awards'])

    intro = t('I am a Ph.D. student in Artificial Intelligence at <a href="https://www.buaa.edu.cn/">Beihang University</a>, jointly trained with Zhongguancun Laboratory and advised by Prof. Baochang Zhang.', '我是北京航空航天大学人工智能专业博士研究生，与中关村实验室联合培养，导师为张宝昌教授。')
    about = f'<section class="about" id="about"><h1>{t("About", "关于我")}</h1><p>{intro}</p><p>{t("My research focuses on", "我的研究方向是")} <strong>{t("VLA post-training", "VLA 后训练")}</strong>。</p></section>'
    if not zh:
        about = about.replace('</strong>。</p>', '</strong>.</p>')
    content = about + section('Updates' if not zh else '最新动态', 'updates', recent)
    content += section(t('Publications', '论文'), 'publications', publications)
    content += section(t('Education', '教育背景'), 'education', ''.join(education))
    content += section(t('Experiences', '研究经历'), 'experiences', experience + projects)
    content += section(t('Mentorship', '指导与教学'), 'mentorship', mentorship)
    content += section(t('Awards', '奖励与荣誉'), 'awards', awards)
    nav = ''.join(f'<a href="#{id_}">{heading}</a>' for id_, heading in [('about', t('About', '关于我')), ('updates', 'Updates'), ('publications', t('Publications', '论文')), ('education', t('Education', '教育')), ('experiences', t('Experiences', '经历'))])
    profile = f'''<aside class="profile"><img class="avatar" src="{asset('avatar.jpg')}" alt="Qixuan Wu’s avatar" width="132" height="132"><div class="profile-info"><h2>Qixuan Wu <span class="nickname">(Moca)</span></h2><p class="role">{t('Ph.D. Student · Artificial Intelligence', '人工智能博士研究生')}</p><p class="affiliation">{t('Beihang University', '北京航空航天大学')}<br>{t('Zhongguancun Laboratory · Joint training', '中关村实验室 · 联合培养')}</p><p class="location">{t('Beijing, China', '中国 · 北京')}</p><div class="profile-links"><a href="mailto:{E(DATA['email'])}">{t('Email', '邮件')}</a><a href="{E(DATA['github'])}">GitHub</a></div></div></aside>'''
    canonical = 'https://mitakemoca.github.io/' + ('zh/' if zh else '')
    description = t('Qixuan Wu: VLA post-training, publications, education, research experience, and teaching at Beihang University.', 'VLA 后训练、学术论文、教育背景、研究经历与课程教学。')
    theme_init = "document.documentElement.classList.add('js');try{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(e){}"
    return f'''<!doctype html><html lang="{'zh-CN' if zh else 'en'}" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="site-version" content="{SITE_VERSION}"><meta name="color-scheme" content="light dark"><title>Qixuan Wu · {t('Homepage', '主页')}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="https://mitakemoca.github.io/"><link rel="alternate" hreflang="zh-CN" href="https://mitakemoca.github.io/zh/"><meta property="og:title" content="Qixuan Wu · Homepage"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml"><script>{theme_init}</script><link rel="stylesheet" href="{asset('home.css')}"><script defer src="{asset('home.js')}"></script></head><body><a class="skip" href="#main">{t('Skip to content', '跳转到正文')}</a><header class="topbar"><div class="top-inner"><a class="wordmark" href="#about">{t('Home', '首页')}</a><nav class="nav" id="navigation" aria-label="{t('Main navigation', '主导航')}">{nav}</nav><div class="tools"><a class="language" href="{home('en' if zh else 'zh')}" aria-label="{t('Switch to Chinese', 'Switch to English')}">{t('中文', 'EN')}</a><button class="theme" data-theme-toggle aria-label="{t('Toggle dark mode', '切换深色模式')}" aria-pressed="false" hidden>◐</button><button class="menu" data-menu-toggle aria-controls="navigation" aria-expanded="false" hidden>{t('Menu', '菜单')}</button></div></div></header><div class="shell">{profile}<main id="main">{content}</main></div><footer class="footer"><span>© 2026 Qixuan Wu</span><span>{t('Updated', '最近更新')} {E(DATA['updated'])} <a href="#about">{t('Back to top ↑', '返回顶部 ↑')}</a></span></footer></body></html>'''


for lang in ('en', 'zh'):
    directory = OUT / ('zh' if lang == 'zh' else '')
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'index.html').write_text(render(lang), encoding='utf-8')
    for page, anchor in LEGACY.items():
        retired = directory / page
        retired.mkdir(parents=True, exist_ok=True)
        target = '../?v=' + SITE_VERSION + '#' + anchor
        (retired / 'index.html').write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><meta name="robots" content="noindex"><title>Qixuan Wu · Homepage</title></head><body><a href="{target}">Continue to the homepage / 返回主页</a></body></html>', encoding='utf-8')
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://mitakemoca.github.io/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://mitakemoca.github.io/</loc></url><url><loc>https://mitakemoca.github.io/zh/</loc></url></urlset>')
(OUT / '404.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title></head><body><h1>Page not found</h1><a href="/?v={SITE_VERSION}">Back to the homepage / 返回主页</a></body></html>')
print(f'Built the academic homepage in English and Chinese, with 8 legacy redirects. Release {SITE_VERSION}.')
