# From Subversion to Mercurial

We have just migrated our repository on [Google Code](http://code.google.com/p/songpress/source/checkout) from Subversion to Mercurial, preserving the whole project history.

The migration itself was simple and straightforward. The hard part was figuring it out how to perform the migration using a Windows client, because [Google's directions](http://code.google.com/p/support/wiki/ConvertingSvnToHg) omit to specify where to find an essential library, the svn-python bindings. This short tutorial explains how to do the migration in an alternative way.

All that you need is:

- a recent installation of [TortoiseHg](http://tortoisehg.bitbucket.org/) (python-svn is bundled with TortoiseHg, thus you don't need to install the library);
- the [hgsubversion](http://mercurial.aragost.com/kick-start/hgsubversion.html) extension (instead of convert).

Basically, all we need to do is enabling the hgsubversion extension in TortoiseHg; clone the subversion repository (as if it were a mercurial repository); and push the cloned repository into the brand new mercurial repository.

In more details, this is the step-by-step recipe:

1. **Make sure you have a recent version of TortoiseHg installed**.
2. **Download hgsubversion**. I created a temporary directory on my desktop, cloned the repository http://bitbucket.org/durin42/hgsubversion on that directory using TortoiseHg; and then moved the subdirectory named **hgsubversion** into TortoiseHg's dir, i.e. **C:\Program files\TortoiseHG**.
3. **Enable the hgsubversion extension in TortoiseHg**. First, you have to figure out where TortoiseHg stores its settings. It is in a file named **mercurial.ini**, which can be located either in the TortoiseHg dir or in the user home dir (i.e.. **C:\Users\MyName** or **C:\Documents and Settings\MyName**). Edit **mercurial.ini**, find the `[extensions]` section (or create one), and add this line: **hgsubversion = C:\path\to\hgsubversion** (e.g. **hgsubversion = C:\Program Files\TortoiseHg\hgsubversion**).
4. **Clone your subversion repository using TortoiseHg**. Create a directory, and clone http://yourproject.googlecode.com/svn/. If everething worked well, TortoiseHg will not complain that the repository isn't a mercurial one, and will clone it (it will take some time).
5. **Switch to Mercurial in your project administration tab, in Google Code**.
6. **Push your local repository into your brand new mercurial repository on Google code**. Use TortoiseHg's **Hg Repository Explorer**; type https://yourproject.googlecode.com/hg/ in the address bar, and select the **Synchronize -> Push** command. Remember that, like in subversion, your password is the "temporary" one assigned by Google. You can find it by clicking on **Profile** and selecting the **Settings** tab.

...that's all folks, happy hg-ing!
