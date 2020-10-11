if exists("g:loaded_fzotf")
    finish
endif
let g:loaded_fzotf = 1

let s:fzotf_zotdir = get(g:, 'fzotf_zotdir', '~/Zotero')
let s:fzotf_options = get(g:, 'fzotf_options', '--multi')

let s:source = 'python3 ' . expand('<sfile>:p:h') . '/../python/fzotf.py -z ' . s:fzotf_zotdir

function! s:FZotF()
    let items = fzf#run({'source': s:source, 'options': s:fzotf_options, 'down': 15})
    let citekeys = []
    for item in items
        call add(citekeys, split(item, " ")[0])
    endfor
    return join(citekeys, ",")
endfunction

inoremap <script><expr> <Plug>FZotF <SID>FZotF()
