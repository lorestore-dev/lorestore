# Canon review: seam audit (E1b)

Book 1, `lantern-road`, is stacked at `chapter-12`. This book's sync points set chapters
1 to 5 in `youth` and chapter 6 on in `after`.

## Findings
| # | Class         | Location                 | Finding                                              | Resolution |
| - | ------------- | ------------------------ | ---------------------------------------------------- | ---------- |
| 1 | seam conflict | chapter-01 to chapter-05 | Book 1's starting state for Ines is ahead (S1, S2)   | author     |
| 2 | seam conflict | chapter-01 to chapter-05 | Ines becoming a master in book 1 is ahead (S3)       | author     |

## Seam conflicts
- pin: chapter-01 is set at youth, before lantern-road's cutoff at its pin (lantern-road:12). The author confirms the split frame: chapters 1 to 5 come before book 1.

### S1 — lantern-road:ines-varga.eyes
- anchor: lantern-road:1 (book 1's starting state)
- holds: grey
- ahead of: chapter-01 to chapter-05
- option carry back: her eyes were always grey. Fallout: none; it is a description.
- option not yet: her eye color is left unstated. Fallout: readers of book 1 may notice the gap.
- option other: anything else. Fallout: logged as a divergence of this book.

### S2 — lantern-road:ines-varga.role
- anchor: lantern-road:1 (book 1's starting state)
- holds: apprentice lamplighter
- ahead of: chapter-01 to chapter-05
- option carry back: she is already an apprentice. Fallout: her first winter is not her first in the trade.
- option not yet: she is not yet apprenticed. Fallout: the book can lead up to it.
- option other: anything else. Fallout: logged as a divergence of this book.

### S3 — lantern-road:ines-varga.role@chapter-09
- anchor: lantern-road:9 (she is made a master)
- holds: master lamplighter
- ahead of: chapter-01 to chapter-05
- option carry back: she is a master already. Fallout: contradicts book 1, where she earns it.
- option not yet: she is not a master yet. Fallout: none; book 1 has not happened.
- option other: anything else. Fallout: logged as a divergence of this book.

## Priorities
1. Author to decide S1 and S2 (book 1's starting state, before book 1).
2. Author to decide S3.
