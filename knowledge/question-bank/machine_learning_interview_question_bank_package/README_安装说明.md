# WeiToLearning — Machine Learning 题库安装说明

## 文件
- `machine_learning_interview_question_bank.qmd`：最终 Quarto 页面。
- 来源：你上传的 `Machine Learning Notion.docx`；对原文进行了整理与技术准确性校正。
- 题目：**127** 道；基于笔记内容 **92** 道；补充 **35** 道。
- 每题：Reference Answer + Detailed Explanation，两个独立可展开区域。

## 五个 Tab
- Data & Feature Engineering: 24 道
- Linear Models & Optimization: 21 道
- Trees & Classical ML: 26 道
- Evaluation & Model Selection: 22 道
- Neural Networks, Causal ML & Production: 34 道


## 放进 Quarto
1. 在网站根目录找到 `knowledge/question-bank/` 文件夹（没有则创建）。
2. 将 `machine_learning_interview_question_bank.qmd` 放到这个文件夹。
3. 在 `index.qmd` 的 Machine Learning 卡片，使用链接 `knowledge/question-bank/machine_learning_interview_question_bank.qmd`。
4. 运行 `quarto preview` 检查显示；运行 `quarto render` 生成页面。
5. 使用 GitHub Desktop Commit -> Push origin。若采用 `/docs` 发布，需确保最新渲染文件位于 `docs/`。

注意：本题库不是一个可执行的机器学习项目；示例公式和代码应在目标 Quarto / Python 环境中测试。
