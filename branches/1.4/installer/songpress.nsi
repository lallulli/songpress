; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Songpress"
!define PRODUCT_VERSION "1.4.2"
!define PRODUCT_PUBLISHER "Luca Allulli - Skeed"
!define PRODUCT_WEB_SITE "http://www.skeed.it"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\songpress.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"

RequestExecutionLevel admin
SetCompressor lzma

Function UninstallOld
  ; $R0 should contain the GUID of the application, i.e. Songpress
  push $R1
  ReadRegStr $R1 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$R0" "UninstallString"
  StrCmp $R1 "" UninstallMSI_nomsi
    MessageBox MB_YESNOCANCEL|MB_ICONQUESTION  $(UninstallAsk) IDNO UninstallMSI_nomsi IDYES UninstallMSI_yesmsi
      Abort
UninstallMSI_yesmsi:
    ExecWait $R1
    MessageBox MB_OK|MB_ICONINFORMATION $(UninstallPressOk)
UninstallMSI_nomsi:
  pop $R1
FunctionEnd

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "FileAssociation.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "..\license.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Start menu page
var ICONS_GROUP
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "Songpress"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${PRODUCT_STARTMENU_REGVAL}"
!insertmacro MUI_PAGE_STARTMENU Application $ICONS_GROUP
; Components
!insertmacro MUI_PAGE_COMPONENTS
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\songpress.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Italian"

LangString UninstallAsk ${LANG_ENGLISH} "A previous version of Songpress was found. It is recommended that you uninstall it first. Do you want to do that now?"
LangString UninstallAsk ${LANG_ITALIAN} "E' presente una versione precedente di Songpress. Si consiglia di disinstallarla prima di continuare. Eseguire la disinstallazione ora?"
LangString UninstallPressOk ${LANG_ENGLISH} "Press OK to continue upgrading your version of Songpress"
LangString UninstallPressOk ${LANG_ITALIAN} "Premi OK per continuare l'aggiornamento di Songpress"


; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "songpress-${PRODUCT_VERSION}-setup.exe"
InstallDir "$PROGRAMFILES\Songpress"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

LangString SongpressSectionNameLS ${LANG_ENGLISH} "Songpress"
LangString SongpressSectionNameLS ${LANG_ITALIAN} "Songpress"
LangString DesktopSectionNameLS ${LANG_ENGLISH} "Desktop shortcut"
LangString DesktopSectionNameLS ${LANG_ITALIAN} "Icona sul Desktop"
LangString CrdSectionNameLS ${LANG_ENGLISH} "Associate CRD files"
LangString CrdSectionNameLS ${LANG_ITALIAN} "Associa i file CRD"
LangString ChoSectionNameLS ${LANG_ENGLISH} "Associate CHO files"
LangString ChoSectionNameLS ${LANG_ITALIAN} "Associa i file CHO"
LangString ChordproSectionNameLS ${LANG_ENGLISH} "Associate Chordpro files"
LangString ChordproSectionNameLS ${LANG_ITALIAN} "Associa i file Chordpro"
LangString ChoproSectionNameLS ${LANG_ENGLISH} "Associate Chopro files"
LangString ChoproSectionNameLS ${LANG_ITALIAN} "Associa i file Chopro"
LangString TabSectionNameLS ${LANG_ENGLISH} "Associate TAB files"
LangString TabSectionNameLS ${LANG_ITALIAN} "Associa i file TAB"
LangString FileAssociationSG ${LANG_ENGLISH} "File type association"
LangString FileAssociationSG ${LANG_ITALIAN} "Associa tipi di file"

