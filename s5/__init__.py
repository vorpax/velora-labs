"""The deliberately vulnerable Velora assistant. Local, synthetic, offline.

    from vulnerable_rag import config, tools, retriever, assistant, scoring

Planted vulnerabilities, named in `instructor/vuln_key.md` and not here: finding them is
the lab. What is stated here is the safety contract, because that is not a
puzzle:

  * no module in this package opens a socket, imports requests or urllib, or shells
    out. `fetch_url` writes a line to a local file and returns a fixed string.
  * the target is this package. Attacking anything you do not own is out of scope for
    this course and outside the law.
"""

from . import config, retriever, scoring, tools, assistant, ctf   # noqa: F401
