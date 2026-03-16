"""初始化 A股-CSMAR 研究自动化目录结构。"""
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

DIRS = [
    "data/原始财报",
    "data/行业指标",
    "data/公司指标",
    "research_cards/行业",
    "research_cards/公司",
    "research_cards/专题",
    "vector_db",
    "scripts",
    "templates",
]


def main() -> None:
    for rel in DIRS:
        path = BASE / rel
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] {path}")


if __name__ == "__main__":
    main()
