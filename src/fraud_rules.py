from collections.abc import Mapping
from typing import Any


def derive_signals(event: Mapping[str, Any]) -> list[str]:
    """Derive deterministic fraud signals from an event payload."""
    signals: list[str] = []
    account_country = event.get("country")
    ip_country = event.get("ip_country")
    card_country = event.get("card_country")

    if account_country and ip_country and ip_country != account_country:
        signals.append(
            f"IP country ({ip_country}) does not match account country "
            f"({account_country})."
        )

    if account_country and card_country and card_country != account_country:
        signals.append(
            f"Card country ({card_country}) does not match account country "
            f"({account_country})."
        )

    prior_accounts = event.get("prior_accounts_from_ip")
    if _is_number(prior_accounts) and prior_accounts > 4:
        signals.append(
            f"IP address is associated with {prior_accounts} prior accounts, "
            "which exceeds the threshold of 4."
        )

    payment_attempts = event.get("payment_attempts_last_hour")
    if _is_number(payment_attempts) and payment_attempts > 4:
        signals.append(
            f"Card has {payment_attempts} purchase attempts in the last hour, "
            "which exceeds the threshold of 4."
        )

    return signals


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
