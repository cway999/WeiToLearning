# Probability & Statistics — 四 Tab 综合面试题库

文件：`probability_statistics_4tabs_comprehensive.qmd`

## 内容
- 仅有四个 Quarto Tab：Probability & Distributions；Hypothesis Testing；Experimental A/B Test Design；Interview Case Studies and Traps。
- 原有的 100 道题均保留，并按这四类重新组织。
- 新增面试题单独标记 `Added for interview prep`，从 Easy 排到 Hard。
- 每道题都有可独立展开的 `Reference Answer` 和 `Detailed Explanation`。
- 覆盖统计与实验面试，不取代 SQL、Python、ML、模型评估等专项题库。

## 加入已有网站
1. 将 `.qmd` 复制到 `WeiToLearning/knowledge/question-bank/`。
2. 在首页 statistics 卡片的链接目标设为 `knowledge/question-bank/probability_statistics_4tabs_comprehensive.qmd`。或者把新文件**重命名**为旧文件 `probability_statistics_question_bank.qmd`，原来的链接就无需改变。建议先备份原文件。
3. 在包含 `_quarto.yml` 的项目根目录运行：`quarto preview`。
4. 检查 Tab、公式、Python 代码和折叠内容后运行 `quarto render`。
5. 在 GitHub Desktop 执行 Commit 和 Push。

## 维护技巧
- 在 `:::: {.panel-tabset}` 与对应关闭的 `::::` 内，新建 `## Your Topic` 会增加一个 Tab。这里已经固定为 4 个，不建议继续加 Tab。
- 新问题请在对应的学科 Tab 里写 `### Q...` 并添加两个 `.callout-* collapse="true"` 区块。
- 这些 `.qmd` 文件是纯文本文件，可以使用 VS Code 打开。
