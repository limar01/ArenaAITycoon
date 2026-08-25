#!/usr/bin/env bash
set -e

ACTION="${1:-help}"

if [ "$ACTION" = "send" ]; then
    CMD="$2"
    if [ -z "$CMD" ]; then
        echo "Usage: bash mq.sh send \"<command>\""
        exit 1
    fi
    python3 -c "
import sys
from bridge.mqagent import exec_remote

cmd = '''$CMD'''
res = exec_remote(cmd, timeout=30)

if 'error' in res:
    print(f\"[ERROR] {res['error']}: {res.get('stderr','')}\", file=sys.stderr)
    sys.exit(1)
else:
    output = res.get('output') or res.get('stdout') or ''
    if output:
        print(output, end='')
    if res.get('stderr'):
        print(res['stderr'], end='', file=sys.stderr)
    sys.exit(res.get('exit_code', 0))
"

elif [ "$ACTION" = "ping" ]; then
    python3 -c "
import sys
from bridge.mqagent import exec_remote

res = exec_remote('echo PONG', timeout=10)
if 'error' in res:
    print(f'Worker offline or not responding ({res[\"error\"]})')
    sys.exit(1)
else:
    print(f'Worker online! Output: {res.get(\"output\", \"\").strip()}')
"

else
    echo "ArenaBridge Worker v4 Client"
    echo "Commands:"
    echo "  bash mq.sh ping                     - Ping remote phone worker"
    echo "  bash mq.sh send \"<command>\"         - Run bash command on remote phone"
fi
