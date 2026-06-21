# Rilevamento automatico della tonalità

Una delle nuove funzionalità della prossima versione 1.1 di [Songpress](../index.md) è la trasposizione delle canzoni. Per effettuare una trasposizione corretta, è necessario conoscere la tonalità attuale del brano (o della sua sezione che si desidera trasporre) e la tonalità di destinazione (oppure, in modo equivalente, l'intervallo tra tonalità di partenza e di arrivo, espresso in semitoni).

Per questo motivo ho deciso di sperimentare un algoritmo in grado di "indovinare" la tonalità corrente di una canzone analizzandone gli accordi. L'idea di base è semplice: ogni tonalità possiede i propri accordi "naturali". Ad esempio, nei brani in tonalità di Do maggiore (C) gli accordi che compaiono più frequentemente sono C, F, G, Am, Dm, Em, E e, talvolta, A e D. Pertanto, se contiamo il numero di occorrenze di ciascun tipo di accordo, otteniamo una sorta di "impronta" del brano, che possiamo confrontare con le impronte di riferimento di tutte le possibili tonalità. La tonalità selezionata sarà quindi quella la cui impronta risulta più simile.

L'idea è semplice ma piuttosto generica; l'algoritmo completo è tanto semplice quanto il concetto stesso. È sufficiente conoscere le basi dell'algebra lineare.

Se si conta il numero di occorrenze di ciascun tipo di accordo in una canzone, si ottiene un vettore. Abbiamo deciso di considerare come tipi di accordo le modalità maggiore, minore, settima dominante e settima minore per ciascuna nota della scala cromatica. Di conseguenza, le componenti dei vettori delle canzoni sono il numero di occorrenze dei seguenti tipi di accordo: C, Cm, C7, Cm7, C#, C#m, C#7, C#m7, D, Dm, ..., B, Bm, B7, Bm7. Il vettore possiede quindi 12 × 4 = 48 componenti.

Ora normalizziamo il vettore della canzone. Otteniamo un versore la cui direzione è correlata alla tonalità del brano: ci aspettiamo infatti che tutte le canzoni in una determinata tonalità condividano approssimativamente lo stesso versore. Di conseguenza, tutto ciò che dobbiamo conoscere è il versore associato a ciascuna tonalità. Consideriamo un insieme di riferimento di canzoni in tonalità di C (nella pratica ho utilizzato il nostro [canzoniere della Santa Messa](http://www.roma21.it/assets/Download/CantiMessaCRD.zip): ho scartato alcuni brani irregolari e trasposto tutti gli altri in tonalità di C); concateniamo tali canzoni e calcoliamo il versore della "canzone" risultante. In questo modo otteniamo il versore di riferimento "C / Am". Mediante una semplice rotazione di tale versore possiamo ottenere i versori corrispondenti alle altre 11 tonalità.

Per determinare la tonalità di una canzone, calcoliamo il versore del brano **v** e lo confrontiamo con i 12 versori delle tonalità: è sufficiente calcolare il prodotto scalare tra **v** e ciascuno dei versori di tonalità e selezionare il valore massimo.

Per curiosità, ecco il versore di riferimento "C / Am" (arrotondato a 2 cifre decimali per migliorarne la leggibilità):

| Accordo | Maggiore | Minore | 7    | Minore 7 |
| ------- | -------- | ------ | ---- | -------- |
| C       | 0,66     | 0      | 0,04 | 0        |
| C#      | 0        | 0      | 0    | 0        |
| D       | 0,03     | 0,12   | 0    | 0,03     |
| D#      | 0        | 0      | 0    | 0        |
| E       | 0,04     | 0,13   | 0,03 | 0        |
| F       | 0,46     | 0,01   | 0    | 0        |
| F#      | 0        | 0      | 0    | 0        |
| G       | 0,50     | 0      | 0,02 | 0        |
| G#      | 0        | 0      | 0    | 0        |
| A       | 0,01     | 0,26   | 0,01 | 0        |
| A#      | 0        | 0      | 0    | 0        |
| B       | 0        | 0      | 0    | 0        |

Quanto bene funziona questo algoritmo? Sorprendentemente bene sul mio insieme di canzoni:

* Ho inizializzato l'algoritmo utilizzando una sola canzone di riferimento e l'ho impiegato per trasporre la prima metà del mio insieme di dati (circa 30 canzoni su 60): l'algoritmo ha fallito soltanto su 4 brani;
* Ho aggiornato il versore di riferimento utilizzando la prima metà del dataset; ho eseguito nuovamente l'algoritmo sui 4 brani problematici e solo 1 continuava a essere classificato erroneamente;
* Ho completato la trasposizione dell'insieme di riferimento senza ulteriori errori e ho aggiornato nuovamente il versore di riferimento;
* Infine, ho testato l'algoritmo completamente calibrato su un altro insieme di canzoni ([canti degli scout lupetti](http://www.roma21.it/assets/Download/FioreRosso/crd.zip)) ottenendo un solo errore.

È interessante osservare che i 2 brani classificati erroneamente sono canzoni fortemente orientate alla modalità minore in Am, nelle quali gli unici accordi presenti sono Am, Dm ed E; l'algoritmo ritiene che la loro tonalità sia E / C#m (poiché E è l'unico accordo maggiore presente nel brano e riceve un peso elevato nel prodotto scalare con il versore E / C#m grazie alla componente E del versore stesso). Forse potrebbe essere utile generare un insieme di versori di riferimento specifici per le canzoni "fortemente" in tonalità minore.
