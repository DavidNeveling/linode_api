from serebii_scraper.data import pokemon_info_dict
from collections import defaultdict
from functools import reduce
from tqdm import tqdm
import itertools


TYPE_LIST = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'steel', 'fairy']
TYPE_CHART_1 = [[1,  1,  1,  1,  1, .5,  1,  0,  1,  1,  1,  1,  1,  1,  1],
                [2,  1, .5, .5,  1,  2, .5,  0,  1,  1,  1,  1, .5,  2,  1],
                [1,  2,  1,  1,  1, .5,  2,  1,  1,  1,  2, .5,  1,  1,  1],
                [1,  1,  1, .5, .5, .5,  2, .5,  1,  1,  2,  1,  1,  1,  1],
                [1,  1,  0,  2,  1,  2, .5,  1,  2,  1, .5,  2,  1,  1,  1],
                [1, .5,  2,  1, .5,  1,  2,  1,  2,  1,  1,  1,  1,  2,  1],
                [1, .5, .5,  2,  1,  1,  1, .5, .5,  1,  2,  1,  2,  1,  1],
                [0,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  0,  1,  1],
                [1,  1,  1,  1,  1, .5,  2,  1, .5, .5,  2,  1,  1,  2, .5],
                [1,  1,  1,  1,  2,  2,  1,  1,  2,  2, .5,  1,  1,  1, .5],
                [1,  1, .5, .5,  2,  2, .5,  1, .5,  2, .5,  1,  1,  1, .5],
                [1,  1,  2,  1,  0,  1,  1,  1,  1,  2, .5, .5,  1,  1, .5],
                [1,  2,  1,  2,  1, .5,  1,  1,  1,  1,  1,  1, .5,  1,  1],
                [1,  1,  2,  1,  2,  1,  1,  1,  1, .5,  2,  1,  1, .5,  2],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2]]
TYPE_CHART_2_5 = [[1,  1,  1,  1,  1, .5,  1,  0,  1,  1,  1,  1,  1,  1,  1,  1, .5],
                  [2,  1, .5, .5,  1,  2, .5,  0,  1,  1,  1,  1, .5,  2,  1,  2,  2],
                  [1,  2,  1,  1,  1, .5,  2,  1,  1,  1,  2, .5,  1,  1,  1,  1, .5],
                  [1,  1,  1, .5, .5, .5,  1, .5,  1,  1,  2,  1,  1,  1,  1,  1,  0],
                  [1,  1,  0,  2,  1,  2, .5,  1,  2,  1, .5,  2,  1,  1,  1,  1,  2],
                  [1, .5,  2,  1, .5,  1,  2,  1,  2,  1,  1,  1,  1,  2,  1,  1, .5],
                  [1, .5, .5, .5,  1,  1,  1, .5, .5,  1,  2,  1,  2,  1,  1,  2, .5],
                  [0,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  1, .5, .5],
                  [1,  1,  1,  1,  1, .5,  2,  1, .5, .5,  2,  1,  1,  2, .5,  1,  2],
                  [1,  1,  1,  1,  2,  2,  1,  1,  2, .5, .5,  1,  1,  1, .5,  1,  1],
                  [1,  1, .5, .5,  2,  2, .5,  1, .5,  2, .5,  1,  1,  1, .5,  1, .5],
                  [1,  1,  2,  1,  0,  1,  1,  1,  1,  2, .5, .5,  1,  1, .5,  1,  1],
                  [1,  2,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, .5,  1,  1,  0, .5],
                  [1,  1,  2,  1,  2,  1,  1,  1, .5, .5,  2,  1,  1, .5,  2,  1, .5],
                  [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1, .5],
                  [1, .5,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  1, .5, .5],
                  [1,  1,  1,  1,  1,  2,  1,  1, .5, .5,  1, .5,  1,  2,  1,  1, .5]]
TYPE_CHART_6_8 = []

