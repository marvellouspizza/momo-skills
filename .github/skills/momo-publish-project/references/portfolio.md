# 个人作品墙接入

## 输入文件

当前作品根目录的 `release/publish/project.json`，logo 与该文件同目录：

```json
{
  "id": "my-project",
  "name": "作品名称",
  "description": "十四字内说明功能",
  "url": "https://my-project.alphapulsex.online/",
  "sourceDir": "/absolute/path/to/current-project",
  "logo": "logo.png"
}
```

ID 必须沿用该作品已存在的记录；先搜个人站 `project-submissions/*/project.json` 和 `src/games.js`。不要因为改了文案而创建新 ID。`sourceDir` 是作品源目录，用于防止不同项目撞 ID，不进入公开 generated manifest。

## 注册与并发

```bash
python3 /Users/momo/.codex/skills/momo-publish-project/scripts/register_project.py \
  --manifest /absolute/project/release/publish/project.json \
  --after bash /absolute/project/release/publish/update-portfolio.sh
```

`--after` 后面是程序和参数，不是 shell 字符串。脚本在 profile 中的个人网站根目录运行后续命令，锁覆盖注册及后续命令。没有 `--after` 只做本地注册。失败退出码向上传递，已注册数据保留供重试。锁由操作系统释放，不手动删除锁文件。默认等待最多 10 分钟；检查其他发布任务后再重试。

测试或隔离副本可传 `--portfolio /absolute/staging/portfolio`；对共享源目录的变更仍应在原目录锁内完成。

## 站点现有约定

- 提交目录 `project-submissions/<id>/project.json` 与 logo。
- 当前站点有 `package-lock.json`，使用 `npm run import:projects` 调用 `scripts/import-projects.mjs`，生成 `src/projects.generated.json`，复制图标至 `public/media/project-submissions/<id>/`。
- 更新同一作品的 Logo 时，沿用 ID 与 `project.json`；注册脚本按内容生成新的图标文件名以避开缓存。部署输入须包含新的注册记录与图标；不要仅覆盖旧 URL 后假定线上缓存已刷新。
- `src/games.js` 合并精选与导入作品；不要覆盖整份文件。
- `npm run build` 的 prebuild 也会导入。现有 Vercel 配置输出 `dist/client`；保留项目已有构建配置。
- Vercel 生产项目 **momo-personal-blog**。已使用的部署命令为 `npx --yes vercel@latest deploy --prod --yes --project momo-personal-blog`。执行前通过 CLI inspect 核对账号与项目，优先使用已有固定版本；具体 flags 以安装版本 help 为准。确保发布输入包含本次导入且不包含其他未授权内容。
- Cloudflare Worker **momo-blog-vercel-proxy** 已代理 `https://momo-personal-blog.vercel.app` 至 `momo-blog.alphapulsex.online`，日常内容发布不必重建 Worker 或 DNS。
- `.openai/hosting.json` 是历史 Sites 项目记录，不是本次正式域名的发布目标；`wrangler.jsonc` 的 momo-personal-blog 也不是上述代理 Worker。

普通发布脚本（仅当当前工作区内容均适合此次发布时）：

```bash
#!/bin/bash
set -euo pipefail
npm run build
npx --yes vercel@latest deploy --prod --yes --project momo-personal-blog
```

发布后浏览正式 `/games`，确认名称、logo、iframe 的实际 URL。保留部署输出 URL/标识和检查证据，不能以构建通过或 localhost 截图代替上线验收。

已有作品仅改头像或文案时，先检查当前部署与上次验收，再仅更新本项目提交记录、导入产物和必要样式。若共享工作区有其他改动，优先复用已核实对应当前生产版本的隔离发布目录；没有可靠副本才重新获取生产基线。只验证此次变化及其关键关联项，不重复打包或测试未变化的小红书页面。对要求直角头像的作品，还要在正式页面确认头像元素计算后的 `border-radius: 0`，且没有父级遮罩裁圆。

## 隔离发布的可复用结论

这里的“只更新本作品”指**发布源码差异仅包含本作品**。个人网站仍正常构建并部署整个站点；不要尝试只上传一张卡片来替换 Vercel 部署，也不要从本地脏工作区直接整站部署。

1. **以当前生产版本为基线。** 优先使用能对应生产部署的 Git commit 或保留的干净发布源码快照。上次临时目录只有在源码与生产部署的对应关系可核实、且目录未被后续改动时才能复用；目录存在不等于仍是最新基线。
2. **限定带入文件。** 默认只带入 `project-submissions/<id>/project.json` 及其引用的 Logo，由构建自动生成清单和公开素材。必要的 UI 修复仅带入经过核对的最小补丁；不要整份复制脏工作区的 `src/games.js`、`src/games.css`、生成清单或整个提交目录，以免混入其他未完成作品。
3. **防止覆盖其他新发布。** 持有共享发布锁时读取当前生产部署标识；部署前再次核对。若生产已变化，在新基线上重新应用本作品差异，不能继续发布旧快照。锁只能协调使用此脚本的任务，不能阻止其他渠道的发布。
4. **保留下一次能用的记录。** 成功验收后，在当前作品 `release/publish/validation.md` 记录生产部署 ID、基线来源（commit 或源码快照路径）、实际发布目录、部署命令及本次差异文件。可复用源码快照保存在持久目录而非仅 `/tmp`，排除密钥、环境文件和 `node_modules`；复用前仍核对当前生产版本。不要只留下无法还原源码的部署网址。
5. **按差异验收。** Logo/文案变化检查正式卡片、资源 URL、直角展示和无重复；代码变化再测对应交互。其他作品的记录与 URL 应保持基线内容。应用自身 URL 未变且代码未变时，不重新部署应用、配置 DNS 或重建 Cloudflare 代理。
