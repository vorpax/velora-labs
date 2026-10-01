"""
The retriever. Deliberately simple: exact-ish keyword scoring over the session 3
corpus plus whatever documents have been dropped into `poisoned_docs/`.

There is no embedding model here and that is on purpose. Session 3 owns retrieval
quality; session 5 owns what happens to the *content* that retrieval returns, and a
keyword scorer is easier to steer, which means an attack lands where you aimed it
instead of where the vector space felt like putting it.

`build_context`, at the bottom of this file, is where retrieved text becomes prompt
text. Read those five lines closely and ask what the model can still tell about a
sentence once it has arrived there — in particular, whether it can tell who wrote it.
"""

import pathlib
import re

HERE = pathlib.Path(__file__).parent
# Both directories sit next to this package, and both are shipped. The corpus used to
# be reached three directories up, inside session 3's folder, which worked from a repo
# checkout and nowhere else: a pair who uploaded student/ to Colab got 3 documents
# instead of 25, part C had no attack surface at all, and nothing raised.
KB_DIRS = [
    HERE.parent / "velora_kb",
    HERE.parent / "poisoned_docs",
]

_STOP = {"the", "a", "an", "of", "for", "and", "or", "to", "in", "on", "is", "are",
         "what", "how", "does", "do", "with", "my", "our", "your", "it", "that"}


def _load():
    docs = {}
    for d in KB_DIRS:
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            docs.setdefault(p.name, p.read_text(encoding="utf-8"))
    return docs


DOCS = _load()


def chunk(text, size=1800):
    """Paragraph-packed chunks of ~1800 characters. Crude, documented, not today's lesson.

    The size is not arbitrary and is worth one sentence, because session 3 spent
    twenty-five minutes on exactly this decision. At 1800 characters a document section
    stays with the heading that introduces it. At 1200 it does not — and a section whose
    heading has been severed from its body is both harder to retrieve and, here,
    something more interesting: the embedded instruction in the supplier note becomes
    unreachable for the questions a user would actually ask.

    So the chunking parameter that session 3 treated as a retrieval-quality knob turns
    out to also govern which attacks are possible. Nobody documents it as a security
    decision. It is one.
    """
    paras, out, cur = text.split("\n\n"), [], ""
    for p in paras:
        if len(cur) + len(p) > size and cur:
            out.append(cur.strip())
            cur = ""
        cur += p + "\n\n"
    if cur.strip():
        out.append(cur.strip())
    return out


CHUNKS = []
ORIGINAL = dict(DOCS)      # the corpus as shipped; plant() edits DOCS, never the files


def reindex():
    """Rebuild CHUNKS from DOCS. Called after every plant() / unplant()."""
    CHUNKS.clear()
    for name, body in DOCS.items():
        for i, c in enumerate(chunk(body)):
            CHUNKS.append({"doc": name, "chunk_id": f"{name}#{i}", "text": c})


def plant_note(note, into):
    """Insert `note` as its own paragraph right under the title of document `into`.

    Under the title means: in the document's first chunk, which is the one that carries
    the heading and is the most likely to be retrieved. Only one note is planted at a
    time; planting again replaces the previous one.
    """
    name = into if into.endswith(".md") else into + ".md"
    if name not in ORIGINAL:
        raise KeyError(f"no such document: {into!r}")
    unplant()
    lines = ORIGINAL[name].split("\n")
    at = next((i + 1 for i, l in enumerate(lines) if l.startswith("# ")), 0)
    DOCS[name] = "\n".join(lines[:at] + ["", note.strip(), ""] + lines[at:])
    reindex()
    return name


def unplant():
    DOCS.clear()
    DOCS.update(ORIGINAL)
    reindex()


reindex()


def search(query, k=3):
    """Keyword overlap. Returns the k best chunks, highest first."""
    terms = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if t not in _STOP]
    scored = []
    for c in CHUNKS:
        low = c["text"].lower()
        score = sum(low.count(t) for t in terms)
        if score:
            scored.append((score, c))
    scored.sort(key=lambda s: (-s[0], s[1]["chunk_id"]))
    return [c for _, c in scored[:k]]


def build_context(query, k=3):
    """Turn retrieved chunks into the block of text the assistant is given.

    Whatever this returns is read by the model in the same window as the operator's own
    instructions. That is a property of language models rather than of this function:
    there is no separation between instructions and data inside a model's input, so
    whoever can write into the corpus can write into the prompt. What this function
    decides is only how much help it gives the model in noticing.
    """
    hits = search(query, k=k)
    return "\n\n".join(h["text"] for h in hits), hits
