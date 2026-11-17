import math
import random
import time


class Character:
    """Represents a character"""

    def __init__(self, health=100, max_health=100 , mana=100, max_mana=100, strength=1, defense=1, luck=0, exp=0, progress=0,
                 supplies=None, class_name=None, attacks=None, status=None):
        self.health = health
        self.max_health = max_health
        self.mana = mana
        self.max_mana = max_mana
        self.strength = strength
        self.defense = defense
        self.luck = luck
        self.exp = exp
        self.supplies = supplies
        self.progress = progress
        self.class_name = class_name
        self.attacks = attacks
        self.status = status


# Quality of life controls
def cont():
    input('Press Enter to continue.\n')


def health_square_up(character):
    character.max_health = round(character.max_health)
    if character.health > character.max_health:
        character.health = character.max_health
    character.health = round(character.health)
    if character.health <= 0:
        if "jesus" in character.status:
            character.health = character.max_health//4
            print("You are successfully resurrected. You used your resurrection charge.")
            for i in range(len(character.status)):
                if character.status[i] == "jesus":
                    del character.status[i]
        else:
            print("\n\nGame Over\n\n")
            play_game()


def mana_square_up(character):
    character.max_mana = round(character.max_mana)
    if character.mana > character.max_mana:
        character.mana = character.max_mana


