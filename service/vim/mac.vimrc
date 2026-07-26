filetype plugin indent on
syntax on

set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent
set expandtab

" 选中配色
set hlsearch        " 高亮搜索结果
set number          " 显示行号
set cursorline      " 高亮当前行
hi CursorLine cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
set ruler           " 右下方显示行数,列数

" 简单键盘映射（支持python、bash和C++）
map <F6> :w<cr>:!echo "【运行结果】" && python3 %<cr>
map <F7> :w<cr>:!echo "【运行结果】" && bash -xe %<cr>
map <F8> :w<cr>:!g++ % && echo "【运行结果】" && ./a.out<cr>

" 复杂键盘映射（将F5映射为通用执行函数）
nnoremap <F5> :call ExecuteCurrentFile()<CR>
inoremap <F5> <ESC>:call ExecuteCurrentFile()<CR>

" 按文件类型分别执行
function! ExecuteCurrentFile()
    write  " 保存当前文件
    let filetype = &filetype  " 获取文件类型
    " python
    if filetype == 'python'
        execute '!python3 "' . expand('%:p') . '"'
    " c++
    elseif filetype == 'cpp'
        let output = expand('%:p:r')  " 无扩展名的完整路径
        if has('win32')
            execute '!g++ -o "' . output . '.exe" "' . expand('%:p') . '" && "' . output . '.exe"'
        else
            execute '!g++ -o "' . output . '" "' . expand('%:p') . '" && "' . output . '"'
        endif
    " shell
    elseif filetype == 'sh'
        execute '!bash -xe "' . expand('%:p') . '"'
    else
        echo "警告：Unsupported file type: " . filetype
    endif
endfunction