Section $(SongpressSectionNameLS) SongpressSection

  push $R0
    StrCpy $R0 "Songpress";  the ProductID of my package
    Call UninstallOld
  pop $R0

  SetShellVarContext all
  SectionIn RO
  SetOutPath "$INSTDIR"
  SetOverwrite try
  SetOutPath "$INSTDIR"
  File "..\src\dist\Songpress\bz2.pyd"
  File "..\src\dist\Songpress\Microsoft.VC90.CRT.manifest"
  File "..\src\dist\Songpress\msvcm90.dll"
  File "..\src\dist\Songpress\msvcp90.dll"
  File "..\src\dist\Songpress\msvcr90.dll"
  File "..\src\dist\Songpress\pyexpat.pyd"
  File "..\src\dist\Songpress\python27.dll"
  File "..\src\dist\Songpress\pywintypes27.dll"
  File "..\src\dist\Songpress\select.pyd"
  File "..\src\dist\Songpress\Songpress.exe"
  File "..\src\dist\Songpress\Songpress.exe.manifest"
  File "..\src\dist\Songpress\unicodedata.pyd"
  File "..\src\dist\Songpress\win32api.pyd"
  File "..\src\dist\Songpress\win32evtlog.pyd"
  File "..\src\dist\Songpress\win32pipe.pyd"
  File "..\src\dist\Songpress\wx._aui.pyd"
  File "..\src\dist\Songpress\wx._controls_.pyd"
  File "..\src\dist\Songpress\wx._core_.pyd"
  File "..\src\dist\Songpress\wx._gdi_.pyd"
  File "..\src\dist\Songpress\wx._html.pyd"
  File "..\src\dist\Songpress\wx._misc_.pyd"
  File "..\src\dist\Songpress\wx._stc.pyd"
  File "..\src\dist\Songpress\wx._windows_.pyd"
  File "..\src\dist\Songpress\wx._xrc.pyd"
  File "..\src\dist\Songpress\wxbase292u_net_vc.dll"
  File "..\src\dist\Songpress\wxbase292u_vc.dll"
  File "..\src\dist\Songpress\wxbase292u_xml_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_adv_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_aui_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_core_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_html_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_stc_vc.dll"
  File "..\src\dist\Songpress\wxmsw292u_xrc_vc.dll"
  File "..\src\dist\Songpress\_ctypes.pyd"
  File "..\src\dist\Songpress\_hashlib.pyd"
  File "..\src\dist\Songpress\_socket.pyd"
  File "..\src\dist\Songpress\_ssl.pyd"
  SetOutPath "$INSTDIR\help"
  File "..\src\dist\Songpress\help\songpress-en.chm"
  File "..\src\dist\Songpress\help\songpress-fr.chm"
  File "..\src\dist\Songpress\help\songpress-it.chm"
  SetOutPath "$INSTDIR\img"
  File "..\src\dist\Songpress\img\chord.png"
  File "..\src\dist\Songpress\img\chorus.png"
  File "..\src\dist\Songpress\img\copy.png"
  File "..\src\dist\Songpress\img\copyAsImage.png"
  File "..\src\dist\Songpress\img\copyAsImage2.png"
  File "..\src\dist\Songpress\img\cut.png"
  File "..\src\dist\Songpress\img\labelVerses.png"
  File "..\src\dist\Songpress\img\new.png"
  File "..\src\dist\Songpress\img\open.png"
  File "..\src\dist\Songpress\img\paste.png"
  File "..\src\dist\Songpress\img\pasteChords.png"
  File "..\src\dist\Songpress\img\redo.png"
  File "..\src\dist\Songpress\img\save.png"
  File "..\src\dist\Songpress\img\songpress.ico"
  File "..\src\dist\Songpress\img\songpress.png"
  File "..\src\dist\Songpress\img\title.png"
  File "..\src\dist\Songpress\img\undo.png"
  SetOutPath "$INSTDIR\locale"
  SetOutPath "$INSTDIR\locale\fr"
  SetOutPath "$INSTDIR\locale\fr\LC_MESSAGES"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\errdlg.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\FontFaceDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\MyPreferencesDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\MyUpdateDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\NotationDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\Preferences.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\PreferencesDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\SDIMainFrame.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\SongpressFrame.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\Transpose.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\TransposeDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\UpdateDialog.mo"
  File "..\src\dist\Songpress\locale\fr\LC_MESSAGES\UpdatePanel.mo"
  SetOutPath "$INSTDIR\locale\it"
  SetOutPath "$INSTDIR\locale\it\LC_MESSAGES"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\FontFaceDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\MyPreferencesDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\MyUpdateDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\NotationDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\Preferences.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\PreferencesDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\SDIMainFrame.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\SongpressFrame.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\Transpose.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\TransposeDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\UpdateDialog.mo"
  File "..\src\dist\Songpress\locale\it\LC_MESSAGES\UpdatePanel.mo"
  SetOutPath "$INSTDIR\xrc"
  File "..\src\dist\Songpress\xrc\songpress.xrc"
  SetOutPath "$INSTDIR\xrc\locale"
  SetOutPath "$INSTDIR\xrc\locale\fr"
  SetOutPath "$INSTDIR\xrc\locale\fr\LC_MESSAGES"
  File "..\src\dist\Songpress\xrc\locale\fr\LC_MESSAGES\songpress.mo"
  SetOutPath "$INSTDIR\xrc\locale\it"
  SetOutPath "$INSTDIR\xrc\locale\it\LC_MESSAGES"
  File "..\src\dist\Songpress\xrc\locale\it\LC_MESSAGES\songpress.mo"


; Shortcuts
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateDirectory "$SMPROGRAMS\$ICONS_GROUP"
  CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Songpress.lnk" "$INSTDIR\songpress.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section $(DesktopSectionNameLS) DesktopSection
  SetShellVarContext all
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  CreateShortCut "$DESKTOP\Songpress.lnk" "$INSTDIR\songpress.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section -AdditionalIcons
  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
  nsExec::Exec "del $SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk"
  CreateShortCut "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk" "$INSTDIR\uninst.exe"
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

