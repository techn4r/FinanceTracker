from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Transaction, Category


@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(owner=request.user)

    kind = request.GET.get("kind")
    if kind in ("income", "expense"):
        qs = qs.filter(kind=kind)

    from_date = request.GET.get("from")
    to_date = request.GET.get("to")
    if from_date:
        qs = qs.filter(date__gte=from_date)
    if to_date:
        qs = qs.filter(date__lte=to_date)

    total_income = qs.filter(kind="income").aggregate(Sum("amount"))["amount__sum"] or 0
    total_expense = qs.filter(kind="expense").aggregate(Sum("amount"))["amount__sum"] or 0
    balance = total_income - total_expense

    return render(
        request,
        "finance/transaction_list.html",
        {
            "transactions": qs.select_related("category"),
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        },
    )


@login_required
def transaction_create(request):
    if request.method == "POST":
        date_str = request.POST.get("date") or str(date.today())
        amount = request.POST.get("amount") or "0"
        kind = request.POST.get("kind") or "expense"
        category_id = request.POST.get("category")
        description = request.POST.get("description", "")

        category = get_object_or_404(Category, id=category_id, owner=request.user)

        Transaction.objects.create(
            owner=request.user,
            date=date.fromisoformat(date_str),
            amount=amount,
            kind=kind,
            category=category,
            description=description,
        )
        return redirect("finance:transaction_list")

    categories = Category.objects.filter(owner=request.user).order_by("name")
    return render(
        request,
        "finance/transaction_form.html",
        {"categories": categories},
    )
