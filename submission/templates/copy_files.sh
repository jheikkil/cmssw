#!/bin/bash

source job_info.sh

source params.sh

echo "CLUSTER:" ${CLUSTERID}
echo "PROC-ID" ${PROCID}
echo 'TASKCONFDIR' ${ABSTASKCONFDIR}
echo 'OUT-DIR' ${OUTDIR}
echo 'OUTPUT-FILE' ${OUTFILE}


BATCH_DIR=${PWD}
echo "Current dir: ${BATCH_DIR}"
ls -l
extension="${OUTFILE##*.}"
filename="${OUTFILE%.*}"
OUTTARGET="${OUTDIR}/${filename}_${CLUSTERID}_${PROCID}.${extension}"
cp ${OUTFILE} ${OUTTARGET}
