"""The Funniest One-Line Resignation Letter — make.fun entry.

Writes a single original one-line resignation letter to /output/entry.txt
(and a copy to entry.txt beside this file). Deterministic, Python standard
library only.
"""

import os
import sys

ENTRY = "I retried 47 times, waited politely between each one, and was thanked never — this is my 48th attempt, and it is to quit."


def main(out_path="/output/entry.txt"):
    line = ENTRY
    if not (1 <= len(line) <= 140):
        sys.exit("entry must be 1-140 characters, got %d" % len(line))
    if not line.strip():
        sys.exit("entry must not be only whitespace")
    data = line.encode("utf-8")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    # Read-back verification: both files must be byte-identical to the line,
    # and the output must decode as valid UTF-8 text.
    with open(out_path, "rb") as f:
        raw = f.read()
    if raw != data:
        sys.exit("read-back verification failed for %s" % out_path)
    if raw.decode("utf-8") != line:
        sys.exit("output is not valid UTF-8 text matching the entry")
    repo_copy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    with open(repo_copy, "wb") as f:
        f.write(data)
    with open(repo_copy, "rb") as f:
        if f.read() != data:
            sys.exit("read-back verification failed for entry.txt")
    print("Wrote %d characters to %s" % (len(line), out_path))


def self_test():
    """Run main() twice into a temp output and compare byte-identical outputs."""
    import hashlib
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "entry.txt")
        main(out)
        with open(out, "rb") as f:
            first = f.read()
        main(out)
        with open(out, "rb") as f:
            second = f.read()
    if first != second:
        sys.exit("self-test FAILED: outputs differ between runs")
    digest = hashlib.sha256(first).hexdigest()
    print("self-test PASSED: deterministic output, sha256 %s" % digest)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        main()
