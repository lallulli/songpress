# Rilasciato Songpress 1.9.0

Buona Epifania dal team Songpress!

Oggi rilasciamo una nuova versione di Songpress: **1.9.0**. Gli obiettivi principali di questa versione sono:

- **Pulizia e modernizzazione del codice**. Semplificare e modernizzare la base di codice in modo che Songpress possa essere costruito con le versioni recenti delle sue dipendenze, in particolare wxPython.
- **Revisione del sistema di installazione**. Songpress è ora pubblicato su PyPI e può essere installato sia su Linux che su Windows utilizzando strumenti standard come pipx o uv. Su Windows, un nuovo programma di installazione GUI basato sulla rete raggruppa e utilizza uv per scaricare e installare tutte le dipendenze richieste in modo standard e affidabile.
- **Parità di funzionalità su Linux**. Linux ora raggiunge la parità di funzionalità con Windows. Il comando Copia come immagine è ora disponibile e copia l'output formattato negli appunti come immagine SVG (con PNG come fallback per le applicazioni che non supportano SVG). Ad esempio, il copia e incolla basato su SVG produce risultati perfetti in Inkscape e nella soluzione di desktop publishing Affinity per Linux non ufficiale basata su Wine.