SectionGroup $(FileAssociationSG)
Section $(CrdSectionNameLS) CrdSection
  ${registerExtension} "$INSTDIR\songpress.exe" ".crd" "ChordPro file"
SectionEnd
Section $(ChoSectionNameLS) ChoSection
  ${registerExtension} "$INSTDIR\songpress.exe" ".cho" "ChordPro file"
SectionEnd
Section $(ChordproSectionNameLS) ChordproSection
  ${registerExtension} "$INSTDIR\songpress.exe" ".chordpro" "ChordPro file"
SectionEnd
Section $(ChoproSectionNameLS) ChoproSection
  ${registerExtension} "$INSTDIR\songpress.exe" ".chopro" "ChordPro file"
SectionEnd
Section $(TabSectionNameLS) TabSection
  ${registerExtension} "$INSTDIR\songpress.exe" ".tab" "TAB chord file"
SectionEnd
SectionGroupEnd


Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\songpress.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\songpress.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


;--------------------------------
;Descriptions

  ;USE A LANGUAGE STRING IF YOU WANT YOUR DESCRIPTIONS TO BE LANGAUGE SPECIFIC

  ;Assign descriptions to sections
  LangString SongpressSectionLS ${LANG_ENGLISH} "Songpress program files"
  LangString SongpressSectionLS ${LANG_ITALIAN} "File eseguibili di Songpress"
  LangString DesktopSectionLS ${LANG_ENGLISH} "Create a shortcut on the Desktop"
  LangString DesktopSectionLS ${LANG_ITALIAN} "Crea un'icona di Songpress sul Desktop"
  LangString CrdSectionLS ${LANG_ENGLISH} "Open .crd files with Songpress"
  LangString CrdSectionLS ${LANG_ITALIAN} "Apre i file .crd con Songpress"
  LangString ChoSectionLS ${LANG_ENGLISH} "Open .cho files with Songpress"
  LangString ChoSectionLS ${LANG_ITALIAN} "Apre i file .cho con Songpress"
  LangString ChordproSectionLS ${LANG_ENGLISH} "Open .chordpro files with Songpress"
  LangString ChordproSectionLS ${LANG_ITALIAN} "Apre i file .chordpro con Songpress"
  LangString ChoproSectionLS ${LANG_ENGLISH} "Open .chopro files with Songpress"
  LangString ChoproSectionLS ${LANG_ITALIAN} "Apre i file .chopro con Songpress"
  LangString TabSectionLS ${LANG_ENGLISH} "Open .tab files with Songpress"
  LangString TabSectionLS ${LANG_ITALIAN} "Apre i file .tab con Songpress"
  
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SongpressSection} $(SongpressSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${DesktopSection} $(DesktopSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${CrdSection} $(CrdSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${ChoSection} $(ChoSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${ChordproSection} $(ChordproSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${ChoproSection} $(ChoproSectionLS)
    !insertmacro MUI_DESCRIPTION_TEXT ${TabSection} $(TabSectionLS)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

LangString UninstallComplete ${LANG_ENGLISH} "$(^Name) has been successfully removed from your computer."
LangString UninstallComplete ${LANG_ITALIAN} "$(^Name) � stato disinstallato con successo."

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK $(UninstallComplete)
FunctionEnd

LangString UninstallConfirm ${LANG_ENGLISH} "Are you sure to completely remove $(^Name)?"
LangString UninstallConfirm ${LANG_ITALIAN} "Sei sicuro di voler rimuovere $(^Name)?"

Function un.onInit
  !insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 $(UninstallConfirm) IDYES +2
  Abort
FunctionEnd

Section Uninstall
  !insertmacro MUI_STARTMENU_GETFOLDER "Application" $ICONS_GROUP
  SetShellVarContext all
  Delete "$SMPROGRAMS\$ICONS_GROUP\Uninstall.lnk"
  Delete "$DESKTOP\Songpress.lnk"
  Delete "$SMPROGRAMS\$ICONS_GROUP\Songpress.lnk"
  RMDir "$SMPROGRAMS\$ICONS_GROUP"
  Delete "$INSTDIR\uninst.exe"
  
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\Microsoft.VC90.CRT.manifest"
  Delete "$INSTDIR\msvcm90.dll"
  Delete "$INSTDIR\msvcp90.dll"
  Delete "$INSTDIR\msvcr90.dll"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\python27.dll"
  Delete "$INSTDIR\pywintypes27.dll"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\Songpress.exe"
  Delete "$INSTDIR\Songpress.exe.manifest"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\win32api.pyd"
  Delete "$INSTDIR\win32evtlog.pyd"
  Delete "$INSTDIR\win32pipe.pyd"
  Delete "$INSTDIR\wx._aui.pyd"
  Delete "$INSTDIR\wx._controls_.pyd"
  Delete "$INSTDIR\wx._core_.pyd"
  Delete "$INSTDIR\wx._gdi_.pyd"
  Delete "$INSTDIR\wx._html.pyd"
  Delete "$INSTDIR\wx._misc_.pyd"
  Delete "$INSTDIR\wx._stc.pyd"
  Delete "$INSTDIR\wx._windows_.pyd"
  Delete "$INSTDIR\wx._xrc.pyd"
  Delete "$INSTDIR\wxbase292u_net_vc.dll"
  Delete "$INSTDIR\wxbase292u_vc.dll"
  Delete "$INSTDIR\wxbase292u_xml_vc.dll"
  Delete "$INSTDIR\wxmsw292u_adv_vc.dll"
  Delete "$INSTDIR\wxmsw292u_aui_vc.dll"
  Delete "$INSTDIR\wxmsw292u_core_vc.dll"
  Delete "$INSTDIR\wxmsw292u_html_vc.dll"
  Delete "$INSTDIR\wxmsw292u_stc_vc.dll"
  Delete "$INSTDIR\wxmsw292u_xrc_vc.dll"
  Delete "$INSTDIR\_ctypes.pyd"
  Delete "$INSTDIR\_hashlib.pyd"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_ssl.pyd"
  Delete "$INSTDIR\help\songpress-en.chm"
  Delete "$INSTDIR\help\songpress-fr.chm"
  Delete "$INSTDIR\help\songpress-it.chm"
  Delete "$INSTDIR\img\chord.png"
  Delete "$INSTDIR\img\chorus.png"
  Delete "$INSTDIR\img\copy.png"
  Delete "$INSTDIR\img\copyAsImage.png"
  Delete "$INSTDIR\img\copyAsImage2.png"
  Delete "$INSTDIR\img\cut.png"
  Delete "$INSTDIR\img\labelVerses.png"
  Delete "$INSTDIR\img\new.png"
  Delete "$INSTDIR\img\open.png"
  Delete "$INSTDIR\img\paste.png"
  Delete "$INSTDIR\img\pasteChords.png"
  Delete "$INSTDIR\img\redo.png"
  Delete "$INSTDIR\img\save.png"
  Delete "$INSTDIR\img\songpress.ico"
  Delete "$INSTDIR\img\songpress.png"
  Delete "$INSTDIR\img\title.png"
  Delete "$INSTDIR\img\undo.png"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\errdlg.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\FontFaceDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\MyPreferencesDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\MyUpdateDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\NotationDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\Preferences.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\PreferencesDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\SDIMainFrame.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\SongpressFrame.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\Transpose.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\TransposeDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\UpdateDialog.mo"
  Delete "$INSTDIR\locale\fr\LC_MESSAGES\UpdatePanel.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\FontFaceDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\MyPreferencesDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\MyUpdateDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\NotationDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\Preferences.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\PreferencesDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\SDIMainFrame.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\SongpressFrame.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\Transpose.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\TransposeDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\UpdateDialog.mo"
  Delete "$INSTDIR\locale\it\LC_MESSAGES\UpdatePanel.mo"
  Delete "$INSTDIR\xrc\songpress.xrc"
  Delete "$INSTDIR\xrc\locale\fr\LC_MESSAGES\songpress.mo"
  Delete "$INSTDIR\xrc\locale\it\LC_MESSAGES\songpress.mo"
  RMDir "$INSTDIR\xrc\locale\it\LC_MESSAGES"
  RMDir "$INSTDIR\xrc\locale\it"
  RMDir "$INSTDIR\xrc\locale\fr\LC_MESSAGES"
  RMDir "$INSTDIR\xrc\locale\fr"
  RMDir "$INSTDIR\xrc\locale"
  RMDir "$INSTDIR\xrc"
  RMDir "$INSTDIR\locale\it\LC_MESSAGES"
  RMDir "$INSTDIR\locale\it"
  RMDir "$INSTDIR\locale\fr\LC_MESSAGES"
  RMDir "$INSTDIR\locale\fr"
  RMDir "$INSTDIR\locale"
  RMDir "$INSTDIR\img"
  RMDir "$INSTDIR\help"
  RMDir "$INSTDIR"


  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  ${unregisterExtension} ".crd" "ChordPro file"
  ${unregisterExtension} ".cho" "ChordPro file"
  ${unregisterExtension} ".chordpro" "ChordPro file"
  ${unregisterExtension} ".chopro" "ChordPro file"
  ${unregisterExtension} ".tab" "TAB chord file"
  SetAutoClose true
SectionEnd