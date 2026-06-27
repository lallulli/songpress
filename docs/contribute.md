# Support the project

First of all: many thanks to spend your time on contributing to this application!

Songpress is hosted at [Github](https://github.com/lallulli/songpress) and you can help in several ways:

- reporting bugs or suggest improvements, via our [issue tracker on Github](https://github.com/lallulli/songpress/issues)
- creating new translations
- providing artwork (icons, buttons etc.)
- contributing to the code, by forking our repository and submitting a pull request
- contributing to the documentation

<span>
<!--
## Contributing to the translation

Songpress internationalization (aka i18n) is performed through the GNU gettext tools, and managed by Transifex.
In order to translate the program, all you need is a Transifex account. If you wish to test translated strings in your local Songpress installation, which is recommended, you need to install:

- gettext tools (commands: `xgettext`, `msgmerge`, `msgfmt`)
- the Transifex client (command: `tx`)

-->
</span>

### Songpress Transifex project

The Transifex project of Songpress is available at the following URL:

https://www.transifex.com/skeed/songpress-2/


### Tips for translators

- Strings with an ampersand (`&`) character in the middle are used to define keyboard shorcuts for menu (and submenu) items. The letter preceded by the ampersand sign becomes underlined, and the user can select that menu item by keying ALT + that letter (or simply the letter for submenu items). For example, if a menu item is defined as `&File`, letter `F` becomes a shortcut for that item, and user can select it by pressing `ALT + F`. It is important that, in translations, translated items have the `&` signs in positions such that the following letter is possibly unique within the menu (or submenu) the item belongs to.
- In several strings you can find placeholders for parameters, such as `%s` (a positional string parameter) or `%(verse_number)d` (an integer parameter named `verse_number`). Every parameter in a string must also appear in the translated version of the string. It is possible to modify the order in which _named_ parameter appear in the string. If you need to modify the order of _positional_ parameters, please open a ticket so that we transform those parameters into named parameter in the original string.


### Testing your translation

Preparation:

1. Make sure you have gettext and Transifex client installed on your system. [Configure the `.transifexrc` file with your Transifex account credentials](http://docs.transifex.com/client/config/).
2. Clone Songpress repository.
3. Make sure that the code of the language you are interested in appears in `tx.py` configuration file.
4. Make sure that the language you are interested in also appears in `src/Globals.py`.

Testing cycle:

1. Translate strings in Transifex
2. Go to the root directory of cloned respository, and type: `python pygettext.py --pull`
3. Run Songpress (don't forget to select your language in Tools -> Options):

```bash
cd src
python main.py
```


### Expert mode

`python pygettext.py -t` analyzes the source directory (according to configuration defined in `tx.py`), extracts i18n strings using `xgettext`, prepares directories and files for i18n (the `locale/<lang>/LC_MESSAGES/<file>.po` files) if they are not existing, or merges and compiles them if they are already existing. Moreover, the command prepares the Transifex configuration file `.tx/config`.

Thus, instead of using Transifex web editor, you can edit `.po` files directly (e.g. with poedit).

In order to upload translations to Transifex you can issue:

```bash
python pygettext.py --push
```

## Contributing to the documentation

[Songpress documentation site](index.md) is written in [Markdown](https://www.markdownguide.org/) and built by the following tools:

- [mkdocs](https://www.mkdocs.org/) static site generator
- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) for theme and functionalities not included in mkdocs
- [mkdocs-static-i18n](https://ultrabug.github.io/mkdocs-static-i18n/) to localize the site in several languages (English and Italian are available by now)


### Setting up your environment

Markdown is just simple text so you can write the documentation via a text editor.
But probably you may want to build and run Songpress documentation site locally, to see your contribution before submitting a pull request.

Firstly, be sure to have python installed on your computer. Open a shell and run: `python --version`.
If Python is installed, you receive a simple output like this: `Python 3.12.3`.

Then create a [virtual environment](https://docs.python.org/3/library/venv.html) for Songpress and activate it(suppose your virtual environments directory is `.venv`):

```bash
python -m venv .venv/songpress

source .venv/songpress/bin/activate
```

and install all the tools via **pip**:

```bash
pip install mkdocs mkdocs-material mkdocs-static-i18n
```

Well done! Now, you are ready to run the documentation site!

Fork the repository, clone it locally and, from the root of the project, run `mkdocs serve`.
Now, pointing your browser to `http://localhost:8000`, you can see the documentation site.

The `serve` Mkdocs command automatically update the site whenever you modify one of the documents or the configuration file `mkdocs.yml`.
