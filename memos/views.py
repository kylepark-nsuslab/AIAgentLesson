
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, MemoForm
from .models import Memo

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('memo_list')  # 로그인 후 메모 목록으로 리다이렉트
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


# 메모 목록
@login_required
def memo_list(request):
    memos = Memo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "memos/memo_list.html", {"memos": memos})

# 메모 상세
@login_required
def memo_detail(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    return render(request, "memos/memo_detail.html", {"memo": memo})

# 메모 생성
@login_required
def memo_create(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect('memo_detail', pk=memo.pk)
    else:
        form = MemoForm()
    return render(request, "memos/memo_form.html", {"form": form})

# 메모 수정
@login_required
def memo_update(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memo_detail', pk=memo.pk)
    else:
        form = MemoForm(instance=memo)
    return render(request, "memos/memo_form.html", {"form": form})

# 메모 삭제
@login_required
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        memo.delete()
        return redirect('memo_list')
    return render(request, "memos/memo_confirm_delete.html", {"memo": memo})
