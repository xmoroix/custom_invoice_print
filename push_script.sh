#\!/bin/bash
eval "$(ssh-agent -s)"
expect -c "
spawn ssh-add ~/.ssh/id_ed25519
expect \"Enter passphrase\"
send \"moroix\r\"
expect eof
"
git push -u origin main
