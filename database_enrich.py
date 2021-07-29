import json

with open('database.json', 'r+') as f:
    openings = json.load(f)
    for opening in openings:
        opening['moves'] = '[Event "Opening Theory"]' + '\n'+'[Site "Worldwide"]' +'\n'+'[Date "1992.11.04"]'+'\n'+'[Round "1"]'+'\n'+'[White "White"]'+'\n'+'[Black "Black"]'+'\n'+'[Result "1/2-1/2"]'+'\n'+'\n'+opening['moves']
        opening['pgn'] = opening.pop('moves')
    f.seek(0)
    json.dump(openings, f)
    f.close()
