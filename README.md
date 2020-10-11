# vim-fzotf

vim-fzotf: insert BibTeX citation keys from Zotero using fzf as a fuzzy finder interface.

Features:
- Queries the Zotero database directly, so if an item is added to Zotero while 
  editing in vim, it is immediately available to be cited
- Uses fzf to search any part of the citation (author, journal, title etc) to 
  reduce the mental friction when recalling the article
- Insert multiple citations at the same time using multiple selections in fzf 
  (press `TAB`)

## Intallation

vim-fzotf requires the [Better BibTeX][BBT] Zotero extension.  I would recommend 
this regardless of whether or not you use vim-fzotf, as it ensures that citation 
keys are stable between exports.

[BBT]: https://github.com/retorquere/zotero-better-bibtex

Install both [fzf][fzf] and vim-fzotf into your `&runtimepath` using your 
favourite package manager or Vim 8's built-in package support.  For example, 
using [vim-plug][vim-plug]:

    Plug 'junegunn/fzf'
    Plug 'andrewlkho/vim-fzotf'

[fzf]: https://github.com/junegunn/fzf/
[vim-plug]: https://github.com/junegunn/vim-plug


## Usage

By default, vim-fzotf does not map any new keybindings.  It provides 
`<Plug>FZotF` for you to remap to your keybinding of choice.  For example, 
I have

    imap <buffer> <C-F> <Plug>FZotF

in my `ftplugin/tex.vim` which means that while in insert mode pressing `CTRL-F`
will bring up the interface for inserting a citation.


## Configuration
    
### `g:fzotf_zotdir`

The location of the Zotero data directory.  This is set in Zotero under 
Preferences > Advanced > Files and Folders > Data Directory Location.  The 
default value in vim-fzotf is the Zotero-default of `~/Zotero` but if you have 
changed this you can set it with:

    let g:fzotf_zotdir = '~/Documents/Zotero'

### `g:fzotf_options`

Options to pass to [`fzf#run`][fzfrun].  The default is `--multi`.  I like to 
only have exact matches of each word as I often think in whole words when 
summoning up a citation, so I have set it to:

    let g:fztof_options = '--multi --exact'

[fzfrun]: https://github.com/junegunn/fzf/blob/master/README-VIM.md#fzfrun


## Issues

vim-fzotf works for my library, but I appreciate that many people put a diverse 
range of items in their Zotero library.  If something doesn't work for you then 
please [file an issue][issues].

[issues]: https://github.com/andrewlkho/vim-fzotf/issues


## Alternatives

- `:h ins-completion` with a BibTeX file open in another window
- [Zotcite][zotcite]: provides autocompletion amongst other useful features but 
  can only complete if you know the start of the citation key (`:Zseek` also 
  searches last author's name and title)
- [citation.vim][citation]: a citation source for [unite.vim][unite]

[zotcite]: https://github.com/jalvesaq/zotcite
[citation]: https://github.com/rafaqz/citation.vim
[unite]: https://github.com/Shougo/unite.vim
