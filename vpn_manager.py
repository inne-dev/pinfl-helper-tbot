import base64
import json
import logging
import os
import signal
import socket
import subprocess
import time
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, unquote, urlparse

import requests

logger = logging.getLogger(__name__)

VPN_CONFIG_FILE = os.environ.get("VPN_CONFIG_FILE", "/app/data/v2ray_config.json")
VPN_STATE_FILE = os.environ.get("VPN_STATE_FILE", "/app/data/vpn_state.json")
VPN_TOKEN = os.environ.get("VPN_TOKEN")
V2RAY_BINARY = os.environ.get("V2RAY_BINARY", "/usr/local/bin/v2ray")
V2RAY_PID_FILE = os.environ.get("V2RAY_PID_FILE", "/app/data/v2ray.pid")
V2RAY_LOG_FILE = os.environ.get("V2RAY_LOG_FILE", "/app/data/v2ray.log")
V2RAY_SOCKS_HOST = os.environ.get("V2RAY_SOCKS_HOST", "127.0.0.1")
V2RAY_SOCKS_PORT = int(os.environ.get("V2RAY_SOCKS_PORT", "1080"))
V2RAY_PROBE_CONFIG_FILE = os.environ.get("V2RAY_PROBE_CONFIG_FILE", "/app/data/v2ray_probe_config.json")
V2RAY_PROBE_SOCKS_PORT = int(os.environ.get("V2RAY_PROBE_SOCKS_PORT", "1081"))
TELEGRAM_PROBE_URL = os.environ.get("TELEGRAM_PROBE_URL", "https://api.telegram.org")
LOCATION_PROBE_TIMEOUT = float(os.environ.get("VPN_LOCATION_PROBE_TIMEOUT", "3.5"))
LOCATION_PROBE_STARTUP_SECONDS = float(os.environ.get("VPN_LOCATION_PROBE_STARTUP_SECONDS", "2.5"))
CHECK_TIMEOUT = int(os.environ.get("VPN_REQUEST_TIMEOUT", "10"))
SUBSCRIPTION_TIMEOUT = int(os.environ.get("VPN_SUBSCRIPTION_TIMEOUT", "20"))
VPN_EXCLUDE_KEYWORDS = os.environ.get("VPN_EXCLUDE_KEYWORDS", "россия,whitelist")


def _load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as exc:
        logger.error("Failed to load JSON from %s: %s", filepath, exc)
        return None


def _save_json_file(filepath: str, data: Dict[str, Any]) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as exc:
        logger.error("Failed to save JSON to %s: %s", filepath, exc)
        return False


def load_vpn_state() -> Optional[Dict[str, Any]]:
    return _load_json_file(VPN_STATE_FILE)


def save_vpn_state(state: Dict[str, Any]) -> bool:
    return _save_json_file(VPN_STATE_FILE, state)


def _decode_base64_urlsafe(data: str) -> str:
    normalized = data.strip().replace("-", "+").replace("_", "/")
    normalized += "=" * ((4 - len(normalized) % 4) % 4)
    return base64.b64decode(normalized).decode("utf-8", errors="ignore")


def _direct_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    return session


def _subscription_text() -> Optional[str]:
    if not VPN_TOKEN:
        logger.warning("VPN_TOKEN not set, cannot load VPN subscription")
        return None

    try:
        if VPN_TOKEN.startswith(("http://", "https://")):
            session = _direct_session()
            response = session.get(VPN_TOKEN, timeout=SUBSCRIPTION_TIMEOUT)
            response.raise_for_status()
            raw = response.text.strip()
        else:
            raw = VPN_TOKEN.strip()

        try:
            decoded = _decode_base64_urlsafe(raw)
            if any(proto in decoded for proto in ("vmess://", "vless://", "trojan://")):
                return decoded
        except Exception:
            pass

        return raw
    except requests.exceptions.Timeout:
        logger.error("Timeout downloading VPN subscription")
        return None
    except Exception as exc:
        logger.error("Failed to load VPN subscription: %s", exc)
        return None


def _parse_vmess_line(line: str) -> Optional[Dict[str, Any]]:
    if not line.startswith("vmess://"):
        return None

    payload = line[len("vmess://") :].strip()
    try:
        node = json.loads(_decode_base64_urlsafe(payload))
    except Exception:
        return None

    host = node.get("add")
    user_id = node.get("id")
    if not host or not user_id:
        return None

    return {
        "name": node.get("ps") or host,
        "host": host,
        "port": int(node.get("port", 443)),
        "protocol": "vmess",
        "user_id": user_id,
        "alter_id": int(node.get("aid", 0)),
        "security": node.get("scy", "auto"),
        "network": node.get("net", "tcp"),
        "path": node.get("path", "/"),
        "host_header": node.get("host", ""),
        "tls": node.get("tls", "") in ("tls", "reality"),
        "sni": node.get("sni") or node.get("host") or host,
        "flow": "",
        "encryption": "",
    }


