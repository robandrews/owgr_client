cd /Users/raandrew/fun

COMMIT_MSG="Update repo for $(date)"

echo $COMMIT_MSG

git add -A
git commit -m "$COMMIT_MSG"
git push origin master
