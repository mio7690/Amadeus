python ${CODEDIR}/japanese_g2p.py -rsa \
    --input_file ${CODEDIR}/vits-japanese/filelists/cris_train.txt \
    --output_file ${CODEDIR}/vits-japanese/filelists/cris_train.txt.cleaned

python ${CODEDIR}/japanese_g2p.py -rsa \
    --input_file ${CODEDIR}/vits-japanese/filelists/cris_val.txt \
    --output_file ${CODEDIR}/vits-japanese/filelists/cris_val.txt.cleaned
    