from agents.spells import Spell, available_spells
from agents.mage_config import DEFAULT_MANA, DEFAULT_LIFE, DEFAULT_RANGE, DEFAULT_SPEED, ELEMENTAL_AFFINITY, AVAILABLE_SPELL_NAMES, WEAK_SPELL_NAMES, NORMAL_SPELL_NAMES, HOUSES
from mesa import Agent
import random

class Mage(Agent):
    elemental_affinity: str = ELEMENTAL_AFFINITY
    
    mana: int = DEFAULT_MANA
    life: int = DEFAULT_LIFE
    range: int = DEFAULT_RANGE
    speed: int = DEFAULT_SPEED

    def __init__(self, model):
        super().__init__(model)
        self.current_spells = random.sample(WEAK_SPELL_NAMES, 3)
        self.aggressiveness = random.random()
        self.house = random.choice(HOUSES)

    def move(self):
        possible_moves = []
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed, self.speed + 1):
                if abs(dx) + abs(dy) <= self.speed and (dx, dy) != (0, 0):
                    nx = self.pos[0] + dx
                    ny = self.pos[1] + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        possible_moves.append((nx, ny))
        if possible_moves:
            new_pos = self.random.choice(possible_moves)
            self.model.grid.move_agent(self, new_pos)

    def attack(self):
        possible_targets = []
        for dx in range(-self.range, self.range + 1):
            for dy in range(-self.range, self.range + 1):
                if abs(dx) + abs(dy) <= self.range and (dx, dy) != (0, 0):
                    nx = self.pos[0] + dx
                    ny = self.pos[1] + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        cell = self.model.grid.get_cell_list_contents((nx, ny))
                        for a in cell:
                            if isinstance(a, Mage) and a.house != self.house:
                                possible_targets.append(a)
        if not possible_targets:
            return

        target = self.random.choice(possible_targets)
        spell = self.random.choice([available_spells[name] for name in self.current_spells])

        target.life -= spell.damage
        self.mana -= spell.mana

        print(f"{self.unique_id} ({self.house})(-{spell.mana}) lançou {spell.name} em {target.unique_id} ({target.house}) (-{spell.damage} vida).")

        if target.life <= 0:
            print(f"{target.unique_id} morreu!")
            self.model.events.append(('death', target.pos))
            self.model.grid.remove_agent(target)
            target.remove()
            self.replace_spell()

    def study(self):
        available_for_study = [s for s in NORMAL_SPELL_NAMES if s not in self.current_spells]
        if available_for_study:
            old_spell = self.random.choice(self.current_spells)
            new_spell = self.random.choice(available_for_study)
            self.current_spells.remove(old_spell)
            self.current_spells.append(new_spell)
            self.model.events.append(('learn', self.pos))
            print(f"{self.unique_id} estudou e trocou {old_spell} por {new_spell}")

    def replace_spell(self):
        new_spell = self.random.choice(NORMAL_SPELL_NAMES)
        old_spell = self.random.choice(self.current_spells)
        self.current_spells.remove(old_spell)
        self.current_spells.append(new_spell)
        self.model.events.append(('learn', self.pos))
        print(f"{self.unique_id} aprendeu {new_spell} ao matar!")

    def step(self):
        study_chance = 0.2 * (1 - self.aggressiveness)
        if self.random.random() < study_chance:
            self.study()
        else:
            self.move()
            self.attack()
        self.mana += 1
        self.life += 1