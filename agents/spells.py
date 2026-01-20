class Spell:
    def __init__(self, name: str, mana: int, damage: int, type: str):
        self.name = name
        self.damage = damage
        self.mana = mana
        self.type = type

    def __repr__(self):
        return f"Spell(name='{self.name}', damage={self.damage}, mana={self.mana}, type='{self.type}')"

available_spells = {
    "Fireball": Spell("Fireball", 5, 5, "fire"),
    "Ice Spike": Spell("Ice Spike", 3, 3, "water"),
    "Lightning Bolt": Spell("Lightning Bolt", 4, 4, "wind"),
    "Water Surge": Spell("Water Surge", 6, 6, "water"),
    "Poison Dart": Spell("Poison Dart", 2, 2, "water"),  
    "Wind Slash": Spell("Wind Slash", 3, 4, "wind"),
    "Shadow Bolt": Spell("Shadow Bolt", 5, 7, "fire"),  
    "Water Blast": Spell("Water Blast", 4, 4, "water"),
    "Fire Storm": Spell("Fire Storm", 7, 8, "fire"),
    "Wind Gust": Spell("Wind Gust", 2, 2, "wind"),
    "Ice Shield": Spell("Ice Shield", 3, 1, "water"),
    "Inferno Blast": Spell("Inferno Blast", 8, 10, "fire"),
    "Frost Nova": Spell("Frost Nova", 5, 6, "water"),
    "Tornado": Spell("Tornado", 7, 9, "wind"),
    "Tsunami": Spell("Tsunami", 9, 11, "water"),
    "Blaze": Spell("Blaze", 4, 5, "fire"),
    "Gale Force": Spell("Gale Force", 6, 7, "wind"),
    "Hydro Cannon": Spell("Hydro Cannon", 6, 8, "water"),
    "Phoenix Fire": Spell("Phoenix Fire", 10, 12, "fire"),
    "Whirlwind": Spell("Whirlwind", 5, 6, "wind"),
    "Ice Age": Spell("Ice Age", 8, 10, "water"),
    "Spark": Spell("Spark", 1, 1, "fire"),
    "Drip": Spell("Drip", 1, 1, "water"),
    "Breeze": Spell("Breeze", 1, 1, "wind"),
    "Ember": Spell("Ember", 2, 2, "fire"),
    "Mist": Spell("Mist", 2, 2, "water"),
    "Gust": Spell("Gust", 2, 2, "wind"),
    "Flame Flicker": Spell("Flame Flicker", 3, 3, "fire"),
    "Splash": Spell("Splash", 3, 3, "water"),
    "Zephyr": Spell("Zephyr", 3, 3, "wind"),
    "Warm Glow": Spell("Warm Glow", 2, 1, "fire"),
}
