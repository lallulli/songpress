# Songpress - Il Canzonatore

Songpress è un programma gratuito e facile da usare, per Linux e Windows, per comporre canzonieri di alta qualità.

Songpress è specializzato nel _formattare le canzoni_. Queste, poi, potranno essere incollate nel'editor di documenti che preferisci: così potrai conferire al tuo canzoniere esattamente l'aspetto che desideri.

![Screenshot](assets/screenshot_mini.png)

## Funzionalità

- Produce _spartiti per chitarra di alta qualità_ (testo e accordi)
- Facile da imparare, veloce nell'utilizzo
- Puoi incollare _le canzoni formattate in qualsiasi applicazione per Linux o Windows_, per comporre il tuo canzoniere con il massimo grado di flessibilità (Affinity, Microsoft Word, LibreOffice, Microsoft Publisher, Inkscape ecc.)
- Espotazione delle canzoni formattate come immagini _SVG, PNG, pagine HTML_ (o porzioni di pagine web) e presentazioni _PPTX_ (karaoke)
- _Trasposizione degli accordi_, con rilevamento automatico della tonalità
- _Semplificazione degli accordi_ per chitarristi principianti: determina la tonalità in cui è più facile suonare la canzone, e la traspone automaticamente
- Supporta _molte notazioni_ per gli accordi: americana (C, D, E), italiana (Do, Re, Mi), francese, tedesca e portoghese; _converte_ da una notazione all'altra
- Supporta i formati _ChordPro_ e _Tab_ (testo e accordi disposti su due linee)
- _Formatta_ le canzoni incollate da pagine web che contengono, ad esempio, linee vuote di troppo

Se hai bisogno di aiuto, o vuoi discutere su Songpress, visita il nostro [gruppo di supporto](https://groups.google.com/g/songpress?pli=1).


## Installazione

Vedi la pagina [Per iniziare](manual/getting_started.it.md) del manuale.


## Esempi di canzonieri

Come appare un canzoniere prodotto con Songpress? Qui puoi vederlo con i tuoi occhi. Se fai clic su una di queste immagini, sarai reindirizzato al sito del nostro Gruppo Scout, dove potrai scaricare sia il PDF dei canzonieri, sia i file ChordPro usati per generarli.

[![Canti per la S. Messa](assets/cantichi_3_copertina_m.png){hspace=30}](http://www.roma21.it/index.php?id=353)
[![Canzonieri dei Lupetti](assets/canzmor_09.png){hspace=30}](http://www.roma21.it/index.php?id=879)


## Codice sorgente e licenza

Songpress è rilasciato con una licenza open source, la [GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).

Segui le indicazioni sul nostro [repository GitHub](https://github.com/lallulli/songpress).


## Storia

Il progetto ebbe origine dalla necessità di produrre un Canzoniere per la S. Messa per il Gruppo Scout Roma 21. Abbiamo creato l'algoritmo di formattazione delle canzoni e le funzionalità di copia-incolla in poco tempo.

Nell'introduzione del canzoniere c'è una promessa::

>Per comporre accuratamente e velocemente testo e accordi, abbiamo prodotto un software apposito.
> Potremo utilizzarlo in futuro per realizzare altri canzonieri; abbiamo in programma di migliorarlo e renderlo disponibile, come software libero (open source)."

Inizialmente non avevamo tempo per migliorare il programma trasformandolo in un'applicazione vera, utilizzabile da utenti che non fossero... smanettoni. Tempo fa abbiamo deciso di riscrivere il programma da zero, in Python (molto più divertente che il C++)... e la promessa è stata mantenuta!


## Aiuta il progetto

Songpress usa il servizio di hosting GitHub (in precedenza, Google Code e BerliOS).

Puoi contribuire in diversi modi:

- [segnalando malfunzionamenti](https://github.com/lallulli/songpress/issues)
- creando nuove traduzioni
- migliorando la grafica (icone, bottoni ecc.)
- contribuendo allo sviluppo (se si un programmatore Python)


## Il formato ChordPro

Songpress usa un sottoinsieme del [formato ChordPro(https://www.chordpro.org/chordpro/chordpro-directives/)].

E' facile da usare. Basta scrivere le parole della canzone, e...

- per inserire il titolo, usa il comando `{title:Il titolo}` o `{t:Il titolo}`: `{title:Fratelli d'Italia}`
- per inserire un accordo, inseriscilo tra parentesi quadre, subito prima della sillaba in cui l'accordo "inizia": `[Do]Fratelli d'Italia l'I[Sol]talia s'è [Do]desta`
- per iniziare una nuova strofa, lascia una linea vuota
- per inserire un ritornello, racchiudilo tra i comandi `{soc}` o `{start_of_chorus}` e `{eoc}` o `{end_of_chorus}`: `{soc}Dov'è la vittoria...{eoc}`
- per inserire un commento, usa il comando `{comment:Il commento}` o `{c:Il commento}` : `{c:2 volte}`
- Ogni linea che inizia con # non genera niente (usalo per i commenti nel file ChordPro)

Per ulteriori informazioni sul formato ChordPro, guarda la relativa [pagina del manuale](manual/chordpro.it.md).