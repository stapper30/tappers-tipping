from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView
from .models import Pick, Match, Tipper
from . import tipping_utilities
from .forms import NewUserForm
from django.urls import reverse_lazy
import datetime
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def get_completed_matches_within_week():
    q = Match.objects.filter(
        date__lte=datetime.datetime.now() + datetime.timedelta(days=7),
        date__gte=datetime.datetime.now() - datetime.timedelta(days=7),
        complete=True,
    ).order_by("-date")
    return q


def get_uncompleted_matches_within_week():
    q = Match.objects.filter(
        date__lte=datetime.datetime.now() + datetime.timedelta(days=10),
        date__gte=datetime.datetime.now(),
        complete=False,
    ).order_by("date")
    return q

# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        tipping_utilities.calculate_points_for_all_users()
        users_picks = Pick.objects.filter(user=request.user)
        users_pick_ints_dict = {}
        users_pick_strings_dict = {}
        for pick in users_picks:
            users_pick_ints_dict[
                pick.match.api_sports_id] = pick.pick_option_integer
        for pick in users_picks:
            users_pick_strings_dict[
                pick.match.api_sports_id] = pick.pick_option_string()
        return render(
            request, "rugby_tipping\\index.html", {
                "picks": Pick.objects.all(),
                "past_matches": get_completed_matches_within_week(),
                "tippers": Tipper.objects.all().order_by("-points"),
                "pick_ints": users_pick_ints_dict,
                "upcoming_matches": get_uncompleted_matches_within_week(),
                "pick_strings": users_pick_strings_dict
            })
    else:
        return redirect(reverse_lazy("login"))


def picking_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            data = request.POST
            keys = data.keys()
            for key in keys:
                if key != "csrfmiddlewaretoken":
                    match = Match.objects.get(api_sports_id=int(key))
                    pick, created = Pick.objects.update_or_create(
                        match=match,
                        user=request.user,
                        defaults={"pick_option_integer": int(str(data[key]))},
                    )
                    pick.save()
            
            return redirect(reverse_lazy("rugby_tipping:index"))
                    
        users_picks = Pick.objects.filter(user=request.user)
        users_pick_ints_dict = {}
        users_pick_strings_dict = {}
        for pick in users_picks:
            users_pick_ints_dict[
                pick.match.api_sports_id] = pick.pick_option_integer
        for pick in users_picks:
            users_pick_strings_dict[
                pick.match.api_sports_id] = pick.pick_option_string()
    
        return render(
            request,
            "rugby_tipping\\pick.html",
            {
                "past_matches": get_completed_matches_within_week(),
                "upcoming_matches": get_uncompleted_matches_within_week(),
                "pick_ints": users_pick_ints_dict,
                "pick_strings": users_pick_strings_dict,
            },
        )
    else: 
        return redirect(reverse_lazy("login"))


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('called')
            tipper = Tipper(user=user)
            tipper.save()
            login(request, user)
            return redirect("rugby_tipping:index")
    form = NewUserForm()
    return render(request=request,
                  template_name="registration\\register.html",
                  context={"form": form})
    