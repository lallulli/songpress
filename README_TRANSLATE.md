Translating Songpress
=====================

Songpress internationalization (aka i18n) is performed through the GNU gettext tools, and managed by Transifex.
In order to translate the program, all you need is a Transifex account. If you wish to test  translated strings
in your local Songpress installation, which is recommended, you need to install:

- gettext tools (commands: xgettext, 
- the Transifex client (command: tx)


Songpress Transifex project
---------------------------

The Transifex project of Songpress is available at the following URL:

https://www.transifex.com/skeed/songpress-2/


Tips for translators
--------------------

- Strings with an ampersand (`&`) character in the middle are used to define keyboard shorcuts for menu (and submenu) items. The letter preceded by the ampersand sign becomes underlined, and the user can select that menu item by keying ALT + that letter (or simply the letter for submenu items). For example, if a menu item is defined as `&File`, letter `F` becomes a shortcut for that item, and user can select it by pressing `ALT + F`. It is important that, in translations, translated items have the `&` signs in positions such that the following letter is possibly unique within the menu (or submenu) the item belongs to.
