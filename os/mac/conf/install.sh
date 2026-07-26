# 判断是否写入，如果没有，则在最后写入
append_to_file() {
    grep -qxF "$1" "$2" || echo "$1" >> "$2"
}

append_to_file 'source "$HOME/Dev/unix_learn/operation_system/mac/conf/bash.conf"' "$HOME/.bash_profile"
append_to_file 'source "$HOME/Dev/unix_learn/operation_system/mac/conf/zsh.conf"' "$HOME/.zshrc"
append_to_file 'source $HOME/Dev/unix_learn/operation_system/mac/conf/vim.conf' "$HOME/.vimrc" # 注意vim的source路径不能加"