def get_gen_name_from_num(gen_num):
    if gen_num == 1:
        return 'Gen I'
    elif gen_num == 2:
        return 'Gen II'
    elif gen_num == 3:
        return 'Gen III'
    elif gen_num == 4:
        return 'Gen IV'
    elif gen_num == 5:
        return 'Gen V'
    elif gen_num == 6:
        return 'Gen VI'
    elif gen_num == 7:
        return 'Gen VII'
    elif gen_num == 8:
        return 'Gen VIII'
    elif gen_num == 9:
        return 'Gen IX'
    else:
        raise

def get_pokemon_type(gen_num, name):
    gen_dict = pokemon_info_dict[get_gen_name_from_num(gen_num)]
    if name in gen_dict:
        return gen_dict[name]['Type']
    else:
        return 'Pokemon not Found'

def get_gen_type_chart(gen_num):
    if gen_num == 1:
        return TYPE_CHART_1
    elif gen_num > 1 and gen_num < 6:
        return TYPE_CHART_2_5
    else:
        return TYPE_CHART_6_8

def is_super_effective(attack_type, defense_type1, defense_type2=None, gen_num=8):
    return get_dmg_modifier(attack_type, defense_type1, defense_type2, gen_num) > 1

def get_dmg_modifier(attack_type, defense_type1, defense_type2=None, gen_num=8):
    dmg_modifier = 1
    a_i = TYPE_LIST.index(attack_type)
    d_i = TYPE_LIST.index(defense_type1)
    dmg_modifier *= get_gen_type_chart(gen_num)[a_i][d_i]
    if defense_type2:
        d_i = TYPE_LIST.index(defense_type2)
        dmg_modifier *= get_gen_type_chart(gen_num)[a_i][d_i]
    return dmg_modifier

def is_super_effective_on_pokemon(attack_type, pokemon_name, gen_num=8):
    return get_dmg_modifier_for_pokemon(attack_type, pokemon_name, gen_num) > 1

def get_dmg_modifier_for_pokemon(attack_type, pokemon_name, gen_num=8):
    pokemon_types = pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon_name]['Type'][:]
    if len(pokemon_types) == 1:
        pokemon_types.append(None)
    args = [attack_type] + pokemon_types + [gen_num]
    # print(pokemon_name)
    # print(pokemon_types)
    return get_dmg_modifier(*args)

def get_optimal_team_naive(pokemon_list, gen_num=8):
    if len(pokemon_list) <= 6:
        return pokemon_list
    else:
        possible_teams = list(itertools.combinations(set(pokemon_list), 6))
        optimal_team = None
        optimal_max = -1
        for team in tqdm(possible_teams):
            total_super_effective = 0
            all_team_types = set(reduce(lambda x, y: x + y, [pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon]['Type'] for pokemon in team]))
            # print({pokemon: pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon]['Type'] for pokemon in team})
            for defending_pokemon in pokemon_info_dict[get_gen_name_from_num(gen_num)].keys():
                if defending_pokemon in ['Wormadam', 'Shaymin']:
                    continue
                for attack_type in list(all_team_types):
                    if is_super_effective_on_pokemon(attack_type, defending_pokemon, gen_num):
                        total_super_effective += 1
                        break
            # print(team)
            # print(list(all_team_types))
            # print(total_super_effective)
            if total_super_effective > optimal_max:
                optimal_team = team
                optimal_max = total_super_effective
        return optimal_team

