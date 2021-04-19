#!/usr/bin/env bash

dest='/app/instance/backup_data'
original='/app/instance/data.xlsx'
expiry='7776000'

base=$(basename -- ${original})
original_name=${base%%.*}
original_ext=${base##*.}
id=$(date '+%y_%m_%d')
back=${dest}/${original_name}-${id}.${original_ext}

mkdir -p $dest
mv ${original} ${back}
for filename in ${dest}/${original_name}*.${original_ext}; do
  name_file=${filename##*-}
  id_file=${name_file%%.*}
  date_diff=$(($(date -d ${id//_/-} '+%s') - $(date -d ${id_file//_/-} '+%s')))
  if (( date_diff > expiry )); then
    rm ${filename}
  fi
done
