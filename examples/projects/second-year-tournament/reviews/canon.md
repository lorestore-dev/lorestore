# Canon review: order audit

Audit of the project order in `bible/sync-points.md` (PS, GoF, CoS, PoA, …). The
author decides each inversion; this review only sets out the options.

## Findings
| # | Class           | Location                        | Finding                                                    | Resolution |
| - | --------------- | ------------------------------- | ---------------------------------------------------------- | ---------- |
| 1 | Order inversion | harry-potter+sirius-black.bond  | GoF:2 "correspondents" now precedes PoA:17 "met"           | author     |
| 2 | Order inversion | cedric-diggory.status           | PoA:9 "alive" now follows GoF:32 "dead"                    | author     |
| 3 | Order inversion | cedric-diggory.role             | PoA:9 "Hufflepuff Seeker" now follows GoF:16 "champion"    | author     |
| 4 | Order inversion | harry-potter (broom, first task) | GoF:20 has Harry summon the Firebolt, which he gets at PoA:11 | author     |

## Order inversions

### I1 — harry-potter+sirius-black.bond
- now earlier: GoF:2 "correspondents" (Harry writes to Sirius about his scar)
- now later: PoA:17 "met in the Shrieking Shack"
- depends on: Harry and Sirius having met
- option remove: Harry writes to no one. Fallout: no adult hears about the scar pain; Sirius's advice before the first task has no source.
- option substitute: Harry writes to someone he already knows (Dumbledore, Hagrid). Fallout: that person learns of the scar months early and must act, or choose not to.
- option supply: an original scene has Harry meet Sirius before the Tournament. Fallout: Harry knows a fugitive; PoA's reveal loses its surprise.
- option reorder: move PoA back before GoF. Fallout: undoes part of the premise.

### I2 — cedric-diggory.status
- now earlier: GoF:32 "dead"
- now later: PoA:9 "alive" (Cedric plays Seeker against Gryffindor)
- depends on: Cedric being alive in Harry's PoA year
- option remove: Cedric's PoA appearances don't happen. Fallout: Hufflepuff needs a different Seeker; the match plays out differently.
- option substitute: another Hufflepuff takes Cedric's place in those scenes. Fallout: a new character, or a minor one promoted.
- option supply: Cedric survives the graveyard (as in `two-witnesses`). Fallout: changes the whole back half of the story.
- option reorder: move PoA back before GoF. Fallout: undoes part of the premise.

### I3 — cedric-diggory.role
- now earlier: GoF:16 "Hogwarts Triwizard champion"
- now later: PoA:9 "Hufflepuff Seeker"
- depends on: the same as I2; resolving I2 resolves this.

### I4 — harry-potter (broom)
- found from the inversion candidate harry-potter (PoA, GoF): no two rows of one
  attribute are reversed
- now earlier: GoF:20, the first task (Harry summons his broom past the dragon)
- now later: PoA:11 "Firebolt" (a gift he has not yet been given)
- depends on: Harry owning the Firebolt
- option remove: Harry flies no broom in the first task. Fallout: he needs another way past the dragon.
- option substitute: he summons his Nimbus Two Thousand. Fallout: a slower broom; the task is closer run.
- option supply: the Firebolt reaches him earlier, by another route. Fallout: Sirius's gift has no occasion later.
- option reorder: move PoA back before GoF. Fallout: undoes part of the premise.

## Inversion candidates
| Candidate                             | Addressed                                  |
| ------------------------------------- | ------------------------------------------ |
| cedric-diggory (PoA, GoF)             | I2 and I3                                  |
| harry-potter (CoS, GoF)               | No inversion: `born` has one row (CoS:8), so a swap reverses nothing; the story set in GoF simply does not yet know Harry's birth year |
| harry-potter (PoA, GoF)               | I4                                         |
| harry-potter+sirius-black (PoA, GoF)  | I1                                         |

## Priorities
1. Author to decide I1.
2. Author to decide I2 (I3 follows it).
3. Author to decide I4.
