from datetime import datetime

def wcadateformat(sd, ed):
    sd = datetime.strptime(sd, '%Y-%m-%d')
    ed = datetime.strptime(ed, '%Y-%m-%d')
    if sd == ed:
        sd = sd.__format__('%B %#d')
        return sd
    else:
        if sd.__format__('%m') == ed.__format__('%m'):
            ed = ed.__format__('%#d')
        else:
            ed = ed.__format__('%B %#d')
        sd = sd.__format__('%B %#d')
        return sd + " - " + ed
