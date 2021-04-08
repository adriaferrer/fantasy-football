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


def get_player_name(player_card):
    id_player = str(player_card).find('class="sr-only"')
    name_player = \
    str(player_card)[id_player + 1 + len('class="sr-only"'):id_player + 1 + len('class="sr-only"') + 25].split('<')[
        0]
    return name_player


def get_transaction_cost(player_card):
    id_trans = str(player_card).find('€')
    cost_raw = str(player_card)[id_trans - 15:id_trans]
    cost_number = re.findall(r"\d", cost_raw)
    cost = int(''.join(map(str, cost_number)))

    return cost

def get_buyer_seller(player_card, move):
    if move[2] == "market":
        id_buyer = str(player_card).find('<!-- --><!-- --></a></user-link>')
        buyer = str(player_card)[id_buyer - 20:id_buyer].split('>')[-1]
        seller = "market"
    elif move[2] == "transfers":
        seller_soup = str(player_card)[id_trans - 1000:id_trans + 1000].split('<!-- --><!-- --></a>')
        seller = seller_soup[0].split('>')[-1]

        buyer_soup = str(player_card)[id_trans:id_trans + 1000].split('<!-- --><!-- --></a>')
        if len(buyer_soup) > 1:
            buyer = buyer_soup[1].split('>')[-1]
        else:
            buyer = "mercado"

    return buyer, seller