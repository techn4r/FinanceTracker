import argparse
from pathlib import Path
from datetime import date, datetime
from typing import Optional, List

from .models import Transaction
from .storage import Storage
from .reports import compute_summary, print_summary


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

    print("ID  | Дата       | Тип     | Категория       | Сумма      | Комментарий")
    print("-" * 80)
    for tx in transactions:
        kind_label = "Доход" if tx.kind == "income" else "Расход"
        print(
            f"{tx.id:>3} | {tx.date.isoformat()} | "
            f"{kind_label:<7} | {tx.category:<14} | "
            f"{tx.amount:10.2f} | {tx.description}"
        )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Простой консольный трекер личных финансов"
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        type=Path,
        default=Path("finance.db"),
        help="Путь к файлу базы данных (по умолчанию ./finance.db)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser(
        "add", help="Добавить доход или расход"
    )
    add_parser.add_argument(
        "kind",
        choices=["income", "expense"],
        help="Тип транзакции: income — доход, expense — расход",
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
        "-c",
        "--comment",
        dest="comment",
        default="",
        help="Комментарий к транзакции",
    )

    # list
    list_parser = subparsers.add_parser(
        "list", help="Показать список транзакций"
    )
    list_parser.add_argument(
        "--from",
        dest="from_date",
        help="Дата начала периода YYYY-MM-DD",
    )
    list_parser.add_argument(
        "--to",
        dest="to_date",
        help="Дата конца периода YYYY-MM-DD",
    )
    list_parser.add_argument(
        "--category",
        dest="category",
        help="Фильтр по категории",
    )

    # summary
    summary_parser = subparsers.add_parser(
        "summary", help="Показать сводку по доходам и расходам"
    )
    summary_parser.add_argument(
        "--from",
        dest="from_date",
        help="Дата начала периода YYYY-MM-DD",
    )
    summary_parser.add_argument(
        "--to",
        dest="to_date",
        help="Дата конца периода YYYY-MM-DD",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)

    storage = Storage(args.db_path)

    if args.command == "add":
        tx = Transaction(
            id=None,
            date=parse_date_or_today(args.date_str),
            amount=args.amount,
            kind=args.kind,
            category=args.category,
            description=args.comment or "",
            created_at=datetime.now(),
        )
        saved = storage.add_transaction(tx)
        print(f"Добавлена транзакция #{saved.id}")

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
