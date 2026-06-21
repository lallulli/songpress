# Da Subversion a Mercurial

Abbiamo appena migrato il nostro repository su [Google Code](http://code.google.com/p/songpress/source/checkout) da Subversion a Mercurial, preservando l'intera cronologia del progetto.

La migrazione in sé è stata semplice e diretta. La parte difficile è stata capire come eseguirla utilizzando un client Windows, perché le [istruzioni di Google](http://code.google.com/p/support/wiki/ConvertingSvnToHg) omettono di specificare dove trovare una libreria essenziale, ovvero i binding svn-python. Questo breve tutorial spiega come eseguire la migrazione in un modo alternativo.

Tutto ciò che serve è:

- un'installazione recente di [TortoiseHg](http://tortoisehg.bitbucket.org/) (python-svn è incluso in TortoiseHg, quindi non è necessario installare la libreria);
- l'estensione [hgsubversion](http://mercurial.aragost.com/kick-start/hgsubversion.html) (invece di convert).

In pratica, tutto ciò che dobbiamo fare è abilitare l'estensione hgsubversion in TortoiseHg; clonare il repository Subversion (come se fosse un repository Mercurial); e caricare il repository clonato nel nuovo repository Mercurial.

Nel dettaglio, ecco la procedura passo passo:

1. **Assicurati di avere una versione recente di TortoiseHg installata**.
2. **Scarica hgsubversion**. Ho creato una directory temporanea sul mio desktop, ho clonato il repository http://bitbucket.org/durin42/hgsubversion in quella directory usando TortoiseHg; e poi ho spostato la sottocartella denominata **hgsubversion** nella directory di TortoiseHg, ovvero **C:\Programmi\TortoiseHG**.
3. **Abilita l'estensione hgsubversion in TortoiseHg**. Per prima cosa, devi capire dove TortoiseHg memorizza le sue impostazioni. Si trovano in un file chiamato **mercurial.ini**, che può essere situato nella directory di TortoiseHg o nella directory home dell'utente (ad esempio, **C:\Utenti\IlMioNome** o **C:\Documenti e Impostazioni\IlMioNome**). Modifica **mercurial.ini**, trova la sezione `[extensions]` (o creane una) e aggiungi questa riga: **hgsubversion = C:\percorso\a\hgsubversion** (ad esempio, **hgsubversion = C:\Program Files\TortoiseHg\hgsubversion**).
4. **Clona il tuo repository Subversion usando TortoiseHg**. Crea una directory e clona http://tuoprogetto.googlecode.com/svn/. Se tutto ha funzionato correttamente, TortoiseHg non segnalerà errori relativi al repository non Mercurial e lo clonerà (l'operazione richiederà del tempo).
5. **Passa a Mercurial nella scheda di amministrazione del progetto, in Google Code**.
6. **Effettua il push del tuo repository locale nel nuovo repository Mercurial su Google Code**. Usa **Hg Repository Explorer** di TortoiseHg; digita https://yourproject.googlecode.com/hg/ nella barra degli indirizzi e seleziona il comando **Sincronizza -> Push**. Ricorda che, come in Subversion, la tua password è quella "temporanea" assegnata da Google. Puoi trovarla cliccando su **Profilo** e selezionando la scheda **Impostazioni**.

...questo è tutto, buon lavoro con Mercurial!