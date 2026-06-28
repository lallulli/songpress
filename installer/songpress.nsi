; ============================================================
;  Songpress - Installer unificato
;  Pagina con radio button: Installazione normale o Portabile
; ============================================================

!define PRODUCT_NAME      "Songpress"
!define PRODUCT_VERSION   "(net installer)"
!define PRODUCT_PUBLISHER "Luca Allulli - Skeed"
!define PRODUCT_WEB_SITE  "http://www.skeed.it"
!define PRODUCT_DIR_REGKEY   "Software\Microsoft\Windows\CurrentVersion\App Paths\songpress.exe"
!define PRODUCT_UNINST_KEY   "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

; Il livello di esecuzione viene alzato a runtime solo se l'utente
; sceglie l'installazione normale. Per la portabile non serve admin.
RequestExecutionLevel admin
SetCompressor lzma

!include "MUI.nsh"
!include "FileAssociation.nsh"
!include "nsDialogs.nsh"   ; necessario per la pagina custom con radio button
!include "LogicLib.nsh"

; ---------------------------------------------------------------
;  MUI Settings
; ---------------------------------------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON   "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

!define MUI_LANGDLL_REGISTRY_ROOT      "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY       "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; ---------------------------------------------------------------
;  Pagine dell'installer
;  Ordine: Welcome > Licenza > [PAGINA SCELTA TIPO] >
;          [Directory solo se normale] > Componenti > Instfiles > Finish
; ---------------------------------------------------------------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\license.txt"

; Pagina custom: scelta tipo installazione
Page custom InstTypePageCreate InstTypePageLeave

; Directory (visibile solo per installazione normale, nascosta per portabile)
!define MUI_PAGE_CUSTOMFUNCTION_PRE  DirPagePre
!insertmacro MUI_PAGE_DIRECTORY