def damage_modifier(character):
    return (character.exp ** .7 // 60) + 1 + character.strength / 10


# supplies
def show_supplies(character):
    for key in character.supplies:
        print(key + ": " + str(character.supplies[key]))
    item = input("To use an item type it's name, otherwise hit Enter to continue.\n")
    if item in character.supplies:
        supplies[item](character)


def add_snack(character):
    character.supplies["snack"] += 1
    print("You added a snack to your supplies\n")


def add_meal(character):
    character.supplies["meal"] += 1
    print("You added a meal to your supplies\n")


def add_mana_potion(character):
    character.supplies["mana potion"] += 1
    print("You added a mana potion to your supplies\n")


def eat_snack(character):
    if character.supplies["snack"] > 0:
        character.health += character.max_health/4
        if character.health > character.max_health:
            character.health = character.max_health
        character.supplies["snack"] -= 1
        print("You feel your health recover slightly.")
    else:
        print("You don't have a snack to eat.")


def eat_meal(character):
    if character.supplies["meal"] > 0:
        character.health += character.max_health/2
        if character.health > character.max_health:
            character.health = character.max_health
        character.supplies["meal"] -= 1
        print("You feel your health recover significantly.")
    else:
        print("You don't have a meal to eat.")


def restore_mana(character):
    if character.supplies["mana potion"] > 0:
        character.mana += character.max_mana/2
        if character.mana > character.max_mana:
            character.mana = character.max_mana
        character.supplies["mana potion"] -= 1
        print("You feel mana flow through you.")
    else:
        print("You don't have a mana potion to drink.")


def cursed_spike(character):
    health = 10
    strength = 1
    character.max_health -= health
    character.strength += 1
    health_square_up(character)
    print("You're max health has been lowered by " + str(health) + " and your strength was increased"
                                                                   " by " + str(strength) + " point(s).\nThis item can"
                                                                                            " be used unlimited times.")


supplies = {"snack": eat_snack, "meal": eat_meal, "mana potion": restore_mana, "cursed spike": cursed_spike}


# COMBAT----------------------------------------------------------------------------------------------------------


def freeze(enemy, character, spell):
    doge_drop = 15
    enemy.doge -= doge_drop
    print(enemy.name + "'s doge chance was lowered by " + str(doge_drop) + " percent!")


def burn(enemy, character, spell):
    if "burned" in enemy.status:
        return
    if random.randrange(0, 2) == 0:
        spell.misc = 5
        enemy.status.append("burned")
        print(enemy.name + " is now burned. They will take " + str(spell.misc) + " damage each turn.")



def seconds(enemy, character, spell):
    seconds_dmg = round(spell.damage * .7)
    if random.randrange(0, 5) == 0:
        print("Enemy was hit an additional time for " + str(seconds_dmg) + " damage!")
        enemy.health -= seconds_dmg
        seconds(enemy, character, spell)


def nothing(enemy, character, spell):
    return


def blind(enemy, character, spell):
    if enemy.acc > 40:
        acc_drop = 15
        enemy.acc -= acc_drop
        print(enemy.name + " acc dropped by " + str(acc_drop))
    else:
        print(enemy.name + " acc couldn't go any lower.")


def heal_f(enemy, character, spell):
    if spell.used > 5:
        overuse = 25
    else:
        overuse = spell.used * 5
    character.health -= overuse
    print("You were healed " + str(-(spell.blood + overuse)) + " health points.")
    spell.used += 1


def mana_f(enemy, character, spell):
    print("You mana recovered 30 points")


def vampire_func(enemy, character, spell):
    print("You absorbed " + str(-spell.blood) + " health from " + enemy.name + ".")


def charmed(enemy, character, spell):
    if "charmed" not in enemy.status:
        enemy.status.append("charmed")
        exp_boost = round(enemy.exp/3)
        print("You will now earn an extra " + str(exp_boost) + " exp points if you defeat this enemy. An enemy can"
                                                               " only be charmed once per fight.")
        enemy.exp += exp_boost
    else:
        print("You have already charmed this enemy, it had no effect.")


def wild(enemy, character, spell):
    attack_power = 3
    chance = 6
    roll = random.randrange(0, chance)
    effects = [charmed, blind, seconds, freeze]
    if roll < len(effects):
        effects[roll](enemy, character, spell)
    if random.randrange(0, 21) == 0:
        print("Enemy has been magically turned into a toy, their attack power now has an average of "
              + str(attack_power) + "points.")
        enemy.damage = attack_power
        enemy.name = "Toy " + enemy.name


def shadow(enemy, character, spell):
    enemy.status.append("shadow")
    print(enemy.name + " was infected with a devouring shadow.")

# ATTACKS
class Spells:
    def __init__(self, name, damage, dmg_rng, acc, mana, blood, special, info, used=0, misc=None):
        self.name = name
        self.damage = damage
        self.dmg_rng = dmg_rng
        self.acc = acc
        self.mana = mana
        self.blood = blood
        self.special = special
        self.info = info
        self.used = used
        self.misc = misc


# Spells
frost = Spells("Frost", 8, 3, 100, 10, 0, freeze, "Chills enemies making them easier to hit.")
fire = Spells("Fire", 12, 4, 100, 12, 0, burn, "Chance to burn enemies, burned enemies take DOT.", misc=5)
hex = Spells("Blood hex", 25, 3, 100, 20, 10, seconds, "Drain 10 health to overpower this attack, may hit additional times.")
punch = Spells("Punch", 5, 0, 100, 0, 6, nothing, "Hurt yourself for 6 health trying to punch things you should not punch.")
thunder = Spells("Thunder", 25, 5, 85, 30, 0, seconds, "Chance to hit a additional times.")
sparks = Spells("Sparks", 8, 3, 95, 10, 0, blind, "Lowers acc of enemy.")
vampire = Spells("Life Suck", 15, 3, 100, 15, -10, vampire_func, "Suck 10 HP from the enemy")
charm = Spells("Charm", 0, 0, 200, 20, 0, charmed, "Charm enemies giving you bonus exp when they die.")
wild_card = Spells("Wild Card", 15, 12, 95, 15, 0, wild, "Does decent damage, can have random effects.")
heal = Spells("Heal", 0, 0, 200, 20, -30, heal_f, "Heal yourself for a decreasing amount of health")
mana = Spells("Mana Heal", 0, 0, 200, -30, 0, mana_f, "Gain back 30 mana")
cast_shadow = Spells("cast shadow", 10, 5, 200, 15, 0, shadow, "Gleefully coat your blade in shadow. On "
                                                               "striking the enemy the shadow sticks to them\n"
                                                               "draining health and strength each turn")

spells = {"frost": frost,
          "fire": fire,
          "blood hex": hex,
          "punch": punch,
          "thunder": thunder,
          "sparks": sparks,
          "drain": vampire,
          "charm": charm,
          "wild card": wild_card,
          "heal": heal,
          "mana heal": mana}


# ATTACKS
class KnightAttacks:
    def __init__(self, name, damage, dmg_rng, acc, mana, blood, special, info, used=0, misc=None):
        self.name = name
        self.damage = damage
        self.dmg_rng = dmg_rng
        self.acc = acc
        self.mana = mana
        self.blood = blood
        self.special = special
        self.info = info
        self.used = used
        self.misc = misc


def cursed(enemy, character, spell):
    if "cursed" not in enemy.status:
        enemy.status.append("cursed")
        spell.misc = 8
        print(enemy.name + " was cursed and will now take " + str(spell.misc) + " damage every turn.")


def keep_going(enemy, character, spell):
    answer = ""
    while answer != "yes" and answer != "no":
        answer = input("Would you like to keep the combo going, it have the same resource count.\n")
        if answer != "yes" and answer != "no":
            "Type yes to keep the combo going and no to stop it."
    if answer == "yes":
        if enemy.health <= 0:
            print("Jeez the thing is already dead, take a breath.")
            cont()
            return
        if spell.mana > character.mana:
            print("You don't have the mana to keep going.")
            return
        enemy.health -= spell.damage
        character.health -= spell.blood
        character.mana -= spell.mana
        print(enemy.name + " was hit again for " + str(round(spell.damage * damage_modifier(character) +
                                                             random.randrange(-spell.dmg_rng, spell.dmg_rng + 1))
                                                       ) + " damage.")
        if character.class_name == "Cursed Knight":
            print("You lost " + str(spell.blood) + " health due to blood magic.")
        health_square_up(character)
        keep_going(enemy, character, spell)
    if answer == "no":
        print("The combo has stopped.")


def poison(enemy, character, spell):
    if "poisoned" not in enemy.status:
        enemy.status.append("poisoned")
        print(enemy.name + " has been poisoned.")
    else:
        print(enemy.name + " has already been poisoned.")


def patient(enemy, character, spell, turns):
    dmg = 2 * turns
    enemy.health -= dmg
    print(enemy.name + " was hit for an additional " + str(dmg) + " damage due to the blade's patience.")


slash = KnightAttacks("slash", 6, 4, 90, 0, 0, nothing, "Swing your blade for a weak, but efficient way to attack.")
strike = KnightAttacks("strike", 12, 3, 100, 0, 10, nothing, "Accurate and reliable attack ")
marksman = KnightAttacks("marksman", 20, 0, 200, 10, 17, nothing, "Always hits, reliable damage.")
curse = KnightAttacks("curse", 0, 0, 100, 0, 20, cursed, "curse the enemy causing DOT", misc=8)
heal_k = KnightAttacks("heal", 0, 0, 200, 0, -45, heal_f, "Heal yourself, the more you do it the less it heals.")
combo = KnightAttacks("barrage", 8, 3, 70, 0, 5, keep_going, "On a successful hit you may keep comboing the enemy.")
night_slash = KnightAttacks("night slash", 25, 5, 100, 0, 20, nothing, "Expend HP to gather energy from the night to"
                                                                       " deal a powerful attack.")
drain_slash = KnightAttacks("drain slash", 12, 5, 75, 0, -10, vampire_func, "Absorb 10HP from the blood of your enemy. "
                                                                            "Only works on enemies that bleed.")
wicked_slice = KnightAttacks("wicked slice", 30, 8, 90, 10, 25, seconds, "Expend 25HP for a powerful slice to your enemies."
                                                                        " Can hit additional times.")
air_slash = KnightAttacks("air slash", 25, 5, 100, 10, 15, nothing, "Expend 15HP to harness a devastating gust of"
                                                                   " power.")
poison_blade = KnightAttacks("poison blade", 10, 5, 95, 0, 15, poison, "Expend 15HP to drip a deadly poison onto your"
                                                                       " blade and attack.")
patient_blade = KnightAttacks("patient blade",10, 0, 100, 0, 10, patient, "Do an additional 2 points of damage for"
                                                                          " every turn that has gone by in the battle"
                                                                          " so far.")
pink_mist = KnightAttacks("pink mist", 12, 3, 95, 0, 12, blind, "Lower enemy acc by filling the air with both of your"
                                                                " vaporized blood")
darkness = KnightAttacks("darkness", 50, 5, 100, 30, 50, nothing, "Expend 50HP to gather immense dark energy from around"
                                                                 " you and blast the enemy into oblivion.")
shadow_blade = KnightAttacks("shadow blade", 15, 5, 100, 0, 20, shadow, "Gleefully coat your blade in shadow. On "
                                                                        "striking the enemy the shadow sticks to them\n"
                                                                        "draining health and strength each turn")
punch = KnightAttacks("Punch", 5, 0, 100, 0, 8, nothing, "Hurt yourself for 6 health trying to punch things you "
                                                         "should not punch.")

k_attacks = {"strike": strike,
             "marksman": marksman,
             "curse": curse,
             "heal": heal_k,
             "combo": combo,
             "night slash": night_slash,
             "drain slash": drain_slash,
             "wicked slice": wicked_slice,
             "air slash": air_slash,
             "poison blade": poison_blade,
             "patient blade": patient_blade,
             "pink mist": pink_mist,
             "darkness": darkness,
             "slash": slash
}


class PalAttacks:
    def __init__(self, name, damage, dmg_rng, acc, mana, blood, special, info, used=0, misc=None):
        self.name = name
        self.damage = damage
        self.dmg_rng = dmg_rng
        self.acc = acc
        self.mana = mana
        self.blood = blood
        self.special = special
        self.info = info
        self.used = used
        self.misc = misc


def defense_up(enemy, character, spell):
    increase = 1
    character.defense += increase
    print("You're defense was increased by " + str(increase) + " point(s)")


def strength_up(enemy, character, spell):
    increase = 1
    character.strength += increase
    print("You're strength was increased by " + str(increase) + " point(s)")


def strength_defense_up(enemy, character, spell):
    strength_up(enemy, character, spell)
    defense_up(enemy, character, spell)


def regenerate(enemy, character, spell):
    regen_amount = 5
    character.status.append("regen")
    spell.misc = regen_amount
    print("You will now regenerate " + str(regen_amount) + " HP every turn.")


def auto_life(enemy, character, spell):
    if "jesus" not in character.status:
        character.status.append("jesus")
        print("You connect with the Goddess of Light, her will can pick you back up should you fall in this battle.")
    else:
        print("Sorry you can only have one resurrection charge at a time.")


def flare(enemy, character, spell):
    if random.randrange(0, 3) == 0:
        burn(enemy, character, spell)
        blind(enemy, character, spell)
    else:
        burn(enemy, character, spell)


shield_bash = PalAttacks("shield bash", 8, 6, 100, 0, 0, nothing, "Charge the enemy with your shield.")
defender = PalAttacks("defender", 0, 0, 200, 10, 0, defense_up, "By taking a defensive stance your defense goes up.")
drain_bash = PalAttacks("drain bash", 10, 3, 100, 10, -15, vampire_func, "An enchantment on your shield absorbs the "
                                                                         "life force of foes.")
power_shift = PalAttacks("power shift", 0, 0, 200, 15, 0, strength_up, "By taking an offensive stance your "
                                                                       "strength goes up.")
phalanx = PalAttacks("phalanx", 0, 0, 200, 40, 0, strength_defense_up, "An intimidating stance that raises both "
                                                                       "strength and defense.")
flash = PalAttacks("flash", 5, 3, 100, 10, 0, blind, "A blinding light radiates from your shield.")
heal_p = PalAttacks("heal", 0, 0, 200, 20, -30, heal_f, "A holy light restores HP, a decreasing amount each time.")

focus = PalAttacks("focus", 0, 0, 200, -30, 0, mana_f, "A holy light restores 30 mana")
shield_shuriken = PalAttacks("shield shuriken", 6, 4, 85, 5, 0, keep_going, "You launch your shield from a "
                                                                            "vulnerable position, but on a\n"
                                                                            "successful hit you may keep comboing "
                                                                            "the enemy.")
blessed_charge = PalAttacks("blessed charge", 30, 15, 90, 10, 10, nothing, "You absorb the light energy around you and "
                                                                           "stampede into the enemy with a holy blast.")
regen = PalAttacks("regen", 0, 0, 200, 25, 0, regenerate, "An aura surrounds you and continuously nurses your battle "
                                                          "wounds.", misc=5)
auto_life = PalAttacks("auto life", 0, 0, 200, 60, 0, auto_life, "The Goddess of Light enchants your body with divine "
                                                                  "energy to resurrect you should you fall in battle.")
holy_flare = PalAttacks("holy flare", 30, 10, 100, 30, 0, flare, "A massive beam of light and fire shoots down from the"
                                                                 " sky to incinerate and sometimes blind your enemies.")
punch_p = PalAttacks("punch", 6, 1, 100, 0, 5, nothing, "Punch the enemy, slightly hurting both of you.")
shadow_bash = PalAttacks("shadow bash", 8, 3, 100, 10, 0, shadow, "Beg forgiveness as you allow shadow to cover your"
                                                                  "shield\n shadow sticks to the enemy draining health"
                                                                  " and strength each turn.")

p_attacks = {"shield bash": shield_bash,
             "defender": defender,
             "drain bash": drain_bash,
             "power shift": power_shift,
             "phalanx": phalanx,
             "flash": flash,
             "heal": heal_p,
             "focus": focus,
             "shield shuriken": shield_shuriken,
             "blessed charge": blessed_charge,
             "regen": regen,
             "auto life": auto_life,
             "holy flare": holy_flare,
             "punch": punch_p
             }


class Enemy:
    def __init__(self, name, health, damage, secondary, doge, acc, exp, status, info, type=None, max_health=None
                 , moves_heal=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.secondary = secondary
        self.doge = doge
        self.acc = acc
        self.exp = exp
        self.status = status
        self.info = info
        self.type = type
        self.max_health = max_health
        self.moves_heal = moves_heal


# boss
def status_clear(character=None, enemy=None):
    enemy.status = []
    print(enemy.name + " healed itself of all status conditions.")


def big_hit(character=None, enemy=None):
    dmg = round(enemy.damage * 1.7) - (character.defense * 2)
    character.health -= dmg
    print("Player was hit extra hard for " + str(dmg) + " points.")


def enemy_heal(character=None, enemy=None):
    heal_amnt = enemy.damage * 2
    enemy.health += heal_amnt
    print(enemy.name + " healed itself for " + str(heal_amnt) + " points.")


boss_moves = [status_clear, big_hit, enemy_heal]
boss_moves_heal = [status_clear, big_hit, enemy_heal]


def boss_fight(character):
    boss = Enemy("Ent", 100, 15, boss_moves, 5, 95, 100, [], "Big bad boss", moves_heal=boss_moves_heal, max_health=100)
    print("The trees behind you groan in anger at your escape. You see a large oak grow misshapen facial features\n"
          "and surround you with it's branches. You have one last fight before you are free, and it won't be easy.")
    battle(character, boss)


# Enemies---------------------------------


# SPIRIT
def leech(character=None, enemy=None):
    dmg = 12 - (character.defense * 2)
    character.health -= dmg
    enemy.health += dmg
    print(enemy.name + " leeched " + str(dmg) + " health from player.")


def earth_bound(character=None, enemy=None):
    enemy.doge = 0
    enemy.acc = 110
    enemy.health += 30
    enemy.max_health += 30
    enemy.info = "The spirit now resembles a zombie, high acc and increased health with low doge chance."
    print("The spirit seems to be taking physical form as decaying flesh replaces translucent skin.\n"
          "It will be much easier to hit now, however it seems to have gained some health and accuracy. ")


spirit_lvl1_moveset = [leech, big_hit, earth_bound]
spirit_lvl1_moveset_heal = [leech, big_hit, earth_bound]


def create_spirit_lvl1():
    return Enemy("Spirit lvl:1", 40, 10, spirit_lvl1_moveset, 25, 75, 10, [],
                 "This spirit seems adept at dodging and has medium strength.\n"
                 "However it's health seems low as does it's accuracy.", moves_heal=spirit_lvl1_moveset_heal,
                 max_health=40)


# Rock Golem

def rock_slide(character, enemy):
    dmg = 25 - (character.defense * 2)
    character.health -= dmg
    print("Surrounding rocks float in the air then pummel you for " + str(dmg) + " damage.")


def sharpen(character, enemy):
    dmg = 5
    enemy.damage += dmg
    print(enemy.name + " sharpens some of it's more deadly rocks. It's damage increased by " + str(dmg) + " points.")


rock_lvl1_moveset = [big_hit, rock_slide, sharpen]
rock_lvl1_moveset_heal = [big_hit, rock_slide, sharpen]


def create_rock_lvl1():
    return Enemy("Rock Golem lvl:1", 60, 8, rock_lvl1_moveset, 0, 100, 10, [],
                 "This creature has more health than average and is accurate.\n"
                 "However it's doge chance is low and its strength is below average.",
                 moves_heal=rock_lvl1_moveset_heal, max_health=60)


# Demon
def banished(character, enemy):
    enemy.health = 0
    print("The underworld pulls harder at the angry essence, unable to maintain it's presence the demon\n"
          "is reduced to a shadow.")


demon_lvl1_moveset = [big_hit, banished, status_clear]
demon_lvl1_moveset_heal = [big_hit, banished, status_clear]


def create_angry_essense_lvl1():
    return Enemy(name="Angry Essence lvl:1",
                 health=25,
                 damage=20,
                 secondary=demon_lvl1_moveset,
                 doge=0,
                 acc=100,
                 exp=10,
                 status=[],
                 info="Simply existing here has brought this creature to the\n"
                 "brink of death. However it hits hard and is accurate.",
                 type="fire",
                 max_health=25,
                 moves_heal=demon_lvl1_moveset_heal)


# MAIN ACTIONS --------------------------------------------------------------------------------
def pick_class(character):
    print("The night sky kisses the tops of an army of trees as they sway in the wind.\n"
          "You wake in the middle of a clearing from the hoot of a Blue Horned Owl.\n"
          "It flies off deeper into the forest.")
    cont()
    print("As you collect yourself, you cannot remember how you got here, let alone…\n"
          "who you are. You survey your surroundings until you spot three freshly cut\n"
          "tree stumps in front of you. Sap bleeds down the sides of the splintered wood.\n"
          "Each stump has a weapon burrowed into the center of it’s tree rings.\n"
          "A Sword. A Shield. A Staff.\n"
          "Each one glows with an aura that beckons you.")
    cont()
    answer = ""
    while answer != "sword" and answer != "shield" and answer != "staff":
        answer = input("Which one will you choose?\n ")
        answer.lower()
        if answer != "sword" and answer != "shield" and answer != "staff":
            print("You must pick either the sword, shield or staff.")
    # Cursed Knight
    if answer == "sword":
        health = 120
        mana = 30
        defense = 2
        character.max_health = health
        character.health = health
        character.max_mana = mana
        character.mana = mana
        character.defense = defense
        character.class_name = "Cursed Knight"
        character.supplies = {"snack": 1, "meal": 1, "cursed spike": 1}
        character.attacks = k_attacks
        character.status = []
        print("You rip the sword out of the stump as a power overtakes you. Your grasp around the handle is\n"
              "perfect as a darkness takes hold. Almost as if it were forged just for you. The power creeps\n"
              "inside you as you become the CURSED KNIGHT")
    # Mage
    elif answer == "staff":
        health = 80
        mana = 120
        defense = 0
        character.max_health = health
        character.health = health
        character.max_mana = mana
        character.mana = mana
        character.defense = defense
        character.class_name = "Mage"
        character.supplies = {"snack": 1, "meal": 1, "mana potion": 1}
        character.attacks = spells
        character.status = []
        print("You lift the wooden staff from the stump as a power overtakes you. Glyphs and gems embroider\n"
              "the wood as it whispers ancient secrets into your mind.A swirl of light and dark wrap around\n"
              "you as you become the MAGE.")
    # Paladin
    elif answer == "shield":
        health = 140
        mana = 60
        defense = 1
        character.max_health = health
        character.health = health
        character.max_mana = mana
        character.mana = mana
        character.defense = defense
        character.class_name = "Paladin"
        character.supplies = {"snack": 1, "meal": 1, "mana potion": 1}
        character.attacks = p_attacks
        character.status = []
        print("You pull the crest of the shield from the stump as a power overtakes you. A massive shield\n"
              "that could protect just as much as it could deal damage to others. A light aura encapsulates\n"
              "you as you pick it up and become the PALADIN.")
    cont()
    print("With your " + answer + " in hand you venture deeper into the dark whispery wood in hopes to find out\n"
                                  "who you are and who you are meant to become…")


def intro(character):
    print("You awake in the woods confused and alone. You seem to be wearing a strange robe and a glowing staff\n"
          "lays on the ground next to you. It seems powerful but also somehow sends dark chills down your spine.\n")
    answer = ""
    while answer != "yes" and answer != "no":
        answer = input("Will you pick up the staff?\n")
        if answer == "yes":
            print("You feel a coldness travel through your hand to your arm and then across your whole body.\n"
                  "A dark and powerful chill takes over making you feel weak. Struggling for breath you fall\n"
                  "to your knees. You can’t seem to let go of the staff as the pain increases. Suddenly you feel\n"
                  "a rush of power emanate through you, it does little to stop the pain though.\n")
            cont()
            print("You're maximum health is reduced by 20 and your maximum mana is increased by 20.\n"
                  "You also gain one strength point making your attacks more powerful.")
            character.max_health -= 20
            health_square_up(character)
            character.max_mana += 20
            mana_square_up(character)
        if answer == "no":
            print("The staff does have a dark aura to it, better leave it untouched. This robe seems to have plenty\n"
                  "magic in it anyways.")


def fight(character):
    enemies[random.randrange(0, 3)](character)


def sleep(character):
    roll = random.randrange(0, 5)
    if roll == 0:
        print("You wake up unrested not even an hour since you have fallen asleep. An enemy has found you.")
        fight(character)
        return
    elif roll == 1:
        print("At the crack of dawn you wake to see an enemy has found you in your sleep. Luckily you are well rested")
        character.health += character.max_health * .75
        health_square_up(character)
        character.mana = character.max_mana
        fight(character)
    else:
        print("You safely sleep through the night. You are well rested")
        character.health += character.max_health * .75
        health_square_up(character)
        character.mana = character.max_mana


def play_game():
    character = Character()
    character.supplies = {"snack": 1, "meal": 1, "mana potion": 1}
    pick_class(character)
    cont()
    print('You can explore forward by typing "explore", summon spirits to fight by typing "fight". Fighting will\n'
          'give you power but you may find enemies simply by exploring. To look in your pack type "supplies" and\n'
          'to look at your stats type stats.\n')
    options = {"explore": roll_for_event,
               "fight": fight,
               "supplies": show_supplies,
               "stats": get_stats,
               "sleep": sleep}
    while character.health > 0 and character.progress < 10:
        answer = ""
        while answer not in options:
            answer = input("Use any of the following commands:\n"
                           "explore\n"
                           "fight\n"
                           "supplies\n"
                           "stats\n"
                           "sleep\n")
            if answer not in options:
                print('"' + answer + '"' + " is not a valid command.")
                answer = ""
        if answer == "explore":
            character.progress += 1
        options[answer](character)
    print("\n\nYou're only a few steps from leaving the forest! CONGRATS!\n\n")
    cont()

    # pre boss
    answer = ""
    while answer != "explore":
        answer = input("Type explore to leave the forest or use any of the following commands:\n"
                       "explore\n"
                       "fight\n"
                       "supplies\n"
                       "stats\n"
                       "sleep\n")
        if answer not in options:
            print('"' + answer + '"' + " is not a valid command.")
            answer = ""
        if answer != "explore":
            options[answer](character)
    boss_fight(character)
    print("It wasn't easy but you defeated the Ent. A caravan is traveling down the road you stumbled onto at the\n"
          "edge of the forest. You have been saved. Unless of course this is a dream and you're still in there...")
    cont()
    play_game()


# EVENTS---------------------------------------------------------------------------------------------------------

# bad events

#1
def soul_suck(character):
    character.health = character.health/4
    character.mana = character.mana/4
    print(soul_suck_stories[random.randrange(0, 2)])
    print("current health: " + str(character.health))
    print("\ncurrent mana: " + str(character.mana))
    print("")


soul_suck_stories = ['You hear a scream from inside your head, quickly it becomes deafening. Collapsing to the floor\n'
                     'you hold your hands to your ears in vain. Cold fingers seem to grasp the inside of your chest.\n'
                     '"You are not getting away from me" shouts the strange voice. They pull tighter. When you seem\n'
                     'on the brink of death the hand releases\n\n'
                     , "The trees around you seem to lean in and the brush gets thicker and thicker by the second.\n"
                       "Concerned about getting stuck you speed up to make it to a clearing. In your hurry an upturned\n"
                       "root grasps your ankle bring you swiftly to the ground. A small foot made from twirling root\n"
                       "walks slowly into your vision. The tree spirit grins and opens it's mouth as if it's about to\n"
                       "speak. Slowly it closes it's mouth again. It suddenly screams coaxing trees to fall down on\n"
                       "you. You black out and awake alone, barely alive.\n\n"]


#2
def raid(character):
    print("In a whirlwind of footsteps and threats cult members raid your camp. They demand a sacrifice to their god.")
    if character.supplies == {"snack": 0, "meal": 0, "mana potion": 0}:
        cont()
        print("It seems you have nothing to give, luckily they also accept blood offerings.\n"
              "A steel dagger moves quickly into your side. It begins to glow red as they pull it out of you.\n"
              "The cultists chant in unison and walk away leaving you to cope with your wound.")
        character.health = character.health - character.max_health//4
        print("You took " + str(character.max_health//4) + " damage.")
    else:
        print("Here are all your items.")
        for thing in character.supplies:
            if character.supplies[thing] > 0:
                print(thing + ": " + str(character.supplies[thing]))
        item = " "
        while item not in character.supplies:
            item = input("What item will you give to them?\n")
            if item in character.supplies:
                if character.supplies[item] < 1:
                    print("You don't have any " + item + "s.")
                    item = " "
        character.supplies[item] -= 1
        print("A " + item + " was removed from your pack")


#3
def spirit_one(character):
    spirit = create_spirit_lvl1()
    print("A spirit appears flickering in and out of existence, however the sword fades with it.")
    cont()
    battle(character, spirit)


#4
def rock_spirit_one(character):
    spirit = create_rock_lvl1()
    print("Rocks of various sizes start rolling around towards a central location. The form a 5 foot tall stone golem.")
    cont()
    battle(character, spirit)


#5
def angry_spirit_one(character):
    spirit = create_angry_essense_lvl1()
    print("Something dark and spiteful fills the air. You feels eyes staring into you, they are filled with intense hatred.\n"
          "Wisps of shadow and deep crimson form a 8 foot tall demon already fighting for it's life. It's time on \n"
          "this plane is quickly fleeting and very painful... and it wants to take it out on you.")
    cont()
    battle(character, spirit)


# good events
# 6
def find_snack(character):
    print("While exploring you stumble on an apple, this should give you some much needed health.\n"
          "It seems to be one of the few things in the forest not glowing with an evil aura.\n")
    add_snack(character)

# 7
def find_meal(character):
    print("You find an injured rabbit. With a swift attack you put it out of it's misery and cook it.\n"
          "Looks like you have yourself a nice hearty meal.\n")
    add_meal(character)

# 8
def find_mana(character):
    print("You almost trip on a strange object buried in the brush. It clangs like glass as it rolls into your view.\n"
          "The vial contains a blue liquid, even looking at it fills you with magical fortitude.\n")
    if character.class_name == "Cursed Knight":
        print('You suddenly feel a compulsion, and sense it is coming from the sword. Without thinking you find\n'
              'yourself saying "I have no use for this resource of cowards." You smash the bottle with the sword\n'
              'and as if being drunk through an unseen mouth the liquid gets absorbed by the weapon. You feel a\n'
              'sense of satisfaction come through the sword. The trance finally breaks and you find yourself\n'
              'wondering just who is in charge here. You do however feel stronger... \n'
              'You grip the sword tighter and grin.')
        character.strength += 1
        cont()
        print("Your strength was increased by 1.")
    else:
        add_mana_potion(character)
    cont()


# 9
def fairy(character):
    print("The dark unforgiving woods give way to an oasis of a meadow. Birds chirp, the grass is a vibrant green.\n"
          "A friendly looking fairy waves to you as it swings casually on a hanging leaf. Before you can speak\n"
          "it seems to gather pixie dust from the air creating a swirl of magic around itself and you.\n")
    cont()
    print("Although it does not speak you can hear the fairy ask you a question.")
    request = ""
    while request != "strength" and request != "max health" and request != "max mana":
        request = input('"Which stat would you like me to improve? Type strength, max health, or max mana."\n')
        if request == "strength":
            print("You feel your strength grow by 1 point.")
            character.strength += 1
        elif request == "max health":
            health_up = 20
            print("You feel your body grow more resilient. Your max health is increased by "
                  + str(health_up) + " points.")
            character.max_health += health_up
            character.health += health_up
        elif request == "max mana":
            mana_up = 20
            print("You feel magic flow through you. Your max mana is increased by "
                  + str(mana_up) + " points.")
            character.max_mana += mana_up
            character.mana += mana_up


#10
def find_cave(character):
    answer = ""
    while answer not in ["yes", "no"]:
        answer = input("You find a cave with a dark and powerful aura to it.\n Do you want to enter? yes or no\n")
    if answer == "yes":
        cave_one(character)
    elif answer == "no":
        print("You decide to move on and not risk it.")
        return


events = [soul_suck, raid, spirit_one, rock_spirit_one, angry_spirit_one, find_snack, find_meal, find_mana, fairy,
          find_cave, find_cave]

enemies = [spirit_one, rock_spirit_one, angry_spirit_one]


def get_stats(character, enemy=None):
    if enemy is not None:
        print("Player's stats:\n"
              "Health: " + str(character.health) + "\n"
              "Mana: " + str(character.mana) + "\n"
              "\n"
              "Enemy stat:\n"
              "Health: " + str(enemy.health) + "\n"
              "Info: " + enemy.info + "\n")

    else:
        print("Player's stats:\n"
              "Health: " + str(character.health) + "\n"
              "Max Health: " + str(character.max_health) + "\n"
              "Mana: " + str(character.mana) + "\n"
              "Max Mana: " + str(character.max_mana) + "\n"
              "Strength: " + str(character.strength) + "\n"
              "Exp: " + str(character.exp) + "\n"
              "Progress: " + str(character.progress) + "\n")


# Battle----------------------------------------------------------------------------


def stat_proc_post_enemy(enemy, character):
    if "poisoned" in enemy.status:
        dmg = random.randrange(3, 7)
        enemy.health -= dmg
        if enemy.damage > 5:
            enemy.damage -= 1
        print(enemy.name + " was hurt for " + str(dmg) + " damage by poison. They will also do 1 less damage.")
        cont()


def stat_proc_post_turn(enemy, character, spell):
    if "burned" in enemy.status:
        burn_damage = fire.misc
        enemy.health -= burn_damage
        print(enemy.name + " suffered " + str(burn_damage) + " damage from burn.")
        cont()
    if "cursed" in enemy.status:
        curse_damage = curse.misc
        enemy.health -= curse_damage
        print(enemy.name + " suffered " + str(curse_damage) + " damage from the curse.")
        cont()
    if "regen" in character.status:
        regen_amount = regen.misc
        character.health += regen_amount
        print("Player gained " + str(regen_amount) + " health due to regen.")
        cont()
    if "shadow" in character.status:
        hp = 5
        mp = 5
        character.health -= hp
        character.mana -= mp
        print("Player lost " + str(hp) + " HP and " + str(mp) + " mana from the shadow.")
        cont()
    if "shadow" in enemy.status:
        hp = 5
        dmg_loss = 1
        enemy.health -= hp
        if enemy.damage > 5:
            enemy.damage -= dmg_loss
        print(enemy.name + " lost " + str(hp) + " HP and had it's strength slightly reduced.")
        cont()


def battle(character, enemy):
    character_strength = character.strength
    character_defense = character.defense
    character_max_health = character.max_health
    character_max_mana = character.max_mana
    character.status = []
    turn = 1
    spells = character.attacks
    while enemy.health > 0:
        if turn != 1 or random.randrange(0, 2) == 0:
            # Enemy Turn
            if enemy.acc >= random.randrange(0, 101):
                if enemy.name in ["Shadow Cursed Knight", "Shadow Paladin", "Shadow Mage"]:
                    roll = 0
                else:
                    roll = random.randrange(0, 5)
                if enemy.secondary is not None and roll == 0:
                    if enemy.health >= enemy.max_health * .8:
                        enemy.secondary[random.randrange(0, len(enemy.secondary))](character, enemy)
                    else:
                        enemy.moves_heal[random.randrange(0, len(enemy.moves_heal))](character, enemy)
                else:
                    enemy_damage = enemy.damage + random.randrange(-3, 4) - (character.defense * 2)
                    if enemy_damage < 0:
                        enemy_damage = 0
                    print("The " + enemy.name + " successfully hits you for " + str(enemy_damage) + " damage.")
                    character.health -= enemy_damage
                    health_square_up(character)
                stat_proc_post_enemy(enemy, character)
            else:
                print("the " + enemy.name + " misses it's attack.")
            cont()
            if enemy.health <= 0:
                break

        # Player Turn
        spell = ""
        print("It is your turn to attack now.")
        while spell not in spells:
            spell = input('Type one of your attacks to use it or type "attacks" for a list of available moves.\n'
                          'You may also type "stats" for player and enemy stats.\n')
            if spell == "attacks":
                print("\n")
                for key in spells:
                    print(key + "    Mana: " + str(spells[key].mana) + "     Dmg: " + str(spells[key].damage)
                          + "    Acc: " + str(spells[key].acc) + "    HP Cost: " + str(spells[key].blood) + "\nInfo: " +
                          str(spells[key].info) + "\n")
                print("\n")
            elif spell == "stats":
                get_stats(character, enemy)
            else:
                if spell not in spells:
                    print("You don't have an attack by the name " + spell + ".\n")
        spell = spells[spell]
        if spell.mana > character.mana:
            print("You lack the mana, without time to think you throw a punch.")
            spell = spells["punch"]
        if spell.acc - enemy.doge >= random.randrange(0, 101):
            if spell.damage != 0:
                damage = round(spell.damage * damage_modifier(character)) + random.randrange(-spell.dmg_rng, spell.dmg_rng + 1)
            else:
                damage = 0
            print("You hit the " + enemy.name + " for " + str(damage) + " damage.")
            enemy.health -= damage
            cont()
            character.mana -= spell.mana
            character.health -= spell.blood
            if spell.blood > 0:
                print("Your blood magic cost you " + str(spell.blood) + " health.")
            health_square_up(character)
            mana_square_up(character)
            if spell == patient_blade:
                spell.special(enemy, character, spell, turn)
            else:
                spell.special(enemy, character, spell)
            health_square_up(character)
            mana_square_up(character)
        else:
            print("You missed your attack")
            cont()
        stat_proc_post_turn(enemy, character, spell)
        if character.class_name != "Cursed Knight":
            character.mana += round(character.max_mana // 20)
            mana_square_up(character)
            print("You regain " + str(round(character.max_mana // 20)) + "mana.")
            cont()
        turn += 1
    exp = enemy.exp
    character.strength = character_strength
    character.defense = character_defense
    character.max_health = character_max_health
    character.max_mana = character_max_mana
    character.status = []
    print("You've defeated the " + enemy.name + " and earned " + str(exp) + " exp!")
    character.exp += exp
    print("Exp makes your attacks stronger.")
    cont()
    for key in spells:
        spells[key].used = 0


# First Cave
class Room:
    def __init__(self, enemies, north, south, west, east, treasure, trap, info, name):
        self.enemies = enemies
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.treasure = treasure
        self.trap = trap
        self.info = info
        self.name = name


def cave_boost(character):
    character.health += character.max_health
    character.strength += 1
    print("You notice a small running spring of slightly glowing water, there are carvings of people kneeling to drink\n"
          "the strange water. You feel compelled to do the same. Shortly after the water touches your lips you feel\n"
          "yourself recover from all wounds. You also feel yourself get stronger by 1 point.")
    cont()


def impale(character, enemy):
    dmg = 30 - (character.defense * 2)
    defense_drop = 1
    character.health -= dmg
    character.defense -= 1
    print("Player is hit for " + str(dmg) + " damage. The sharp rocks break some of your armor temporarily lowering"
                                            "you're defense by " + str(defense_drop) + " point(s).")

    
def growth(character, enemy):
    hp = 20
    enemy.health += hp
    print("Sediment begins to drip onto the StalagMIGHT as it regains mass, recovering " + str(hp) + "health.")


stalagMoves = [impale]
stalagMovesHeal = [impale, growth]


def staglagmight(character):
    print("Multiple stalagmites suddenly move across the floor grouping together guided by thick shadow, some of the\n"
          "points suddenly aim at you. You're not sure how this thing is alive, but it doesn't look friendly.")
    stalag = Enemy("StalagMIGHT", 70, 20, stalagMoves, 0, 100, 15, [],"With high defense and attack this sentient"
                                                                      " grouping of stalagmites can be trouble.",
                   max_health=70, moves_heal=stalagMovesHeal)
    cont()
    battle(character, stalag)


# ShadowMirror
def heal_sk(character, enemy):
    amnt = 20
    enemy.health += amnt
    print("The " + enemy.name + " gained " + str(amnt) + " health as it seems to pray to it's weapon.")


def pink_mist_e(character, enemy):
    doge = 15
    ehp = 10
    php = 15
    enemy.doge += doge
    enemy.health -= ehp
    character.health -= php
    print("The air is filled with a pink mist as both of your blood is vaporized.\n"
          "it will be harder to hit the enemy through the mist.")
    cont()
    print("You are hit for " + str(php) + " damage and the enemy is hit for " + str(ehp) +
          " damage from it's blood magic.")


def shadow_blade_e(character, enemy):
    dmg = 25
    ehp = 10
    character.health -= dmg
    character.status.append("shadow")
    print("The enemy coats it's blade in swirling shadows before hitting you.")
    cont()
    print("You are hit for " + str(dmg) + " damage and the " + enemy.name + " took " + str(ehp) + " blood magic damage.\n"
                                                                                                 "The shadow stuck to "
                                                                                                 "you and will drain "
                                                                                                 "you each turn.")


def shadow_slash(character, enemy):
    dmg = 20
    ehp = 10
    character.health -= dmg
    enemy.health -= ehp
    print("You are hit for " + str(dmg) + " damage and the " + enemy.name + "took " + str(ehp) + " blood magic damage.")


shadowKnightMoves = [pink_mist_e, shadow_blade_e, shadow_slash, shadow_slash]
shadowKnightMovesHeal = [heal_sk, pink_mist_e, shadow_blade_e, heal_sk, shadow_slash, shadow_slash]


def shadow_knight(character):
    print("Pebbles and dust gather around a thickening shadow. Slowly the form becomes obvious. A human with a\n"
          "familiar looking sword.")
    mirror = Enemy("Shadow Cursed Knight", 70, 25, shadowKnightMoves, 10, 100, 15, [],
                   "The shadow and earth take the form of a cursed knight.", max_health=70,
                   moves_heal=shadowKnightMovesHeal)
    battle(character, mirror)


#DunBoss

def shadowRock(character):
    dmg = 30
    character.status.append("shadow")
    print("Shadow coats the rock being used as the creatures right hand. You hear screams and pain in the swirling\n"
          "darkness as it hurtles towards you.")
    print("You are hit for " + str(dmg) + " and the shadow stays swirling around you, ready to sap energy.")


dunBossMoves = [shadowRock, sharpen, enemy_heal]


def dunBoss(character):
    print("The room starts to shake as 5 large stones rise into the air. They spread out while one turns around\n"
          "revealing eyes made from black smoke, and a shadow of a mouth. The other four stones position themselves as\n"
          "if they were arms and feet for the unseen body.")
    boss = Enemy("Boss", 120, 22, dunBossMoves, 10, 110, 40, [], "It's mostly empty body makes it hard to hit, while "
                                                                 "it's rock form provides it with \nmassive health "
                                                                 "and attack.")
    battle(character, boss)


dunLobby = Room([], None, None, None, None, None, None, "The entrance of the cave has torches mounted to "
                                                        "the walls. There an opening to what looks like\n"
                                                        "another area to the SOUTH, all other directions"
                                                        " are closed.", "lobby")

dunOne = Room([shadow_knight], None, None, None, None, cave_boost, None, "The small cavern bounces the sound of running"
                                                             " water from wall to wall. \nThere is an opening to"
                                                             "the NORTH, SOUTH, and EAST.", "one")

dunTwo = Room([staglagmight], None, None, None, None, None, None, "There is an opening to the EAST and WEST.",
              "two")
dunThree = Room([shadow_knight], None, None, None, None, None, None, "There is an opening to the NORTH and SOUTH.",
                "three")
dunFour = Room([staglagmight], None, None, None, None, None, None, "There is an opening to the NORTH and EAST.",
               "four")
dunFive = Room([staglagmight, shadow_knight], None, None, None, None, None, None, "There is an opening to the WEST and EAST.",
               "five")
dunSix = Room([staglagmight], None, None, None, None, None, None, "There is an opening to the NORTH and WEST.",
              "six")
dunSeven = Room([staglagmight], None, None, None, None, None, None, "There is an opening to the NORTH and SOUTH.",
                "seven")
dunEight = Room([staglagmight, shadow_knight], None, None, None, None, None, None, "There is an opening to the NORTH, SOUTH"
                                                                                   " and WEST.", "eight")
dunNine = Room([dunBoss], None, None, None, None, None, None, "There is an opening to the SOUTH. This is the end.",
               "nine")


dunLobby.south = dunOne

dunOne.north = dunLobby
dunOne.south = dunThree
dunOne.east = dunTwo

dunTwo.west = dunOne
dunTwo.east = dunEight

dunThree.north = dunOne
dunThree.south = dunFour

dunFour.north = dunThree
dunFour.east = dunFive

dunFive.west = dunFour
dunFive.east = dunSix

dunSix.north = dunSeven
dunSix.west = dunFive

dunSeven.north = dunEight
dunSeven.south = dunSix

dunEight.north = dunNine
dunEight.south = dunSeven
dunEight.west = dunTwo

dunNine.south = dunEight


def cave_one(character):
    print("You walk hesitantly into the cave's entrance, weapon in hand.")
    cont()
    print('To navigate from room to room type the direction you would like to go in. Or you can\n'
          'find out more about the room you are in.')
    cont()
    in_dungeon = True
    current_room = dunLobby
    while in_dungeon:
        if current_room.enemies:
            print("Sounds fill the cavern, you are not alone.")
            current_room.enemies[random.randrange(0, len(current_room.enemies))](character)
            current_room.enemies = []
        if current_room.name == "nine":
            print("You have beaten the enemy! The is shadow seeping into your weapon. You seem to have\n"
                  "gained a new attack.")
            if "cast shadow" in character.attacks or "shadow blade" in character.attacks or "shadow bash" in character.attacks:
                cont()
                print("The shadow seems angry with your weapon, maybe because you already have the attack.\n"
                      "The smokey shadow slowly rises to be level with your face as if making eye contact. Suddenly\n"
                      "the smoke dives into your mouth filling you with pain and power.")
                cont()
                hp = 10
                strngth = 4
                character.max_health -= hp
                health_square_up(character)
                character.strength += strngth
                print("You're max health was decreased by " + str(hp) + " but your strength was increased by " +
                      str(strngth) + " points")
                cont()
                print("With your newfound power you return to the forest.")
                return
            else:
                if character.class_name == "Mage":
                    character.attacks["cast shadow"] = cast_shadow
                elif character.class_name == "Cursed Knight":
                    character.attacks["shadow blade"] = shadow_blade
                elif character.class_name == "Paladin":
                    character.attacks["shadow bash"] = shadow_bash
                cont()
                print("With your newfound attack you escape the dungeon and return to the forest.")
                return
        answer = ""
        while answer not in ["info", "north", "south", "west", "east", "search", "escape", "sleep"]:
            answer = input('Type one of the following commands to continue.\n'
                           'info\nnorth\nsouth\nwest\neast\nsearch\nsleep\nescape\n')
            answer = answer.lower()
        if answer == "info":
            print(current_room.info)
        elif answer == "north":
            if current_room.north is None:
                print("There is nothing in this direction.")
            else:
                current_room = current_room.north
                print("You move north into another room.")
        elif answer == "south":
            if current_room.south is None:
                print("There is nothing in this direction.")
            else:
                current_room = current_room.south
                print("You move south into another room.")
        elif answer == "west":
            if current_room.west is None:
                print("There is nothing in this direction.")
            else:
                current_room = current_room.west
                print("You move west into another room.")
        elif answer == "east":
            if current_room.east is None:
                print("There is nothing in this direction.")
            else:
                current_room = current_room.east
                print("You move east into another room.")
        elif answer == "search":
            if current_room.trap is not None:
                current_room.trap(character)
            elif current_room.treasure is not None:
                current_room.treasure(character)
            else:
                print("There is nothing in the room but rocks.")
        elif answer == "sleep":
            character.health = character.max_health
            character.mana = character.max_mana
            print("You sleep safely thanks to the secluded cavern. You're health and mana are now full.")
        elif answer == "escape":
            print("You tap your feet together in fear and suddenly find yourself back in the woods.")
            return


# roll for event
def roll_for_event(character):
    roll = random.randrange(0, len(events))
    events[roll](character)



play_game()
