# Rilasciata la versione 1.9.0rc1 di Songpress

Buon anno dal team di Songpress!

Oggi rilasciamo la Release Candidate di una nuova versione di Songpress: **1.9.0**. Gli obiettivi principali di questa release sono:

- **Pulizia e modernizzazione del codice**. Semplificare e modernizzare il codice sorgente in modo che Songpress possa essere compilato con le versioni più recenti delle sue dipendenze, in particolare wxPython.

- **Riprogettazione del sistema di installazione**. Songpress è ora pubblicato su PyPI e può essere installato sia su Linux che su Windows utilizzando strumenti standard come pipx o uv. Su Windows, un nuovo programma di installazione GUI basato sulla rete raggruppa e utilizza uv per scaricare e installare tutte le dipendenze necessarie in modo standard e affidabile.

- **Parità di funzionalità su Linux**. Linux ora raggiunge la parità di funzionalità con Windows. Il comando "Copia come immagine" è ora disponibile e copia l'output formattato negli appunti come immagine SVG (con PNG come fallback per le applicazioni che non supportano SVG). Ad esempio, la funzione copia e incolla basata su SVG produce risultati perfetti in Inkscape e nella soluzione di desktop publishing non ufficiale Affinity per Linux, basata su Wine.
