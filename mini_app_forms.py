"""Mini-app forms stream listener and custom PINFL generation helpers."""

import json
import os
import time
from collections import deque
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
import sseclient

from pinfl_utilities_generator import PinflUtilitiesGenerator


class MiniAppFormProcessor:
    """Convert form responses into custom PINFL generation input."""

    def __init__(
        self,
        birth_date_field_id: str,
        gender_field_id: str,
        area_code_field_id: str,
        serial_number_field_id: str,
    ):
        self.birth_date_field_id = birth_date_field_id
        self.gender_field_id = gender_field_id
        self.area_code_field_id = area_code_field_id
        self.serial_number_field_id = serial_number_field_id
        self.generator = PinflUtilitiesGenerator()

    def process_payload(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract required fields and generate custom PINFL."""
        if payload.get("event") != "form.response.created":
            return None

        response_payload = payload.get("response", {})
        if not isinstance(response_payload, dict):
            raise ValueError("Invalid response payload")

        form_data = response_payload.get("data", {})
        if not isinstance(form_data, dict):
            raise ValueError("Invalid response data payload")

        context = response_payload.get("context", {})
        if not isinstance(context, dict):
            context = {}
        telegram_user = response_payload.get("telegram_user", {})
        if not isinstance(telegram_user, dict):
            telegram_user = {}

        birth_date = self._parse_birth_date(form_data.get(self.birth_date_field_id))
        gender = self._normalize_gender(form_data.get(self.gender_field_id))
        area_code = self._normalize_three_digit_value(
            form_data.get(self.area_code_field_id), "area code"
        )
        serial_number = self._normalize_three_digit_value(
            form_data.get(self.serial_number_field_id), "serial number"
        )

        pinfl = self.generator.generate_custom(
            gender=gender,
            birth_date=birth_date,
            area_code=area_code,
            serial_number=serial_number,
        )

        return {
            "pinfl": pinfl,
            "birth_date": birth_date.isoformat(),
            "gender": gender,
            "area_code": area_code,
            "serial_number": serial_number,
            "response_id": response_payload.get("id"),
            "respondent_id": response_payload.get("respondent_id"),
            "language_code": response_payload.get("lang")
            or context.get("lang")
            or context.get("tg_language_code")
            or "ru",
            "tg_user_id": self._extract_tg_user_id(
                context=context,
                response_payload=response_payload,
                telegram_user=telegram_user,
            ),
            "context": context,
            "telegram_user": telegram_user,
        }

    def _parse_birth_date(self, value: Any):
        if not isinstance(value, str):
            raise ValueError(f"Invalid birth date: {value}")

        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError(f"Invalid birth date: {value}") from error

    def _normalize_gender(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError(f"Invalid gender: {value}")

        normalized = value.strip().lower()
        male_values = {"male", "m", "man", "мужской", "мужчина", "erkak"}
        female_values = {"female", "f", "woman", "женский", "женщина", "ayol"}

        if normalized in male_values:
            return "male"
        if normalized in female_values:
            return "female"

        raise ValueError(f"Invalid gender: {value}")

    def _normalize_three_digit_value(self, value: Any, field_name: str) -> str:
        text_value = str(value).strip()
        if not text_value.isdigit():
            raise ValueError(f"Invalid {field_name}: {value}")

        number = int(text_value)
        if number < 1 or number > 999:
            raise ValueError(f"Invalid {field_name}: {value}")

        return str(number).zfill(3)

    def _extract_tg_user_id(
        self,
        context: Dict[str, Any],
        response_payload: Dict[str, Any],
        telegram_user: Dict[str, Any],
    ) -> Optional[str]:
        for key in ("tg_user_id", "user_id", "external_user_id", "tg_id"):
            value = _stringify_context_value(context.get(key))
            if value:
                return value

        respondent_id = _stringify_context_value(response_payload.get("respondent_id"))
        if respondent_id:
            return respondent_id

        tg_user = context.get("tg_user")
        if isinstance(tg_user, dict):
            value = _stringify_context_value(tg_user.get("id"))
            if value:
                return value

        telegram_user_id = _stringify_context_value(telegram_user.get("id"))
        if telegram_user_id:
            return telegram_user_id

        return None


class MiniAppFormsListener:
    """Read mini-app form events from SSE endpoint."""

    def __init__(
        self,
        stream_url: str,
        webhook_secret: str,
        processor: MiniAppFormProcessor,
        on_pinfl_generated,
        reconnect_delay_seconds: int = 5,
        start_from_now: bool = True,
        transport: str = "sse",
        poll_interval_seconds: int = 3,
        max_recent_events: int = 5000,
    ):
        self.stream_url = stream_url
        self.webhook_secret = webhook_secret
        self.processor = processor
        self.on_pinfl_generated = on_pinfl_generated
        self.reconnect_delay_seconds = reconnect_delay_seconds
        self.start_from_now = start_from_now
        self.transport = transport.strip().lower()
        self.poll_interval_seconds = max(1, poll_interval_seconds)
        self.last_event_id: Optional[str] = None
        self.max_recent_events = max(100, max_recent_events)
        self.recent_event_ids = set()
        self.recent_event_queue = deque()

    def run_forever(self):
        """Run SSE loop with automatic reconnect."""
        if self.transport == "poll" or "/responses_poll" in self.stream_url:
            self._run_poll_forever()
            return

        headers = {"X-Wappy-Webhook-Secret": self.webhook_secret}
        if self.start_from_now and self.last_event_id is None:
            self.last_event_id = str(time.time())

        while True:
            response = None
            try:
                stream_url = self._build_stream_url()
                response = requests.get(
                    stream_url, headers=headers, stream=True, timeout=(5, 300)
                )
                response.raise_for_status()
                client = sseclient.SSEClient(response)

                for event in client.events():
                    if event.event != "form.response.created":
                        continue

                    if event.id:
                        self.last_event_id = event.id

                    payload = self._parse_payload(event.data)
                    if payload is None:
                        continue

                    try:
                        generation_data = self.processor.process_payload(payload)
                    except ValueError as error:
                        print(f"Mini-app forms listener skipped invalid payload: {error}")
                        continue

                    if generation_data is None:
                        continue

                    event_uid = self._build_event_uid(payload.get("response"))
                    if self._already_processed(event_uid):
                        continue

                    self.on_pinfl_generated(generation_data)
                    self._remember_processed(event_uid)
            except requests.RequestException as error:
                print(f"Mini-app forms listener connection error: {error}")
                time.sleep(self.reconnect_delay_seconds)
            except Exception as error:  # pylint: disable=broad-except
                print(f"Mini-app forms listener processing error: {error}")
                time.sleep(self.reconnect_delay_seconds)
            finally:
                if response is not None:
                    response.close()

    def _build_stream_url(self) -> str:
        if not self.last_event_id:
            return self.stream_url

        parsed = urlsplit(self.stream_url)
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query_params["last_event_id"] = self.last_event_id
        query = urlencode(query_params, doseq=True)
        return urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment)
        )

    def _run_poll_forever(self):
        headers = {"X-Wappy-Webhook-Secret": self.webhook_secret}
        if self.start_from_now and self.last_event_id is None:
            self.last_event_id = str(time.time())

        while True:
            try:
                poll_url = self._build_stream_url()
                response = requests.get(poll_url, headers=headers, timeout=(5, 30))
                response.raise_for_status()

                payload = response.json()
                if not isinstance(payload, dict):
                    time.sleep(self.poll_interval_seconds)
                    continue

                poll_last_event_id = payload.get("last_event_id")
                if isinstance(poll_last_event_id, str) and poll_last_event_id.strip():
                    self.last_event_id = poll_last_event_id.strip()

                events = payload.get("responses", [])
                if not isinstance(events, list):
                    events = []

                for response_payload in events:
                    if not isinstance(response_payload, dict):
                        continue

                    event_uid = self._build_event_uid(response_payload)
                    if self._already_processed(event_uid):
                        continue

                    event_payload = {
                        "event": "form.response.created",
                        "response": response_payload,
                    }
                    try:
                        generation_data = self.processor.process_payload(event_payload)
                    except ValueError as error:
                        print(f"Mini-app forms listener skipped invalid payload: {error}")
                        continue

                    if generation_data:
                        self.on_pinfl_generated(generation_data)
                        self._remember_processed(event_uid)
            except requests.RequestException as error:
                print(f"Mini-app forms poll error: {error}")
                time.sleep(self.reconnect_delay_seconds)
                continue
            except ValueError as error:
                print(f"Mini-app forms poll JSON error: {error}")
                time.sleep(self.reconnect_delay_seconds)
                continue

            time.sleep(self.poll_interval_seconds)

    def _build_event_uid(self, response_payload: Any) -> Optional[str]:
        if not isinstance(response_payload, dict):
            return None

        stat_id = _stringify_context_value(response_payload.get("stat_id"))
        if stat_id:
            return f"stat:{stat_id}"

        response_id = _stringify_context_value(response_payload.get("id"))
        if response_id:
            return f"response:{response_id}"

        submitted_at = _stringify_context_value(response_payload.get("submitted_at"))
        respondent_id = _stringify_context_value(response_payload.get("respondent_id"))
        if submitted_at and respondent_id:
            return f"time:{submitted_at}:{respondent_id}"

        return None

    def _already_processed(self, event_uid: Optional[str]) -> bool:
        if not event_uid:
            return False
        return event_uid in self.recent_event_ids

    def _remember_processed(self, event_uid: Optional[str]):
        if not event_uid or event_uid in self.recent_event_ids:
            return

        self.recent_event_ids.add(event_uid)
        self.recent_event_queue.append(event_uid)

        while len(self.recent_event_queue) > self.max_recent_events:
            old_uid = self.recent_event_queue.popleft()
            self.recent_event_ids.discard(old_uid)

    def _parse_payload(self, data: str) -> Optional[Dict[str, Any]]:
        try:
            payload = json.loads(data)
            if not isinstance(payload, dict):
                print("Mini-app forms listener: payload must be object")
                return None
            return payload
        except json.JSONDecodeError:
            print("Mini-app forms listener: invalid JSON payload")
            return None


def mini_app_forms_enabled() -> bool:
    """Check feature flag for mini-app forms integration."""
    return os.environ.get("MINI_APP_FORMS_ENABLED", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def build_telegram_client_context(
    user_id: Any, user_lang: str, telegram_user: Optional[Any] = None
) -> Dict[str, str]:
    """Build mini app context query params from Telegram user data."""
    base_user_id = _stringify_context_value(user_id)
    if not base_user_id:
        raise ValueError("user_id is required")

    language_code = (
        _stringify_context_value(getattr(telegram_user, "language_code", None))
        or _stringify_context_value(user_lang)
        or "ru"
    )

    params = {
        "source": "pinfl-helper-tbot",
        "tg_user_id": base_user_id,
        "user_id": base_user_id,
        "external_user_id": base_user_id,
        "tg_language_code": language_code,
        "lang": language_code,
        "tg_first_name": _stringify_context_value(
            getattr(telegram_user, "first_name", None)
        ),
        "tg_last_name": _stringify_context_value(
            getattr(telegram_user, "last_name", None)
        ),
        "tg_username": _stringify_context_value(
            getattr(telegram_user, "username", None)
        ),
        "tg_is_bot": _stringify_context_value(getattr(telegram_user, "is_bot", None)),
    }
    return {key: value for key, value in params.items() if value}


def build_mini_app_launch_url(base_url: str, params: Dict[str, Any]) -> str:
    """Merge query params into mini app launch URL."""
    parsed = urlsplit(base_url)
    existing_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    existing_params.update(
        {
            key: _stringify_context_value(value)
            for key, value in params.items()
            if value is not None
        }
    )
    query = urlencode(existing_params, doseq=True)
    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment)
    )


def _stringify_context_value(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).strip()
    return text or None
