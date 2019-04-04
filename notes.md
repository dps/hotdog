# Howto hotdog pin images

`https://emoji.slack-edge.com/T024F4A92/ylukem-hotdog/265cfab870a3c85c.png`

```
cat hdc | grep -o https://emoji[^\']*hotdog[^\']* > urls.txt
for a in `cat ../urls.txt`; do curl -o `echo $a | cut -d'/' -f 5`.png $a; done
```


# Products etc


blueprints/382
print_providers/20
```
{u'variants': [{u'print_areas': [{u'position': u'front', u'width': 283, u'height': 283}], u'options': {u'size': u'1"'}, u'id': 45153, u'title': u'1"'}, {u'print_areas': [{u'position': u'front', u'width': 425, u'height': 425}], u'options': {u'size': u'1,5"'}, u'id': 45154, u'title': u'1,5"'}], u'id': 20, u'title': u'Troupe Jewelry'}
```

# Mogrify
```
$ mogrify -path ../mog -bordercolor transparent -border 40 -format png *.png
```