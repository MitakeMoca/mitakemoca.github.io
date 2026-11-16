# Qixuan Wu · 吴奇宣

为 `https://mitakemoca.github.io` 制作的中英双语学术主页。纯静态 HTML / CSS / JavaScript，无前端依赖、无外部字体、无追踪脚本。

包含主页、Research、Experiences、Mentorship、Education & Awards。中文版本位于 `/zh/`。

## 本地查看

已经生成的 `dist/` 可直接部署，无需重新构建。建议通过本地 HTTP 服务查看：

```sh
python3 -m http.server 4173 --directory dist
```

打开 `http://localhost:4173`，中文版本为 `http://localhost:4173/zh/`。

修改内容后，使用 **Python 3.12 或更新版本**重新生成页面：

```sh
python3.12 build.py
```

## 部署到 GitHub Pages

目标仓库：`MitakeMoca/mitakemoca.github.io`。

### 方式一：GitHub Actions（推荐，保留可维护源码）

1. 在自己的 GitHub 账号下创建公开仓库 `mitakemoca.github.io`。
2. 将本项目全部文件（包括隐藏的 `.github/` 文件夹）推送到该仓库的 `main` 分支。
3. 在仓库的 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
4. 在 **Actions** 中查看 `Deploy personal homepage` 工作流；如首次未自动成功，可手动运行或重新运行。
5. 部署成功后访问 `https://mitakemoca.github.io`。

工作流使用 Python 3.12 生成 `dist/`，再部署该目录。后续修改并推送 `main` 即自动更新。

### 方式二：仅上传静态成品

将 `dist/` **里面的所有文件**上传到 `mitakemoca.github.io` 仓库根目录（不要多套一层 `dist`）。在 **Settings → Pages** 中选择 **Deploy from a branch → main → /(root)**。此方式不需要构建，但修改源内容后要重新生成并上传。

GitHub 官方说明：https://docs.github.com/en/pages/quickstart

## 日常更新

- `content.json`：个人信息、Updates、教育背景、获奖记录、助教记录、代表论文。
- `build.py`：页面布局与专题页长文。百度经历、在研工作和项目介绍目前也在这里。
- `assets/site.css`：颜色、排版、响应式布局。
- `assets/site.js`：主题切换、手机导航、Updates 展开、助教组长筛选。
- `dist/`：生成的可部署站点，不建议手工改动。

双语字段的数组第一项为英文、第二项为中文。新增 Updates 时，将记录加在 `updates` 数组前面；`page` 可用 `research`、`experiences`、`mentorship`、`background`。同步修改 `updated` 日期，再运行构建。

## 内容来源与处理

- 用户提供的《吴奇宣的简历.pdf》：教育、科研、项目、荣誉与业务联系邮箱。
- 用户提供的助教经历截图：8 门次助教经历、2 次助教组长与优秀助教荣誉。相同课程跨学期按不同教学经历计数。
- 用户确认：百度 Agentic 具身智能方向，从 2026 年 11 月开始。没有添加未经确认的职务或具体工作成果。
- ACM MM 2026 官方会议日程：S³-LoRA 完整论文题名与作者顺序。共同第一作者身份依据用户简历。
- 用户要求两篇 ICEBE 论文以后补充到 Updates；当前版本未加入。
- ICLR 2027 工作单列为在研/在投，未列入已录用论文。
- 硕士阶段写为“Master's studies”，不声称已取得硕士学位。
- 简历原件及手机号码未放入站点。头像使用用户提供的动漫图片。
- 助教截图的仓库 star 数属于历史快照，页面使用仓库链接，不显示易过期的数字。
- 设计参考 https://yifu-ding.github.io 的学术主页信息组织；页面代码与视觉样式为本项目重新实现。

## 验证

已检查站内链接、全部双语页面、八条课程记录，以及手机菜单、语言切换、深色模式、Updates 展开和组长筛选。上线需另行确认 GitHub 账号授权、仓库推送与 Pages 部署结果。
