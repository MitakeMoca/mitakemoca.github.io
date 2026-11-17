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
# Brand paths: Simple Icons (CC0), github.svg and xiaohongshu.svg.
CONTACT_ICONS = {'email': '<svg class="contact-icon" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></svg>', 'github': '<svg class="contact-icon" viewBox="0 0 24 24" width="17" height="17" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>', 'redbook': '<svg class="contact-icon redbook" viewBox="0 7 24 10" width="25" height="17" fill="currentColor" aria-hidden="true" focusable="false"><path d="M22.405 9.879c.002.016.01.02.07.019h.725a.797.797 0 0 0 .78-.972.794.794 0 0 0-.884-.618.795.795 0 0 0-.692.794c0 .101-.002.666.001.777zm-11.509 4.808c-.203.001-1.353.004-1.685.003a2.528 2.528 0 0 1-.766-.126.025.025 0 0 0-.03.014L7.7 16.127a.025.025 0 0 0 .01.032c.111.06.336.124.495.124.66.01 1.32.002 1.981 0 .01 0 .02-.006.023-.015l.712-1.545a.025.025 0 0 0-.024-.036zM.477 9.91c-.071 0-.076.002-.076.01a.834.834 0 0 0-.01.08c-.027.397-.038.495-.234 3.06-.012.24-.034.389-.135.607-.026.057-.033.042.003.112.046.092.681 1.523.787 1.74.008.015.011.02.017.02.008 0 .033-.026.047-.044.147-.187.268-.391.371-.606.306-.635.44-1.325.486-1.706.014-.11.021-.22.03-.33l.204-2.616.022-.293c.003-.029 0-.033-.03-.034zm7.203 3.757a1.427 1.427 0 0 1-.135-.607c-.004-.084-.031-.39-.235-3.06a.443.443 0 0 0-.01-.082c-.004-.011-.052-.008-.076-.008h-1.48c-.03.001-.034.005-.03.034l.021.293c.076.982.153 1.964.233 2.946.05.4.186 1.085.487 1.706.103.215.223.419.37.606.015.018.037.051.048.049.02-.003.742-1.642.804-1.765.036-.07.03-.055.003-.112zm3.861-.913h-.872a.126.126 0 0 1-.116-.178l1.178-2.625a.025.025 0 0 0-.023-.035l-1.318-.003a.148.148 0 0 1-.135-.21l.876-1.954a.025.025 0 0 0-.023-.035h-1.56c-.01 0-.02.006-.024.015l-.926 2.068c-.085.169-.314.634-.399.938a.534.534 0 0 0-.02.191.46.46 0 0 0 .23.378.981.981 0 0 0 .46.119h.59c.041 0-.688 1.482-.834 1.972a.53.53 0 0 0-.023.172.465.465 0 0 0 .23.398c.15.092.342.12.475.12l1.66-.001c.01 0 .02-.006.023-.015l.575-1.28a.025.025 0 0 0-.024-.035zm-6.93-4.937H3.1a.032.032 0 0 0-.034.033c0 1.048-.01 2.795-.01 6.829 0 .288-.269.262-.28.262h-.74c-.04.001-.044.004-.04.047.001.037.465 1.064.555 1.263.01.02.03.033.051.033.157.003.767.009.938-.014.153-.02.3-.06.438-.132.3-.156.49-.419.595-.765.052-.172.075-.353.075-.533.002-2.33 0-4.66-.007-6.991a.032.032 0 0 0-.032-.032zm11.784 6.896c0-.014-.01-.021-.024-.022h-1.465c-.048-.001-.049-.002-.05-.049v-4.66c0-.072-.005-.07.07-.07h.863c.08 0 .075.004.075-.074V8.393c0-.082.006-.076-.08-.076h-3.5c-.064 0-.075-.006-.075.073v1.445c0 .083-.006.077.08.077h.854c.075 0 .07-.004.07.07v4.624c0 .095.008.084-.085.084-.37 0-1.11-.002-1.304 0-.048.001-.06.03-.06.03l-.697 1.519s-.014.025-.008.036c.006.01.013.008.058.008 1.748.003 3.495.002 5.243.002.03-.001.034-.006.035-.033v-1.539zm4.177-3.43c0 .013-.007.023-.02.024-.346.006-.692.004-1.037.004-.014-.002-.022-.01-.022-.024-.005-.434-.007-.869-.01-1.303 0-.072-.006-.071.07-.07l.733-.003c.041 0 .081.002.12.015.093.025.16.107.165.204.006.431.002 1.153.001 1.153zm2.67.244a1.953 1.953 0 0 0-.883-.222h-.18c-.04-.001-.04-.003-.042-.04V10.21c0-.132-.007-.263-.025-.394a1.823 1.823 0 0 0-.153-.53 1.533 1.533 0 0 0-.677-.71 2.167 2.167 0 0 0-1-.258c-.153-.003-.567 0-.72 0-.07 0-.068.004-.068-.065V7.76c0-.031-.01-.041-.046-.039H17.93s-.016 0-.023.007c-.006.006-.008.012-.008.023v.546c-.008.036-.057.015-.082.022h-.95c-.022.002-.028.008-.03.032v1.481c0 .09-.004.082.082.082h.913c.082 0 .072.128.072.128V11.19s.003.117-.06.117h-1.482c-.068 0-.06.082-.06.082v1.445s-.01.068.064.068h1.457c.082 0 .076-.006.076.079v3.225c0 .088-.007.081.082.081h1.43c.09 0 .082.007.082-.08v-3.27c0-.029.006-.035.033-.035l2.323-.003c.098 0 .191.02.28.061a.46.46 0 0 1 .274.407c.008.395.003.79.003 1.185 0 .259-.107.367-.33.367h-1.218c-.023.002-.029.008-.028.033.184.437.374.871.57 1.303a.045.045 0 0 0 .04.026c.17.005.34.002.51.003.15-.002.517.004.666-.01a2.03 2.03 0 0 0 .408-.075c.59-.18.975-.698.976-1.313v-1.981c0-.128-.01-.254-.034-.38 0 .078-.029-.641-.724-.998z"/></svg>'}


