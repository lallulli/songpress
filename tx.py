# coding: utf-8

# tx_config = {
# 	'host': Transifex URL, e.g. 'https://www.transifex.com',
#		'project': Project SLUG
# 	'lang': List of target languages, e.g. ['it', 'fr', 'es'],
# 	'dir': Sorce directory, e.g. 'src',
# 	'xrc': Enable parsing of XRC files (boolean),
# 	'slugs': Opional mapping of resource filenames to slugs, e.g. {'xrc/songpress.xrc': 'songpress-gui'}
#   'exclude': List of excluded files and dirs
# }

config = {
	'host': 'https://www.transifex.com',
	'project': 'songpress-2',
	'lang': ['it', 'fr', 'es'],
	'dir': 'src',
	'xrc': True,
	'slugs': {'xrc/songpress.xrc': 'songpress-gui'},
	'exclude': ['__init__.py', 'build'],
}