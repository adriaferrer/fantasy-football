import regex as re


def PlayerAttributes(player_card):
    # Finds player name
    id_name = player_card.find('class="sr-only"') + len('class="sr-only"')
    name = player_card[id_name + 1: id_name + 20].split('<')[0]

    # Finds Valor de Mercado for the player
    id_vm = player_card.find('Valor de Mercado') + len('Valor de Mercado')
    valor = player_card[id_vm + 2: id_vm + 12]
    number = re.findall(r"\d", valor)
    valor_mercado = int(''.join(map(str, number)))

    # Finds player team
    id_team = player_card.find('aria-label') + len('aria-label')
    team = player_card[id_team + 2: id_team + 20].split('class')[0][:-2]

    # Finds total player points
    # BUG: quan només té 1 punt, no ho troba
    id_points = player_card.find('punto') - 5
    points_raw = player_card[id_points + 1: id_points + 4]
    number = re.findall(r"\d", points_raw)
    points = int(''.join(map(str, number)))

    return [name, team, valor_mercado, points]