import os
import os.path
import shutil
from optparse import OptionParser

def createDirAndGo(path, dir):
    final = os.path.join(path, dir)
    if not os.path.isdir(final) and not os.path.isfile(final):
        os.mkdir(final)
    return final

transifex_header = """
[main]
host = {host}
"""

transifex_item = """
[{project}.{slug}]
file_filter = {prefix}locale/<lang>/LC_MESSAGES/{file}.po
source_file = {prefix}{file}.pot
source_lang = en
type = PO
"""

def execute(path, relpath, xrc=False, lang=[], tx=None):
    print(path)
    tx_out = ""
    d = os.listdir(path)
    created = []
    prefix = relpath
    for f in d:
        if tx is None or not f in tx['exclude']:
            fp = os.path.join(path, f)
            relpath = os.path.join(prefix, f)
            if os.path.isfile(fp):
                n, e = os.path.splitext(f)
                if xrc and e == '.xrc':
                    newfp = os.path.join(path, n + '.pos')
                    print(newfp, fp)
                    wx.tools.pywxrc.main(['', '-g', '-o', newfp, fp])
                    fp = newfp
                if e == '.py' or (xrc and e == '.xrc'):
                    pot = os.path.join(path, n + '.pot')
                    s = 'xgettext -L python "%s" -o "%s"' % (fp, pot)
                    print(s)
                    os.system(s)
                    if os.path.isfile(pot):
                        created.append(n + ".pot")
                        if tx is not None:
                            slug = n
                            print("Relpath", relpath)
                            if relpath in tx['slugs']:
                                slug = tx['slugs'][relpath]
                            tx_out += transifex_item.format(
                                project=tx['project'],
                                slug=slug,
                                prefix='' if prefix == '' else prefix + '/',
                                file=n,
                            )
            else:
                tx_out += execute(fp, relpath, xrc, lang, tx)
    if len(lang)>0 and len(created)>0:
        p = createDirAndGo(path, 'locale')
        for l in lang:
            pl = createDirAndGo(p, l)
            pl = createDirAndGo(pl, 'LC_MESSAGES')
            for f in created:
                n, e = os.path.splitext(f)
                fn = os.path.join(pl, n + ".po")
                fm = os.path.join(pl, n + ".mo")
                fo = os.path.join(path, f)
                if os.path.isfile(fn):
                    s = 'msgmerge -U "%s" "%s"' % (fn, fo)
                    print(s)
                    os.system(s)
                    s = 'msgfmt -o "%s" "%s"' % (fm, fn)
                    print(s)
                    os.system(s)
                else:
                    shutil.copy(fo, fn)
    return tx_out

def tx_push(dir):
    pwd = os.getcwd()
    os.chdir(dir)
    os.system('tx push -s -t --skip')
    os.chdir(pwd)

def tx_pull(dir, mode):
    pwd = os.getcwd()
    os.chdir(dir)
    c = 'tx pull --mode {}'.format(mode)
    print(c)
    os.system(c)
    os.chdir(pwd)



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-P", "--push",
                                        action="store_true", dest="push", default=False,
                                        help="transifex push after extracting strings",
                                        )
    parser.add_option("-p", "--pull",
                                        action="store_true", dest="pull", default=False,
                                        help="transifex pull and compile translations",
                                        )
    parser.add_option("-m", "--mode",
                                        action="store", dest="mode", type="string", default="translator",
                                        help="for --pull, specify pull mode: translator (default), developer or reviewed",
                                        )
    parser.add_option("-t", "--transifex",
                                        action="store_true", dest="transifex", default=False,
                                        help="enable Transifex support (requires configuration file tx.py, ignore other options)")
    parser.add_option("-d", "--dir", dest="dir",
                                        help="directory to process")
    parser.add_option("-l", "--languages", dest="lang",
                                        help="comma-separated list of languages to handle (init, merge)")
    parser.add_option("-x", "--xrc",
                                        action="store_true", dest="xrc", default=True,
                                        help="process xrc files (wxWidgets required)")

    (options, args) = parser.parse_args()

    if options.transifex or options.push or options.pull:
        import tx

        if tx.config['xrc']:
            import wx.tools.pywxrc

        out = transifex_header.format(host=tx.config['host'])
        out += execute(tx.config['dir'], '', tx.config['xrc'], tx.config['lang'], tx.config)
        with open(os.path.join(tx.config['dir'], '.tx', 'config'), "w") as w:
            w.write(out)

        if options.pull:
            tx_pull(tx.config['dir'], options.mode)
            execute(tx.config['dir'], '', tx.config['xrc'], tx.config['lang'], tx.config)

        if options.push:
            tx_push(tx.config['dir'])

        exit(0)

    if options.xrc:
        import wx.tools.pywxrc
    if options.lang != None:
        lang = options.lang.split(',')
    else:
        lang = []
    if options.dir == None:
        path = os.path.join(os.path.abspath(os.curdir), 'src')
    else:
        path = options.dir
    execute(path, '', options.xrc, lang)
