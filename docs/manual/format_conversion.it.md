# Conversioni di formato

## Dal formato tab a Chordpro

Songpress è in grado di convertire le canzoni dal formato "tab" a ChordPro.

Nel formato "tab" gli accordi si trovano sopra il testo, in linee separate:

```
   Do                                 Sol
Un gobo ed una goba a l'età di novant'anni
                                                    Do
per por fine ai loro affanni per por fine ai loro affanni...
```

Per convertire una singola linea di accordi al formato ChordPro, posiziona li cursore sulla linea e seleziona **Modifica -> Integra gli accordi**.

Per convertire l'intera canzone, o una selezione, usa **Strumenti -> Converti formato da tab a ChordPro**.


## Canzoni con linee vuote di troppo

Frequentemente ci si imbatte in canzoni, sia in formato ChordPro che (più spesso) in formato "tab", con alcune linee vuote di troppo. A volte le linee vuote compaiono in seguito ad un'operazione di copia-incolla. Per esempio:

```
   Do                                 Sol
Un gobo ed una goba a l'età di novant'anni
                                          (questa è una linea vuota)
                                                    Do
per por fine ai loro affanni per por fine ai loro affanni...
```
 

E' necessario rimuovere tutte le linee vuote, ad eccezione di quelle che servono a separare due strofe. Fortunatamente ci può pensare Songpress: è sufficiente selezionare **Strumenti -> Rimuovi** le linee vuote di troppo.

!!! warning "Ricorda"
    Se una canzone è nel formato "tab", prima rimuovi le linee vuote di troppo (se ci sono); dopodiché converti la canzone al formato ChordPro.


## Strumenti automatici

Songpress è in grado di rilevare se una canzone ha linee vuote di troppo, o se è nel formato "tab", e convertirla automaticamente al formato ChordPro pulito (naturalmente dopo aver chiesto conferma). Questa caratteristica è attiva di default; se vuoi disattivarla, seleziona **Strumenti -> Opzioni** e **disattiva gli Strumenti automatici**.
