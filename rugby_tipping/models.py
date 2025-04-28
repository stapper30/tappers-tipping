from django.db import models
from django.contrib.auth.models import User


class Match(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)
    match_round = models.IntegerField()
    date = models.DateField()
    api_sports_id = models.IntegerField(null=True)
    home_api_sports_id = models.IntegerField(null=True)
    away_api_sports_id = models.IntegerField(null=True)

    def get_winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.home_score == self.away_score:
            return 'draw'
        else:
            return self.away_team

    def get_margin(self):
        return abs(self.home_score - self.away_score)

    def get_result(self):
        return {'winner': self.get_winner(), 'margin': self.get_margin()}

    def get_correct_pick_string(self):
        if self.complete:
            options = [
                f'{self.home_team} by 2+',
                f'{self.home_team} by 1',
                'Draw',
                f'{self.away_team} by 1',
                f'{self.away_team} by 2+',
            ]
            if self.get_result()['winner'] == self.home_team:
                if self.get_result()['margin'] >= 2:
                    return options[0]
                else:
                    return options[1]
            elif self.get_result()['winner'] == self.away_team:
                if self.get_result()['margin'] >= 2:
                    return options[4]
                else:
                    return options[3]
            elif self.get_result()['winner'] == 'draw':
                return options[2]

    def get_correct_pick_int(self):
        if self.complete:
            if self.get_result()['winner'] == self.home_team:
                if self.get_result()['margin'] >= 2:
                    return 0
                else:
                    return 1
            elif self.get_result()['winner'] == self.away_team:
                if self.get_result()['margin'] >= 2:
                    return 4
                else:
                    return 3
            elif self.get_result()['winner'] == 'draw':
                return 2

    def __str__(self):
        if self.complete:
            return f'{self.home_team} - {self.home_score} vs {self.away_score} - {self.away_team}'
        else:
            return str(self.home_team) + ' vs ' + str(self.away_team)


class Pick(models.Model):
    class Options(models.IntegerChoices):
        BIG_HOME = 0
        SMALL_HOME = 1
        DRAW = 2
        SMALL_AWAY = 3
        BIG_AWAY = 4

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pick_option_integer = models.IntegerField(choices=Options.choices)

    def __str__(self) -> str:
        return self.pick_option_string()

    def pick_option_string(self):
        options = [
            f'{self.match.home_team} by 2+',
            f'{self.match.home_team} by 1',
            'Draw',
            f'{self.match.away_team} by 1',
            f'{self.match.away_team} by 2+',
        ]
        return options[self.pick_option_integer]

    def get_points(self):
        if self.match.complete:
            if self.match.get_result()['winner'] == self.match.home_team:
                if self.match.get_result()['margin'] >= 2:
                    if self.pick_option_integer == 0:
                        return 8
                    elif self.pick_option_integer == 1:
                        return 5
                    else:
                        return 0
                else:
                    if self.pick_option_integer == 1:
                        return 8
                    elif self.pick_option_integer == 0:
                        return 5
                    else:
                        return 0
            elif self.match.get_result()['winner'] == self.match.away_team:
                if self.match.get_result()['margin'] >= 2:
                    if self.pick_option_integer == 4:
                        return 8
                    elif self.pick_option_integer == 3:
                        return 5
                    else:
                        return 0
                else:
                    if self.pick_option_integer == 3:
                        return 8
                    elif self.pick_option_integer == 4:
                        return 5
                    else:
                        return 0
            elif self.match.get_result()['winner'] == 'draw':
                if self.pick_option_integer == 2:
                    return 20
                else:
                    return 0
            else:
                return 0
        else:
            return 0


class Tipper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def calculate_points(self):
        tipper_points = 0
        for pick in self.user.pick_set.all():
            tipper_points += pick.get_points()
        self.points = tipper_points
        self.save()
        return tipper_points

    def __str__(self):
        return self.user.username + " - " + str(self.points)