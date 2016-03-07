Translating Songpress
=====================

Songpress internationalization (aka i18n) is performed through the GNU gettext tools, and managed by Transifex.
In order to translate the program, all you need is a Transifex account. If you wish to test  translated strings
in your local Songpress installation, which is recommended, you need to install:

- gettext tools (commands: `xgettext`, `msgmerge`, `msgfmt`)
- the Transifex client (command: `tx`)


Songpress Transifex project
---------------------------

The Transifex project of Songpress is available at the following URL:

https://www.transifex.com/skeed/songpress-2/


Tips for translators
--------------------

- Strings with an ampersand (`&`) character in the middle are used to define keyboard shorcuts for menu (and submenu) items. The letter preceded by the ampersand sign becomes underlined, and the user can select that menu item by keying ALT + that letter (or simply the letter for submenu items). For example, if a menu item is defined as `&File`, letter `F` becomes a shortcut for that item, and user can select it by pressing `ALT + F`. It is important that, in translations, translated items have the `&` signs in positions such that the following letter is possibly unique within the menu (or submenu) the item belongs to.
- In several strings you can find placeholders for parameters, such as `%s` (a positional string parameter) or `%(verse_number)d` (an integer parameter named `verse_number`). Every parameter in a string must also appear in the translated version of the string. It is possible to modify the order in which _named_ parameter appear in the string. If you need to modify the order of _positional_ parameters, please open a ticket so that we transform those parameters into named parameter in the original string.


Testing your translation
------------------------

Preparation:

1. Make sure you have gettext and Transifex client installed on your system. [Configure the `.transifexrc` file with your Transifex account credentials](http://docs.transifex.com/client/config/).
2. Clone Songpress repository.
3. Make sure that the code of the language you are interested in appears in `tx.py` configuration file.
4. Make sure that the language you are interested in also appears in `src/Globals.py`.

Testing cycle:

1. Translate strings in Transifex
2. Go to the root directory of cloned respository, and type: <pre>python2 pygettext.py --pull</pre>
3. Run Songpress (don't forget to select your language in Tools -> Options):
<pre>
cd src
python2 main.py
</pre>
