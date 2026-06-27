# Panoramica

Songpress è un'applicazione che ti permette di comporre canzoni, con parole ed accordi, in modo semplice.

Dopo aver composto una canzone non puoi stamparla direttamente da Songpress. Invece la devi "trasferire" ad un'applicazione che sia in grado di stamparla; ad esempio puoi usare il tuo wordprocessor preferito (Microsoft Word, Openoffice.org ecc.), oppure un'applicazione di desktop publishing (come Affinity). Perché? Perché il mestiere di Songpress è comporre canzoni in modo gradevole - e Songpress è molto bravo a farlo! Ma preparare il layout di una pagina da stampare è il mestiere di altri tipi di programmi, come ad esempio i programmi di desktop publishing.

In breve, come comporre una canzone?

1. In Songpress, comporre una canzone nel formato ChordPro. Essenzialmente si tratta di scrivere le parole con gli accordi tra parentesi quadre: `[Do]Quando io ve[La-]dere [Re-]buccia di ba[Sol7]nana`.
2. Verifica la riuscita sul riquadro di anteprima. Se ti piace, vai al punto 3.
3. Copia la canzone formattata negli Appunti: seleziona Modifica -> Copia come Immagine
4. Apri il tuo _programma di pubblicazione_ preferito (es. Affinity) e incolla la tua canzone (Modifica -> Incolla).

## Installazione

Songpress supporta ufficialmente Windows e Linux. [L'installazione Linux](#installazione-tramite-ambiente-virtuale-python-e-pip) potrebbe funzionare anche su macOS, ma il programma non è stato testato su tale piattaforma.

### Installazione su Windows

Per installare Songpress su Windows, forniamo il [network installer](https://github.com/lallulli/songpress/releases/download/1.9.0/songpress-net-setup.exe) che scarica e installa la versione più aggiornata di Songpress.

Songpress è distribuito tramite [PyPI](https://pypi.org/project/songpress/), il gestore di pacchetti standard di Python. Il network installer usa la utility `uv` e compie le seguenti azioni:

1. Verifica se la versione più recente di Songpress è già installata sul computer. Se non lo è, l'installer scarica una versione locale di Python, dedicata a Songpress.
2. Scarica e installa Songpress e tutte le sue dipendenze.

Tutti i file sono contenuti in una singola sottocartella della directory _Programmi_, per consentire una rimozione pulita del programma, tramite l'_uninstaller_ .

### Installazione su Linux

!!! Warning "Attenzione"
    Songpress è scritto in [Python](https://python.org): verifica di avere Python installato sul tuo sistema Linux.

Su Linux, puoi installare Songpress in tre modi alternativi:

1. [Python virtual environment](https://docs.python.org/3/library/venv.html) e [pip](https://pypi.org/project/pip/)
2. [pipx](https://github.com/pypa/pipx)
3. [uv](https://github.com/astral-sh/uv)

Il processo di installazione può richiedere diversi minuti perché è necessario scaricare e compilare le librerie [wxPython](https://wxpython.org/) e [wxWidgets](https://wxwidgets.org/).

!!! Warning "Attenzione"
    Assicurati che il tuo sistema abbia i requisiti per  compilare le librerire [wxWidgets](https://docs.wxwidgets.org/3.2.10/page_introduction.html) e [wxPython](https://wiki.wxpython.org/How%20to%20install%20wxPython)


#### Installazione tramite ambiente virtuale Python e pip

Per prima cosa, crea un nuovo ambiente virtuale. Supponiamo che la cartella che contiene gli ambienti virtuali Python sia `~/.venv`:

```bash
python -m venv ~/.venv/songpress
```

quindi attiva l'ambiente appena creato:

```bash
source ~/.venv/songpress/bin/activate
```

quindi installa Songpress via pip:

```bash
pip install songpress
```

#### Installazione tramite pipx

Se hai installato [pipx](https://github.com/pypa/pipx) sul tuo computer:

```bash
pipx install songpress
```

#### Installazione tramite uv

In alternativa, puoi usare [uv](https://github.com/astral-sh/uv):

```bash
uv tool install songpress
```

### Lanciare Songpress

!!! note "Nota Bene"
    Se hai installato Songpress in un [virtual environment](#installazione-tramite-ambiente-virtuale-python-e-pip), devi attivare l'ambiente prima di lanciare l'applicazione:

    `source ~/.venv/songpress/bin/activate`

Puoi lanciare Songpress digitando:

```bash
songpress
```

Puoi aggiungere Songpress al menù Start lanciando:

```bash
songpress --create-shortcuts
```

Per aggiornare Songpress su Linux, digita:

```bash
pipx upgrade 

# se invece usi pip in un virtual environment:
#
# pip upgrade
#
```
