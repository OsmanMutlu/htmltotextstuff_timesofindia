#!/bin/sh
#Takes a full path of the html_dir without slash / charachter at the end. text_dir needs to be in the same folder as html_dir and given with no path
HTML_DIR=$1
TEXT_DIR=$2
#cd $HTML_DIR
#if [ ! -d ../$TEXT_DIR ]; then
# mkdir ../$TEXT_DIR
#fi
#python3 /ai/work/emw/htmltotextstuff_timesofindia/gettext.py ../$TEXT_DIR/
#echo "Finished justext"
#cd ..
#cp -r $TEXT_DIR backup_$TEXT_DIR
#echo "Got backup"
cd $TEXT_DIR
python3 /ai/work/emw/htmltotextstuff_timesofindia/all_in_one.py $HTML_DIR/
#python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py
#python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr.py
#python3 /ai/work/emw/htmltotextstuff_timesofindia/deletecertainstr2.py
#python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewstime.py $HTML_DIR/
#python3 /ai/work/emw/htmltotextstuff_timesofindia/addnewslink.py
#python3 /ai/work/emw/htmltotextstuff_timesofindia/deletesamesubstr.py
exit 0
