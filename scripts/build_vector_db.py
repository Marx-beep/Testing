"""将 research_cards 下的 Markdown 导入本地 Chroma 向量库。"""
from pathlib import Path

from chromadb import PersistentClient
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE = Path(__file__).resolve().parent.parent
CARD_DIR = BASE / "research_cards"
VECTOR_DIR = BASE / "vector_db"


def main() -> None:
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    client = PersistentClient(path=str(VECTOR_DIR))
    collection = client.get_or_create_collection("csmar_cards")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    mds = list(CARD_DIR.rglob("*.md"))
    if not mds:
        print("[WARN] research_cards 下没有 Markdown 文件。")
        return

    ids, docs, metas = [], [], []
    for md in mds:
        raw = md.read_text(encoding="utf-8")
        chunks = splitter.split_text(raw)
        for i, c in enumerate(chunks):
            ids.append(f"{md.stem}-{i}")
            docs.append(c)
            metas.append({"path": str(md.relative_to(BASE)), "chunk": i})

    collection.upsert(ids=ids, documents=docs, metadatas=metas)
    print(f"[OK] 已写入 {len(ids)} 个文本块到 {VECTOR_DIR}")


if __name__ == "__main__":
    main()
