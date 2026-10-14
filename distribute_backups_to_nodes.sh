#!/usr/bin/env bash
# Script sinkronisasi cadangan dari Node 10 ke Node 6 (Master SG) & Node 8 (lightvela3)
while true; do
    if [ -f "/root/uh-zero/uh_zero_v2_checkpoint.pt" ]; then
        # 1. Simpan salinan cadangan snapshot lokal di Node 10
        mkdir -p /root/uh-zero/backups
        cp -u /root/uh-zero/uh_zero_v2_checkpoint.pt /root/uh-zero/backups/uh_zero_v2_checkpoint_backup.pt
        
        # 2. Replikasi ke Node 6 (Master SG 94.237.69.121)
        rsync -avz --inplace /root/uh-zero/uh_zero_v2_checkpoint.pt root@94.237.69.121:/root/uh-zero/backups/uh_zero_v2_checkpoint.pt >/dev/null 2>&1
        
        # 3. Replikasi ke Node 8 (100.95.44.105 lightvela3)
        rsync -avz --inplace /root/uh-zero/uh_zero_v2_checkpoint.pt agentuser@100.95.44.105:/home/agentuser/uh-zero-backup/uh_zero_v2_checkpoint.pt >/dev/null 2>&1
    fi
    sleep 900 # Replikasi antar-node setiap 15 menit
done
