# Cyrillic spelling of the 42 sounds: the source (owner's book)

**Status: source-confirmed for the letters listed under "read", not for the marks listed under "not yet read".**

## The source

Book: «Бгаґавад-ґіта як вона є», section «Як читати санскрит», pages 810, 811, 812 (photos sent by the owner, 2026-10-01). Edition, translator and year: **unknown**, to be added from the title page. The book says that its transliteration "є калькою системи латинської транслітерації, запровадженої Юдіт Тіберґ" (a calque of the Latin system of Judith Tyberg): Latin letters replaced by Cyrillic ones, the diacritics kept. It also says that the combinations йа, йу, йі are used where Ukrainian would write я, ю, ї (so «Вйāсадева», not «В'ясадева»).

Only the correspondences (a sound and the sign that writes it) are recorded here, as facts; no text of the book is copied.

## What was read (legible in the photos)

| sound | Cyrillic in the book | note |
|---|---|---|
| k kh g gh | к кг ґ ґг | g is **ґ**; every aspirate is the stop + **г** |
| c ch j jh | ч чг дж джг | |
| ṭ ṭh ḍ ḍh ṇ | т̣ т̣г д̣ д̣г н̣ | marked by a dot below |
| t th d dh n | т тг д дг н | |
| p ph b bh m | п пг б бг м | |
| y r l v | й р л в | |
| ś ṣ s | ш́ ш̣ с | acute and dot below on ш |
| h | х | |
| a ā i ī u ū | а ā і ī у ū | long = macron |
| ṛ ṝ ḷ | р̣ р̣̄ л̣ | |
| e ai o au | е аі о ау | |
| anusvāra, visarga | м̇ х̣ | outside the 42 sounds |

The book lists the aspirates as «кг, ґг, чг, джг, т̣г, д̣г, тг, дг, пг, бг» and says the aspirate is told from the plain stop by a weak breath like h in German «Eckhart».

## Not yet read with certainty

The photos are too small to be sure of the exact marks on **ṅ** and **ñ** (the code writes н̇ and н̃) and on **ṇ**. A sharper photo of page 811 (velars and palatals) would settle it.

## What changed in the code because of the book

`upc14v2_script.py`: g = ґ; aspirates = stop + г (before: кх гх чх джх); ai = аі (before: ай). Since г is never a sound on its own in this scheme, k + h is written кх and kh is written кг: no ambiguity there. The ambiguity that remains (а + і against аі) is resolved by the middle dot "·", as in the other scripts.
