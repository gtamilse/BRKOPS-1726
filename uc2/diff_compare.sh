files=(command_outputs*)
if [ ${#files[@]} -eq 2 ]; then
    diff -u "${files[0]}" "${files[1]}" | grep -E "^\+|^-"
else
    echo "There are not exactly two files matching the pattern."
fi