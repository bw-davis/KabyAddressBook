# you need to ensure you have already done git add <files> and git commit.  
# then ->
git checkout master
git pull
git checkout $1
git rebase master
git push origin $1