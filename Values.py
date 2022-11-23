"""
The variables and values used for the enemys, and items available in the game


The values from the uppercased variables need to be copied before using them
since otherwise the variable itself is changed

The lowercased variables list the emojis used for the reactions
"""

ENEMYS = {"dragon": {"type": "dragon", "minlevel": 100, "attack": "incinerated", "stats": {"health": 2800, "damagemin": 50, "damagemax": 1000, "coinsmin": 2000, "coinsmax": 4000, "xp": 10000}},
          "minotaur": {"type": "Minotaur", "minlevel": 80, "attack": "charged at", "stats": {"health": 700, "damagemin": 120, "damagemax": 501, "coinsmin": 220, "coinsmax": 220, "xp": 1650}},
          "orc": {"type": "Orc", "minlevel": 60, "attack": "slammed", "stats": {"health": 1000, "damagemin": 189, "damagemax": 214, "coinsmin": 75, "coinsmax": 110, "xp": 1400}},
          "bandit": {"type": "Bandit", "minlevel": 40, "attack": "shanked", "stats": {"health": 350, "damagemin": 82, "damagemax": 91, "coinsmin": 30, "coinsmax": 90, "xp": 1150}},
          "dwarf": {"type": "Dwarf", "minlevel": 25, "attack": "mined", "stats": {"health": 185, "damagemin": 21, "damagemax": 28, "coinsmin": 20, "coinsmax": 28, "xp": 780}},
          "goblin": {"type": "Goblin", "minlevel": 10, "attack": "stabbed", "stats": {"health": 85, "damagemin": 12, "damagemax": 25, "coinsmin": 8, "coinsmax": 12, "xp": 450}},
          "slime": {"type": "Slime", "minlevel": 5, "attack": "sucked", "stats": {"health": 120, "damagemin": 4, "damagemax": 6, "coinsmin": 3, "coinsmax": 4, "xp": 80}},
          "rat": {"type": "Rat", "minlevel": 1, "attack": "bit", "stats": {"health": 50, "damagemin": 2, "damagemax": 5, "coinsmin": 1, "coinsmax": 2, "xp": 20}}}

POTIONS = {"tiny": {"type": "tiny", "effect": " +50 Health ", "cost": 5}, "small": {"type": "small", "effect": " +25% of max Health ", "cost": 8},
           "medium": {"type": "medium", "effect": " +50% of max Health ", "cost": 20}, "large": {"type": "large", "effect": " +75% of max Health ", "cost": 50}, "dragon": {"type": "dragon", "effect": " **Full** Health + Evasion chance", "cost": 100}}

ARMOR = {"🪖": {"type": "helmet", "health": 40, "cost": 200}, "🎽": {"type": "chestplate", "health": 70, "cost": 350},
         "👖": {"type": "leggins", "health": 60, "cost": 300}, "🥾": {"type": "boots", "health": 30, "cost": 150}}

SHOP = {"🧙‍♂️": {"Infinity Gauntlet": {"type": "Infinity Gauntlet", "cost": 1300, "attack": "Endgamed", "damage": 190, "durability": 25},
                 "Holy staff": {"type": "Holy staff", "cost": 400, "attack": "vanquished", "damage": 95, "durability": 15},
                 "spellbook": {"type": "spellbook", "cost": 100, "attack": "flamed", "damage": 28, "durability": 12},
                 "wand": {"type": "wand", "cost": 35, "attack": "tickled", "damage": 20, "durability": 4},
                 "floating flying disk": {"type": "floating flying disk", "cost": 15, "attack": "cut", "damage": 8, "durability": 5},
                 "magic stick": {"type": "magic stick", "cost": 1, "attack": "poked", "damage": 4, "durability": 10}}, "🏹":  {"bazooka": {"type": "bazooka", "cost": 1300, "attack": "gigsploded", "damage": 230, "durability": 25},
                                                                                                                              "fireworks": {"type": "fireworks", "cost": 400, "attack": "bursted", "damage": 120, "durability": 15},
                                                                                                                              "compound bow": {"type": "compound bow", "cost": 100, "attack": "bullseyed", "damage": 35, "durability": 12},
                                                                                                                              "wooden bow": {"type": "wooden bow", "cost": 35, "attack": "tapped", "damage": 25, "durability": 4},
                                                                                                                              "spear": {"type": "spear", "cost": 15, "attack": "pierced", "damage": 10, "durability": 5},
                                                                                                                              "throwing stick": {"type": "throwing stick", "cost": 1, "attack": "poked", "damage": 5, "durability": 10}}, "🗡️": {"warhammer": {"type": "warhammer", "cost": 1300, "attack": "kasmashed", "damage": 230, "durability": 25},
                                                                                                                                                                                                                                                 "mighty sword": {"type": "mighty sword", "cost": 400, "attack": "slashed", "damage": 120, "durability": 15},
                                                                                                                                                                                                                                                 "golden axe": {"type": "golden axe", "cost": 100, "attack": "chopped", "damage": 35, "durability": 12},
                                                                                                                                                                                                                                                 "rusty sword": {"type": "rusty sword", "cost": 35, "attack": "scratched", "damage": 25, "durability": 4},
                                                                                                                                                                                                                                                 "club": {"type": "club", "cost": 15, "attack": "squashed", "damage": 10, "durability": 5},
                                                                                                                                                                                                                                                 "stick": {"type": "stick", "cost": 1, "attack": "poked", "damage": 5, "durability": 10}}
        }


enemyemojis = {"🐀": "rat", "🦠": "slime", "🧟‍♂️": "goblin", "🧝‍♂️": "dwarf",
               "🦹‍♂️": "bandit", "🦧": "orc", "🦬": "minotaur", "🐉": "dragon"}

fightemojis = {"⚔️": "attack", "❤️‍🩹": "heal", "🆘": "retreat"}

classes = {"🗡️": "Melee attacks that always hit for base damage",
           "🏹": "Evasion chance for both attacker and enemy", "🧙‍♂️": "Crit chance for extra damage but lower base damage", }

armoryemojis = {"helmet": "🪖", "chestplate": "🎽", "leggins": "👖", "boots": "🥾"}

shopemojis = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🧉", "🍸", "🍹", "🍾", "🏺"]

healemojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
              "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
