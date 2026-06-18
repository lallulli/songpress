---
hide: toc
---

# Il Formato Chordpro

Un file nel formato ChordPro è costituito dalle parole della canzone, intervallate da qualche "comando" per definire il titolo, gli accordi, ecc.

Songpress supporta un sottoinsieme del formato ChordPro originale. Questa tabella mostra i comandi ChordPro supportati da Songpress.

| Comando | Comando abbreviato | Descrizione | Esempio |
| :-------| ------------------ | ----------- | ------- |
| {title:Titolo della canzone}| {t:Titolo della canzone} | Il comando **title** produce il titolo della canzone | {title:La Fameja Dei Gobon} |
| {subtitle:Sottotitolo} | {st:Sottotitolo} | Il comando **subtitle** produce il sottotitolo della canzone | {st:Canto popolare veneto} |
| {start_of_chorus}...{end_of_chorus} | {soc}...{eoc} | Il comando **chorus** produce il ritonello con il testo e gli accordi contenuti fra i due comandi | {soc} Gobo so [Do]pare, goba sa mare goba la fja de so so [Sol]rela...{eoc} |
| {soc:Etichetta}...{eoc} | | **Chorus con etichetta** produce il ritornello, con l'etichetta specificata al posto di "Rit.". E' anche possibile omettere del tutto l'etichetta con `{soc:}...{eoc}`. ==**N.B.**: Questo è un comando proprietario di Songpress, non fa parte dello standard ChordPro== | {soc:Coro} Gobo so [Do]pare, goba sa mare goba la fja de so so[Sol]rela...{eoc} |
| (blank line) | | Inizia una nuova strofa |
| {verse:Etichetta} | | Inizia una nuova strofa, con l'etichetta specificata al posto dell'etichetta con il numero della strofa. La strofa non viene conteggiata nella numerazione. E' anche possibile omettere del tutto l'etichetta, con il comando `{verse:}`.==**N.B.**: Questo è un comando proprietario di Songpress, non fa parte dello standard ChordPro== | {verse:strum}  [Do]  [Fa]  [Sol] |
| [Chord] | | Il comando **Chord** produce un accordo esattamente sopra la posizione corrente | Un [Do]gobo ed una goba a l'età di novant'[Sol]anni |
| {comment:Un commento} | {c:Un commento} | Il comando **comment** produce un commento | {c:due volte} |
| # Commento sorgente | | Commento nel file ChordPro, non produce niente | # RICORDA: devo aggiungere l'ultima strofa |
| {textfont:nome del font} | | Imposta il **font** da questo punto in poi. Quando il parametro è omesso, viene ripristinato il valore di default: `{textfont}` | {textfont:Arial} |
| {textsize:dimensione del font} | | Imposta la **dimensione del font** da questo punto in poi. Quando il parametro è omesso, viene ripristinato il valore di default: `{textsize}` | {textsize:12} |
| {textcolour:un colore} | | Imposta il **colore del font** da questo punto in poi. Il colore del testo è espresso in un formato compatibile con il web, ad esempio `#RRGGBB`. Quando il parametro è omesso, viene ripristinato il valore di default: `{textcolour}` | {textcolour:#FF0000} |
| {chordfont:nome del font} | | Analogo a `{textfont}`, ma imposta il font degli accordi. | {chordfont:Courier New} |
| {chordsize:dimensione del font} | | Analogo a `{textsize}`, ma imposta la dimensione del font per gli accordi. | {chordsize:12}
| {chordcolour:un colore} | | Analogo a `{textcolour}`, ma imposta il colore del font per gli accordi. | {chordcolour:blue} |
