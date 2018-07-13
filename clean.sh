#!/bin/sh
#Takes a full path of the html_dir without slash / charachter at the end
HTML_DIR=$1
TEXT_DIR=$2
cd $HTML_DIR
if [ ! -d $TEXT_DIR ]; then
 mkdir $TEXT_DIR
 mkdir $TEXT_DIR/empties
fi
python3 /scratch/users/omutlu/htmltotextstuff_timesofindia/gettext.py $TEXT_DIR/
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr2.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewstime.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewslink.py ../random_newstext/$tmp
#  python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py ../random_newstext/$tmp
#ls | grep -v "https__timesofindia" | grep "https" | sed -E "s/\d+\s*http/http/g" > ../random_newstext/redirected.txt
exit 0
