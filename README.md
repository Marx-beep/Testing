# A股-CSMAR研究自动化

本仓库提供一个可落地的工作流骨架，用于把 CSMAR 财报/行业数据转成可归档研究卡片，并构建长期知识库与向量检索能力。

## 1) 环境准备

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_project.py
```

## 2) 数据采集（人工 + 自动）

- 使用 Team 账号登录 CSMAR，按公司/行业/指标/年份下载数据。
- 将文件放入：
  - `data/原始财报`
  - `data/行业指标`
  - `data/公司指标`
- 建议额外维护抓取日志（日期、来源 URL、字段口径说明）。

> 注：涉及账号登录与网站策略，仓库仅提供本地处理脚本，不内置绕过登录的抓取代码。

## 3) 研究卡片生成

```bash
python scripts/generate_research_cards.py
```

输出：
- `research_cards/*/*.md`
- `research_cards/*/*.csv`

命名规范：
- `[行业]-[公司]-[指标]-[日期].md`
- `[行业]-[公司]-[指标]-[日期].csv`

卡片模板字段：标题/日期/来源/标签、研究问题、结论关键数据、样本范围/指标口径/单位、证据链、风险与局限、后续问题。

## 4) 长期知识库构建

- 可将 `research_cards` 同步到 Notion 或 Obsidian。
- 按公司、行业、指标、日期建立索引。
- 可选向量检索：

```bash
python scripts/build_vector_db.py
```

默认写入 `vector_db` 目录。

## 5) 个人账号调用建议

查询提示词建议：

- “请优先依据本项目知识库、研究卡片回答问题。若资料不足，请说明缺口。”
- “若知识库有多条冲突，请说明来源与时间。”

## 6) 自动化循环

建议使用 cron 或 CI（每天/每周）触发：
1. Team 端抓取最新数据
2. 自动生成研究卡片
3. 同步到个人知识库
4. 重新构建向量库

## 7) 目录结构

```text
/workspace
    /data
        /原始财报
        /行业指标
        /公司指标
    /research_cards
        /行业
        /公司
        /专题
    /vector_db
    /scripts
```

## 8) 提示词规范

- Team 端：
  “你是A股研究助手。请按标准研究卡片模板输出：
  1. 先明确口径、样本
  2. 再列证据、结论
  3. 输出 Markdown + CSV 可归档格式”

- 个人端：
  “请优先依据本项目知识库、研究卡片回答问题。
  若知识库有多条冲突，请说明来源与时间。
  若资料不足，请明确指出缺口。”
