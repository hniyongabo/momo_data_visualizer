from __future__ import annotations

import argparse
import json
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List, Optional

ROOT_PATH = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = ROOT_PATH / 'parsed_sms.json'


def load_records(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError('Expected the JSON file to contain a list of records.')
    if len(data) < 20:
        raise ValueError('Need at least 20 records to run the comparison.')
    return data


def extract_transactions(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    transactions: List[Dict[str, Any]] = []
    for record in records:
        transaction = record.get('transaction')
        if isinstance(transaction, dict) and 'transaction_id' in transaction:
            transactions.append(transaction)
    if len(transactions) < 20:
        raise ValueError('Could not find at least 20 transactions with transaction_id fields.')
    return transactions


def linear_search(transactions: List[Dict[str, Any]], target_id: str) -> Optional[Dict[str, Any]]:
    for transaction in transactions:
        if transaction.get('transaction_id') == target_id:
            return transaction
    return None


def dictionary_lookup(transaction_map: Dict[str, Dict[str, Any]], target_id: str) -> Optional[Dict[str, Any]]:
    return transaction_map.get(target_id)


def measure_linear(transactions: List[Dict[str, Any]], targets: List[str], iterations: int) -> float:
    start = perf_counter()
    for _ in range(iterations):
        for target_id in targets:
            linear_search(transactions, target_id)
    return perf_counter() - start


def measure_dictionary(transactions: List[Dict[str, Any]], targets: List[str], iterations: int) -> float:
    transaction_map = {txn['transaction_id']: txn for txn in transactions}
    start = perf_counter()
    for _ in range(iterations):
        for target_id in targets:
            dictionary_lookup(transaction_map, target_id)
    return perf_counter() - start


def benchmark(data_path: Path, sample_size: int, iterations: int) -> Dict[str, Any]:
    records = load_records(data_path)
    transactions = extract_transactions(records)
    sample_size = min(sample_size, len(transactions))
    targets = [transactions[i]['transaction_id'] for i in range(sample_size)]

    linear_time = measure_linear(transactions, targets, iterations)
    dict_time = measure_dictionary(transactions, targets, iterations)

    return {
        'records_evaluated': len(transactions),
        'targets': sample_size,
        'iterations': iterations,
        'linear_seconds': linear_time,
        'dict_seconds': dict_time,
        'speedup': linear_time / dict_time if dict_time else float('inf'),
    }


def format_results(results: Dict[str, Any]) -> str:
    lines = [
        'Search Performance Comparison',
        f"Records evaluated: {results['records_evaluated']}",
        f"Target count: {results['targets']}",
        f"Iterations per method: {results['iterations']}",
        f"Linear search total: {results['linear_seconds']:.6f} seconds",
        f"Dictionary lookup total: {results['dict_seconds']:.6f} seconds",
        f"Observed speedup: {results['speedup']:.2f}x",
    ]
    return '\n'.join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Compare linear search vs dictionary lookup on transaction records.')
    parser.add_argument('-d', '--data', type=Path, default=DEFAULT_DATA_PATH, help='Path to parsed_sms.json')
    parser.add_argument('-n', '--sample-size', type=int, default=20, help='Number of transaction IDs to query (>=20).')
    parser.add_argument('-i', '--iterations', type=int, default=1000, help='Number of full passes for timing.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = benchmark(args.data, args.sample_size, args.iterations)
    print(format_results(results))


if __name__ == '__main__':
    main()
