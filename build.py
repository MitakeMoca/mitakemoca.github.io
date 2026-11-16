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
PAGES = {'home': ('Home', '主页'), 'research': ('Research', '研究'), 'experiences': ('Experiences', '经历'), 'mentorship': ('Mentorship', '指导与教学'), 'background': ('Background', '教育与荣誉')}


def render(language, page):
    zh = language == 'zh'
    idx = int(zh)
    t = lambda en, cn: cn if zh else en
    val = lambda value: value[idx]
    depth = (1 if zh else 0) + (0 if page == 'home' else 1)
    base = '../' * depth or './'

    def url(name, lang=None):
        lang = language if lang is None else lang
        return base + ('zh/' if lang == 'zh' else '') + ('' if name == 'home' else name + '/')

    def link(name, text):
        return f'<a class="text-link" href="{url(name)}">{text}<span aria-hidden="true">↗</span></a>'

    def section(title, number, content, id_, destination=None, more=None):
        right = link(destination, more or t('View all', '查看全部')) if destination else ''
        return f'<section class="section" id="{id_}"><div class="section-head"><h2><span class="number">{number}</span>{title}</h2>{right}</div>{content}</section>'

    def title(label, heading, desc, topics=''):
        return f'<header class="page-title"><div class="eyebrow"><span class="dot"></span>{label}</div><h1>{heading}</h1><p>{desc}</p>{topics}</header>'

    def education():
        return ''.join(f'<article class="mini-edu"><time>{E(val(x["date"]))}</time><div><h3>{E(val(x["degree"]))}</h3><div class="school">{t("Beihang University", "北京航空航天大学")}</div><p>{E(val(x["detail"]))}</p></div></article>' for x in DATA['education'])

    def awards(limit=None):
        return ''.join(f'<article class="award-row"><span class="award-year">{E(x["year"])}</span><div><h3>{E(val(x["title"]))}</h3><p>{E(val(x["detail"]))}</p></div></article>' for x in DATA['awards'][:limit])

    def publication(detailed=False):
        p = DATA['publication']
        author = E(p['authors']).replace('Qixuan Wu', '<strong>Qixuan Wu</strong>')
        bars = ''.join(f'<i style="height:{h}px"></i>' for h in [23, 40, 31, 56, 34, 47, 26, 51])
        art = f'<div class="paper-art" aria-hidden="true"><div class="art-label">S³-LoRA</div><div class="sample-bars">{bars}</div><div class="art-caption">score → sample → adapt</div></div>'
        description = f'<p class="abstract">{E(val(p["description"]))}</p>'
        metrics = ''
        if detailed:
            metrics = f'<div class="metrics"><div class="metric"><strong>1.3–1.4×</strong><span>{t("training speedup vs. LoRA", "相对标准 LoRA 的训练加速")}</span></div><div class="metric"><strong>88.9 → 89.7</strong><span>{t("LLaMA3-8B · GLUE average", "LLaMA3-8B · GLUE 均分")}</span></div></div>'
        return f'<article class="publication">{art}<div><div class="meta">ACM MULTIMEDIA 2026 &nbsp; <span class="badge">{t("Accepted · Co-first author", "已录用 · 共同第一作者")}</span></div><h3>{E(p["title"])}</h3><p class="authors">{author}</p>{description}<div class="paper-links"><a href="{p["url"]}">{t("Conference programme ↗", "会议日程 ↗")}</a>{link("research", t("Research details", "研究详情")) if not detailed else ''}</div>{metrics}</div></article>'

    def baidu():
        return f'<article class="experience"><div class="date">2026.11<br>— {t("Present", "至今")}</div><div><h3>{t("Baidu", "百度")}</h3><div class="job">{t("Agentic Embodied Intelligence", "Agentic 具身智能")}</div><p>{t("Research in Agentic embodied intelligence.", "开展 Agentic 具身智能方向研究。")}</p></div></article>'

    def explore():
        options = [('research', t('Efficient adaptation, temporal memory, and selected research.', '高效适配、时序记忆与研究工作。')), ('mentorship', t('Teaching, student research, and open learning resources.', '课程教学、科研指导与开源学习资源。')), ('experiences', t('Industry research and projects built from ideas to systems.', '产业研究与从方法走向系统的项目。')), ('background', t('Education, academic milestones, and awards.', '教育背景、学习经历与荣誉。'))]
        return '<div class="explore-grid">' + ''.join(f'<a class="explore-item" href="{url(k)}"><h3>{val(PAGES[k])}<span aria-hidden="true">↗</span></h3><p>{d}</p></a>' for k, d in options) + '</div>'

    def contact():
        return f'<section class="contact" id="contact"><div class="eyebrow">{t("KEEP IN TOUCH", "保持联系")}</div><h2 style="margin-top:12px">{t("Let’s exchange ideas.", "欢迎交流。")}</h2><p>{t("For research, collaboration, or questions about the teaching materials:", "如果你想交流研究、探讨合作，或讨论教学资料：")}<br><a href="mailto:{DATA["email"]}">{DATA["email"]}</a> &nbsp; / &nbsp; <a href="{DATA["github"]}">GitHub ↗</a></p></section>'

    if page == 'home':
        content = f'<header class="hero"><div class="eyebrow"><span class="dot"></span>{t("BEIHANG UNIVERSITY · AI RESEARCH", "北京航空航天大学 · 人工智能研究")}</div><h1>Qixuan Wu<small>吴奇宣</small></h1><p class="hero-line">{t("Efficient learning.<br><em>Intelligent action.</em>", "高效地学习，<br><em>智能地行动。</em>")}</p><p class="intro">{t("I’m a Ph.D. student in Artificial Intelligence at <a href=\"https://www.buaa.edu.cn/\">Beihang University</a>, advised by <strong>Prof. Baochang Zhang</strong>. My research connects efficient model adaptation with embodied intelligence, with a focus on low-rank fine-tuning, temporal memory for VLA models, and intelligent agents.", "我是北京航空航天大学人工智能专业博士研究生，导师为<strong>张宝昌教授</strong>。我关注高效模型适配与具身智能，研究兴趣包括低秩微调、VLA 模型的时序记忆，以及智能体系统。")}</p><div class="hero-bottom">{link("research", t("Explore my research", "了解我的研究"))}<span class="annotation">{t("BASED IN BEIJING, CHINA", "中国 · 北京")}</span></div></header>'
        updates = ''.join(f'<article class="update" {"data-older-update" if n >= 4 else ""}><time>{E(x["date"])}</time><div><span class="kind">{E(val(x["type"]))}</span><a href="{url(x["page"])}">{E(val(x["text"]))}</a></div></article>' for n, x in enumerate(DATA['updates']))
        updates += f'<button class="plain-button" data-more-updates aria-expanded="false" data-more="{t("Show earlier updates ↓", "展开往期动态 ↓")}" data-less="{t("Show fewer updates ↑", "收起往期动态 ↑")}" hidden>{t("Show earlier updates ↓", "展开往期动态 ↓")}</button>'
        content += section(t('Updates', '最新动态'), '01', updates, 'updates')
        content += section(t('Selected publication', '代表论文'), '02', publication(), 'publications', 'research', t('All research', '全部研究'))
        content += section(t('Experiences', '研究经历'), '03', baidu(), 'experiences', 'experiences', t('Projects & experience', '经历与项目'))
        content += section('Education' if not zh else '教育背景', '04', education(), 'education', 'background')
        m = f'<div class="mentorship-callout"><div><p>{t("I have served as a teaching assistant across eight course offerings at Beihang since 2023, including two as head TA. I also support student research on intelligent credit evaluation and share programming resources openly.", "自 2023 年起，我在北航累计参与八门次课程助教工作，其中两次担任助教组长。同时参与企业信用评价方向的学生科研指导，并开源编程课程学习资料。")}</p><div style="margin-top:18px">{link("mentorship", t("Teaching & mentorship", "课程教学与科研指导"))}</div></div><div class="big-stat"><strong>08</strong><span>{t("course offerings", "课程助教经历")}</span></div></div>'
        content += section('Mentorship' if not zh else '指导与教学', '05', m, 'mentorship')
        content += section(t('Selected awards', '代表荣誉'), '06', awards(3), 'awards', 'background')
        content += section(t('Explore further', '更多专题'), '07', explore(), 'explore') + contact()

    elif page == 'research':
        content = title('RESEARCH / 01', t('Research & publications', '研究与论文'), t('Making adaptation more efficient, and giving embodied policies a useful memory.', '让模型适配更高效，让具身策略用好历史记忆。'), '<div class="topic-strip"><span>PEFT / LoRA</span><span>VLA / MEMORY</span><span>LOW-PRECISION TRAINING</span></div>')
        content += section(t('Publications', '已录用论文'), '01', publication(True), 'publications')
        desc = t('VLA post-training & temporal memory', 'VLA 后训练与时序记忆建模')
        note = f'<div class="meta">{t("ICLR 2027 · Under review · First author", "ICLR 2027 · 在投 · 第一作者")}</div><h3>{desc}</h3><div class="research-note"><div><p>{t("A robot’s current observation can hide information that matters for its next action. This work explores lightweight temporal memory while keeping the pretrained VLA backbone and action expert frozen.", "机器人的当前观测可能缺少决定后续动作的关键信息。这项研究在冻结预训练 VLA 主干与动作专家的条件下，通过轻量后训练引入时序记忆。")}</p><p>{t("An external video encoder writes observed history into a fixed-capacity recurrent memory. Action-conditioned retrieval supplies a constrained residual before the final action head, without appending historical frames to the backbone context.", "使用外部视频编码器，将已观测历史写入固定容量递归记忆；通过动作条件检索，在最终动作头前注入受约束的残差特征，无需向主干上下文追加历史帧。")}</p><div class="metrics"><div class="metric"><strong>87.12 → 89.80%</strong><span>{t("RoboTwin success rate · 50 tasks · 5,000 evaluations", "RoboTwin 成功率 · 50 项任务 · 5,000 次评测")}</span></div></div></div><figure class="flow"><div>{t("Observed visual history", "已观测视觉历史")}</div><span aria-hidden="true">↓</span><div>{t("Fixed-capacity memory", "固定容量时序记忆")}</div><span aria-hidden="true">↓</span><div>{t("Action-conditioned retrieval", "动作条件检索")}</div><span aria-hidden="true">↓</span><div>{t("Residual → Action head", "残差适配 → 动作头")}</div><figcaption>{t("Conceptual overview of the research direction.", "研究方法概念示意。")}</figcaption></figure></div>'
        content += section(t('Ongoing research', '在研工作'), '02', note, 'ongoing')
        content += section(t('Low-bit adaptation', '低比特适配'), '03', f'<article class="project" style="padding-top:0"><div class="meta">{t("HUAWEI PANGU · PROJECT RESEARCH", "华为盘古大模型 · 项目研究")}</div><h3>{t("Quantization-aware parameter-efficient fine-tuning", "量化感知的参数高效微调")}</h3><p>{t("Reproduced L4Q and adapted MXFP8 training configurations for the Pangu framework. Studied how quantization error interacts with low-rank updates, with comparative experiments on convergence, downstream performance, and training stability.", "完成 L4Q 复现与盘古训练框架适配，推进 MXFP8 低精度训练方案的配置与验证。通过对比实验研究量化误差与低秩更新的相互影响，分析收敛表现、下游性能与训练稳定性。")}</p></article>', 'low-bit') + contact()

    elif page == 'experiences':
        content = title('EXPERIENCES / 02', t('From methods to systems.', '从方法走向系统。'), t('Research in embodied intelligence, efficient adaptation, and practical agent systems.', '在具身智能、高效适配与智能体系统中开展研究和实践。'))
        content += section(t('Industry research', '产业研究'), '01', baidu(), 'industry')
        star = f'<article class="project" style="padding-top:0"><div class="meta">2025.05 — 2025.10 &nbsp; <span class="badge">{t("National Champion · Challenge Cup", "挑战杯 · 全国擂主")}</span></div><h3>StarOps · {t("Intelligent operations for Kylin", "星维管家")}</h3><p>{t("Built a system-level agent for the Kylin operating system, connecting monitoring, anomaly diagnosis, and system optimisation in an automated loop.", "面向银河麒麟操作系统，构建集系统状态监控、异常诊断与自动调优于一体的系统级 Agent。")}</p><ul><li>{t("Designed and implemented a GUI assistant with anomaly detection, root-cause chain analysis, tuning, and system Q&A.", "设计并实现 GUI 智能管家，集成异常检测、异常链路分析、自动调优与系统问答。")}</li><li>{t("Exposed system services through MCP-compatible interfaces for integration with Kylin’s model assistant.", "构建符合 MCP 协议的系统接口，对接麒麟操作系统的大模型助手。")}</li><li>{t("Developed a log anomaly detector combining BERT representations, a semantic projector, and a LLaMA decoder.", "实现结合 BERT 编码、语义空间对齐与 LLaMA 解码的日志异常检测算法。")}</li></ul><div class="paper-links"><a href="https://github.com/Kylin-StarOps-Team/StarOps">{t("Source code ↗", "项目代码 ↗")}</a></div></article>'
        pangu = f'<article class="project"><div class="meta">{t("HUAWEI PANGU · MODEL ADAPTATION", "华为盘古大模型 · 模型适配")}</div><h3>{t("Low-precision fine-tuning", "低精度微调")}</h3><p>{t("Reproduced L4Q and adapted MXFP8 training schemes, investigating quantization-aware PEFT under limited compute and memory budgets.", "复现 L4Q，适配 MXFP8 训练方案，在有限算力与显存条件下探索量化感知 PEFT。")}</p><div class="paper-links">{link("research", t("Research details", "研究详情"))}</div></article>'
        fibers = f'<article class="project"><div class="meta">2025 &nbsp; <span class="badge">{t("Capital Challenge Cup · Champion", "首都挑战杯 · 擂主")}</span></div><h3>{t("SmartFibers · AI-based industrial inspection", "SmartFibers · AI 工业质检")}</h3><p>{t("High-precision imaging and intelligent inspection of spandex yarn packages, awarded in the Capital Challenge Cup special competition.", "基于 AI 的氨纶丝饼高精度成像智能检测技术研究及应用，获首都挑战杯“青智未来”专项赛擂主。")}</p><div class="paper-links"><a href="https://github.com/MitakeMoca/SmartFibers-frontend">Frontend ↗</a><a href="https://github.com/MitakeMoca/SmartFibers-backend">Backend ↗</a></div></article>'
        content += section(t('Selected projects', '代表项目'), '02', star + pangu + fibers, 'projects') + contact()

    elif page == 'mentorship':
        content = title('MENTORSHIP / 03', t('Teaching & growing together.', '在教学中共同成长。'), t('Course teaching, research guidance, and learning resources at Beihang University.', '北京航空航天大学课程助教、学生科研指导与开放学习资源。'))
        content += f'<div class="summary-stats"><div><strong>08</strong><span>{t("TA appointments", "课程助教经历")}</span></div><div><strong>02</strong><span>{t("head TA appointments", "助教组长经历")}</span></div><div><strong>2023—</strong><span>{t("teaching since", "开始参与课程教学")}</span></div></div>'
        rows = ''
        for course in DATA['courses']:
            extra = ''
            if course.get('award'):
                extra = f'<p>{t("Outstanding Teaching Assistant · Beihang College", "获评北航学院优秀助教")}</p>'
            if course.get('repo'):
                extra = f'<p><a href="{course["repo"]}">{t("Open teaching repository ↗", "开源教学仓库 ↗")}</a></p>'
            rows += f'<article class="course" data-course data-lead="{str(course["lead"]).lower()}"><time>{E(val(course["term"]))}</time><div><h3>{E(val(course["title"]))}</h3>{extra}</div><span class="course-role">{t("Head TA", "助教组长") if course["lead"] else t("Teaching Assistant", "课程助教")}</span></article>'
        filters = f'<div class="filters js-only" hidden aria-label="{t("Filter teaching appointments", "筛选助教经历")}"><button class="filter" data-filter="all" aria-pressed="true">{t("All 8 appointments", "全部 8 门次")}</button><button class="filter" data-filter="lead" aria-pressed="false">{t("Head TA · 2", "助教组长 · 2")}</button></div>'
        content += section(t('Course teaching', '课程教学'), '01', filters + rows, 'courses')
        research = f'<article class="project" style="padding-top:0"><div class="meta">{t("QINGHAI SCIENCE & TECHNOLOGY PROJECT · 2025-GX-143", "青海省科技厅项目 · 2025-GX-143")}</div><h3>{t("Intelligent enterprise credit evaluation", "企业信用评价智能化")}</h3><p>{t("As the project lead, I guided two research studies on credit evaluation using structured financial indicators and unstructured risk disclosures. My work covered research design, feature modelling, method selection, experimental design, and manuscript revision.", "担任项目主要负责人，围绕结构化财务指标与非结构化风险披露文本，开展企业信用评价研究。主要负责研究方案设计与技术指导，指导两项研究的特征建模、方法选择与实验设计，并参与结果分析和论文修改。")}</p><p>{t("Supported by Qinghai’s Key R&D and Achievement Transformation Programme.", "项目获青海省重点研发与成果转化计划资助。")}</p></article>'
        content += section(t('Research mentorship', '科研指导'), '02', research, 'research-mentorship')
        resource = f'<a class="resource" href="https://github.com/MitakeMoca/BUAA_DS"><h3>BUAA_DS <span aria-hidden="true">↗</span></h3><p>{t("Reference implementations for Beihang’s Data Structures course. Open materials for studying algorithms and programming.", "北航数据结构课程部分参考代码，为算法和编程学习提供开放资料。")}</p><div class="meta">C / DATA STRUCTURES / OPEN SOURCE</div></a>'
        content += section(t('Open learning resources', '开放学习资源'), '03', resource, 'resources') + contact()

    else:
        content = title('BACKGROUND / 04', t('Education & awards', '教育背景与荣誉'), t('My academic path at Beihang, from software engineering to artificial intelligence.', '从软件工程到人工智能，在北京航空航天大学的求学经历。'))
        content += section(t('Education', '教育背景'), '01', education(), 'education')
        content += section(t('Awards & recognition', '奖励与荣誉'), '02', awards(), 'awards') + contact()

    nav = ''.join(f'<a href="{url(k)}" {"aria-current=page" if k == page else ""}>{val(v)}</a>' for k, v in PAGES.items())
    index = [('updates', t('Updates', '最新动态')), ('publications', t('Publications', '论文')), ('education', t('Education', '教育背景')), ('mentorship', t('Mentorship', '指导与教学')), ('awards', t('Awards', '荣誉'))] if page == 'home' else []
    index_html = '<nav class="page-index" aria-label="On this page">' + ''.join(f'<a href="#{k}">{v}</a>' for k, v in index) + '</nav>' if index else ''
    profile = f'<aside class="profile"><div class="avatar"><img src="{base}assets/avatar.jpg" alt="{t('Qixuan Wu’s avatar', '吴奇宣的头像')}" width="104" height="104"></div><h2>Qixuan Wu</h2><p class="native-name">吴奇宣</p><div class="role"><strong>{t("Ph.D. Student · Artificial Intelligence", "人工智能博士研究生")}</strong><strong>{t("Beihang University", "北京航空航天大学")}</strong></div><p class="location">{t("Beijing, China", "中国 · 北京")}</p><div class="profile-links"><a href="{DATA["github"]}">GitHub ↗</a><a href="mailto:{DATA["email"]}">{t("Email ↗", "邮件 ↗")}</a></div><ul class="profile-topics"><li>{t("Efficient model adaptation", "高效模型适配")}</li><li>{t("Embodied intelligence", "具身智能")}</li><li>{t("Agent systems", "智能体系统")}</li></ul>{index_html}</aside>'
    absolute = 'https://mitakemoca.github.io/' + ('zh/' if zh else '') + ('' if page == 'home' else page + '/')
    en_absolute = 'https://mitakemoca.github.io/' + ('' if page == 'home' else page + '/')
    label = 'Qixuan Wu · ' + val(PAGES[page])
    desc = t('Qixuan Wu, Ph.D. student at Beihang University. Efficient adaptation, embodied intelligence, research, and mentorship.', '吴奇宣，北京航空航天大学人工智能博士研究生。高效模型适配、具身智能、研究与教学。')
    theme_init = "try{document.documentElement.dataset.theme=localStorage.getItem('theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(e){}"
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}" data-theme="light">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{E(label)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{absolute}"><link rel="alternate" hreflang="en" href="{en_absolute}"><link rel="alternate" hreflang="zh-CN" href="{en_absolute.replace('.io/', '.io/zh/')}"><meta property="og:title" content="{E(label)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{absolute}"><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><script>{theme_init}</script><link rel="stylesheet" href="{base}assets/site.css"><script defer src="{base}assets/site.js"></script><noscript><style>@media(max-width:620px){{.top-inner{{height:auto;flex-wrap:wrap;padding-top:15px}}.nav{{display:flex;position:static;order:3;width:100%;flex-direction:row;flex-wrap:wrap;padding:0 0 12px;gap:15px}}.nav a{{line-height:30px}}}}</style></noscript></head>
<body><a class="skip" href="#main">{t('Skip to content', '跳转到正文')}</a><header class="topbar"><div class="top-inner"><a class="wordmark" href="{url('home')}">Qixuan Wu<span>.</span></a><nav class="nav" id="navigation" aria-label="{t('Main navigation', '主导航')}">{nav}</nav><div class="tools"><a href="{url(page, 'en' if zh else 'zh')}" lang="{'en' if zh else 'zh-CN'}" aria-label="{t('Switch to Chinese', 'Switch to English')}">{t('中文', 'EN')}</a><button class="theme js-only" data-theme-toggle aria-label="{t('Toggle dark mode', '切换深色模式')}" aria-pressed="false" hidden>◐</button><button class="menu js-only" data-menu-toggle aria-controls="navigation" aria-expanded="false" hidden>{t('Menu', '菜单')}</button></div></div></header><div class="shell">{profile}<main id="main">{content}</main></div><footer class="footer"><span>© 2026 Qixuan Wu · 吴奇宣</span><span>{t('Last updated', '最近更新')} {DATA['updated']} &nbsp; <a href="#main">{t('Back to top ↑', '返回顶部 ↑')}</a></span></footer></body></html>'''


for lang in ('en', 'zh'):
    for page in PAGES:
        directory = OUT / ('zh' if lang == 'zh' else '') / ('' if page == 'home' else page)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(lang, page), encoding='utf-8')

(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://mitakemoca.github.io/sitemap.xml\n')
locations = ['https://mitakemoca.github.io/' + ('zh/' if lang == 'zh' else '') + ('' if page == 'home' else page + '/') for lang in ('en','zh') for page in PAGES]
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{x}</loc><lastmod>{DATA["updated"]}</lastmod></url>' for x in locations) + '</urlset>')
(OUT / '404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Qixuan Wu</title><style>body{background:#fbfaf7;color:#22352d;font:18px/1.7 Georgia,serif;max-width:600px;margin:15vh auto;padding:24px}a{color:#25664d}</style></head><body><p>404 / PAGE NOT FOUND</p><h1>A different path, perhaps.</h1><p>This page could not be found. 这个页面暂时找不到。</p><a href="/">Back to the homepage / 返回主页 →</a></body></html>''')
print(f'Built {len(locations)} bilingual pages in {OUT}')
