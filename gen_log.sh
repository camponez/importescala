git log -n 6  --no-merges --pretty=format:"<li>%h - %cr - %s</li>" > changelog.html
echo >> changelog.html
