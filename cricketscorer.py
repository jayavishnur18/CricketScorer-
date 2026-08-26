import json
import os
from datetime import datetime
from copy import deepcopy

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

============================================================

MATCH HISTORY

============================================================

def history_file():
return os.path.join(
App.get_running_app().user_data_dir,
"matches.json"
)

def load_history():
try:
with open(history_file(), "r") as f:
return json.load(f)
except:
return []

def save_history(data):
with open(history_file(), "w") as f:
json.dump(data, f, indent=2)

============================================================

HOME / SETUP

============================================================

class SetupScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    layout = BoxLayout(  
        orientation="vertical",  
        padding=dp(20),  
        spacing=dp(10)  
    )  

    layout.add_widget(Label(  
        text="🏏 CRICKET SCORER",  
        font_size=dp(28),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    layout.add_widget(Label(text="Team A"))  

    self.team_a = TextInput(  
        hint_text="Enter Team A",  
        multiline=False,  
        size_hint_y=None,  
        height=dp(50)  
    )  
    layout.add_widget(self.team_a)  

    layout.add_widget(Label(text="Team B"))  

    self.team_b = TextInput(  
        hint_text="Enter Team B",  
        multiline=False,  
        size_hint_y=None,  
        height=dp(50)  
    )  
    layout.add_widget(self.team_b)  

    layout.add_widget(Label(text="Overs"))  

    self.overs = TextInput(  
        hint_text="Example: 6",  
        input_filter="int",  
        multiline=False,  
        size_hint_y=None,  
        height=dp(50)  
    )  
    layout.add_widget(self.overs)  

    start = Button(  
        text="NEXT → PLAYERS",  
        size_hint_y=None,  
        height=dp(60)  
    )  
    start.bind(on_press=self.next_page)  
    layout.add_widget(start)  

    history = Button(  
        text="📚 MATCH HISTORY",  
        size_hint_y=None,  
        height=dp(50)  
    )  
    history.bind(on_press=self.open_history)  
    layout.add_widget(history)  

    self.add_widget(layout)  

def next_page(self, instance):  

    team_a = self.team_a.text.strip() or "TEAM A"  
    team_b = self.team_b.text.strip() or "TEAM B"  

    try:  
        overs = int(self.overs.text)  
        if overs <= 0:  
            overs = 6  
    except:  
        overs = 6  

    screen = self.manager.get_screen("players")  

    screen.team_a = team_a  
    screen.team_b = team_b  
    screen.max_overs = overs  
    screen.create_page()  

    self.manager.current = "players"  

def open_history(self, instance):  

    screen = self.manager.get_screen("history")  
    screen.show_history()  
    self.manager.current = "history"

============================================================

PLAYERS

============================================================

class PlayersScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical"  
    )  
    self.add_widget(self.main)  

def create_page(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="👥 PLAYERS",  
        font_size=dp(25),  
        bold=True,  
        size_hint_y=None,  
        height=dp(55)  
    ))  

    scroll = ScrollView()  

    content = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    content.bind(  
        minimum_height=content.setter("height")  
    )  

    content.add_widget(Label(  
        text=self.team_a,  
        font_size=dp(21),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    self.a_inputs = []  

    for i in range(11):  

        box = TextInput(  
            hint_text=f"{self.team_a} Player {i + 1}",  
            multiline=False,  
            size_hint_y=None,  
            height=dp(45)  
        )  

        self.a_inputs.append(box)  
        content.add_widget(box)  

    content.add_widget(Label(  
        text=self.team_b,  
        font_size=dp(21),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    self.b_inputs = []  

    for i in range(11):  

        box = TextInput(  
            hint_text=f"{self.team_b} Player {i + 1}",  
            multiline=False,  
            size_hint_y=None,  
            height=dp(45)  
        )  

        self.b_inputs.append(box)  
        content.add_widget(box)  

    scroll.add_widget(content)  
    self.main.add_widget(scroll)  

    button = Button(  
        text="NEXT → TOSS",  
        size_hint_y=None,  
        height=dp(60)  
    )  

    button.bind(on_press=self.next_page)  
    self.main.add_widget(button)  

def next_page(self, instance):  

    team_a_players = []  

    for i, box in enumerate(self.a_inputs):  

        name = box.text.strip()  

        if not name:  
            name = f"Player {i + 1}"  

        team_a_players.append(name)  

    team_b_players = []  

    for i, box in enumerate(self.b_inputs):  

        name = box.text.strip()  

        if not name:  
            name = f"Player {i + 1}"  

        team_b_players.append(name)  

    toss = self.manager.get_screen("toss")  

    toss.team_a = self.team_a  
    toss.team_b = self.team_b  

    toss.team_a_players = team_a_players  
    toss.team_b_players = team_b_players  
    toss.max_overs = self.max_overs  

    toss.show_page()  

    self.manager.current = "toss"

============================================================

TOSS

============================================================

class TossScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(20),  
        spacing=dp(15)  
    )  

    self.add_widget(self.main)  

def show_page(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="🪙 TOSS",  
        font_size=dp(30),  
        bold=True,  
        size_hint_y=None,  
        height=dp(70)  
    ))  

    self.main.add_widget(  
        Label(text="WHO WON THE TOSS?")  
    )  

    a = Button(  
        text=self.team_a,  
        size_hint_y=None,  
        height=dp(60)  
    )  

    b = Button(  
        text=self.team_b,  
        size_hint_y=None,  
        height=dp(60)  
    )  

    a.bind(  
        on_press=lambda x:  
        self.choose_winner(self.team_a)  
    )  

    b.bind(  
        on_press=lambda x:  
        self.choose_winner(self.team_b)  
    )  

    self.main.add_widget(a)  
    self.main.add_widget(b)  

def choose_winner(self, winner):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=f"{winner}\nWON THE TOSS",  
        font_size=dp(25),  
        bold=True  
    ))  

    bat = Button(  
        text="🏏 BAT FIRST",  
        size_hint_y=None,  
        height=dp(60)  
    )  

    bowl = Button(  
        text="🎯 BOWL FIRST",  
        size_hint_y=None,  
        height=dp(60)  
    )  

    bat.bind(  
        on_press=lambda x:  
        self.finish(winner, True)  
    )  

    bowl.bind(  
        on_press=lambda x:  
        self.finish(winner, False)  
    )  

    self.main.add_widget(bat)  
    self.main.add_widget(bowl)  

