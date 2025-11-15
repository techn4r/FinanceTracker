import argparse
from pathlib import Path
from datetime import date, datetime
from typing import Optional, List

from .models import Transaction
from .storage import Storage
from .reports import compute_summary,print_summary


def parse_date_or_today(date_str: Optional[str]) -> date:
    if not date_str:
        return date.today()
    return date.fromisoformat(date_str)


def parse_date_or_none(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    return date.fromisoformat(date_str)


def print_transactions(transactions: List[Transaction]) -> None:
    if not transactions:
        print("Транзакций не найдено.")
        return

    print(f"{'ID':<4} {'Дата':<10} {'Тип':<8} {'Сумма':>10}  {'Категория':<15} Описание")
    print("-" * 70)
    for tx in transactions:
        print(
            f"{tx.id:<4} {tx.date.isoformat():<10} {tx.kind:<8} "
            f"{tx.amount:>10.2f}  {tx.category:<15} {tx.description}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fintracker",
        description="Простой трекер личных финансов (CLI).",
    )
    parser.add_argument(
        "--db",
        default="finances.db",
        help="Путь к файлу базы данных (по умолчанию finances.db)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Добавить транзакцию")
    add_parser.add_argument(
        "kind",
        choices=["income", "expense"],
        help="Тип: income (доход) или expense (расход)",
    )
    add_parser.add_argument(
        "amount",
        type=float,
        help="Сумма транзакции (положительное число)",
    )
    add_parser.add_argument(
        "category",
        help="Категория (еда, жильё, зарплата, фриланс и т.п.)",
    )
    add_parser.add_argument(
        "-d",
        "--date",
        dest="date_str",
        help="Дата в формате YYYY-MM-DD (по умолчанию сегодня)",
    )
    add_parser.add_argument(
        "-m",
        "--message",
        "--description",
        dest="description",
        default="",
        help="Описание / комментарий к транзакции",
    )

    list_parser = subparsers.add_parser("list", help="Показать транзакции")
    list_parser.add_argument(
        "--from",
        dest="from_date",
        help="Начальная дата (YYYY-MM-DD)",
    )
    list_parser.add_argument(
        "--to",
        dest="to_date",
        help="Конечная дата (YYYY-MM-DD)",
    )
    list_parser.add_argument(
        "--category",
        dest="category",
        help="Фильтр по категории",
    )

    summary_parser = subparsers.add_parser("summary", help="Сводка по доходам/расходам")
    summary_parser.add_argument(
        "--from",
        dest="from_date",
        help="Начальная дата (YYYY-MM-DD)",
    )
    summary_parser.add_argument(
        "--to",
        dest="to_date",
        help="Конечная дата (YYYY-MM-DD)",
    )

    args = parser.parse_args()
    storage = Storage(Path(args.db))

    if args.command == "add":
        tx_date = parse_date_or_today(args.date_str)
        created_at = datetime.utcnow()

        if args.amount <= 0:
            raise SystemExit("Сумма должна быть положительной.")

        tx = Transaction(
            id=None,
            date=tx_date,
            amount=args.amount,
            kind=args.kind,
            category=args.category,
            description=args.description.strip(),
            created_at=created_at,
        )
        saved = storage.add_transaction(tx)
        print(
            f"Добавлена транзакция #{saved.id}: "
            f"{saved.date} {saved.kind} {saved.amount:.2f} {saved.category}"
        )

    elif args.command == "list":
        from_date = parse_date_or_none(args.from_date)
        to_date = parse_date_or_none(args.to_date)
        transactions = storage.list_transactions(
            from_date=from_date,
            to_date=to_date,
            category=args.category,
        )
        print_transactions(transactions)

    elif args.command == "summary":
        from_date = parse_date_or_none(args.from_date)
        to_date = parse_date_or_none(args.to_date)
        transactions = storage.list_transactions(
            from_date=from_date,
            to_date=to_date,
            category=None,
        )
        summary = compute_summary(transactions)
        print_summary(summary)