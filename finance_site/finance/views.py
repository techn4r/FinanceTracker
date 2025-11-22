from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TransactionForm, CategoryForm
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

    total_income = (
        qs.filter(kind="income").aggregate(Sum("amount"))["amount__sum"] or 0
    )
    total_expense = (
        qs.filter(kind="expense").aggregate(Sum("amount"))["amount__sum"] or 0
    )
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
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.owner = request.user
            tx.save()
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm(
            user=request.user,
            initial={"date": date.today()},
        )

    return render(
        request,
        "finance/transaction_form.html",
        {
            "form": form,
            "title": "Новая транзакция",
        },
    )


@login_required
def transaction_edit(request, pk: int):
    tx = get_object_or_404(Transaction, pk=pk, owner=request.user)

    if request.method == "POST":
        form = TransactionForm(
            request.POST,
            instance=tx,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect("finance:transaction_list")
    else:
        form = TransactionForm(instance=tx, user=request.user)

    return render(
        request,
        "finance/transaction_form.html",
        {
            "form": form,
            "title": "Редактирование транзакции",
            "transaction": tx,
        },
    )


@login_required
def transaction_delete(request, pk: int):
    tx = get_object_or_404(Transaction, pk=pk, owner=request.user)

    if request.method == "POST":
        tx.delete()
        return redirect("finance:transaction_list")

    return render(
        request,
        "finance/transaction_confirm_delete.html",
        {
            "transaction": tx,
        },
    )


# ---------- Категории ----------


@login_required
def category_list(request):
    categories = Category.objects.filter(owner=request.user).order_by(
        "is_income", "name"
    )
    return render(
        request,
        "finance/category_list.html",
        {
            "categories": categories,
        },
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            return redirect("finance:category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "finance/category_form.html",
        {
            "form": form,
            "title": "Новая категория",
        },
    )


@login_required
def category_edit(request, pk: int):
    cat = get_object_or_404(Category, pk=pk, owner=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect("finance:category_list")
    else:
        form = CategoryForm(instance=cat)

    return render(
        request,
        "finance/category_form.html",
        {
            "form": form,
            "title": "Редактирование категории",
            "category": cat,
        },
    )


@login_required
def category_delete(request, pk: int):
    cat = get_object_or_404(Category, pk=pk, owner=request.user)

    if request.method == "POST":
        cat.delete()
        return redirect("finance:category_list")

    return render(
        request,
        "finance/category_confirm_delete.html",
        {
            "category": cat,
        },
    )
