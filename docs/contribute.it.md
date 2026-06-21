# Supporta il progetto

Prima di tutto: grazie mille per dedicare il tuo tempo a contribuire a questa applicazione!

Songpress è ospitato su [Github](https://github.com/lallulli/songpress) e puoi aiutare il progetto in diversi modi:

- segnalando bug o suggerendo miglioramenti tramite il nostro [issue tracker su Github](https://github.com/lallulli/songpress/issues)
- creando nuove [traduzioni](#contribuire-alla-traduzione)
- fornendo materiale grafico (icone, pulsanti, ecc.)
- contribuendo al codice, effettuando un fork del repository e inviando una pull request
- contribuendo alla documentazione


## Contribuire alla traduzione

L'internazionalizzazione (i18n) di Songpress viene effettuata tramite gli strumenti GNU gettext ed è gestita attraverso Transifex.
Per tradurre il programma è sufficiente disporre di un account Transifex. Se desideri testare le stringhe tradotte nella tua installazione locale di Songpress, operazione consigliata, è necessario installare:

- gli strumenti gettext (comandi: `xgettext`, `msgmerge`, `msgfmt`)
- il client Transifex (comando: `tx`)

### Progetto Songpress su Transifex

Il progetto Transifex di Songpress è disponibile al seguente URL:

https://www.transifex.com/skeed/songpress-2/


### Suggerimenti per i traduttori

- Le stringhe che contengono un carattere e commerciale (`&`) al loro interno vengono utilizzate per definire le scorciatoie da tastiera per le voci di menu (e sottomenu). La lettera preceduta dal simbolo `&` viene sottolineata e l'utente può selezionare quella voce di menu premendo `ALT + lettera` (oppure semplicemente la lettera nel caso dei sottomenu). Ad esempio, se una voce di menu è definita come `&File`, la lettera `F` diventa una scorciatoia per tale voce e l'utente può selezionarla premendo `ALT + F`. È importante che, nelle traduzioni, i simboli `&` siano posizionati in modo che la lettera successiva sia possibilmente univoca all'interno del menu (o sottomenu) di appartenenza.
- In diverse stringhe sono presenti segnaposto per parametri, ad esempio `%s` (parametro stringa posizionale) oppure `%(verse_number)d` (parametro intero denominato `verse_number`). Ogni parametro presente nella stringa originale deve comparire anche nella versione tradotta. È possibile modificare l'ordine dei parametri _denominati_ all'interno della stringa. Se è necessario modificare l'ordine dei parametri _posizionali_, apri un ticket affinché tali parametri vengano convertiti in parametri denominati nella stringa originale.


### Test della traduzione

Preparazione:

1. Assicurati che gettext e il client Transifex siano installati sul sistema. [Configura il file `.transifexrc` con le credenziali del tuo account Transifex](http://docs.transifex.com/client/config/).
2. Clona il repository di Songpress.
3. Verifica che il codice della lingua di interesse sia presente nel file di configurazione `tx.py`.
4. Verifica che la lingua di interesse sia presente anche in `src/Globals.py`.

Ciclo di test:

1. Traduci le stringhe su Transifex.
2. Posizionati nella directory principale del repository clonato ed esegui: `python pygettext.py --pull`
3. Avvia Songpress (non dimenticare di selezionare la tua lingua in Strumenti -> Opzioni):

```bash
cd src
python main.py
```

Ecco la traduzione in italiano tecnico, mantenendo la formattazione Markdown originale:

````markdown


### Configurazione dell'ambiente

Markdown è un semplice formato testuale, quindi puoi scrivere la documentazione utilizzando un qualsiasi editor di testo.
Tuttavia, probabilmente vorrai compilare ed eseguire localmente il sito della documentazione di Songpress, in modo da poter verificare il tuo contributo prima di inviare una pull request.

Per prima cosa, assicurati che Python sia installato sul tuo computer. Apri una shell ed esegui: `python --version`.
Se Python è installato correttamente, otterrai un output simile al seguente: `Python 3.12.3`

Successivamente, crea un [ambiente virtuale](https://docs.python.org/3/library/venv.html) per Songpress e attivalo (supponendo che la directory dedicata agli ambienti virtuali sia `.venv`):

```bash
python -m venv .venv/songpress

source .venv/songpress/bin/activate
```

Quindi installa tutti gli strumenti necessari tramite **pip**:

```bash
pip install mkdocs mkdocs-material mkdocs-static-i18n
```

Perfetto! Ora sei pronto per eseguire il sito della documentazione.

Effettua un fork del repository, clonalo in locale e, dalla directory principale del progetto, esegui il comando `mkdocs serve`.

A questo punto, aprendo nel browser l'indirizzo `http://localhost:8000`, potrai visualizzare il sito della documentazione.

Il comando `serve` di MkDocs aggiorna automaticamente il sito ogni volta che modifichi uno dei documenti oppure il file di configurazione `mkdocs.yml`.
