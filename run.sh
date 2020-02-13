rm -r -f img __pycache__
mkdir img
python3 buildMovie.py --enable-libfreetype --enable-libfontconfig --enable-libfribidi
open img/out.mp4
