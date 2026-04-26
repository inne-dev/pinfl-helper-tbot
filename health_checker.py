import http.server
import json
import logging
import os
import threading
import time
from typing import Optional

import docker
import requests

from vpn_manager import (
    connect_to_location,
    find_best_location,
    is_v2ray_running,
    load_vpn_state,
    save_vpn_state,
    stop_v2ray,
)

TELEGRAM_CHECK_URL = "https://api.telegram.org"
CHECK_INTERVAL = int(os.environ.get("VPN_CHECK_INTERVAL", "15"))
BOT_CONTAINER_NAME = os.environ.get("BOT_CONTAINER_NAME", "pinfl-helper-tbot")
HEALTH_PORT = int(os.environ.get("HEALTH_PORT", "8080"))
REQUEST_TIMEOUT = int(os.environ.get("VPN_REQUEST_TIMEOUT", "10"))
SOCKS_PROXY_URL = os.environ.get("VPN_SOCKS_PROXY_URL", "socks5h://127.0.0.1:1080")

logger = logging.getLogger(__name__)


def _telegram_reachable_via_vpn() -> bool:
    if not is_v2ray_running():
        return False

    try:
        response = requests.get(
            TELEGRAM_CHECK_URL,
            timeout=REQUEST_TIMEOUT,
            proxies={"http": SOCKS_PROXY_URL, "https": SOCKS_PROXY_URL},
        )
        return response.status_code in (200, 204)
    except Exception as exc:
        logger.debug("Telegram via VPN check failed: %s", exc)
        return False


def restart_bot() -> None:
    try:
        client = docker.from_env()
        container = client.containers.get(BOT_CONTAINER_NAME)
        container.restart(timeout=15)
        logger.info("Container %s restarted", BOT_CONTAINER_NAME)
    except docker.errors.NotFound:
        logger.error("Container %s not found", BOT_CONTAINER_NAME)
    except Exception as exc:
        logger.error("Failed to restart container: %s", exc)


def stop_bot() -> None:
    try:
        client = docker.from_env()
        container = client.containers.get(BOT_CONTAINER_NAME)
        container.stop(timeout=15)
        logger.info("Container %s stopped", BOT_CONTAINER_NAME)
    except docker.errors.NotFound:
        logger.warning("Container %s not found while stopping", BOT_CONTAINER_NAME)
    except Exception as exc:
        logger.error("Failed to stop container: %s", exc)


def location_changed(old: Optional[dict], new: Optional[dict]) -> bool:
    if old is None and new is None:
        return False
    if old is None or new is None:
        return True
    old_host = old.get("host") or old.get("ip") or old.get("address")
    new_host = new.get("host") or new.get("ip") or new.get("address")
    return old_host != new_host


def reconnect_vpn() -> bool:
    logger.info("Finding best VPN location")
    previous = load_vpn_state()
    new_location = find_best_location()

    if new_location is None:
        logger.error("No locations available")
        return False

    if location_changed(previous, new_location):
        logger.info(
            "Location changed: %s -> %s (%s, %s ms)",
            previous.get("name") if previous else "none",
            new_location.get("name"),
            new_location.get("host"),
            f"{new_location.get('latency_ms', 0):.1f}",
        )
        save_vpn_state(new_location)

    logger.info("Connecting to location: %s", new_location.get("name"))
    if connect_to_location(new_location):
        logger.info("VPN connected successfully")
        return True

    logger.error("Failed to connect to location")
    return False


def run_health_monitor() -> None:
    logger.info("Health monitor started (interval: %ds)", CHECK_INTERVAL)
    while True:
        time.sleep(CHECK_INTERVAL)

        if _telegram_reachable_via_vpn():
            logger.debug("Telegram reachable via VPN")
            continue

        logger.warning("Telegram unreachable via VPN — reconnecting")
        stop_bot()
        stop_v2ray()
        time.sleep(1)

        if reconnect_vpn():
            logger.info("VPN reconnected — restarting bot")
            restart_bot()
        else:
            logger.error("Failed to reconnect VPN, will retry in %ds", CHECK_INTERVAL)


class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # pylint: disable=invalid-name
        if self.path == "/ready":
            vpn_ok = is_v2ray_running() and _telegram_reachable_via_vpn()
            self._respond(200 if vpn_ok else 503, {"status": "ok" if vpn_ok else "vpn_offline"})
        elif self.path == "/health":
            reachable = _telegram_reachable_via_vpn()
            location = load_vpn_state()
            payload = {
                "telegram_reachable_via_vpn": reachable,
                "v2ray_running": is_v2ray_running(),
                "location": location,
            }
            self._respond(200 if reachable else 503, payload)
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            logger.debug("Client closed health-check connection before response body write")

    def log_message(self, fmt, *args):
        logger.debug("HTTP %s", fmt % args)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [health-checker] %(message)s",
    )

    logger.info("Starting initial VPN connection")
    if reconnect_vpn():
        location = load_vpn_state() or {}
        logger.info(
            "VPN connected to: %s (%s)",
            location.get("name"),
            location.get("host"),
        )
    else:
        logger.warning("Failed to connect to VPN at startup")
        stop_bot()

    monitor_thread = threading.Thread(target=run_health_monitor, daemon=True)
    monitor_thread.start()

    server = http.server.HTTPServer(("0.0.0.0", HEALTH_PORT), HealthHandler)
    logger.info("Health endpoints: /health and /ready on port %d", HEALTH_PORT)
    server.serve_forever()


if __name__ == "__main__":
    main()
