#!/bin/sh
#Takes a full path of the html_dir without slash / charachter at the end
HTML_DIR=$1
cd $HTML_DIR
if [ ! -d ../newstext ]; then
 mkdir ../newstext
 mkdir ../newstext/empties
fi
for file in http*
do
 if [ ! -f ../newstext/$file ]; then
  tmp=$(echo "${file%.cms}.txt")
  python3 /home/osman/Dropbox/work/htmltotextstuff_timesofindia/gettext.py $file
  python3 /home/osman/Dropbox/work/htmltotextstuff_timesofindia/deletesamesubstr.py ../newstext/$tmp
  python3 /home/osman/Dropbox/work/htmltotextstuff_timesofindia/deletecertainstr.py ../newstext/$tmp
  python3 /home/osman/Dropbox/work/htmltotextstuff_timesofindia/addnewstime.py ../newstext/$tmp
  python3 /home/osman/Dropbox/work/htmltotextstuff_timesofindia/addnewslink.py ../newstext/$tmp
  echo "Finished $file"
 fi
done
exit 0
