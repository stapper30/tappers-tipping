from datetime import datetime, timedelta
from django.test import TestCase, Client
from urllib import response
from django.urls import reverse, reverse_lazy
from .models import Match, Pick, Tipper
from django.contrib.auth.models import User

def create_match_without_date(complete, home_score, away_score):
    match = Match(home_team='team one', away_team='team two', complete=complete, home_score=home_score, away_score=away_score, match_round=5, date='2022-10-15')
    return match

def create_match_with_date(complete, home_score, away_score, date):
    match = Match(home_team='team one', away_team='team two', complete=complete, home_score=home_score, away_score=away_score, match_round=5, date=date)
    return match

def create_pick(pick_option_integer, match, user):
    pick = Pick(pick_option_integer=pick_option_integer, user=user, match=match)
    return pick

def create_user(uname):
    user=User(username=uname, password="12345678gchjg")
    return user


# Create your tests here.
class MatchModelTests(TestCase):
    def test_match_get_margin_home(self):
        match = create_match_without_date(complete=True, home_score=30, away_score=20)
        self.assertEqual(match.get_result(), {'winner': "team one", 'margin': 10})

    def test_match_get_margin_away(self):
        match = create_match_without_date(complete=True, home_score=20, away_score=30)
        self.assertEqual(match.get_result(), {'winner': "team two", 'margin': 10})

    def test_match_points_correct_margin(self):
        match = create_match_without_date(complete=True, home_score=30, away_score=20)
        user = create_user("user")
        pick = create_pick(1, match, user)
        self.assertEqual(pick.get_points(), 8)

    def test_match_points_correct_team(self):
        match = create_match_without_date(complete=True, home_score=30, away_score=20)
        user = create_user("user")
        pick = create_pick(0, match, user)
        self.assertEqual(pick.get_points(), 5)

    def test_match_points_draw(self):
        match = create_match_without_date(complete=True, home_score=20, away_score=20)
        user = create_user("user")
        pick = create_pick(2, match, user)
        self.assertEqual(pick.get_points(), 20)

    def test_match_points_wrong(self):
        match = create_match_without_date(complete=True, home_score=20, away_score=25)
        user = create_user("user")
        pick = create_pick(1, match, user=user)
        self.assertEqual(pick.get_points(), 0)

class TipperModelTests(TestCase):        
    def test_calculate_user_points(self):
        user = create_user("usertwo")
        user.save()
        tipper = Tipper(user=user, points=0)
        match_one = create_match_without_date(True, 50, 20)
        match_one.save()
        pick_one = create_pick(0, match_one, user)
        pick_one.save()  #8 points
        match_two = create_match_without_date(True, 50, 20)
        match_two.save()
        pick_two = create_pick(1, match_two, user)
        pick_two.save()  #5 points
        match_three = create_match_without_date(True, 20, 50)
        match_three.save()
        pick_three = create_pick(3, match_three, user)
        pick_three.save()  #5 points
        match_four = create_match_without_date(True, 20, 50)
        match_four.save()
        pick_four = create_pick(4, match_four, user)
        pick_four.save()  #8 points
        tipper.calculate_points()
        self.assertEqual(tipper.points, 26) 

# class IndexViewTests(TestCase):
#     def test_index_loads(self):
#         response = self.client.get(reverse('rugby_tipping:index'))
#         self.assertEqual(response.status_code, 200)
    
#     def test_index_uses_correct_template(self):
#         user = create_user(uname='foo')
#         self.client.login(username=user.username, password=user.password)
#         response = self.client.get(reverse('rugby_tipping:index'))
#         self.assertTemplateUsed(response, 'rugby_tipping\\index.html')
    
#     def test_index_context_gives_correct_data(self):
#         for i in range(3):
#             user = create_user("user_" + str(i))
#             user.save()
#             tipper = Tipper(user=user, points=0)
#             tipper.save()
#         user = create_user(uname='foo')
#         self.client.login(username=user.username, password=user.password)
#         response = self.client.get(reverse('rugby_tipping:index'))
#         self.assertQuerysetEqual(response.context['tippers'], Tipper.objects.all().order_by('-points'))

# class PickViewTests(TestCase):
    # def test_picks_loads(self):
    #     user = create_user(uname='foo')
    #     self.client.login(username=user.username, password=user.password)
    #     response = self.client.get(reverse_lazy('rugby_tipping:pick'))
    #     self.assertEqual(response.status_code, 200)

    # def test_pick_uses_correct_template(self):
    #     user = create_user(uname='foo')
    #     self.client.login(username=user.username, password=user.password)
    #     response = self.client.get(reverse('rugby_tipping:pick'))
    #     self.assertTemplateUsed(response, 'rugby_tipping\\pick.html')
    
    # def test_get_completed_matches(self):
    #     for i in range(3):
    #         match = create_match_with_date(True, 50, 20, datetime.now() - timedelta(days=5))
    #         match.save()
    #     for i in range(2):
    #         match = create_match_with_date(True, 50, 20, datetime.now() - timedelta(days=9))
    #         match.save()

    #     for i in range(2):
    #         match = create_match_without_date(False, 50, 20)
    #         match.save()
    #     user = create_user(uname='foo')
    #     self.client.login(username=user.username, password=user.password)
    #     response = self.client.get(reverse('rugby_tipping:pick'))
    #     self.assertEqual(3, len(response.context['completed_matches']))

    # def test_get_uncompleted_matches(self):
    #     for i in range(3):
    #         match = create_match_with_date(False, 50, 20, datetime.now() - timedelta(days=5))
    #         match.save()
    #     for i in range(3):
    #         match = create_match_with_date(True, 50, 20, datetime.now() - timedelta(days=5))
    #         match.save()
    #     for i in range(2):
    #         match = create_match_with_date(False, 50, 20, datetime.now() - timedelta(days=9))
    #         match.save()

    #     for i in range(2):
    #         match = create_match_without_date(False, 50, 20)
    #         match.save()
    #     user = create_user(uname='foo')
    #     self.client.login(username=user.username, password=user.password)
    #     response = self.client.get(reverse('rugby_tipping:pick'))
    #     self.assertEqual(3, len(response.context['completed_matches']))
        
        