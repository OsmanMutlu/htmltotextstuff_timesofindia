#!/bin/sh
#Takes a full path of the html_dir without slash / charachter at the end
HTML_DIR=$1
cd $HTML_DIR
if [ ! -d ../random_newstext ]; then
 mkdir ../random_newstext
 mkdir ../random_newstext/empties
fi
for file in http*
do
 if [ ! -f ../random_newstext/$file ]; then
  tmp=$(echo "${file%.cms}.txt")
  python3 /ai/work/emw/htmltotextstuff_timesofindia/gettext.py $file
  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py ../random_newstext/$tmp
  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr2.py ../random_newstext/$tmp
  python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewstime.py ../random_newstext/$tmp
  python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewslink.py ../random_newstext/$tmp
  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py ../random_newstext/$tmp
  echo "Finished $file"
 fi
done
ls | grep -v "https__timesofindia" | grep "https" | sed -E "s/\d+\s*http/http/g" > ../random_newstext/redirected.txt
exit 0
