# Esportare in altri formati

Lo scopo principale di Songpress è permetterti di incorporare spartiti di alta qualità all’interno di documenti di qualsiasi tipo grazie al copia-incolla. 

Tuttavia Songpress ti permette di esportare le canzoni formattate in diversi altri formati. 

Attenzione però, la qualità delle canzoni esportate varia a seconda del formato di esportazione, e non sempre raggiunge la qualità che si ottiene con il copia-incolla.


## Esportare come immagine SVG

SVG è il formato standard per le immagini vettoriali. In linea di principio un'immagine SVG ha la stessa qualità dell'originale, e può essere ingrandita a piacimento senza perdita di definizione.
Tuttavia non tutti i programmi sono in grado di trattare i testi incorporati in un'immagine SVG allo stesso modo. Ad esempio, Scribus e alcuni browser web (Firefox, Chrome) visualizzano le immagini SVG prodotte da Songpress in modo molto simile all'originale, mentre la spaziatura dei testi in Inkscape risulta incorretta.

Per esportare una canzone, o la porzione di canzone selezionata, in formato SVG dai il comando **File -> Esporta -> Esporta come SVG**.


## Esportare come Enhanced Metafile (solo per Windows)

Il formato EMF (Enhanched Metafile) è un formato di grafica vettoriale proprietario di Microsoft Windows. Produrre un file EMF con Songpress ed importarlo in un'applicazione per Windows equivale a copiare l'immagine negli appunti da Songpress ed incollarla nell'applicazione di destinazione. La qualità dell'immagine è la massima possibile, anche qualora l'immagine sia ingrandita.

Per esportare una canzone, o la porzione di canzone selezionata, come metafile avanzato dai il comando **File -> Esporta -> Esporta come Enhanced Metafile**.


## Esportare come immagine PNG

Selezionando **File -> Esporta  -> Esporta come PNG** Songpress esporta la canzone, o la selezione corrente, come immagine PNG. Si tratta di un formato raster per le immagini. In altre parole, visualizzata con _zoom al 100%_ l’immagine _apparirà esattamente_ come la canzone nel riquadro di anteprima di Songpress. Aumentando il livello di zoom o stampando l’immagine, invece, questa sgranerà.


## Esportare come file HTML, ed incorporare la canzone in una pagina web

Selezionando **File -> Esporta -> Esporta come HTML** Songpress esporta la canzone, o la selezione corrente, come pagina web. La pagina generata appare molto simile alla canzone formattata in Songpress. Tuttavia le etichette delle strofe e dei ritornelli (cioè i numeri delle strofe e le “intestazioni” dei ritornelli) non saranno generati.

Per incorporare la canzone all’interno di un’altra pagina web:

1. Apri il file HTML generato in un editor di testo come Notepad2.
2. Copia tutto l’elemento `<style>…</style>` della pagina generata all’interno dell’elemento `<head>…</head>` della pagina di destinazione (per esempio immediatamente prima di `</head>`).
3. Copia tutto il contenuto dell’elemento `<body>…</body>` della pagina generata (escludendo i tag stessi) all’interno del body della pagina di destinazione, nel punto esatto dove vuoi far apparire la canzone incorporata.


## Esportare come file TAB/TXT con accordi sopra il testo

Selezionando **File -> Esporta  -> Esporta come TAB/TXT** Songpress esporta la canzone, o la selezione corrente, come semplice file di testo. 

Gli accordi sono posizionati al di sopra delle linee con il testo, utilizzando degli spazi per il posizionamento. Per una visione corretta del file di testo, occorre selezionare un font con i caratteri a dimensione fissa, come Courier New o Consolas.


## Generare una presentazione PowerPoint in stile karaoke

Selezionando **File -> Export  -> Esporta karaoke come PPTX** Songpress esporta la canzone, la selezione, o anche più canzoni (se sono tutte caricate nell'area di testo di Songpress, una dopo l'altra) come presentazione karaoke. Ogni diapositiva contiene fino a due versi: il verso corrente e il successivo. Se sono presenti più canzoni, sarà inserita una slide vuota tra una canzone e l'altra.

Alcuni template sono già disponibili, con sfondo nero e testo giallo/bianco, posizionato in punti diversi della diapositiva. Puoi creare template personalizzati copiando un file PPTX nella cartella templates/slides, all'interno del percorso di installazione di Songpress oppure nel percorso dei dati delle applicazioni dell'utente. Per esempio in Windows 10 i percorsi potrebbero essere i seguenti:

- C:\Program Files (x86)\Songpress\templates\slides (percorso di installazione di Songpress)
- C:\Users\YourName\AppData\Roaming\songpress\templates\slides (percorso dei dati delle applicazioni dell'utente)

Per creare un template personalizzato, modifica lo Schema Diapositiva del template (in PowerPoint: **Visualizza --> Schema Diapositiva**). Progetta la slide chiamata **Two Contents Layout**: contiene due aree di testo, che conterranno i due versi (il verso corrente e il successivo) da visualizzare in ogni slide.
