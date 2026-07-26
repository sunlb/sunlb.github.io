" indent配置
set tabstop=4
set shiftwidth=4
set softtabstop=4

set autoindent
set expandtab

filetype plugin indent on

" 选中配色
set hlsearch
syntax on
set number
set cursorline
hi CursorLine cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
set ruler

" 键盘映射（支持python、bash和C++）
map <F5> :w<cr>:!python %<cr>
map <F6> :w<cr>:!python3 %<cr>
map <F7> :w<cr>:!bash -xe %<cr>
map <F8> :w<cr>:!g++ % && ./a.out<cr>
