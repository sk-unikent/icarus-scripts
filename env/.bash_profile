# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# Add local bin paths.
PATH=$HOME/.local/bin:$HOME/bin:$PATH
export PATH

# For our other stuff.
for file in ~/.config/kent/shellext/.bash_*; do
    [ -f "$file" ] && source "$file"
done