def finish(self, winner, bat_first):  

    if bat_first:  

        batting = winner  

        bowling = (  
            self.team_b  
            if winner == self.team_a  
            else self.team_a  
        )  

    else:  

        bowling = winner  

        batting = (  
            self.team_b  
            if winner == self.team_a  
            else self.team_a  
        )  

    selection = self.manager.get_screen("selection")  

    selection.batting_team = batting  
    selection.bowling_team = bowling  

    if batting == self.team_a:  

        selection.batting_players = self.team_a_players  
        selection.bowling_players = self.team_b_players  

    else:  

        selection.batting_players = self.team_b_players  
        selection.bowling_players = self.team_a_players  

    selection.max_overs = self.max_overs  
    selection.innings_number = 1  
    selection.target = 0  
    selection.out_players = []  

    selection.show_striker()  

    self.manager.current = "selection"

============================================================

PLAYER SELECTION

============================================================

class SelectionScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(15),  
        spacing=dp(7)  
    )  

    self.add_widget(self.main)  

def show_striker(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=f"🏏 {self.batting_team}",  
        font_size=dp(24),  
        bold=True,  
        size_hint_y=None,  
        height=dp(55)  
    ))  

    self.main.add_widget(Label(  
        text="SELECT STRIKER",  
        font_size=dp(19),  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    for player in self.batting_players:  

        if player in self.out_players:  
            continue  

        button = Button(  
            text=player,  
            size_hint_y=None,  
            height=dp(50)  
        )  

        button.bind(  
            on_press=lambda x, p=player:  
            self.select_striker(p)  
        )  

        grid.add_widget(button)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

def select_striker(self, player):  

    self.striker = player  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=f"⭐ STRIKER\n{player}",  
        font_size=dp(22),  
        bold=True,  
        size_hint_y=None,  
        height=dp(75)  
    ))  

    self.main.add_widget(Label(  
        text="SELECT NON-STRIKER",  
        font_size=dp(19),  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    for player in self.batting_players:  

        if player == self.striker:  
            continue  

        if player in self.out_players:  
            continue  

        button = Button(  
            text=player,  
            size_hint_y=None,  
            height=dp(50)  
        )  

        button.bind(  
            on_press=lambda x, p=player:  
            self.select_non_striker(p)  
        )  

        grid.add_widget(button)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

def select_non_striker(self, player):  

    self.non_striker = player  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=(  
            f"STRIKER: {self.striker}\n"  
            f"NON-STRIKER: {self.non_striker}"  
        ),  
        font_size=dp(18),  
        size_hint_y=None,  
        height=dp(65)  
    ))  

    self.main.add_widget(Label(  
        text="SELECT BOWLER",  
        font_size=dp(19),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    for player in self.bowling_players:  

        if player == getattr(self, "last_bowler", ""):  
            continue  

        button = Button(  
            text=player,  
            size_hint_y=None,  
            height=dp(50)  
        )  

        button.bind(  
            on_press=lambda x, p=player:  
            self.select_bowler(p)  
        )  

        grid.add_widget(button)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

def select_bowler(self, bowler):  

    scorer = self.manager.get_screen("scorer")  

    scorer.start_innings(  
        self.batting_team,  
        self.bowling_team,  
        self.batting_players,  
        self.bowling_players,  
        self.striker,  
        self.non_striker,  
        bowler,  
        self.max_overs,  
        self.innings_number,  
        self.target,  
        self.out_players  
    )  

    self.manager.current = "scorer"

============================================================

PLAYER PROFILE

============================================================

class ProfileScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(10),  
        spacing=dp(8)  
    )  

    self.add_widget(self.main)  

def show_profile(self, player, scorer):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=f"👤 {player}",  
        font_size=dp(28),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    scroll = ScrollView()  

    content = GridLayout(  
        cols=1,  
        spacing=dp(8),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    content.bind(  
        minimum_height=content.setter("height")  
    )  

    content.add_widget(Label(  
        text="🏏 BATTING",  
        font_size=dp(22),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    runs = scorer.bat_runs.get(player, 0)  
    balls = scorer.bat_balls.get(player, 0)  
    fours = scorer.bat_fours.get(player, 0)  
    sixes = scorer.bat_sixes.get(player, 0)  

    strike_rate = (  
        (runs / balls) * 100  
        if balls > 0  
        else 0  
    )  

    for text in [  
        f"Runs: {runs}",  
        f"Balls: {balls}",  
        f"Fours: {fours}",  
        f"Sixes: {sixes}",  
        f"Strike Rate: {strike_rate:.2f}"  
    ]:  

        content.add_widget(Label(  
            text=text,  
            font_size=dp(18),  
            size_hint_y=None,  
            height=dp(40)  
        ))  

    content.add_widget(Label(  
        text="🎯 BOWLING",  
        font_size=dp(22),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    bowl_balls = scorer.bowl_balls.get(player, 0)  
    bowl_runs = scorer.bowl_runs.get(player, 0)  
    wickets = scorer.bowl_wickets.get(player, 0)  

    overs = bowl_balls // 6  
    remaining = bowl_balls % 6  

    economy = (  
        (bowl_runs / bowl_balls) * 6  
        if bowl_balls > 0  
        else 0  
    )  

    for text in [  
        f"Overs: {overs}.{remaining}",  
        f"Runs Conceded: {bowl_runs}",  
        f"Wickets: {wickets}",  
        f"Economy: {economy:.2f}"  
    ]:  

        content.add_widget(Label(  
            text=text,  
            font_size=dp(18),  
            size_hint_y=None,  
            height=dp(40)  
        ))  

    content.add_widget(Label(  
        text="📋 STATUS",  
        font_size=dp(22),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    if player in scorer.out_players:  
        status = "❌ OUT"  
    elif (  
        player == scorer.striker or  
        player == scorer.non_striker  
    ):  
        status = "🏏 CURRENT BATSMAN"  
    else:  
        status = "✅ NOT OUT / NOT CURRENT"  

    content.add_widget(Label(  
        text=status,  
        font_size=dp(18),  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll.add_widget(content)  
    self.main.add_widget(scroll)  

    back = Button(  
        text="← BACK TO PLAYER LIST",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    back.bind(  
        on_press=lambda x:  
        self.back_to_profiles(scorer)  
    )  

    self.main.add_widget(back)  

def back_to_profiles(self, scorer):  

    screen = self.manager.get_screen("profiles")  
    screen.show_players(scorer)  
    self.manager.current = "profiles"

============================================================

PLAYER LIST

============================================================

class ProfilesScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(10),  
        spacing=dp(8)  
    )  

    self.add_widget(self.main)  

def show_players(self, scorer):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="👤 PLAYER PROFILES",  
        font_size=dp(27),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    grid.add_widget(Label(  
        text=scorer.batting_team,  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    for player in scorer.batting_players:  

        b = Button(  
            text=f"👤 {player}",  
            size_hint_y=None,  
            height=dp(55)  
        )  

        b.bind(  
            on_press=lambda x, p=player:  
            self.open_profile(p, scorer)  
        )  

        grid.add_widget(b)  

    grid.add_widget(Label(  
        text=scorer.bowling_team,  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    for player in scorer.bowling_players:  

        b = Button(  
            text=f"👤 {player}",  
            size_hint_y=None,  
            height=dp(55)  
        )  

        b.bind(  
            on_press=lambda x, p=player:  
            self.open_profile(p, scorer)  
        )  

        grid.add_widget(b)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

    back = Button(  
        text="← BACK TO SCORING",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    back.bind(  
        on_press=lambda x:  
        self.back_to_scorer(scorer)  
    )  

    self.main.add_widget(back)  

def open_profile(self, player, scorer):  

    profile = self.manager.get_screen("profile")  

    profile.show_profile(  
        player,  
        scorer  
    )  

    self.manager.current = "profile"  

def back_to_scorer(self, scorer):  

    self.manager.current = "scorer"  

    scorer.build_screen()  
    scorer.update_screen()

============================================================

SCORER

============================================================

class ScorerScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(8),  
        spacing=dp(5)  
    )  

    self.add_widget(self.main)  

# ========================================================  
# START INNINGS  
# ========================================================  

def start_innings(  
    self,  
    batting_team,  
    bowling_team,  
    batting_players,  
    bowling_players,  
    striker,  
    non_striker,  
    bowler,  
    max_overs,  
    innings_number,  
    target,  
    out_players  
):  

    self.batting_team = batting_team  
    self.bowling_team = bowling_team  

    self.batting_players = batting_players  
    self.bowling_players = bowling_players  

    self.striker = striker  
    self.non_striker = non_striker  
    self.bowler = bowler  

    self.max_overs = max_overs  
    self.innings_number = innings_number  
    self.target = target  

    self.out_players = list(out_players)  

    self.runs = 0  
    self.wickets = 0  
    self.balls = 0  
    self.over_balls = 0  
    self.current_over = 1  

    self.wides = 0  
    self.no_balls = 0  

    self.bat_runs = {  
        p: 0 for p in batting_players  
    }  

    self.bat_balls = {  
        p: 0 for p in batting_players  
    }  

    self.bat_fours = {  
        p: 0 for p in batting_players  
    }  

    self.bat_sixes = {  
        p: 0 for p in batting_players  
    }  

    self.bowl_runs = {  
        p: 0 for p in bowling_players  
    }  

    self.bowl_balls = {  
        p: 0 for p in bowling_players  
    }  

    self.bowl_wickets = {  
        p: 0 for p in bowling_players  
    }  

    self.partnership_runs = 0  
    self.partnership_balls = 0  

    self.undo_stack = []  
    self.current_over_history = []  

    self.finished = False  

    self.build_screen()  
    self.update_screen()  

# ========================================================  
# SAVE STATE  
# ========================================================  

def save_state(self):  

    self.undo_stack.append({  
        "runs": self.runs,  
        "wickets": self.wickets,  
        "balls": self.balls,  
        "over_balls": self.over_balls,  
        "current_over": self.current_over,  
        "wides": self.wides,  
        "no_balls": self.no_balls,  
        "striker": self.striker,  
        "non_striker": self.non_striker,  
        "bowler": self.bowler,  
        "out_players": deepcopy(self.out_players),  
        "bat_runs": deepcopy(self.bat_runs),  
        "bat_balls": deepcopy(self.bat_balls),  
        "bat_fours": deepcopy(self.bat_fours),  
        "bat_sixes": deepcopy(self.bat_sixes),  
        "bowl_runs": deepcopy(self.bowl_runs),  
        "bowl_balls": deepcopy(self.bowl_balls),  
        "bowl_wickets": deepcopy(self.bowl_wickets),  
        "partnership_runs": self.partnership_runs,  
        "partnership_balls": self.partnership_balls,  
        "current_over_history":  
            deepcopy(self.current_over_history)  
    })  

# ========================================================  
# UNDO  
# ========================================================  

def undo_last_ball(self, instance):  

    if not self.undo_stack:  
        return  

    state = self.undo_stack.pop()  

    self.runs = state["runs"]  
    self.wickets = state["wickets"]  
    self.balls = state["balls"]  
    self.over_balls = state["over_balls"]  
    self.current_over = state["current_over"]  

    self.wides = state["wides"]  
    self.no_balls = state["no_balls"]  

    self.striker = state["striker"]  
    self.non_striker = state["non_striker"]  
    self.bowler = state["bowler"]  

    self.out_players = state["out_players"]  

    self.bat_runs = state["bat_runs"]  
    self.bat_balls = state["bat_balls"]  
    self.bat_fours = state["bat_fours"]  
    self.bat_sixes = state["bat_sixes"]  

    self.bowl_runs = state["bowl_runs"]  
    self.bowl_balls = state["bowl_balls"]  
    self.bowl_wickets = state["bowl_wickets"]  

    self.partnership_runs = state["partnership_runs"]  
    self.partnership_balls = state["partnership_balls"]  

    self.current_over_history = (  
        state["current_over_history"]  
    )  

    self.finished = False  

    self.build_screen()  
    self.update_screen()  

# ========================================================  
# BUILD SCORER  
# ========================================================  

def build_screen(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=(  
            f"{self.batting_team} "  
            f"{self.runs}/{self.wickets}"  
        ),  
        font_size=dp(26),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    self.score_label = Label(  
        text="",  
        font_size=dp(14),  
        size_hint_y=None,  
        height=dp(65)  
    )  

    self.main.add_widget(self.score_label)  

    self.players_label = Label(  
        text="",  
        font_size=dp(14),  
        size_hint_y=None,  
        height=dp(65)  
    )  

    self.main.add_widget(self.players_label)  

    self.bowler_label = Label(  
        text="",  
        font_size=dp(14),  
        size_hint_y=None,  
        height=dp(35)  
    )  

    self.main.add_widget(self.bowler_label)  

    self.partnership_label = Label(  
        text="",  
        font_size=dp(14),  
        size_hint_y=None,  
        height=dp(35)  
    )  

    self.main.add_widget(self.partnership_label)  

    self.ball_label = Label(  
        text="",  
        font_size=dp(14),  
        size_hint_y=None,  
        height=dp(35)  
    )  

    self.main.add_widget(self.ball_label)  

    buttons = GridLayout(  
        cols=3,  
        spacing=dp(5),  
        size_hint_y=None,  
        height=dp(165)  
    )  

    for run in [0, 1, 2, 3, 4, 6]:  

        b = Button(text=str(run))  

        b.bind(  
            on_press=lambda x, r=run:  
            self.add_runs(r)  
        )  

        buttons.add_widget(b)  

    wicket = Button(text="WICKET")  
    wicket.bind(on_press=self.add_wicket)  

    wide = Button(text="WIDE")  
    wide.bind(on_press=self.add_wide)  

    noball = Button(text="NO BALL")  
    noball.bind(on_press=self.add_no_ball)  

    buttons.add_widget(wicket)  
    buttons.add_widget(wide)  
    buttons.add_widget(noball)  

    self.main.add_widget(buttons)  

    bottom = GridLayout(  
        cols=3,  
        spacing=dp(5),  
        size_hint_y=None,  
        height=dp(105)  
    )  

    undo = Button(text="↩ UNDO")  
    undo.bind(on_press=self.undo_last_ball)  

    scorecard = Button(text="📊 SCORECARD")  
    scorecard.bind(  
        on_press=lambda x:  
        self.show_scorecard()  
    )  

    profile = Button(text="👤 PROFILE")  
    profile.bind(  
        on_press=lambda x:  
        self.open_profile_list()  
    )  

    bottom.add_widget(undo)  
    bottom.add_widget(scorecard)  
    bottom.add_widget(profile)  

    self.main.add_widget(bottom)  

# ========================================================  
# RUNS  
# ========================================================  

def add_runs(self, run):  

    if self.finished:  
        return  

    self.save_state()  

    self.runs += run  

    self.balls += 1  
    self.over_balls += 1  

    self.partnership_runs += run  
    self.partnership_balls += 1  

    self.bat_runs[self.striker] += run  
    self.bat_balls[self.striker] += 1  

    if run == 4:  
        self.bat_fours[self.striker] += 1  

    if run == 6:  
        self.bat_sixes[self.striker] += 1  

    self.bowl_runs[self.bowler] += run  
    self.bowl_balls[self.bowler] += 1  

    self.current_over_history.append(str(run))  

    if run % 2 == 1:  

        self.striker, self.non_striker = (  
            self.non_striker,  
            self.striker  
        )  

    if self.innings_number == 2:  

        if self.runs >= self.target:  
            self.win_by_chase()  
            return  

    if self.over_balls == 6:  

        self.complete_over()  
        return  

    self.update_screen()  

# ========================================================  
# WICKET  
# ========================================================  

def add_wicket(self, instance):  

    if self.finished:  
        return  

    self.save_state()  

    player = self.striker  

    self.out_players.append(player)  

    self.wickets += 1  

    self.balls += 1  
    self.over_balls += 1  

    self.partnership_balls += 1  

    self.bat_balls[player] += 1  

    self.bowl_balls[self.bowler] += 1  
    self.bowl_wickets[self.bowler] += 1  

    self.current_over_history.append("W")  

    self.partnership_runs = 0  
    self.partnership_balls = 0  

    if self.wickets >= 10:  
        self.end_innings()  
        return  

    if self.over_balls == 6:  
        self.complete_over()  
        return  

    self.select_new_batsman()  

# ========================================================  
# WIDE  
# ========================================================  

def add_wide(self, instance):  

    if self.finished:  
        return  

    self.save_state()  

    self.runs += 1  
    self.wides += 1  

    self.bowl_runs[self.bowler] += 1  

    self.current_over_history.append("Wd")  
    self.partnership_runs += 1  

    if self.innings_number == 2:  

        if self.runs >= self.target:  
            self.win_by_chase()  
            return  

    self.update_screen()  

# ========================================================  
# NO BALL  
# ========================================================  

def add_no_ball(self, instance):  

    if self.finished:  
        return  

    self.save_state()  

    self.runs += 1  
    self.no_balls += 1  

    self.bowl_runs[self.bowler] += 1  

    self.current_over_history.append("Nb")  
    self.partnership_runs += 1  

    if self.innings_number == 2:  

        if self.runs >= self.target:  
            self.win_by_chase()  
            return  

    self.update_screen()  

# ========================================================  
# NEW BATSMAN  
# ========================================================  

def select_new_batsman(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="🚨 WICKET!",  
        font_size=dp(28),  
        bold=True,  
        size_hint_y=None,  
        height=dp(55)  
    ))  

    self.main.add_widget(Label(  
        text="SELECT NEW BATSMAN",  
        font_size=dp(20),  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    for player in self.batting_players:  

        if player in self.out_players:  
            continue  

        if player == self.non_striker:  
            continue  

        b = Button(  
            text=player,  
            size_hint_y=None,  
            height=dp(55)  
        )  

        b.bind(  
            on_press=lambda x, p=player:  
            self.new_batsman(p)  
        )  

        grid.add_widget(b)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

def new_batsman(self, player):  

    self.striker = player  

    self.build_screen()  
    self.update_screen()  

# ========================================================  
# NEW BOWLER  
# ========================================================  

def complete_over(self):  

    self.current_over_history = []  

    self.current_over += 1  
    self.over_balls = 0  

    self.striker, self.non_striker = (  
        self.non_striker,  
        self.striker  
    )  

    if self.balls >= self.max_overs * 6:  

        self.end_innings()  
        return  

    self.select_new_bowler()  

def select_new_bowler(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text=f"🏏 OVER {self.current_over}",  
        font_size=dp(28),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    self.main.add_widget(Label(  
        text="SELECT NEW BOWLER",  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    grid = GridLayout(  
        cols=1,  
        spacing=dp(7),  
        padding=dp(10),  
        size_hint_y=None  
    )  

    grid.bind(  
        minimum_height=grid.setter("height")  
    )  

    for player in self.bowling_players:  

        if player == self.bowler:  
            continue  

        b = Button(  
            text=player,  
            size_hint_y=None,  
            height=dp(55)  
        )  

        b.bind(  
            on_press=lambda x, p=player:  
            self.new_bowler(p)  
        )  

        grid.add_widget(b)  

    scroll.add_widget(grid)  
    self.main.add_widget(scroll)  

def new_bowler(self, player):  

    self.bowler = player  

    self.build_screen()  
    self.update_screen()  

# ========================================================  
# UPDATE SCREEN  
# ========================================================  

def update_screen(self):  

    overs = self.balls // 6  
    balls = self.balls % 6  

    run_rate = (  
        (self.runs / self.balls) * 6  
        if self.balls > 0  
        else 0  
    )  

    text = (  
        f"OVER: {overs}.{balls}/{self.max_overs}\n"  
        f"Run Rate: {run_rate:.2f}"  
    )  

    if self.innings_number == 2:  

        remaining_runs = max(  
            0,  
            self.target - self.runs  
        )  

        remaining_balls = max(  
            0,  
            self.max_overs * 6 - self.balls  
        )  

        required_rate = (  
            (remaining_runs / remaining_balls) * 6  
            if remaining_balls > 0  
            else 0  
        )  

        text += (  
            f"\nNeed {remaining_runs} runs "  
            f"from {remaining_balls} balls"  
            f"\nRequired RR: {required_rate:.2f}"  
        )  

    self.score_label.text = text  

    sr = self.bat_runs[self.striker]  
    sb = self.bat_balls[self.striker]  

    nr = self.bat_runs[self.non_striker]  
    nb = self.bat_balls[self.non_striker]  

    self.players_label.text = (  
        f"⭐ {self.striker}: {sr} ({sb})\n"  
        f"{self.non_striker}: {nr} ({nb})"  
    )  

    bb = self.bowl_balls[self.bowler]  

    bo = bb // 6  
    ball = bb % 6  

    self.bowler_label.text = (  
        f"🎯 {self.bowler}: "  
        f"{bo}.{ball} overs | "  
        f"{self.bowl_runs[self.bowler]} runs | "  
        f"{self.bowl_wickets[self.bowler]} W"  
    )  

    self.partnership_label.text = (  
        f"🤝 Partnership: "  
        f"{self.partnership_runs} runs "  
        f"({self.partnership_balls} balls)"  
    )  

    if self.current_over_history:  

        self.ball_label.text = (  
            "THIS OVER: " +  
            "  ".join(self.current_over_history)  
        )  

    else:  

        self.ball_label.text = "THIS OVER: -"  

# ========================================================  
# PROFILE LIST  
# ========================================================  

def open_profile_list(self):  

    profile_screen = self.manager.get_screen(  
        "profiles"  
    )  

    profile_screen.show_players(self)  

    self.manager.current = "profiles"  

# ========================================================  
# SCORECARD  
# ========================================================  

def show_scorecard(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="📊 SCORECARD",  
        font_size=dp(28),  
        bold=True,  
        size_hint_y=None,  
        height=dp(55)  
    ))  

    self.main.add_widget(Label(  
        text=(  
            f"{self.batting_team} "  
            f"{self.runs}/{self.wickets}"  
        ),  
        font_size=dp(23),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    scroll = ScrollView()  

    content = GridLayout(  
        cols=1,  
        spacing=dp(5),  
        padding=dp(8),  
        size_hint_y=None  
    )  

    content.bind(  
        minimum_height=content.setter("height")  
    )  

    content.add_widget(Label(  
        text="🏏 BATTING",  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(40)  
    ))  

    for player in self.batting_players:  

        r = self.bat_runs[player]  
        b = self.bat_balls[player]  

        f4 = self.bat_fours[player]  
        f6 = self.bat_sixes[player]  

        sr = (  
            (r / b) * 100  
            if b > 0  
            else 0  
        )  

        status = (  
            " OUT"  
            if player in self.out_players  
            else ""  
        )  

        content.add_widget(Label(  
            text=(  
                f"{player}{status}\n"  
                f"{r} runs | {b} balls | "  
                f"{f4} fours | {f6} sixes | "  
                f"SR {sr:.2f}"  
            ),  
            font_size=dp(14),  
            size_hint_y=None,  
            height=dp(55)  
        ))  

    content.add_widget(Label(  
        text=(  
            f"EXTRAS: "  
            f"{self.wides + self.no_balls}"  
            f" (Wd {self.wides}, "  
            f"Nb {self.no_balls})"  
        ),  
        font_size=dp(16),  
        bold=True,  
        size_hint_y=None,  
        height=dp(40)  
    ))  

    content.add_widget(Label(  
        text=f"TOTAL: {self.runs}/{self.wickets}",  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(45)  
    ))  

    content.add_widget(Label(  
        text="🎯 BOWLING",  
        font_size=dp(20),  
        bold=True,  
        size_hint_y=None,  
        height=dp(40)  
    ))  

    for player in self.bowling_players:  

        balls = self.bowl_balls[player]  

        if balls == 0:  
            continue  

        overs = balls // 6  
        remaining = balls % 6  

        runs = self.bowl_runs[player]  
        wickets = self.bowl_wickets[player]  

        economy = (  
            (runs / balls) * 6  
            if balls > 0  
            else 0  
        )  

        content.add_widget(Label(  
            text=(  
                f"{player}\n"  
                f"Overs {overs}.{remaining} | "  
                f"Runs {runs} | "  
                f"Wickets {wickets} | "  
                f"Econ {economy:.2f}"  
            ),  
            font_size=dp(14),  
            size_hint_y=None,  
            height=dp(55)  
        ))  

    scroll.add_widget(content)  

    self.main.add_widget(scroll)  

    # ====================================================  
    # STEP 18 - SHARE SCORECARD BUTTON  
    # ====================================================  

    share = Button(  
        text="📤 SHARE SCORECARD",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    share.bind(  
        on_press=self.share_scorecard  
    )  

    self.main.add_widget(share)  

    back = Button(  
        text="← BACK TO SCORING",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    back.bind(  
        on_press=lambda x:  
        self.return_to_scoring()  
    )  

    self.main.add_widget(back)  

# ========================================================  
# STEP 18 - SHARE SCORECARD  
# ========================================================  

def share_scorecard(self, instance):  

    scorecard_text = (  
        "🏏 CRICKET SCORER\n\n"  
        f"{self.batting_team}: "  
        f"{self.runs}/{self.wickets}\n"  
        f"Overs: "  
        f"{self.balls // 6}."  
        f"{self.balls % 6}\n\n"  
        "🏏 BATTING\n"  
    )  

    # Batting statistics  
    for player in self.batting_players:  

        runs = self.bat_runs.get(player, 0)  
        balls = self.bat_balls.get(player, 0)  
        fours = self.bat_fours.get(player, 0)  
        sixes = self.bat_sixes.get(player, 0)  

        status = ""  

        if player in self.out_players:  
            status = " OUT"  

        scorecard_text += (  
            f"{player}{status}: "  
            f"{runs} ({balls}) "  
            f"4s:{fours} "  
            f"6s:{sixes}\n"  
        )  

    # Extras  
    scorecard_text += (  
        "\nEXTRAS\n"  
        f"Total Extras: "  
        f"{self.wides + self.no_balls}\n"  
        f"Wides: {self.wides}\n"  
        f"No Balls: {self.no_balls}\n\n"  
    )  

    # Bowling statistics  
    scorecard_text += "🎯 BOWLING\n"  

    for player in self.bowling_players:  

        balls = self.bowl_balls.get(player, 0)  

        if balls == 0:  
            continue  

        overs = balls // 6  
        remaining = balls % 6  

        runs = self.bowl_runs.get(player, 0)  
        wickets = self.bowl_wickets.get(player, 0)  

        scorecard_text += (  
            f"{player}: "  
            f"{overs}.{remaining} overs | "  
            f"{runs} runs | "  
            f"{wickets} wickets\n"  
        )  

    scorecard_text += (  
        "\n🏏 CRICKET SCORER"  
    )  

    # ====================================================  
    # ANDROID SHARE  
    # ====================================================  

    try:  

        from jnius import autoclass  

        PythonActivity = autoclass(  
            "org.kivy.android.PythonActivity"  
        )  

        Intent = autoclass(  
            "android.content.Intent"  
        )  

        String = autoclass(  
            "java.lang.String"  
        )  

        intent = Intent(  
            Intent.ACTION_SEND  
        )  

        intent.setType(  
            "text/plain"  
        )  

        intent.putExtra(  
            Intent.EXTRA_TEXT,  
            String(scorecard_text)  
        )  

        activity = (  
            PythonActivity.mActivity  
        )  

        chooser = Intent.createChooser(  
            intent,  
            "Share Scorecard"  
        )  

        activity.startActivity(  
            chooser  
        )  

    except Exception as e:  

        print(  
            "Share Scorecard Error:",  
            e  
        )  

# ========================================================  
# RETURN TO SCORING  
# ========================================================  

def return_to_scoring(self):  

    self.build_screen()  
    self.update_screen()  

# ========================================================  
# END INNINGS  
# ========================================================  

def end_innings(self):  

    if self.finished:  
        return  

    self.finished = True  

    if self.innings_number == 1:  

        self.manager.first_team = (  
            self.batting_team  
        )  

        self.manager.first_score = self.runs  
        self.manager.first_wickets = self.wickets  

        self.manager.second_team = (  
            self.bowling_team  
        )  

        self.manager.first_players = (  
            self.batting_players  
        )  

        self.manager.second_players = (  
            self.bowling_players  
        )  

        self.show_first_innings_result()  

    else:  

        self.manager.second_score = self.runs  
        self.manager.second_wickets = self.wickets  

        margin = (  
            self.manager.first_score -  
            self.runs  
        )  

        self.manager.winner = (  
            self.bowling_team  
        )  

        self.manager.result = (  
            f"Won by {margin} runs"  
        )  

        self.show_result()  

# ========================================================  
# FIRST INNINGS COMPLETE  
# ========================================================  

def show_first_innings_result(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="🏁 1ST INNINGS COMPLETE",  
        font_size=dp(27),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    self.main.add_widget(Label(  
        text=(  
            f"{self.batting_team}\n"  
            f"{self.runs}/{self.wickets}"  
        ),  
        font_size=dp(23)  
    ))  

    scorecard = Button(  
        text="📊 VIEW SCORECARD",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    scorecard.bind(  
        on_press=lambda x:  
        self.show_scorecard()  
    )  

    self.main.add_widget(scorecard)  

    start = Button(  
        text="▶ START SECOND INNINGS",  
        size_hint_y=None,  
        height=dp(60)  
    )  

    start.bind(  
        on_press=self.start_second_innings  
    )  

    self.main.add_widget(start)  

# ========================================================  
# SECOND INNINGS  
# ========================================================  

def start_second_innings(self, instance):  

    target = self.runs + 1  

    selection = self.manager.get_screen(  
        "selection"  
    )  

    selection.batting_team = (  
        self.manager.second_team  
    )  

    selection.bowling_team = (  
        self.manager.first_team  
    )  

    selection.batting_players = (  
        self.manager.second_players  
    )  

    selection.bowling_players = (  
        self.manager.first_players  
    )  

    selection.max_overs = self.max_overs  
    selection.innings_number = 2  
    selection.target = target  
    selection.out_players = []  

    selection.show_striker()  

    self.manager.current = "selection"  

# ========================================================  
# CHASE WIN  
# ========================================================  

def win_by_chase(self):  

    if self.finished:  
        return  

    self.finished = True  

    wickets_left = 10 - self.wickets  

    self.manager.second_score = self.runs  
    self.manager.second_wickets = self.wickets  

    self.manager.winner = (  
        self.batting_team  
    )  

    self.manager.result = (  
        f"Won by {wickets_left} wickets"  
    )  

    self.show_result()  

# ========================================================  
# FINAL RESULT  
# ========================================================  

def show_result(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="🏆 MATCH COMPLETE",  
        font_size=dp(30),  
        bold=True,  
        size_hint_y=None,  
        height=dp(65)  
    ))  

    self.main.add_widget(Label(  
        text=(  
            f"🏆 {self.manager.winner}\n\n"  
            f"{self.manager.result}"  
        ),  
        font_size=dp(23)  
    ))  

    scorecard = Button(  
        text="📊 VIEW SCORECARD",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    scorecard.bind(  
        on_press=lambda x:  
        self.show_scorecard()  
    )  

    self.main.add_widget(scorecard)  

    save = Button(  
        text="💾 SAVE MATCH",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    save.bind(  
        on_press=self.save_match  
    )  

    self.main.add_widget(save)  

# ========================================================  
# SAVE MATCH  
# ========================================================  

def save_match(self, instance):  

    history = load_history()  

    toss = self.manager.get_screen("toss")  

    match = {  
        "date": datetime.now().strftime(  
            "%d-%m-%Y %I:%M %p"  
        ),  
        "team_a": toss.team_a,  
        "team_b": toss.team_b,  
        "overs": self.max_overs,  
        "first_team":  
            self.manager.first_team,  
        "first_score":  
            self.manager.first_score,  
        "first_wickets":  
            self.manager.first_wickets,  
        "second_team":  
            self.manager.second_team,  
        "second_score":  
            self.manager.second_score,  
        "second_wickets":  
            self.manager.second_wickets,  
        "winner":  
            self.manager.winner,  
        "result":  
            self.manager.result  
    }  

    history.append(match)  
    save_history(history)  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="✅ MATCH SAVED!",  
        font_size=dp(30),  
        bold=True  
    ))  

    home = Button(  
        text="🏠 HOME",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    home.bind(  
        on_press=lambda x:  
        setattr(  
            self.manager,  
            "current",  
            "setup"  
        )  
    )  

    self.main.add_widget(home)

============================================================

HISTORY

============================================================

class HistoryScreen(Screen):

def __init__(self, **kwargs):  
    super().__init__(**kwargs)  

    self.main = BoxLayout(  
        orientation="vertical",  
        padding=dp(10),  
        spacing=dp(8)  
    )  

    self.add_widget(self.main)  

def show_history(self):  

    self.main.clear_widgets()  

    self.main.add_widget(Label(  
        text="📚 MATCH HISTORY",  
        font_size=dp(27),  
        bold=True,  
        size_hint_y=None,  
        height=dp(60)  
    ))  

    history = load_history()  

    if not history:  

        self.main.add_widget(  
            Label(text="No saved matches.")  
        )  

    else:  

        scroll = ScrollView()  

        content = GridLayout(  
            cols=1,  
            spacing=dp(10),  
            padding=dp(10),  
            size_hint_y=None  
        )  

        content.bind(  
            minimum_height=content.setter("height")  
        )  

        for match in reversed(history):  

            text = (  
                f"{match['team_a']} vs "  
                f"{match['team_b']}\n\n"  

                f"{match['first_team']}: "  
                f"{match['first_score']}/"  
                f"{match['first_wickets']}\n"  

                f"{match['second_team']}: "  
                f"{match['second_score']}/"  
                f"{match['second_wickets']}\n\n"  

                f"🏆 {match['winner']}\n"  
                f"{match['result']}\n"  
                f"{match['date']}"  
            )  

            content.add_widget(  
                Label(  
                    text=text,  
                    font_size=dp(15),  
                    size_hint_y=None,  
                    height=dp(150)  
                )  
            )  

        scroll.add_widget(content)  
        self.main.add_widget(scroll)  

    home = Button(  
        text="🏠 HOME",  
        size_hint_y=None,  
        height=dp(55)  
    )  

    home.bind(  
        on_press=lambda x:  
        setattr(  
            self.manager,  
            "current",  
            "setup"  
        )  
    )  

    self.main.add_widget(home)

============================================================

APP

============================================================

class CricketScorerApp(App):

def build(self):  

    manager = ScreenManager()  

    manager.add_widget(  
        SetupScreen(name="setup")  
    )  

    manager.add_widget(  
        PlayersScreen(name="players")  
    )  

    manager.add_widget(  
        TossScreen(name="toss")  
    )  

    manager.add_widget(  
        SelectionScreen(name="selection")  
    )  

    manager.add_widget(  
        ScorerScreen(name="scorer")  
    )  

    manager.add_widget(  
        ProfilesScreen(name="profiles")  
    )  

    manager.add_widget(  
        ProfileScreen(name="profile")  
    )  

    manager.add_widget(  
        HistoryScreen(name="history")  
    )  

    return manager

if name == "main":
CricketScorerApp().run()