def _parse_vless_line(line: str) -> Optional[Dict[str, Any]]:
    if not line.startswith("vless://"):
        return None

    parsed = urlparse(line)
    if not parsed.hostname or not parsed.username:
        return None

    query = parse_qs(parsed.query)
    security = (query.get("security", [""])[0] or "").lower()
    network = (query.get("type", ["tcp"])[0] or "tcp").lower()
    path = query.get("path", ["/"])[0] or "/"
    host_header = query.get("host", [""])[0] or ""
    name = unquote(parsed.fragment) if parsed.fragment else parsed.hostname

    return {
        "name": name,
        "host": parsed.hostname,
        "port": int(parsed.port or 443),
        "protocol": "vless",
        "user_id": parsed.username,
        "alter_id": 0,
        "security": "auto",
        "network": network,
        "path": path,
        "host_header": host_header,
        "tls": security in ("tls", "reality"),
        "sni": query.get("sni", [host_header or parsed.hostname])[0],
        "flow": query.get("flow", [""])[0],
        "encryption": query.get("encryption", ["none"])[0],
    }


def _parse_location_line(line: str) -> Optional[Dict[str, Any]]:
    return _parse_vmess_line(line) or _parse_vless_line(line)


def _locations_from_subscription() -> List[Dict[str, Any]]:
    text = _subscription_text()
    if not text:
        return []

    locations: List[Dict[str, Any]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        parsed = _parse_location_line(line)
        if parsed:
            locations.append(parsed)

    if locations:
        logger.info("Loaded %d VPN locations from subscription", len(locations))
    else:
        logger.error("No supported nodes in subscription (expected vmess:// or vless://)")

    return locations


def _is_excluded_location(location: Dict[str, Any]) -> bool:
    name = str(location.get("name") or "").casefold()
    keywords = [part.strip().casefold() for part in VPN_EXCLUDE_KEYWORDS.split(",") if part.strip()]
    return any(keyword in name for keyword in keywords)


def _is_socks_listener_up() -> bool:
    return _is_socks_listener_up_on_port(V2RAY_SOCKS_HOST, V2RAY_SOCKS_PORT)


def _is_socks_listener_up_on_port(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False


def _tail_v2ray_log(max_lines: int = 20) -> str:
    try:
        with open(V2RAY_LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        return "".join(lines[-max_lines:]).strip()
    except Exception:
        return ""


def _pid_from_file() -> Optional[int]:
    try:
        with open(V2RAY_PID_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return None


def _write_pid(pid: int) -> None:
    with open(V2RAY_PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(pid))


def _clear_pid_file() -> None:
    try:
        os.remove(V2RAY_PID_FILE)
    except FileNotFoundError:
        pass


def _pid_is_v2ray(pid: int) -> bool:
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cmdline = f.read().decode("utf-8", errors="ignore")
        return "v2ray" in cmdline
    except Exception:
        return False


def _find_v2ray_pids() -> List[int]:
    pids: List[int] = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        pid = int(entry)
        if _pid_is_v2ray(pid):
            pids.append(pid)
    return pids


def is_v2ray_running() -> bool:
    pid = _pid_from_file()
    if pid and _pid_is_v2ray(pid):
        return _is_socks_listener_up()

    return len(_find_v2ray_pids()) > 0 and _is_socks_listener_up()


def stop_v2ray() -> None:
    pids = []
    pid = _pid_from_file()
    if pid and _pid_is_v2ray(pid):
        pids.append(pid)
    else:
        pids = _find_v2ray_pids()

    for current_pid in pids:
        try:
            os.kill(current_pid, signal.SIGTERM)
        except ProcessLookupError:
            continue
        except Exception as exc:
            logger.error("Failed to stop v2ray pid %s: %s", current_pid, exc)

    if pids:
        logger.info("v2ray stopped")
    _clear_pid_file()
    time.sleep(1)


def start_v2ray(config: Dict[str, Any]) -> bool:
    try:
        with open(VPN_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)

        launch_variants = [
            [V2RAY_BINARY, "run", "-config", VPN_CONFIG_FILE],
            [V2RAY_BINARY, "-config", VPN_CONFIG_FILE],
        ]

        for cmd in launch_variants:
            with open(V2RAY_LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write("\n===== START %s cmd=%s =====\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(cmd)))
                process = subprocess.Popen(
                    cmd,
                    stdout=log_file,
                    stderr=log_file,
                )

            _write_pid(process.pid)

            for _ in range(10):
                if process.poll() is not None:
                    logger.warning("v2ray exited early with code %s using cmd: %s", process.returncode, " ".join(cmd))
                    break

                if _is_socks_listener_up():
                    logger.info("v2ray started")
                    return True
                time.sleep(1)

            stop_v2ray()

        logger.error("v2ray failed to start SOCKS listener on %s:%s", V2RAY_SOCKS_HOST, V2RAY_SOCKS_PORT)
        tail = _tail_v2ray_log()
        if tail:
            logger.error("v2ray log tail:\n%s", tail)
        return False
    except Exception as exc:
        logger.error("Failed to start v2ray: %s", exc)
        return False


def _check_location_latency(location: Dict[str, Any]) -> Optional[float]:
    config = _build_v2ray_config(location)
    config["inbounds"][0]["port"] = V2RAY_PROBE_SOCKS_PORT

    try:
        with open(V2RAY_PROBE_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)
    except Exception:
        return None

    launch_variants = [
        [V2RAY_BINARY, "run", "-config", V2RAY_PROBE_CONFIG_FILE],
        [V2RAY_BINARY, "-config", V2RAY_PROBE_CONFIG_FILE],
    ]

    for cmd in launch_variants:
        process: Optional[subprocess.Popen] = None
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Give location-local tunnel short window to bring up SOCKS.
            ready = False
            startup_checks = max(1, int(LOCATION_PROBE_STARTUP_SECONDS / 0.15))
            for _ in range(startup_checks):
                if process.poll() is not None:
                    break
                if _is_socks_listener_up_on_port("127.0.0.1", V2RAY_PROBE_SOCKS_PORT):
                    ready = True
                    break
                time.sleep(0.15)

            if not ready:
                continue

            session = _direct_session()
            proxies = {
                "http": f"socks5h://127.0.0.1:{V2RAY_PROBE_SOCKS_PORT}",
                "https": f"socks5h://127.0.0.1:{V2RAY_PROBE_SOCKS_PORT}",
            }
            start = time.time()
            response = session.get(
                TELEGRAM_PROBE_URL,
                timeout=LOCATION_PROBE_TIMEOUT,
                proxies=proxies,
            )
            # Telegram endpoint reachable through this location.
            if response.status_code < 500:
                return (time.time() - start) * 1000
        except Exception:
            pass
        finally:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=2)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass

    return None


def find_best_location() -> Optional[Dict[str, Any]]:
    locations = _locations_from_subscription()
    if not locations:
        logger.error("No locations available")
        return None

    allowed_locations = []
    for location in locations:
        if _is_excluded_location(location):
            logger.info("Location skipped by filter: %s", location.get("name"))
            continue
        allowed_locations.append(location)

    if not allowed_locations:
        logger.error("No locations available after applying filters")
        return None

    best: Optional[Dict[str, Any]] = None
    best_latency = float("inf")

    for index, location in enumerate(allowed_locations, start=1):
        latency = _check_location_latency(location)
        if latency is None:
            logger.info(
                "Location %d/%d failed: %s (%s:%s)",
                index,
                len(allowed_locations),
                location.get("name"),
                location.get("host"),
                location.get("port"),
            )
            continue

        logger.info(
            "Location %d/%d latency: %s (%s:%s) %.1f ms",
            index,
            len(allowed_locations),
            location.get("name"),
            location.get("host"),
            location.get("port"),
            latency,
        )

        if latency < best_latency:
            best_latency = latency
            best = {**location, "latency_ms": latency}

    if best is None:
        logger.error("No reachable VPN locations after probing %d nodes", len(allowed_locations))
        return None

    logger.info(
        "Best VPN location selected: %s (%s:%s, %.1f ms)",
        best.get("name"),
        best.get("host"),
        best.get("port"),
        best.get("latency_ms", -1),
    )
    return best


def connect_to_location(location: Dict[str, Any]) -> bool:
    config = _build_v2ray_config(location)
    stop_v2ray()
    time.sleep(1)
    return start_v2ray(config)


def _build_outbound(location: Dict[str, Any]) -> Dict[str, Any]:
    protocol = location.get("protocol", "vmess")

    if protocol == "vless":
        user = {
            "id": location.get("user_id"),
            "encryption": location.get("encryption") or "none",
        }
        if location.get("flow"):
            user["flow"] = location.get("flow")

        return {
            "tag": "proxy",
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": location.get("host"),
                        "port": int(location.get("port", 443)),
                        "users": [user],
                    }
                ]
            },
        }

    return {
        "tag": "proxy",
        "protocol": "vmess",
        "settings": {
            "vnext": [
                {
                    "address": location.get("host"),
                    "port": int(location.get("port", 443)),
                    "users": [
                        {
                            "id": location.get("user_id"),
                            "alterId": int(location.get("alter_id", 0)),
                            "security": location.get("security", "auto"),
                        }
                    ],
                }
            ]
        },
    }


def _build_v2ray_config(location: Dict[str, Any]) -> Dict[str, Any]:
    stream_settings: Dict[str, Any] = {"network": location.get("network", "tcp")}

    if location.get("network") == "ws":
        stream_settings["wsSettings"] = {
            "path": location.get("path") or "/",
            "headers": {"Host": location.get("host_header") or ""},
        }

    if location.get("tls"):
        stream_settings["security"] = "tls"
        stream_settings["tlsSettings"] = {
            "serverName": location.get("sni") or location.get("host"),
        }

    outbound = _build_outbound(location)
    outbound["streamSettings"] = stream_settings

    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": "socks-in",
                "protocol": "socks",
                "port": 1080,
                "listen": "0.0.0.0",
                "settings": {"auth": "noauth", "udp": True},
            }
        ],
        "outbounds": [
            outbound,
            {"tag": "direct", "protocol": "freedom"},
        ],
    }
