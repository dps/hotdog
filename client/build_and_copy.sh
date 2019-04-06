OLD_VERSION=`cat ../live_client_version.txt`
git rm ../static/js/$OLD_VERSION
npm run build
OUTPUT=`cat build/index.html | grep -o "main.[a-z0-9]*.js"`
cp build/static/js/$OUTPUT ../static/js/
echo $OUTPUT > ../live_client_version.txt
git add ../static/js/$OUTPUT
git add ../live_client_version.txt

echo New version is $OUTPUT. You have staged git changes to commit.