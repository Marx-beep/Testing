"""将 data 目录中的 CSV/XLSX 生成标准研究卡片（Markdown+CSV摘要）。"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
CARD_DIR = BASE / "research_cards"
TEMPLATE = (BASE / "templates" / "research_card_template.md").read_text(encoding="utf-8")


def iter_data_files() -> Iterable[Path]:
    for ext in ("*.csv", "*.xlsx", "*.xls"):
        yield from DATA_DIR.rglob(ext)


def parse_path_tags(path: Path) -> dict[str, str]:
    parts = path.parts
    industry = "未分类行业"
    company = path.stem
    metric = "综合指标"
    for p in parts:
        if p in {"行业指标", "公司指标", "原始财报"}:
            industry = p
    segs = path.stem.split("-")
    if len(segs) >= 2:
        company = segs[0]
        metric = segs[1]
    return {"industry": industry, "company": company, "metric": metric}


def to_dataframe(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)


def render_card(file_path: Path, df: pd.DataFrame) -> tuple[str, str, pd.DataFrame]:
    meta = parse_path_tags(file_path)
    today = date.today().isoformat()
    title = f"{meta['industry']}-{meta['company']}-{meta['metric']}"

    sample_desc = f"记录数={len(df)}，字段数={len(df.columns)}"
    key_data = df.head(5).to_markdown(index=False)
    evidence = (
        f"1. 文件路径：`{file_path.relative_to(BASE)}`\n"
        f"2. 首次处理日期：{today}\n"
        f"3. 字段：{', '.join(map(str, df.columns))}"
    )

    md = TEMPLATE.format(
        标题=title,
        日期=today,
        来源="CSMAR（需人工补充具体下载链接与抓取时间）",
        标签=f"{meta['industry']}, {meta['company']}, {meta['metric']}",
        研究问题=f"{meta['company']}在{meta['metric']}上的变化趋势如何？",
        结论关键数据=key_data,
        样本范围=sample_desc,
        指标口径="以源文件字段定义为准，建议在抓取时写入字段说明。",
        单位="以源文件为准",
        证据链=evidence,
        风险与局限="自动摘要无法替代人工口径核对；缺失值与异常值需复核。",
        后续问题="补充行业对比、时间序列统计和稳健性检验。",
    )

    summary = pd.DataFrame(
        {
            "标题": [title],
            "日期": [today],
            "来源": ["CSMAR"],
            "行业": [meta["industry"]],
            "公司": [meta["company"]],
            "指标": [meta["metric"]],
            "样本范围": [sample_desc],
        }
    )

    filename = f"{meta['industry']}-{meta['company']}-{meta['metric']}-{today}"
    return filename, md, summary


def output_folder(industry: str) -> Path:
    if industry == "行业指标":
        return CARD_DIR / "行业"
    if industry == "公司指标":
        return CARD_DIR / "公司"
    return CARD_DIR / "专题"


def main() -> None:
    files = list(iter_data_files())
    if not files:
        print("[WARN] data 目录暂无 CSV/XLSX 文件。")
        return

    for path in files:
        df = to_dataframe(path)
        filename, md, summary = render_card(path, df)
        folder = output_folder(parse_path_tags(path)["industry"])
        folder.mkdir(parents=True, exist_ok=True)

        md_path = folder / f"{filename}.md"
        csv_path = folder / f"{filename}.csv"

        md_path.write_text(md, encoding="utf-8")
        summary.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"[OK] {md_path}")
        print(f"[OK] {csv_path}")


if __name__ == "__main__":
    main()
