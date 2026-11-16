#!/usr/bin/env python3
"""Build a bilingual, dependency-free GitHub Pages site from content.json."""
import argparse
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--out', default='dist')
OUT = ROOT / parser.parse_args().out
OUT.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
E = html.escape
PAGES = {'home': ('Home', '主页'), 'research': ('Research', '研究'), 'experiences': ('Experiences', '经历'), 'background': ('Background', '教育与荣誉')}


def render(language, page):
    zh = language == 'zh'
    idx = int(zh)
    t = lambda en, cn: cn if zh else en
    val = lambda value: value[idx]
    depth = (1 if zh else 0) + (0 if page == 'home' else 1)
    base = '../' * depth or './'

    def url(name, lang=None):
        lang = language if lang is None else lang
        if name == 'mentorship':
            return url('home', lang) + '#mentorship'
        return base + ('zh/' if lang == 'zh' else '') + ('' if name == 'home' else name + '/')

    def link(name, text):
        return f'<a class="text-link" href="{url(name)}">{text}<span aria-hidden="true">↗</span></a>'

    def section(title, number, content, id_, destination=None, more=None):
        right = link(destination, more or t('View all', '查看全部')) if destination else ''
        return f'<section class="section" id="{id_}"><div class="section-head"><h2><span class="number">{number}</span>{title}</h2>{right}</div>{content}</section>'

    def title(label, heading, desc, topics=''):
        return f'<header class="page-title"><div class="eyebrow"><span class="dot"></span>{label}</div><h1>{heading}</h1><p>{desc}</p>{topics}</header>'

    def emphasize(text):
        value = E(text)
        value = value.replace('Ranked 1st', '<strong>Ranked 1st</strong>')
        value = value.replace('专业排名第 1', '<strong>专业排名第 1</strong>')
        return value

    def education():
        rows = []
        for item in DATA['education']:
            school = val(item.get('institution', ['Beihang University', '北京航空航天大学']))
            rows.append(f'<article class="mini-edu"><time>{E(val(item["date"]))}</time><div><h3>{E(val(item["degree"]))}</h3><div class="school">{E(school)}</div><p>{emphasize(val(item["detail"]))}</p></div></article>')
        return ''.join(rows)

    def awards(limit=None):
        return ''.join(f'<article class="award-row"><span class="award-year">{E(x["year"])}</span><div><h3>{E(val(x["title"]))}</h3><p>{E(val(x["detail"]))}</p></div></article>' for x in DATA['awards'][:limit])

    def publications():
        papers = []
        for paper in DATA['publications']:
            authors = []
            for author in paper['authors']:
                name = E(author['name'])
                if author['name'] == 'Qixuan Wu':
                    name = '<strong>' + name + '</strong>'
                markers = ('*' if author.get('equal') else '') + ('†' if author.get('corresponding') else '')
                authors.append(name + (f'<sup>{markers}</sup>' if markers else ''))
            author_line = ', '.join(authors)
            figure_url = base + 'assets/' + paper['figure']
            figure = f'<a class="paper-figure" href="{figure_url}" target="_blank" rel="noopener"><img src="{figure_url}" alt="{E(val(paper["figure_alt"]))}" loading="lazy"><span>{t("View figure ↗", "查看主图 ↗")}</span></a>'
            links = ''.join(f'<a href="{x["url"]}">{E(x["label"])} ↗</a>' for x in paper.get('links', []))
            papers.append(f'<article class="publication" id="{paper["id"]}">{figure}<div><div class="meta">{E(paper["venue"])}</div><h3>{E(paper["title"])}</h3><p class="authors">{author_line}</p><details class="paper-abstract"><summary><span class="expand-label">{t('Show abstract', '展开摘要')}</span><span class="collapse-label">{t('Hide abstract', '收起摘要')}</span><span class="abstract-chevron" aria-hidden="true">⌄</span></summary><p class="abstract" data-full-abstract>{E(val(paper["abstract"]))}</p></details>{f"<div class=paper-links>{links}</div>" if links else ""}</div></article>')
        legend = t('* Equal contribution. † Corresponding author.', '* 共同第一作者。† 通讯作者。')
        return ''.join(papers) + f'<p class="author-note">{legend}</p>'

    def compact_teaching():
        rows = []
        for course in DATA['courses']:
            notes = []
            if course.get('lead'):
                notes.append(t('Head TA', '助教组长'))
            name = E(val(course['title']))
            repo = f' <a class="ta-repo" href="{E(course["repo"])}">{t("Repository ↗", "教学仓库 ↗")}</a>' if course.get('repo') else ''
            note = f'<span class="ta-note"> · {" · ".join(notes)}</span>' if notes else ''
            rows.append(f'<div class="ta-row" data-home-course><time>{E(val(course["term"]))}</time><div>{name}{note}{repo}</div></div>')
        heading = t('Teaching Assistant · Beihang University', '课程助教 · 北京航空航天大学')
        return f'<p class="ta-heading">{heading}</p><div class="ta-list">{"".join(rows)}</div>'

    def baidu():
        return f'<article class="experience"><div class="date">2026.11<br>— {t("Present", "至今")}</div><div><h3>{t("Baidu", "百度")}</h3><div class="job">{t("Agentic Embodied Intelligence", "Agentic 具身智能")}</div><p>{t("VLA post-training for Agentic embodied intelligence.", "围绕 Agentic 具身智能开展 VLA 后训练研究。")}</p></div></article>'

    def explore():
        options = [('research', t('VLA post-training and selected publications.', 'VLA 后训练与代表论文。')), ('experiences', t('Industry research and projects built from ideas to systems.', '产业研究与从方法走向系统的项目。')), ('background', t('Education, academic milestones, and awards.', '教育背景、学习经历与荣誉。'))]
        return '<div class="explore-grid">' + ''.join(f'<a class="explore-item" href="{url(k)}"><h3>{val(PAGES[k])}<span aria-hidden="true">↗</span></h3><p>{d}</p></a>' for k, d in options) + '</div>'

    def contact():
        return f'<section class="contact" id="contact"><div class="eyebrow">{t("KEEP IN TOUCH", "保持联系")}</div><p>{t("For research, collaboration, or questions about the teaching materials:", "如果你想交流研究、探讨合作，或讨论教学资料：")}<br><a href="mailto:{DATA["email"]}">{DATA["email"]}</a> &nbsp; / &nbsp; <a href="{DATA["github"]}">GitHub ↗</a></p></section>'

    if page == 'home':
        content = f'<header class="hero"><div class="eyebrow"><span class="dot"></span>{t("BEIHANG UNIVERSITY · ZHONGGUANCUN LABORATORY", "北京航空航天大学 · 中关村实验室")}</div><h1>{t("VLA post-training", "VLA 后训练")}</h1><p class="intro">{t("I’m a Ph.D. student in Artificial Intelligence at <a href=\"https://www.buaa.edu.cn/\">Beihang University</a>, jointly trained with <strong>Zhongguancun Laboratory</strong> and advised by Prof. Baochang Zhang. My research focuses on <strong>VLA post-training</strong>.", "我是北京航空航天大学人工智能专业博士研究生，与<strong>中关村实验室</strong>联合培养，导师为张宝昌教授。我的研究方向是 <strong>VLA 后训练</strong>。")}</p><div class="hero-bottom">{link("research", t("Research & publications", "研究与论文"))}<span class="annotation">{t("BEIJING, CHINA", "中国 · 北京")}</span></div></header>'
        updates = []
        for n, item in enumerate(DATA['updates']):
            body = E(val(item['text']))
            for name in item.get('people', []):
                body = body.replace(E(name), f'<span class="person-name">{E(name)}</span>')
            paper_list = ''.join(f'<li>{E(name)}</li>' for name in item.get('papers', []))
            if paper_list:
                body += f'<ul class="update-papers">{paper_list}</ul>'
            updates.append(f'<article class="update" {"data-older-update" if n >= 8 else ""}><time>{E(item["date"])}</time><div><span class="kind">{E(val(item["type"]))}</span>{body}</div></article>')
        updates_html = ''.join(updates)
        if len(DATA['updates']) > 8:
            updates_html += f'<button class="plain-button" data-more-updates aria-expanded="false" data-more="{t("Show earlier updates ↓", "展开往期动态 ↓")}" data-less="{t("Show fewer updates ↑", "收起往期动态 ↑")}" hidden>{t("Show earlier updates ↓", "展开往期动态 ↓")}</button>'
        content += section(t('Updates', '最新动态'), '01', updates_html, 'updates')
        content += section(t('Publications', '论文'), '02', publications(), 'publications', 'research', t('All research', '全部研究'))
        content += section(t('Experiences', '研究经历'), '03', baidu(), 'experiences', 'experiences', t('Projects & experience', '经历与项目'))
        content += section('Education' if not zh else '教育背景', '04', education(), 'education', 'background')
        content += section('Mentorship' if not zh else '指导与教学', '05', compact_teaching(), 'mentorship')
        content += section(t('Selected awards', '代表荣誉'), '06', awards(3), 'awards', 'background')
        content += section(t('Explore further', '更多专题'), '07', explore(), 'explore') + contact()

    elif page == 'research':
        content = title('RESEARCH / 01', t('Research & publications', '研究与论文'), t('Research focus: VLA post-training.', '研究方向：VLA 后训练。'))
        content += section(t('Publications', '论文'), '01', publications(), 'publications') + contact()

    elif page == 'experiences':
        content = title('EXPERIENCES / 02', t('From methods to systems.', '从方法走向系统。'), t('VLA post-training research and selected agent-system projects.', 'VLA 后训练研究与智能体系统项目实践。'))
        content += section(t('Industry research', '产业研究'), '01', baidu(), 'industry')
        star = f'<article class="project" style="padding-top:0"><div class="meta">2025.05 — 2025.10 &nbsp; <span class="badge">{t("National Champion · Challenge Cup", "挑战杯 · 全国擂主")}</span></div><h3>StarOps · {t("Intelligent operations for Kylin", "星维管家")}</h3><p>{t("Built a system-level agent for the Kylin operating system, connecting monitoring, anomaly diagnosis, and system optimisation in an automated loop.", "面向银河麒麟操作系统，构建集系统状态监控、异常诊断与自动调优于一体的系统级 Agent。")}</p><ul><li>{t("Designed and implemented a GUI assistant with anomaly detection, root-cause chain analysis, tuning, and system Q&A.", "设计并实现 GUI 智能管家，集成异常检测、异常链路分析、自动调优与系统问答。")}</li><li>{t("Exposed system services through MCP-compatible interfaces for integration with Kylin’s model assistant.", "构建符合 MCP 协议的系统接口，对接麒麟操作系统的大模型助手。")}</li><li>{t("Developed a log anomaly detector combining BERT representations, a semantic projector, and a LLaMA decoder.", "实现结合 BERT 编码、语义空间对齐与 LLaMA 解码的日志异常检测算法。")}</li></ul><div class="paper-links"><a href="https://github.com/Kylin-StarOps-Team/StarOps">{t("Source code ↗", "项目代码 ↗")}</a></div></article>'
        pangu = f'<article class="project"><div class="meta">{t("HUAWEI PANGU · MODEL ADAPTATION", "华为盘古大模型 · 模型适配")}</div><h3>{t("Low-precision fine-tuning", "低精度微调")}</h3><p>{t("Reproduced L4Q and adapted MXFP8 training schemes, investigating quantization-aware PEFT under limited compute and memory budgets.", "复现 L4Q，适配 MXFP8 训练方案，在有限算力与显存条件下探索量化感知 PEFT。")}</p><div class="paper-links">{link("research", t("Research details", "研究详情"))}</div></article>'
        fibers = f'<article class="project"><div class="meta">2025 &nbsp; <span class="badge">{t("Capital Challenge Cup · Champion", "首都挑战杯 · 擂主")}</span></div><h3>{t("SmartFibers · AI-based industrial inspection", "SmartFibers · AI 工业质检")}</h3><p>{t("High-precision imaging and intelligent inspection of spandex yarn packages, awarded in the Capital Challenge Cup special competition.", "基于 AI 的氨纶丝饼高精度成像智能检测技术研究及应用，获首都挑战杯“青智未来”专项赛擂主。")}</p><div class="paper-links"><a href="https://github.com/MitakeMoca/SmartFibers-frontend">Frontend ↗</a><a href="https://github.com/MitakeMoca/SmartFibers-backend">Backend ↗</a></div></article>'
        content += section(t('Selected projects', '代表项目'), '02', star + pangu + fibers, 'projects') + contact()


    else:
        content = title('BACKGROUND / 04', t('Education & awards', '教育背景与荣誉'), t('My academic path at Beihang, from software engineering to artificial intelligence.', '从软件工程到人工智能，在北京航空航天大学的求学经历。'))
        content += section(t('Education', '教育背景'), '01', education(), 'education')
        content += section(t('Awards & recognition', '奖励与荣誉'), '02', awards(), 'awards') + contact()

    nav_items = [('home', PAGES['home']), ('research', PAGES['research']), ('experiences', PAGES['experiences']), ('mentorship', ('Mentorship', '指导与教学')), ('background', PAGES['background'])]
    nav = ''.join(f'<a href="{url(k)}" {"aria-current=page" if k == page else ""}>{val(v)}</a>' for k, v in nav_items)
    index = [('updates', t('Updates', '最新动态')), ('publications', t('Publications', '论文')), ('education', t('Education', '教育背景')), ('mentorship', t('Mentorship', '指导与教学')), ('awards', t('Awards', '荣誉'))] if page == 'home' else []
    index_html = '<nav class="page-index" aria-label="On this page">' + ''.join(f'<a href="#{k}">{v}</a>' for k, v in index) + '</nav>' if index else ''
    profile = f'<aside class="profile"><div class="avatar"><img src="{base}assets/avatar.jpg" alt="Qixuan Wu’s avatar" width="104" height="104"></div><h2>Qixuan Wu</h2><div class="role"><strong>{t("Ph.D. Student · Artificial Intelligence", "人工智能博士研究生")}</strong><strong>{t("Beihang University", "北京航空航天大学")}</strong><strong>{t("Zhongguancun Laboratory · Joint training", "中关村实验室 · 联合培养")}</strong></div><p class="location">{t("Beijing, China", "中国 · 北京")}</p><div class="profile-links"><a href="{DATA["github"]}">GitHub ↗</a><a href="mailto:{DATA["email"]}">{t("Email ↗", "邮件 ↗")}</a></div><ul class="profile-topics"><li>{t("VLA post-training", "VLA 后训练")}</li></ul>{index_html}</aside>'
    absolute = 'https://mitakemoca.github.io/' + ('zh/' if zh else '') + ('' if page == 'home' else page + '/')
    en_absolute = 'https://mitakemoca.github.io/' + ('' if page == 'home' else page + '/')
    label = 'Qixuan Wu · ' + val(PAGES[page])
    desc = t('Qixuan Wu, Ph.D. student at Beihang University, jointly trained with Zhongguancun Laboratory. VLA post-training, publications, and mentorship.', '北京航空航天大学人工智能博士研究生，与中关村实验室联合培养。VLA 后训练、论文与教学。')
    theme_init = "try{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(e){}"
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}" data-theme="light">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{E(label)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{absolute}"><link rel="alternate" hreflang="en" href="{en_absolute}"><link rel="alternate" hreflang="zh-CN" href="{en_absolute.replace('.io/', '.io/zh/')}"><meta property="og:title" content="{E(label)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{absolute}"><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><script>{theme_init}</script><link rel="stylesheet" href="{base}assets/site.css"><script defer src="{base}assets/site.js"></script><noscript><style>@media(max-width:620px){{.top-inner{{height:auto;flex-wrap:wrap;padding-top:15px}}.nav{{display:flex;position:static;order:3;width:100%;flex-direction:row;flex-wrap:wrap;padding:0 0 12px;gap:15px}}.nav a{{line-height:30px}}}}</style></noscript></head>
<body><a class="skip" href="#main">{t('Skip to content', '跳转到正文')}</a><header class="topbar"><div class="top-inner"><a class="wordmark" href="{url('home')}">Qixuan Wu<span>.</span></a><nav class="nav" id="navigation" aria-label="{t('Main navigation', '主导航')}">{nav}</nav><div class="tools"><a href="{url(page, 'en' if zh else 'zh')}" lang="{'en' if zh else 'zh-CN'}" aria-label="{t('Switch to Chinese', 'Switch to English')}">{t('中文', 'EN')}</a><button class="theme js-only" data-theme-toggle aria-label="{t('Toggle dark mode', '切换深色模式')}" aria-pressed="false" hidden>◐</button><button class="menu js-only" data-menu-toggle aria-controls="navigation" aria-expanded="false" hidden>{t('Menu', '菜单')}</button></div></div></header><div class="shell">{profile}<main id="main">{content}</main></div><footer class="footer"><span>© 2026 Qixuan Wu</span><span>{t('Last updated', '最近更新')} {DATA['updated']} &nbsp; <a href="#main">{t('Back to top ↑', '返回顶部 ↑')}</a></span></footer></body></html>'''


for lang in ('en', 'zh'):
    for page in PAGES:
        directory = OUT / ('zh' if lang == 'zh' else '') / ('' if page == 'home' else page)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(lang, page), encoding='utf-8')

# Preserve existing bookmarks while keeping teaching on the homepage.
for lang in ('en', 'zh'):
    directory = OUT / ('zh' if lang == 'zh' else '') / 'mentorship'
    directory.mkdir(parents=True, exist_ok=True)
    label = 'Continue to teaching appointments' if lang == 'en' else '查看首页助教经历'
    (directory / 'index.html').write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=../#mentorship"><meta name="robots" content="noindex"><title>{label}</title></head><body><a href="../#mentorship">{label}</a></body></html>', encoding='utf-8')

(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://mitakemoca.github.io/sitemap.xml\n')
locations = ['https://mitakemoca.github.io/' + ('zh/' if lang == 'zh' else '') + ('' if page == 'home' else page + '/') for lang in ('en','zh') for page in PAGES]
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{x}</loc><lastmod>{DATA["updated"]}</lastmod></url>' for x in locations) + '</urlset>')
(OUT / '404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Qixuan Wu</title><style>body{background:#fbfaf7;color:#22352d;font:18px/1.7 Georgia,serif;max-width:600px;margin:15vh auto;padding:24px}a{color:#25664d}</style></head><body><p>404 / PAGE NOT FOUND</p><h1>A different path, perhaps.</h1><p>This page could not be found. 这个页面暂时找不到。</p><a href="/">Back to the homepage / 返回主页 →</a></body></html>''')
print(f'Built {len(locations)} bilingual pages in {OUT}')
