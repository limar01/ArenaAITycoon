#!/usr/bin/env python3
"""
sync_push.py - Chunked MQTT push of a large file to the remote ArenaBridge worker.
Worker v4 'put_file' op (base64 b64 field, MAX_FILE=2,000,000 bytes, path locked to SYNC_ROOT).
Broker packet limit measured ~700KB raw per publish -> chunk = 700*1024 bytes.

Usage:
  python3 sync_push.py prepare <tar.gz> <remote_dir>   # split parts, write state
  python3 sync_push.py push <tar.gz> <remote_dir> [--limit N]   # upload up to N chunks (resumable)
"""
import sys, os, json, time, base64, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mqagent import sign_payload, verify_and_unpack, TOPIC_CMD, TOPIC_RES, BROKER, PORT
import paho.mqtt.client as mqtt

CHUNK = 700 * 1024
STATE_PATH = "/tmp/sync_state.json"


def load_state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return {"done": []}


def save_state(st):
    json.dump(st, open(STATE_PATH, "w"))


def prepare(tar_path, remote_dir):
    st = load_state()
    st["tar"] = tar_path
    st["remote_dir"] = remote_dir
    st["size"] = os.path.getsize(tar_path)
    parts_dir = "/tmp/sync_parts"
    os.makedirs(parts_dir, exist_ok=True)
    st["parts_dir"] = parts_dir
    st["parts"] = []
    with open(tar_path, "rb") as f:
        idx = 0
        while True:
            buf = f.read(CHUNK)
            if not buf:
                break
            name = f"part_{idx:04d}.bin"
            with open(os.path.join(parts_dir, name), "wb") as out:
                out.write(buf)
            st["parts"].append({"name": name, "size": len(buf),
                                "sha": hashlib.sha256(buf).hexdigest()})
            idx += 1
    st["done"] = []
    save_state(st)
    print(f"PREPARED: {len(st['parts'])} parts x {CHUNK} bytes -> {parts_dir}")
    return st


def put_one(client, req_id, path, raw):
    result = {"done": False, "resp": None}
    payload = {"op": "put_file", "path": path, "id": req_id, "ts": time.time(),
               "b64": base64.b64encode(raw).decode()}
    t0 = time.time()
    client.publish(TOPIC_CMD, sign_payload(payload), qos=1)
    while not result["done"] and time.time() - t0 < 25:
        time.sleep(0.08)
    return result


def push(tar_path, remote_dir, limit=10**9):
    st = load_state()
    if st.get("tar") != tar_path or not st.get("parts"):
        st = prepare(tar_path, remote_dir)
    parts_dir = st["parts_dir"]
    remote = remote_dir.strip("/")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id=f"push_{int(time.time())}")
    current = {"id": None}
    resp = {}

    def on_msg(c, u, msg):
        if msg.topic == TOPIC_RES:
            d = verify_and_unpack(msg.payload)
            if d and d.get("id") == current["id"]:
                resp["d"] = d
                resp["done"] = True

    client.on_message = on_msg
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    client.subscribe(TOPIC_RES, qos=1)

    done_set = set(st["done"])
    sent = 0
    t_start = time.time()
    for part in st["parts"]:
        if part["name"] in done_set:
            continue
        if sent >= limit:
            break
        fpath = os.path.join(parts_dir, part["name"])
        if not os.path.exists(fpath):
            print("missing part file:", fpath)
            break
        raw = open(fpath, "rb").read()
        req_id = f"p_{int(time.time()*1000)}_{part['name']}"
        resp.clear(); resp["done"] = False; current["id"] = req_id
        ok = False
        for attempt in range(3):
            resp.clear(); resp["done"] = False
            client.publish(TOPIC_CMD, sign_payload({"op": "put_file",
                                                   "path": f"{remote}/{part['name']}",
                                                   "id": req_id, "ts": time.time(),
                                                   "b64": base64.b64encode(raw).decode()}), qos=1)
            t0 = time.time()
            while not resp.get("done") and time.time() - t0 < 25:
                time.sleep(0.08)
            if resp.get("done") and resp["d"].get("ok"):
                ok = True
                break
            time.sleep(1.0)
        if not ok:
            print(f"FAIL {part['name']} after 3 tries")
            client.loop_stop(); client.disconnect()
            sys.exit(1)
        done_set.add(part["name"])
        st["done"] = sorted(done_set)
        save_state(st)
        sent += 1
        if sent % 10 == 0 or sent == 1:
            pct = len(done_set) * 100.0 / len(st["parts"])
            el = time.time() - t_start
            print(f"  [{len(done_set)}/{len(st['parts'])}] {pct:.0f}%  {el:.0f}s elapsed", flush=True)

    client.loop_stop(); client.disconnect()
    print(f"DONE push phase: {len(done_set)}/{len(st['parts'])} parts uploaded")
    return len(done_set) >= len(st["parts"])


if __name__ == "__main__":
    mode = sys.argv[1]
    tar = sys.argv[2]
    remote = sys.argv[3]
    if mode == "prepare":
        prepare(tar, remote)
    else:
        limit = 10**9
        if "--limit" in sys.argv:
            limit = int(sys.argv[sys.argv.index("--limit") + 1])
        ok = push(tar, remote, limit)
        sys.exit(0 if ok else 2)
