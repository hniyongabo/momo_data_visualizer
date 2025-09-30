from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import xml.etree.ElementTree as ET

ROOT_PATH = Path(__file__).resolve().parents[1]
DEFAULT_XML_PATH = ROOT_PATH / 'modified_sms_v2.xml'

_AMOUNT_REGEX = re.compile(r'(?:received|payment of|transferred\s*(?:to)?|deposit of)\s*([\d,]+)\s*RWF', re.IGNORECASE)
_RAW_AMOUNT_REGEX = re.compile(r'(\d[\d,]*)\s*RWF', re.IGNORECASE)
_TX_ID_REGEX = re.compile(r'(?:TxId:|Financial Transaction Id:)\s*([\d]+)', re.IGNORECASE)
_COUNTERPARTY_REGEXES = (
    re.compile(r'received\s+[\d,]+\s*RWF\s+from\s+([^.(]+)', re.IGNORECASE),
    re.compile(r'payment\s+of\s+[\d,]+\s*RWF\s+to\s+([^.(]+)', re.IGNORECASE),
    re.compile(r'transferred\s+[\d,]+\s*RWF\s+to\s+([^.(]+)', re.IGNORECASE),
    re.compile(r'transferred\s+[\d,]+\s*RWF\s+from\s+([^.(]+)', re.IGNORECASE),
)


@dataclass
class MessageRecord:
    protocol: int
    address: str
    is_read: bool
    subject: Optional[str]
    body: str
    sms_protocol: Optional[str]
    service_center: Optional[str]
    contact_name: Optional[str]
    sub_id: Optional[int]
    readable_date: Optional[str]


@dataclass
class TransactionRecord:
    transaction_id: str
    user_id: Optional[int]
    transaction_date: datetime
    toa: Optional[str]
    sc_toa: Optional[str]
    readable_date: Optional[str]
    amount: Optional[float]
    status: str
    service_center_number: Optional[str]
    sender_name: Optional[str]


@dataclass
class CategoryRecord:
    transaction_type: str
    payment_type: str


@dataclass
class ParsedRecord:
    message: MessageRecord
    transaction: TransactionRecord
    category: CategoryRecord

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            'message': asdict(self.message),
            'transaction': asdict(self.transaction),
            'category': asdict(self.category),
        }
        payload['transaction']['transaction_date'] = self.transaction.transaction_date.isoformat()
        return payload


def _parse_timestamp(raw_value: str) -> datetime:
    try:
        millis = int(raw_value)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)
    return datetime.fromtimestamp(millis / 1000, tz=timezone.utc)


def _parse_bool(raw_value: Optional[str]) -> bool:
    return str(raw_value) == '1'


def _parse_int(raw_value: Optional[str]) -> Optional[int]:
    if raw_value in (None, '', 'null'):
        return None
    try:
        return int(raw_value)
    except ValueError:
        return None


def _parse_amount(text: str) -> Optional[float]:
    match = _AMOUNT_REGEX.search(text)
    if not match:
        match = _RAW_AMOUNT_REGEX.search(text)
    if not match:
        return None
    number = match.group(1).replace(',', '')
    try:
        return float(number)
    except ValueError:
        return None


def _parse_status(body: str) -> str:
    lowered = body.lower()
    if 'failed' in lowered:
        return 'FAILED'
    if 'pending' in lowered:
        return 'PENDING'
    return 'COMPLETED'


def _parse_transaction_type(body: str) -> str:
    lowered = body.lower()
    if 'received' in lowered or 'deposit' in lowered:
        return 'CREDIT'
    return 'DEBIT'


def _parse_payment_type(body: str) -> str:
    lowered = body.lower()
    if 'airtime' in lowered:
        return 'Airtime'
    if 'cash' in lowered or 'deposit' in lowered:
        return 'CASH'
    return 'MoMoPay'


def _parse_counterparty(body: str) -> Optional[str]:
    for regex in _COUNTERPARTY_REGEXES:
        match = regex.search(body)
        if match:
            candidate = match.group(1).strip()
            candidate = re.sub(r'\(.*?\)$', '', candidate).strip()
            if candidate:
                return candidate
    return None


def _parse_transaction_id(body: str, fallback: str) -> str:
    match = _TX_ID_REGEX.search(body)
    if match:
        return match.group(1)
    return fallback


def _iter_sms_elements(xml_path: Path) -> Iterable[Dict[str, str]]:
    context = ET.iterparse(xml_path, events=('start',))
    for event, elem in context:
        if elem.tag != 'sms':
            continue
        yield dict(elem.attrib)
        elem.clear()


def _build_record(raw: Dict[str, str], counter: int) -> ParsedRecord:
    body = raw.get('body', '')
    transaction_date = _parse_timestamp(raw.get('date', '0'))
    transaction_id = _parse_transaction_id(body, f"{transaction_date.isoformat()}#{counter}")
    category = CategoryRecord(
        transaction_type=_parse_transaction_type(body),
        payment_type=_parse_payment_type(body),
    )
    transaction = TransactionRecord(
        transaction_id=transaction_id,
        user_id=_parse_int(raw.get('sub_id')),
        transaction_date=transaction_date,
        toa=raw.get('toa'),
        sc_toa=raw.get('sc_toa'),
        readable_date=raw.get('readable_date'),
        amount=_parse_amount(body),
        status=_parse_status(body),
        service_center_number=raw.get('service_center'),
        sender_name=_parse_counterparty(body),
    )
    message = MessageRecord(
        protocol=int(raw.get('protocol', '0')),
        address=raw.get('address', ''),
        is_read=_parse_bool(raw.get('read')),
        subject=None if raw.get('subject') in (None, 'null', '') else raw.get('subject'),
        body=body,
        sms_protocol=raw.get('status'),
        service_center=raw.get('service_center'),
        contact_name=None if raw.get('contact_name') == '(Unknown)' else raw.get('contact_name'),
        sub_id=_parse_int(raw.get('sub_id')),
        readable_date=raw.get('readable_date'),
    )
    return ParsedRecord(message=message, transaction=transaction, category=category)


def parse_sms_backup(xml_path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for idx, raw in enumerate(_iter_sms_elements(xml_path), start=1):
        record = _build_record(raw, idx)
        records.append(record.to_dict())
    return records


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert SMS backup into structured JSON.')
    parser.add_argument('-i', '--input', type=Path, default=DEFAULT_XML_PATH, help='Path to modified_sms_v2.xml')
    parser.add_argument('-o', '--output', type=Path, help='Optional JSON output path')
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    xml_path: Path = args.input
    if not xml_path.exists():
        raise FileNotFoundError(f'XML file not found: {xml_path}')

    records = parse_sms_backup(xml_path)

    if args.output:
        args.output.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(records, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
