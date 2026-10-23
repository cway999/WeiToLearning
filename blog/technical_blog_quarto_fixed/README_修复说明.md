# WeiToLearning Technical Blog – Quarto 修复版

问题：旧 `.qmd` 中 4 个 difficulty filter 的 `<button>` 每行有四个空格缩进，Pandoc 把它们误解析为代码块，导致 Quarto 页面直接显示 `<button ...>` 文本。

修复：使用 Pandoc/Quarto 原生 ````{=html}` raw HTML fence 将搜索及筛选组件作为原生 HTML 渲染，不改变原有 80 个资源、4 个 Quarto Tab、三列卡片与搜索筛选逻辑。

安装：将本 ZIP 内的 `blog/index.qmd` 放进 WeiToLearning 仓库 `blog/index.qmd`，替换旧文件。

检查：在仓库根目录运行 `quarto preview`，查看难度按钮及交互；然后 `quarto render`，GitHub Desktop Commit + Push。

注意：已经通过 Pandoc 结构检查并确认 4 个 `<button>`、80 张卡片及 4 个 Tab，但尚未使用 Quarto CLI 实际渲染。