def render(language):
    zh = language == 'zh'
    t = lambda en, cn: cn if zh else en
    val = lambda values: values[int(zh)]
    base = '../' if zh else './'
    asset = lambda name: base + 'assets/' + name + '?v=' + SITE_VERSION
    home = lambda lang: base + ('zh/' if lang == 'zh' else '') + '?v=' + SITE_VERSION

    def section(heading, id_, body):
        return f'<section class="section" id="{id_}"><h2>{heading}</h2>{body}</section>'

    def date_label(value):
        # Keep each month/year together; a range may wrap only between endpoints.
        parts = value.split(' — ', 1)
        content = f'<span class="date-part">{E(parts[0])}</span>'
        if len(parts) == 2:
            content += f' <span class="date-part">— {E(parts[1])}</span>'
        kind = ' date-range' if len(parts) == 2 else ''
        return f'<time class="date-label{kind}">{content}</time>'

    def update(item, older=False):
        body = E(val(item['text']))
        for name in item.get('people', []):
            body = body.replace(E(name), f'<span class="person-name">{E(name)}</span>')
        for word in ('Champion', 'Oral', '擂主'):
            body = body.replace(word, f'<strong>{word}</strong>')
        papers = ''.join(f'<li>{E(name)}</li>' for name in item.get('papers', []))
        if papers:
            body += f'<ul class="update-papers">{papers}</ul>'
        return f'<article class="update" {"data-older-update" if older else ""}>{date_label(item["date"])}<div>{body}</div></article>'

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
        education.append(f'<article class="timeline-row mini-edu">{date_label(val(item["date"]))}<div><h3>{E(val(item["degree"]))}</h3><p class="school">{school}</p><p class="detail">{E(val(item["detail"]))}</p></div></article>')

    experience = f'<article class="timeline-row">{date_label("2026.11 — " + t("Present", "至今"))}<div><h3 class="company-heading"><img class="company-logo" src="{asset("baidu-logo.png")}" alt="Baidu logo" width="90" height="32"><span>{t("Baidu", "百度")}</span></h3><p class="job">{t("Embodied Intelligence", "具身智能")}</p><p class="detail">{t("Research on VLA post-training for embodied intelligence.", "围绕具身智能开展 VLA 后训练研究。")}</p></div></article>'
    projects = f'''<details class="project-details"><summary><span class="when-closed">{t('Show projects (3)', '展开项目（3）')}</span><span class="when-open">{t('Hide projects', '收起项目')}</span><span class="chevron" aria-hidden="true">⌄</span></summary><div class="project-list">
<article><h3>StarOps · {t('Intelligent operations for Kylin', '星维管家')}</h3><p>{t('Built a system-level agent for the Kylin operating system, integrating monitoring, anomaly diagnosis, automated optimisation, MCP-compatible services, and log anomaly detection.', '面向银河麒麟操作系统构建系统级 Agent，集成状态监控、异常诊断与自动调优，开发符合 MCP 协议的系统接口与日志异常检测算法。')}</p><a href="https://github.com/Kylin-StarOps-Team/StarOps">{t('Source code ↗', '项目代码 ↗')}</a></article>
<article><h3>{t('Low-precision adaptation · Huawei Pangu', '低精度模型适配 · 华为盘古')}</h3><p>{t('Reproduced L4Q and adapted MXFP8 training schemes, investigating quantization-aware PEFT under limited compute and memory budgets.', '复现 L4Q，适配 MXFP8 训练方案，在有限算力与显存条件下探索量化感知 PEFT。')}</p></article>
<article><h3>SmartFibers · {t('AI-based industrial inspection', 'AI 工业质检')}</h3><p>{t('High-precision imaging and intelligent inspection of spandex yarn packages, awarded in the Capital Challenge Cup special competition.', '基于 AI 的氨纶丝饼高精度成像与智能检测技术研究及应用，获首都挑战杯“青智未来”专项赛擂主。')}</p><div class="project-links"><a href="https://github.com/MitakeMoca/SmartFibers-frontend">Frontend ↗</a><a href="https://github.com/MitakeMoca/SmartFibers-backend">Backend ↗</a></div></article>
</div></details>'''

    courses = []
    for course in DATA['courses']:
        role = f'<span class="ta-note"> · {t("Head TA", "助教组长")}</span>' if course.get('lead') else ''
        repo = f' <a class="ta-repo" href="{E(course["repo"])}">{t("Repository ↗", "教学仓库 ↗")}</a>' if course.get('repo') else ''
        courses.append(f'<div class="ta-row" data-home-course>{date_label(val(course["term"]))}<div>{E(val(course["title"]))}{role}{repo}</div></div>')
    mentorship = f'<p class="ta-heading">{t("Teaching Assistant · Beihang University", "课程助教 · 北京航空航天大学")}</p><div class="ta-list">{"".join(courses)}</div>'
    awards = ''.join(f'<article class="timeline-row award-row">{date_label(item["year"])}<div><h3>{E(val(item["title"]))}</h3><p class="detail">{E(val(item["detail"]))}</p></div></article>' for item in DATA['awards'])

    intro = t('I am a Ph.D. student in Artificial Intelligence at <a href="https://www.buaa.edu.cn/">Beihang University</a>, jointly trained with Zhongguancun Laboratory and advised by Prof. Baochang Zhang.', '我是北京航空航天大学人工智能专业博士研究生，与中关村实验室联合培养，导师为张宝昌教授。')
    about = f'<section class="about" id="about"><h1>{t("About", "关于我")}</h1><p>{intro}</p><p>{t("My research focuses on", "我的研究方向是")} <strong>{t("VLA post-training", "VLA 后训练")}</strong>。</p></section>'
    if not zh:
        about = about.replace('</strong>。</p>', '</strong>.</p>')
    content = about + section('Updates' if not zh else '最新动态', 'updates', recent)
    content += section(t('Publications', '论文'), 'publications', publications)
    content += section(t('Education', '教育背景'), 'education', ''.join(education))
    content += section(t('Experiences', '研究经历'), 'experiences', experience)
    content += section(t('Projects', '项目'), 'projects', projects)
    content += section(t('Mentorship', '指导与教学'), 'mentorship', mentorship)
    content += section(t('Awards', '奖励与荣誉'), 'awards', awards)
    nav = ''.join(f'<a href="#{id_}">{heading}</a>' for id_, heading in [('about', t('About', '关于我')), ('updates', 'Updates'), ('publications', t('Publications', '论文')), ('education', t('Education', '教育')), ('experiences', t('Experiences', '经历'))])
    contacts = f'''<a class="contact-link" href="mailto:{E(DATA['email'])}">{CONTACT_ICONS['email']}<span>{t('Email', '邮件')}</span></a><a class="contact-link" href="{E(DATA['github'])}">{CONTACT_ICONS['github']}<span>GitHub</span></a><a class="contact-link" href="{E(DATA['xiaohongshu']['url'])}" title="{E(DATA['xiaohongshu']['name'])}" aria-label="小红书 Red Book：{E(DATA['xiaohongshu']['name'])}">{CONTACT_ICONS['redbook']}<span>小红书 Red Book</span></a>'''
    profile = f'''<header class="profile"><img class="avatar" src="{asset('avatar.jpg')}" alt="Qixuan Wu’s avatar" width="112" height="112"><div class="profile-info"><h2>Qixuan Wu <span class="nickname">(Moca)</span></h2><p class="role">{t('Ph.D. Student · Artificial Intelligence', '人工智能博士研究生')}</p><p class="affiliation">{t('Beihang University', '北京航空航天大学')} · {t('Zhongguancun Laboratory · Joint training', '中关村实验室 · 联合培养')}</p><div class="profile-links"><span class="location">{t('Beijing, China', '中国 · 北京')}</span>{contacts}</div></div></header>'''
    canonical = 'https://mitakemoca.github.io/' + ('zh/' if zh else '')
    description = t('Qixuan Wu: VLA post-training, publications, education, research experience, and teaching at Beihang University.', 'VLA 后训练、学术论文、教育背景、研究经历与课程教学。')
    theme_init = "document.documentElement.classList.add('js');try{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(e){}"
    return f'''<!doctype html><html lang="{'zh-CN' if zh else 'en'}" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="site-version" content="{SITE_VERSION}"><meta name="color-scheme" content="light dark"><title>Qixuan Wu · {t('Homepage', '主页')}</title><meta name="description" content="{E(description)}"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="https://mitakemoca.github.io/"><link rel="alternate" hreflang="zh-CN" href="https://mitakemoca.github.io/zh/"><meta property="og:title" content="Qixuan Wu · Homepage"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml"><script>{theme_init}</script><link rel="stylesheet" href="{asset('home.css')}"><script defer src="{asset('home.js')}"></script></head><body id="top"><a class="skip" href="#main">{t('Skip to content', '跳转到正文')}</a><header class="topbar"><div class="top-inner"><a class="wordmark" href="#top">{t('Home', '首页')}</a><nav class="nav" id="navigation" aria-label="{t('Main navigation', '主导航')}">{nav}</nav><div class="tools"><a class="language" href="{home('en' if zh else 'zh')}" aria-label="{t('Switch to Chinese', 'Switch to English')}">{t('中文', 'EN')}</a><button class="theme" data-theme-toggle aria-label="{t('Toggle dark mode', '切换深色模式')}" aria-pressed="false" hidden>◐</button><button class="menu" data-menu-toggle aria-controls="navigation" aria-expanded="false" hidden>{t('Menu', '菜单')}</button></div></div></header><div class="shell">{profile}<main id="main">{content}</main></div><footer class="footer"><span>© 2026 Qixuan Wu</span><span>{t('Updated', '最近更新')} <time class="footer-date" datetime="{E(DATA['updated'])}">{E(DATA['updated'])}</time> <a href="#top">{t('Back to top ↑', '返回顶部 ↑')}</a></span></footer></body></html>'''


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
