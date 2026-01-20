from agents.mage import Mage
import numpy as np
import matplotlib.pyplot as plt
from mesa import Model
from mesa.space import MultiGrid 
from agents.mage_config import HOUSES
import matplotlib.animation as animation

class HogwartsModel(Model):
    def __init__(self, width, height, num_mages):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.events = []
        self.mana_history = []
        self.life_history = []
        self.step_count = 0

        self.mages = Mage.create_agents(model=self, n=num_mages)

        for m in self.mages:
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(m, (x,y))

    def step(self):
        self.mages.shuffle_do("step")

model = HogwartsModel(10,10,100)

house_colors = {
    "Gryffindor": "#740001",  # Dark red
    "Slytherin": "#1A472A",   # Dark green
    "Ravenclaw": "#0E1A40",   # Dark blue
    "Hufflepuff": "#FFDB00"   # Gold
}

fig, ax = plt.subplots(figsize=(8,8))

def update(frame):
    model.step()
    model.step_count += 1
    model.mana_history.append(sum(m.mana for m in model.mages if m.pos is not None))
    model.life_history.append(sum(m.life for m in model.mages if m.pos is not None))
    
    # Evolution every 30 steps
    if model.step_count % 30 == 0 and model.step_count > 0:
        alive_mages = [m for m in model.mages if m.pos is not None]
        if alive_mages:
            parent = model.random.choice(alive_mages)  # or last one, but random for now
            new_mage = Mage(model, model.next_id())
            # 30% chance of random error (big mutation)
            if model.random.random() < 0.3:
                new_mage.aggressiveness = model.random.random()
                new_mage.mana = model.random.randint(5, 15)
                new_mage.life = model.random.randint(5, 15)
                new_mage.range = model.random.randint(1, 3)
                new_mage.speed = model.random.randint(1, 3)
            else:
                new_mage.aggressiveness = max(0, min(1, parent.aggressiveness + model.random.uniform(-0.1, 0.1)))
                new_mage.mana = max(1, parent.mana + model.random.randint(-2, 2))
                new_mage.life = max(1, parent.life + model.random.randint(-2, 2))
                new_mage.range = max(1, parent.range + model.random.randint(-1, 1))
                new_mage.speed = max(1, parent.speed + model.random.randint(-1, 1))
            new_mage.house = parent.house
            new_mage.current_spells = parent.current_spells.copy()
            # Place near parent
            x, y = parent.pos
            nx = x + model.random.randint(-2, 2)
            ny = y + model.random.randint(-2, 2)
            nx = max(0, min(9, nx))
            ny = max(0, min(9, ny))
            model.grid.place_agent(new_mage, (nx, ny))
            model.mages.append(new_mage)
            print(f"Novo mago {new_mage.unique_id} evoluiu de {parent.unique_id} na casa {parent.house}!")
    ax.clear()
    positions = {}
    for m in model.mages:
        if m.pos is not None:
            pos = m.pos
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(m)
    
    for pos, mages in positions.items():
        x, y = pos
        for i, m in enumerate(mages):
            offset_x = (i % 3 - 1) * 0.15
            offset_y = (i // 3 - 1) * 0.15
            color = house_colors.get(m.house, "black")
            ax.scatter(x + offset_x, y + offset_y, color=color, s=150, edgecolors='white', linewidth=2, alpha=0.8)
    
    # Draw events
    for event, pos in model.events:
        x, y = pos
        if event == 'death':
            ax.text(x, y, 'X', fontsize=24, ha='center', va='center', color='red', fontweight='bold')
        elif event == 'learn':
            ax.text(x, y, '+', fontsize=24, ha='center', va='center', color='green', fontweight='bold')
    
    model.events = []  # clear events
    
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 9.5)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_title(f"Posições dos Magos por Casa", fontsize=16, fontweight='bold')
    ax.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=12, markeredgecolor='white', markeredgewidth=2, label=house) for house, color in house_colors.items()], bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12, title="Casas", title_fontsize=14)

ani = animation.FuncAnimation(fig, update, frames=200, interval=1000, repeat=False)
plt.tight_layout()
plt.show()
# After animation, plot statistics
winners = [m for m in model.mages if m.pos is not None]

# House of winners
house_count = {}
for m in winners:
    house_count[m.house] = house_count.get(m.house, 0) + 1

# Spells of winners
spell_count = {}
for m in winners:
    for spell in m.current_spells:
        spell_count[spell] = spell_count.get(spell, 0) + 1

# Plot
fig2, axs = plt.subplots(2, 2, figsize=(12, 10))

# Mana evolution
axs[0,0].plot(model.mana_history, color='blue')
axs[0,0].set_title('Evolução da Mana Total')
axs[0,0].set_xlabel('Passo')
axs[0,0].set_ylabel('Mana Total')

# Life evolution
axs[0,1].plot(model.life_history, color='red')
axs[0,1].set_title('Evolução da Vida Total')
axs[0,1].set_xlabel('Passo')
axs[0,1].set_ylabel('Vida Total')

# Houses of winners
axs[1,0].bar(house_count.keys(), house_count.values(), color=[house_colors[h] for h in house_count.keys()])
axs[1,0].set_title('Casas dos Vencedores')
axs[1,0].set_ylabel('Número de Magos')

# Spells of winners
axs[1,1].bar(spell_count.keys(), spell_count.values(), color='purple')
axs[1,1].set_title('Feitiços dos Vencedores')
axs[1,1].set_ylabel('Contagem')
axs[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()