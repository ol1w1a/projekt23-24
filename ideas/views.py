from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Idea, Vote  # DODANO: Vote
from .forms import IdeaForm


def idea_list(request):
    sort = request.GET.get('sort')
    # Pobieramy pomysły i od razu liczymy głosy dla każdego z nich
    ideas = Idea.objects.annotate(num_votes=Count('votes'))

    if sort == 'min':
        ideas = ideas.order_by('num_votes')
    elif sort == 'max':
        ideas = ideas.order_by('-num_votes')
    else:
        # Najnowsze na górze (pamiętaj, że musisz mieć pole created_at w modelu!)
        ideas = ideas.order_by('-created_at')

    # Agregacja statystyk globalnych
    stats = Idea.objects.aggregate(total_ideas=Count('id'), total_votes=Count('votes'))

    return render(request, 'ideas/list.html', {
        'ideas': ideas,
        'stats': stats,
    })


def idea_detail(request, pk):
    # Pobieramy konkretny pomysł
    idea = get_object_or_404(Idea, pk=pk)
    can_vote = True

    # Obsługa sesji (żeby wiedzieć, kto już głosował)
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    # Sprawdzenie czy ten użytkownik (ta sesja) już głosował na ten projekt
    if Vote.objects.filter(idea=idea, session_id=session_id).exists():
        can_vote = False

    # Jeśli użytkownik kliknął "Głosuj" (POST) i ma do tego prawo
    if request.method == 'POST' and can_vote:
        Vote.objects.create(idea=idea, session_id=session_id)
        return redirect('idea_detail', pk=pk)

    return render(request, 'ideas/detail.html', {
        'idea': idea,
        'can_vote': can_vote
    })


def idea_create(request):
    # Prosta obsługa formularza - jeśli POST to zapisz, jeśli GET to wyświetl pusty
    form = IdeaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('idea_list')

    return render(request, 'ideas/form.html', {'form': form})