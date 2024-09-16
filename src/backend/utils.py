from datetime import date, datetime


def log_actions(text: str) -> None:
    """
    log actions in text file
    """
    print(text)
    f = open('zlog_actions.txt', 'a+')
    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " | " + text + "\n")
    f.close()

def preprocess_team_text(text_input: str) -> list[list[str, date, int]]:
    """
    pre-process team insertion text into list of list containing each team details

    E.g.
    input:
        "firstTeam 17/05 2
        secondTeam 07/02 2"
    output:
        [['firstTeam', 17/05/2000, 2], ['secondTeam', 07/02/2000, 2]]
    """
    output = []
    preprocess_text = text_input.split()
    if len(preprocess_text) % 3 != 0:
        raise ValueError("team details length is incorrect.")
    for i in range(0, len(preprocess_text), 3):
        print(i)
        team_name = preprocess_text[i]
        team_date = preprocess_text[i+1].split("/")
        team_grp = preprocess_text[i+2]
        output.append([team_name, 
                       date(day=int(team_date[0]), month=int(team_date[-1]), year=2000),
                       int(team_grp)])
    return output

def preprocess_match_text(text_input: str) -> list[list[str, str, int, int]]:
    """
    pre-process match insertion text into list of list containing each match details

    E.g.
    input:
        "firstTeam secondTeam 0 3
        thirdTeam fourthTeam 1 1"
    output:
        [['firstTeam', 'secondTeam', 0, 3], ['thirdTeam', 'fourthTeam', 1, 1]]
    """
    output = []
    preprocess_text = text_input.split()
    if len(preprocess_text) % 4 != 0:
        raise ValueError("match details length is incorrect.")
    for i in range(0, len(preprocess_text), 4):
        team_one_name = preprocess_text[i]
        team_two_name = preprocess_text[i+1]
        team_one_goal = preprocess_text[i+2]
        team_two_goal = preprocess_text[i+3]
        output.append([team_one_name, team_two_name, int(team_one_goal), int(team_two_goal)])
    return output