; Menu Start (solo installazione normale)
var ICONS_GROUP
!define MUI_STARTMENUPAGE_DEFAULTFOLDER   "Songpress"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT   "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY    "${PRODUCT_UNINST_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${PRODUCT_STARTMENU_REGVAL}"
!define MUI_PAGE_CUSTOMFUNCTION_PRE  StartMenuPagePre
!insertmacro MUI_PAGE_STARTMENU Application $ICONS_GROUP

; Componenti (solo installazione normale)
!define MUI_PAGE_CUSTOMFUNCTION_PRE  ComponentsPagePre
!insertmacro MUI_PAGE_COMPONENTS

!insertmacro MUI_PAGE_INSTFILES

; Pagina Finish: il tasto "Avvia" varia in base alla scelta
!define MUI_FINISHPAGE_RUN_FUNCTION  FinishRun
!define MUI_FINISHPAGE_RUN_TEXT      "$(STR_LAUNCH_SONGPRESS)"
!define MUI_FINISHPAGE_RUN           ""   ; non usato direttamente, usiamo la funzione
!insertmacro MUI_PAGE_FINISH

; Pagine disinstaller
!insertmacro MUI_UNPAGE_INSTFILES

; ---------------------------------------------------------------
;  Lingue
; ---------------------------------------------------------------
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Italian"

; --- Stringhe English ---
LangString UninstallAsk          ${LANG_ENGLISH} "A previous version of Songpress was found. It is recommended that you uninstall it first. Do you want to do that now?"
LangString UninstallPressOk      ${LANG_ENGLISH} "Press OK to continue upgrading your version of Songpress"
LangString STR_INSTALLING_SONGPRESS ${LANG_ENGLISH} "Installing Songpress via uv..."
LangString STR_INSTALL_SUCCESS   ${LANG_ENGLISH} "Installation completed successfully."
LangString STR_FALLBACK_PS       ${LANG_ENGLISH} "Attempting fallback via PowerShell..."
LangString STR_CRITICAL_ERROR    ${LANG_ENGLISH} "Critical error: Songpress not installed."
LangString STR_LAUNCH_SONGPRESS  ${LANG_ENGLISH} "Launch Songpress"
LangString STR_INSTTYPE_TITLE    ${LANG_ENGLISH} "Installation type"
LangString STR_INSTTYPE_SUBTITLE ${LANG_ENGLISH} "Choose how to install Songpress"
LangString STR_INSTTYPE_NORMAL   ${LANG_ENGLISH} "Standard installation (recommended)"
LangString STR_INSTTYPE_NORMAL_D ${LANG_ENGLISH} "Installs Songpress in Program Files, adds Start Menu shortcuts and file type associations. Requires administrator privileges."
LangString STR_INSTTYPE_PORTABLE ${LANG_ENGLISH} "Portable installation"
LangString STR_INSTTYPE_PORTAB_D ${LANG_ENGLISH} "Installs Songpress in a self-contained folder. No registry entries, no shortcuts. The folder can be moved to any PC or USB drive."
LangString STR_PORTABLE_NOTE     ${LANG_ENGLISH} "PORTABLE: Launch Songpress.exe to start the program."


; --- Stringhe Italian ---
LangString UninstallAsk          ${LANG_ITALIAN} "E' presente una versione precedente di Songpress. Si consiglia di disinstallarla prima di continuare. Eseguire la disinstallazione ora?"
LangString UninstallPressOk      ${LANG_ITALIAN} "Premi OK per continuare l'aggiornamento di Songpress"
LangString STR_INSTALLING_SONGPRESS ${LANG_ITALIAN} "Installazione Songpress in corso con uv..."
LangString STR_INSTALL_SUCCESS   ${LANG_ITALIAN} "Installazione completata con successo."
LangString STR_FALLBACK_PS       ${LANG_ITALIAN} "Tentativo di fallback tramite PowerShell..."
LangString STR_CRITICAL_ERROR    ${LANG_ITALIAN} "Errore critico: Songpress non installato."
LangString STR_LAUNCH_SONGPRESS  ${LANG_ITALIAN} "Avvia Songpress"
LangString STR_INSTTYPE_TITLE    ${LANG_ITALIAN} "Tipo di installazione"
LangString STR_INSTTYPE_SUBTITLE ${LANG_ITALIAN} "Scegli come installare Songpress"
LangString STR_INSTTYPE_NORMAL   ${LANG_ITALIAN} "Installazione standard (consigliata)"
LangString STR_INSTTYPE_NORMAL_D ${LANG_ITALIAN} "Installa Songpress in Programmi, crea scorciatoie nel menu Start e associa i tipi di file. Richiede privilegi di amministratore."
LangString STR_INSTTYPE_PORTABLE ${LANG_ITALIAN} "Installazione portabile"
LangString STR_INSTTYPE_PORTAB_D ${LANG_ITALIAN} "Installa Songpress in una cartella autonoma. Nessuna voce nel registro, nessuna scorciatoia. La cartella puo' essere spostata su qualsiasi PC o chiavetta USB."
LangString STR_PORTABLE_NOTE     ${LANG_ITALIAN} "PORTABILE: Avvia Songpress.exe per avviare il programma."

!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; ---------------------------------------------------------------
;  Variabili globali
; ---------------------------------------------------------------
Name    "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "songpress-${PRODUCT_VERSION}-setup.exe"
InstallDir "$PROGRAMFILES\Songpress"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show
AutoCloseWindow false

Var SongpressExe
Var UvCmd
Var InstallType          ; 0 = normale, 1 = portabile
Var RadioNormal
Var RadioPortable
Var LabelNormalDesc
Var LabelPortableDesc

; ---------------------------------------------------------------
;  Pagina custom: scelta tipo installazione
; ---------------------------------------------------------------
Function InstTypePageCreate
  !insertmacro MUI_HEADER_TEXT "$(STR_INSTTYPE_TITLE)" "$(STR_INSTTYPE_SUBTITLE)"

  nsDialogs::Create 1018
  Pop $0

  ; Radio button: Installazione normale
  ${NSD_CreateRadioButton} 10u 20u 280u 12u "$(STR_INSTTYPE_NORMAL)"
  Pop $RadioNormal
  ${NSD_CreateLabel} 24u 34u 266u 24u "$(STR_INSTTYPE_NORMAL_D)"
  Pop $LabelNormalDesc

  ; Radio button: Portabile
  ${NSD_CreateRadioButton} 10u 66u 280u 12u "$(STR_INSTTYPE_PORTABLE)"
  Pop $RadioPortable
  ${NSD_CreateLabel} 24u 80u 266u 28u "$(STR_INSTTYPE_PORTAB_D)"
  Pop $LabelPortableDesc

  ; Seleziona il radio corrispondente alla scelta precedente (o normale di default)
  ${If} $InstallType == 1
    ${NSD_SetState} $RadioPortable ${BST_CHECKED}
    ${NSD_SetState} $RadioNormal   ${BST_UNCHECKED}
  ${Else}
    ${NSD_SetState} $RadioNormal   ${BST_CHECKED}
    ${NSD_SetState} $RadioPortable ${BST_UNCHECKED}
  ${EndIf}

  nsDialogs::Show
FunctionEnd

Function InstTypePageLeave
  ${NSD_GetState} $RadioPortable $0
  ${If} $0 == ${BST_CHECKED}
    StrCpy $InstallType 1
    ; Portabile: cartella di default accanto all'installer
    StrCpy $INSTDIR "$EXEDIR\Songpress-portable"
  ${Else}
    StrCpy $InstallType 0
    ; Normale: ripristina cartella standard
    StrCpy $INSTDIR "$PROGRAMFILES\Songpress"
  ${EndIf}
FunctionEnd

; ---------------------------------------------------------------
;  Pre-funzioni pagine condizionali
; ---------------------------------------------------------------
Function DirPagePre
  ${If} $InstallType == 1
    Abort   ; salta la pagina Directory per l'installazione portabile
  ${EndIf}
FunctionEnd

Function StartMenuPagePre
  ${If} $InstallType == 1
    Abort   ; niente menu Start per la portabile
  ${EndIf}
FunctionEnd

Function ComponentsPagePre
  ${If} $InstallType == 1
    Abort   ; niente scelta componenti per la portabile
  ${EndIf}
FunctionEnd

; ---------------------------------------------------------------
;  Funzione Finish: avvia il programma correttamente
; ---------------------------------------------------------------
Function FinishRun
  ${If} $InstallType == 1
    Exec "$INSTDIR\Songpress.exe"
  ${Else}
    Exec "$INSTDIR\bin\songpress.exe"
  ${EndIf}
FunctionEnd

; ---------------------------------------------------------------
;  Disinstallazione vecchie versioni
; ---------------------------------------------------------------
Function UninstallOld
  push $R1
  ReadRegStr $R1 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$R0" "UninstallString"
  StrCmp $R1 "" UninstallMSI_nomsi
    MessageBox MB_YESNOCANCEL|MB_ICONQUESTION $(UninstallAsk) IDNO UninstallMSI_nomsi IDYES UninstallMSI_yesmsi
      Abort
UninstallMSI_yesmsi:
    ExecWait $R1
    MessageBox MB_OK|MB_ICONINFORMATION $(UninstallPressOk)
UninstallMSI_nomsi:
  pop $R1
FunctionEnd

; ---------------------------------------------------------------
;  Installazione core: uv + Python + Songpress
; ---------------------------------------------------------------
Function DoInstallPythonAndSongpress
  ; 1. Prepara uv
  InitPluginsDir
  File "/oname=$PLUGINSDIR\uv.exe" "uv.exe"
  StrCpy $UvCmd "$PLUGINSDIR\uv.exe"

  ; 2. Variabili d'ambiente per uv (puntano sempre a $INSTDIR)
  System::Call 'kernel32::SetEnvironmentVariable(t "UV_TOOL_BIN_DIR",       t "$INSTDIR\bin")'
  System::Call 'kernel32::SetEnvironmentVariable(t "UV_TOOL_DIR",           t "$INSTDIR\tools")'
  System::Call 'kernel32::SetEnvironmentVariable(t "UV_PYTHON_INSTALL_DIR", t "$INSTDIR\python")'
  System::Call 'kernel32::SetEnvironmentVariable(t "UV_CACHE_DIR",          t "$INSTDIR\cache")'

  ; 3. Installa Songpress
  DetailPrint "$(STR_INSTALLING_SONGPRESS)"
  nsExec::ExecToLog '"$UvCmd" tool install --force --python-preference system songpress'

  ; 4. Verifica e fallback PowerShell
  ${If} ${FileExists} "$INSTDIR\bin\songpress.exe"
    DetailPrint "$(STR_INSTALL_SUCCESS)"
  ${Else}
    DetailPrint "$(STR_FALLBACK_PS)"
    nsExec::ExecToLog 'powershell -Command "& { \
      $$env:UV_TOOL_BIN_DIR=$\"$INSTDIR\bin$\"; \
      $$env:UV_TOOL_DIR=$\"$INSTDIR\tools$\"; \
      $$env:UV_PYTHON_INSTALL_DIR=$\"$INSTDIR\python$\"; \
      $$env:UV_CACHE_DIR=$\"$INSTDIR\cache$\"; \
      & $\"$UvCmd$\" tool install --force songpress \
    }"'
    ${Unless} ${FileExists} "$INSTDIR\bin\songpress.exe"
      DetailPrint "$(STR_CRITICAL_ERROR)"
      Abort
    ${EndUnless}
  ${EndIf}

  StrCpy $SongpressExe "$INSTDIR\bin\songpress.exe"

  ; 5. Applica icona
  File "/oname=$PLUGINSDIR\icon-changer.exe" "icon-changer.exe"
  nsExec::ExecToLog '"$PLUGINSDIR\icon-changer.exe" "$INSTDIR\songpress.ico" "$SongpressExe"'

  ; 6. Pulizia cache
  RMDir /r "$INSTDIR\cache"
FunctionEnd

; ---------------------------------------------------------------
;  Disinstallazione Songpress
; ---------------------------------------------------------------
Function un.DoUninstallSongpress
  RMDir /r "$INSTDIR\bin"
  RMDir /r "$INSTDIR\tools"
  RMDir /r "$INSTDIR\python"
  RMDir /r "$INSTDIR\cache"
  Delete "$INSTDIR\songpress.ico"
  Delete "$INSTDIR\uninst.exe"
  RMDir  "$INSTDIR"
FunctionEnd

; ---------------------------------------------------------------
;  onInit
; ---------------------------------------------------------------
Function .onInit
  StrCpy $InstallType 0   ; default: installazione normale
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

; ---------------------------------------------------------------
;  Stringhe sezioni
; ---------------------------------------------------------------
LangString SongpressSectionNameLS ${LANG_ENGLISH} "Songpress"
LangString SongpressSectionNameLS ${LANG_ITALIAN} "Songpress"
LangString DesktopSectionNameLS   ${LANG_ENGLISH} "Desktop shortcut"
LangString DesktopSectionNameLS   ${LANG_ITALIAN} "Icona sul Desktop"
LangString CrdSectionNameLS       ${LANG_ENGLISH} "Associate CRD files"
LangString CrdSectionNameLS       ${LANG_ITALIAN} "Associa i file CRD"
LangString ChoSectionNameLS       ${LANG_ENGLISH} "Associate CHO files"
LangString ChoSectionNameLS       ${LANG_ITALIAN} "Associa i file CHO"
LangString ChordproSectionNameLS  ${LANG_ENGLISH} "Associate Chordpro files"
LangString ChordproSectionNameLS  ${LANG_ITALIAN} "Associa i file Chordpro"
LangString ChoproSectionNameLS    ${LANG_ENGLISH} "Associate Chopro files"
LangString ChoproSectionNameLS    ${LANG_ITALIAN} "Associa i file Chopro"
LangString ProSectionNameLS       ${LANG_ENGLISH} "Associate PRO files"
LangString ProSectionNameLS       ${LANG_ITALIAN} "Associa i file PRO"
LangString TabSectionNameLS       ${LANG_ENGLISH} "Associate TAB files"
LangString TabSectionNameLS       ${LANG_ITALIAN} "Associa i file TAB"
LangString FileAssociationSG      ${LANG_ENGLISH} "File type association"
LangString FileAssociationSG      ${LANG_ITALIAN} "Associa tipi di file"

; ---------------------------------------------------------------
;  SEZIONE PRINCIPALE: installazione normale o portabile
; ---------------------------------------------------------------
Section $(SongpressSectionNameLS) SongpressSection
  SectionIn RO

  SetOutPath "$INSTDIR"
  File "songpress.ico"

  ${If} $InstallType == 0
    ; ---- INSTALLAZIONE NORMALE ----
    push $R0
      StrCpy $R0 "Songpress"
      Call UninstallOld
    pop $R0

    SetShellVarContext all
    Call DoInstallPythonAndSongpress

    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
      CreateDirectory "$SMPROGRAMS\$ICONS_GROUP"
      CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Songpress.lnk" \
        "$INSTDIR\bin\songpress.exe" "" "$INSTDIR\songpress.ico" 0
    !insertmacro MUI_STARTMENU_WRITE_END

  ${Else}
    ; ---- INSTALLAZIONE PORTABILE ----
    Call DoInstallPythonAndSongpress

    ; Copia il vero exe di Songpress dalla cartella tools nella radice
    ; della cartella portabile come "Songpress.exe".
    ; Doppio click diretto, nessun intermediario, nessuna finestra CMD.
    CopyFiles "$INSTDIR\tools\songpress\Scripts\songpress.exe" "$INSTDIR\Songpress.exe"

    ; Applica l'icona anche a questo exe
    File "/oname=$PLUGINSDIR\icon-changer.exe" "icon-changer.exe"
    nsExec::ExecToLog '"$PLUGINSDIR\icon-changer.exe" "$INSTDIR\songpress.ico" "$INSTDIR\Songpress.exe"'

    DetailPrint "$(STR_PORTABLE_NOTE)"
  ${EndIf}

SectionEnd

; ---------------------------------------------------------------
;  Sezioni aggiuntive (solo installazione normale)
; ---------------------------------------------------------------
Section $(DesktopSectionNameLS) DesktopSection
  ${If} $InstallType == 0
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
      CreateShortCut "$DESKTOP\Songpress.lnk" \
        "$INSTDIR\bin\songpress.exe" "" "$INSTDIR\songpress.ico"
    !insertmacro MUI_STARTMENU_WRITE_END
  ${EndIf}
SectionEnd

Section -AdditionalIcons
  ${If} $InstallType == 0
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
      nsExec::Exec "del $SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk"
      CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk" "$INSTDIR\uninst.exe"
    !insertmacro MUI_STARTMENU_WRITE_END
  ${EndIf}
SectionEnd

SectionGroup $(FileAssociationSG)
Section $(CrdSectionNameLS) CrdSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".crd" "ChordPro"
    WriteRegStr HKCU "Software\Classes\ChordPro\DefaultIcon" "" "$INSTDIR\songpress.ico"
  ${EndIf}
SectionEnd
Section $(ChoSectionNameLS) ChoSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".cho" "ChordPro"
    WriteRegStr HKCU "Software\Classes\ChordPro\DefaultIcon" "" "$INSTDIR\songpress.ico"
  ${EndIf}
SectionEnd
Section $(ChordproSectionNameLS) ChordproSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".chordpro" "ChordPro"
    WriteRegStr HKCU "Software\Classes\ChordPro\DefaultIcon" "" "$INSTDIR\songpress.ico"
  ${EndIf}
SectionEnd
Section $(ChoproSectionNameLS) ChoproSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".chopro" "ChordPro"
    WriteRegStr HKCU "Software\Classes\ChordPro\DefaultIcon" "" "$INSTDIR\songpress.ico"
  ${EndIf}
SectionEnd
Section $(TabSectionNameLS) TabSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".tab" "TABChord"
    WriteRegStr HKCU "Software\Classes\TABChord\DefaultIcon" "" "$INSTDIR\songpress.ico"
  ${EndIf}
SectionEnd
Section $(ProSectionNameLS) ProSection
  ${If} $InstallType == 0
    ${registerExtension} "$INSTDIR\bin\songpress.exe" ".pro" "PROChord"
    WriteRegStr HKCU "Software\Classes\PROChord\DefaultIcon" "" "$INSTDIR\songpress.ico"
    System::Call 'shell32::SHChangeNotify(i 0x08000000, i 0, i 0, i 0)'
  ${EndIf}
SectionEnd
SectionGroupEnd

; ---------------------------------------------------------------
;  Sezione Post: registro e disinstallatore (solo normale)
; ---------------------------------------------------------------
Section -Post
  ${If} $InstallType == 0
    WriteUninstaller "$INSTDIR\uninst.exe"
    WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\songpress.exe"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName"     "$(^Name)"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon"     "$INSTDIR\songpress.exe"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion"  "${PRODUCT_VERSION}"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout"    "${PRODUCT_WEB_SITE}"
    WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher"       "${PRODUCT_PUBLISHER}"
  ${EndIf}
SectionEnd

; ---------------------------------------------------------------
;  Descrizioni sezioni
; ---------------------------------------------------------------
LangString SongpressSectionLS ${LANG_ENGLISH} "Songpress program files"
LangString SongpressSectionLS ${LANG_ITALIAN} "File eseguibili di Songpress"
LangString DesktopSectionLS   ${LANG_ENGLISH} "Create a shortcut on the Desktop"
LangString DesktopSectionLS   ${LANG_ITALIAN} "Crea un'icona di Songpress sul Desktop"
LangString CrdSectionLS       ${LANG_ENGLISH} "Open .crd files with Songpress"
LangString CrdSectionLS       ${LANG_ITALIAN} "Apre i file .crd con Songpress"
LangString ChoSectionLS       ${LANG_ENGLISH} "Open .cho files with Songpress"
LangString ChoSectionLS       ${LANG_ITALIAN} "Apre i file .cho con Songpress"
LangString ChordproSectionLS  ${LANG_ENGLISH} "Open .chordpro files with Songpress"
LangString ChordproSectionLS  ${LANG_ITALIAN} "Apre i file .chordpro con Songpress"
LangString ChoproSectionLS    ${LANG_ENGLISH} "Open .chopro files with Songpress"
LangString ChoproSectionLS    ${LANG_ITALIAN} "Apre i file .chopro con Songpress"
LangString TabSectionLS       ${LANG_ENGLISH} "Open .tab files with Songpress"
LangString TabSectionLS       ${LANG_ITALIAN} "Apre i file .tab con Songpress"
LangString ProSectionLS       ${LANG_ENGLISH} "Open .pro files with Songpress"
LangString ProSectionLS       ${LANG_ITALIAN} "Apre i file .pro con Songpress"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SongpressSection} $(SongpressSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${DesktopSection}   $(DesktopSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${CrdSection}       $(CrdSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${ChoSection}       $(ChoSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${ChordproSection}  $(ChordproSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${ChoproSection}    $(ChoproSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${TabSection}       $(TabSectionLS)
  !insertmacro MUI_DESCRIPTION_TEXT ${ProSection}       $(ProSectionLS)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; ---------------------------------------------------------------
;  Disinstallatore
; ---------------------------------------------------------------
LangString UninstallComplete ${LANG_ENGLISH} "$(^Name) has been successfully removed from your computer."
LangString UninstallComplete ${LANG_ITALIAN} "$(^Name) e' stato disinstallato con successo."
LangString UninstallConfirm  ${LANG_ENGLISH} "Are you sure to completely remove $(^Name)?"
LangString UninstallConfirm  ${LANG_ITALIAN} "Sei sicuro di voler rimuovere $(^Name)?"

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK $(UninstallComplete)
FunctionEnd

Function un.onInit
  !insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 $(UninstallConfirm) IDYES +2
  Abort
FunctionEnd

Section Uninstall
  !insertmacro MUI_STARTMENU_GETFOLDER "Application" $ICONS_GROUP
  Delete "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk"
  Delete "$DESKTOP\Songpress.lnk"
  Delete "$SMPROGRAMS\$ICONS_GROUP\Songpress.lnk"
  RMDir  "$SMPROGRAMS\$ICONS_GROUP"
  Delete "$INSTDIR\uninst.exe"

  Call un.DoUninstallSongpress

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  ${unregisterExtension} ".crd"      "ChordPro"
  ${unregisterExtension} ".cho"      "ChordPro"
  ${unregisterExtension} ".chordpro" "ChordPro"
  ${unregisterExtension} ".chopro"   "ChordPro"
  ${unregisterExtension} ".tab"      "TABChord"
  ${unregisterExtension} ".pro"      "PROChord"

  System::Call 'shell32::SHChangeNotify(i 0x08000000, i 0, i 0, i 0)'
  SetAutoClose true
SectionEnd
