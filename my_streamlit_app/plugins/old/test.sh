## #!/Program Files/Git/bin/bash.exe

echo Hello
echo "Current dir: $(pwd)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Sending plugins/folder_test.sh with args: $1 and $2, $3"

bash "$SCRIPT_DIR/../plugins/folder_test.sh" "$1" "$2" "$3"

