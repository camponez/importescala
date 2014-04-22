git log -n 6  --no-merges --pretty=format:"<li>%h - %cd - %s</li>" > changelog.html
echo >> changelog.html
