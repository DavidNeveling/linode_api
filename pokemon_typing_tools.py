from serebii_scraper.data import pokemon_info_dict

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
                  [1,  1,  1,  1,  2,  2,  1,  1,  2,  2, .5,  1,  1,  1, .5,  1,  1],
                  [1,  1, .5, .5,  2,  2, .5,  1, .5,  2, .5,  1,  1,  1, .5,  1, .5],
                  [1,  1,  2,  1,  0,  1,  1,  1,  1,  2, .5, .5,  1,  1, .5,  1,  1],
                  [1,  2,  1,  2,  1, .5,  1,  1,  1,  1,  1,  1, .5,  1,  1,  0, .5],
                  [1,  1,  2,  1,  2,  1,  1,  1, .5, .5,  2,  1,  1, .5,  2,  1, .5],
                  [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1, .5],
                  [1, .5,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  1, .5, .5],
                  [1,  1,  1,  1,  1,  2,  1,  1, .5, .5,  1, .5,  1,  2,  1,  1, .5]]
TYPE_CHART_6_8 = [],  1,  1

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
    pokemon_types = pokemon_info_dict[get_gen_name_from_num(gen_num)][pokemon_name]['Type']
    if len(pokemon_types) == 1:
        pokemon_types.append(None)
    args = [attack_type] + pokemon_types + [gen_num]
    return get_dmg_modifier(*args)

def main():
    print(get_dmg_modifier_for_pokemon('psychic', 'Spiritomb', gen_num=4))

if __name__ == '__main__':
    main()