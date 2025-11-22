from typing import Iterable, Dict, Any

from .models import Transaction


def compute_summary(transactions: Iterable[Transaction]) -> Dict[str, Any]:
    total_income = 0.0
    total_expenses = 0.0
    by_category: Dict[str, float] = {}

    for tx in transactions:
        if tx.kind == "income":
            total_income += tx.amount
        else:
            total_expenses += tx.amount
            by_category[tx.category] = by_category.get(tx.category, 0.0) + tx.amount

    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "by_category": by_category,
    }


def print_summary(summary: Dict[str, Any]) -> None:
    total_income = summary["total_income"]
    total_expenses = summary["total_expenses"]
    balance = summary["balance"]
    by_category: Dict[str, float] = summary["by_category"]

    print("=== Сводка по периодам ===")
    print(f"Доходы : {total_income:10.2f}")
    print(f"Расходы: {total_expenses:10.2f}")
    print(f"Баланс : {balance:10.2f}")
    print()

    if not by_category:
        print("Нет расходов для показа по категориям.")
        return

    print("Расходы по категориям:")
    for cat, amount in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f" - {cat:<15} {amount:10.2f}")
