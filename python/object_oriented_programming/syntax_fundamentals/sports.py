# Sports -> Football, Basketball, Cricket, Tennis

class Sports:
    class Football:
        def __init__(self, team, stadium):
            self.team = team
            self.stadium = stadium

        def details(self):
            return f"Football team: {self.team} | Stadium: {self.stadium}"

    class Basketball:
        def __init__(self, team, court):
            self.team = team
            self.court = court

        def details(self):
            return f"Basketball team: {self.team} | Court: {self.court}"

    class Cricket:
        def __init__(self, team, venue):
            self.team = team
            self.venue = venue

        def details(self):
            return f"Cricket team: {self.team} | Venue: {self.venue}"

    class Tennis:
        def __init__(self, tournament, surface):
            self.tournament = tournament
            self.surface = surface

        def details(self):
            return f"Tennis tournament: {self.tournament} | Surface: {self.surface}"


football = Sports.Football("Arsenal", "Emirates Stadium")
basketball = Sports.Basketball("Lakers", "Staples Center")
cricket = Sports.Cricket("England", "Lord's")
tennis = Sports.Tennis("Wimbledon", "Grass")

print(football.details())
print(basketball.details())
print(cricket.details())
print(tennis.details())