def get_optimal_team(pokemon_list, gen_num=8):
    if len(pokemon_list) <= 6:
        return pokemon_list
    else:
        # possible_teams = list(itertools.combinations(set(pokemon_list), 6))
        optimal_team_types = None
        optimal_max = -1
        all_pokemon_types = [pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon]['Type'] for pokemon in pokemon_list]
        types_2 = set([tuple(sorted(x)) for x in all_pokemon_types if len(x) > 1])
        types_1 = set([x[0] for x in all_pokemon_types if len(x) == 1])
        types_2_list = reduce(lambda x, y: x + y, [types_2_type for types_2_type in types_2])
        viable_single_types = []
        for single_type in types_1:
            if single_type not in types_2_list:
                viable_single_types.append(single_type)
        types_to_check = viable_single_types + list(types_2)
        possible_team_types = list(itertools.combinations(set(types_to_check), 6))
        for all_team_types in tqdm(possible_team_types):
            total_super_effective = 0
            # print({pokemon: pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon]['Type'] for pokemon in team})
            most_pokemon_types = [pokemon_info_dict[get_gen_name_from_num(gen_num)][x]['Type'] for x in pokemon_info_dict[get_gen_name_from_num(gen_num)].keys() if not x in ['Wormadam', 'Shaymin']]
            most_pokemon_types = [[p_type] if isinstance(p_type, str) else list(p_type) for p_type in most_pokemon_types]
            for defending_pokemon in most_pokemon_types:
                for attack_type in reduce(lambda x, y: x + y, [[team_type] if isinstance(team_type, str) else list(team_type) for team_type in all_team_types]):
                    type1 = defending_pokemon[0]
                    type2 = defending_pokemon[1] if len(defending_pokemon) > 1 else None
                    if is_super_effective(attack_type, type1, type2, gen_num):
                        total_super_effective += 1
                        break
                    # if is_super_effective_on_pokemon(attack_type, defending_pokemon, gen_num):
                    #     total_super_effective += 1
                    #     break
            # print(team)
            # print(all_team_types)
            # print(total_super_effective)
            if total_super_effective > optimal_max:
                optimal_team_types = all_team_types
                optimal_max = total_super_effective
            if total_super_effective == optimal_max:
                if len(reduce(lambda x, y: x + y, [[team_type] if isinstance(team_type, str) else list(team_type) for team_type in all_team_types])) > len(reduce(lambda x, y: x + y, [[team_type] if isinstance(team_type, str) else list(team_type) for team_type in optimal_team_types])):
                    optimal_team_types = all_team_types
                    optimal_max = total_super_effective
        return get_possible_teams(optimal_team_types, pokemon_list, gen_num)

def get_possible_teams(team_types, pokemon_list, gen_num=8):
    all_possible_teams = []
    def get_possible_teams_recurse(team_types, pokemon_list, pokemon_sub_list):
        if len(team_types) <= 0:
            all_possible_teams.append(pokemon_sub_list)
            return
        print(team_types)
        print(pokemon_list)
        print(pokemon_sub_list)
        poke_type = [team_types[0]] if isinstance(team_types[0], str) else team_types[0]
        all_pokemon_that_match = [x for x in pokemon_list if set(pokemon_info_dict[get_gen_name_from_num(gen_num)][x]['Type']) == set(poke_type)]
        next_list = [x for x in pokemon_list if not x in all_pokemon_that_match]
        for pokemon in all_pokemon_that_match:
            get_possible_teams_recurse(team_types[1:], next_list, pokemon_sub_list + [pokemon])
    get_possible_teams_recurse(team_types, pokemon_list, [])
    return all_possible_teams
        

def main():
    # print(get_dmg_modifier_for_pokemon('psychic', 'Spiritomb', gen_num=4))
    # print(pokemon_info_dict['Gen IV']['Lucario']['Type'])
    print(get_optimal_team(['Linoone', 'Flareon', 'Vaporeon', 'Jolteon', 'Espeon', 'Umbreon', 'Glaceon', 'Leafeon', 'Granbull', 'Tauros', 'Raticate', 'Wigglytuff', 'Blaziken', 'Typhlosion', 'Charizard', 'Lucario', 'Rampardos', 'Crawdaunt', 'Lumineon', 'Noctowl', 'Dodrio', 'Murkrow', 'Butterfree', 'Illumise', 'Shaymin', 'Banette', 'Heatran', 'Raichu', 'Ampharos', 'Yanmega', 'Muk', 'Sharpedo', 'Infernape', 'Forretress', 'Exeggutor', 'Graveler', 'Salamence'], gen_num=4))
    # print(get_optimal_team(['Linoone', 'Flareon', 'Vaporeon', 'Jolteon', 'Espeon', 'Umbreon', 'Glaceon', 'Leafeon', 'Raticate', 'Wigglytuff', 'Blaziken', 'Charizard', 'Lucario', 'Crawdaunt', 'Sharpedo'], gen_num=4))
if __name__ == '__main__':
    main()