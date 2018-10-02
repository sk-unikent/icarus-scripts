# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# Add local bin paths.
export PATH=$HOME/.local/bin:$HOME/bin:$PATH

# Add local LD paths.
export LD_RUN_PATH=$LD_RUN_PATH:~/.local/lib/:~/.local/lib64/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib/:~/.local/lib64/
export PKG_CONFIG_PATH=.local/lib/pkgconfig

# For our other stuff.
for file in ~/.config/kent/shellext/.bash_*; do
    [ -f "$file" ] && source "$file"
done

# For your custom stuff.
for file in ~/.config/local/.bash_*; do
    [ -f "$file" ] && source "$file"
done
