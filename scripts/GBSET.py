#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Name: <GBSET>
Description: <GBSET - Grid Balance Simulation-based Experiment Tool>
Author: <rafal polak>
Date: <2025.02.07>
GitHub Repository: <https://github.com/rafpolak/linStack>
"""

import pygame
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import defaultdict

# Simulation experiment config.
time_interv = 0.5 # time step
time_clock = 0  # Time clock start

# Battery variables
battery_capacity = 180
charge_rate = 30  # kWh per charge action
discharge_rate = 35  # kWh per discharge action
charge_efficiency = 0.9  # 90% efficiency in charging
discharge_efficiency = 0.9  # 90% efficiency in discharging
dischTresh=-35 # Balande level for discharging
chrgTresh=10 # Balance level for charging
battery_charge = 0  # Initial charge level
charging_locked = False  # Initial charge lock

# Flexability service
flexChng=0.33 # Flex. mod.
flexTime=12 # total time (phase 1+2)
demand_modification = 1.0  # Initial mod.
modification_timer = 0  # Initial timer.

# Grid variables
base_demand = 50  # Base grid demand (kW)
max_generation = 130  # Max renewable generation (kW)
sun_hours = 14 # Sun hours per day
time_shift=7 # Offset for demand function

# Time or state-based functions config.
grid_demand = base_demand  # Initial grid demand (kW)
renewable_generation = max_generation  # Initial renewable generation (kW)
grid_balance = renewable_generation - grid_demand  # Initial Net energy available

def renewable_generation_function(t):
    sun_position = math.sin((math.pi / sun_hours) * t)  # Sinusoidal variation (0 to 1)
    noise_factor = random.uniform(0.8, 1.2)  # Randomness factor for noise
    return max_generation * sun_position * noise_factor if sun_position > 0 else 0  # No generation at night

def demand_function(t):
    profile = math.sin((math.pi / 12) * (t - time_shift)) * random.uniform(0.2, 1.8)  
    return base_demand * demand_modification + profile * base_demand/2.5 if base_demand * demand_modification + profile * base_demand/2.5>0 else 0

def BESS_control():
    if renewable_generation-grid_demand < dischTresh and battery_charge > 0:  # battery should discharge
        return "discharge"
    elif renewable_generation-grid_demand > chrgTresh and battery_charge < battery_capacity:  # Excess energy, battery should charge
        return "charge"
    elif battery_charge > 0:
        return "hold"  # Do nothing
    else:
        return "waiting"

def update_flexibility_service():
    new_modification_timer = modification_timer-time_interv
    if new_modification_timer <= flexTime / 2 and demand_modification == 1 + flexChng:
        new_demand_modification = 1 - flexChng  
    elif new_modification_timer <= 0:
        new_demand_modification = 1.0
    else: new_demand_modification=demand_modification
    return new_modification_timer,new_demand_modification

# Exp. data sets
time_data, generation_data, battery_data, demand_data, balance_data, mag, flex = [], [], [], [], [], [], []

# pygame init
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, GREEN, YELLOW, BLUE, ORANGE, GRAY = (255, 255, 255), (20, 20, 20), (200, 0, 0), (0, 200, 0), (200, 200, 0), (0, 100, 255), (255, 165, 0), (40, 50, 40)
graph_width = WIDTH - 100 # Plot size
graph_height = 250 # Plot size
start_x = 50 # Plot coord.
start_y = HEIGHT - graph_height - 50
FPS = 8  # FPS, more for smoother animation
max_points = int(7*24/time_interv) # Max plot X-axis limit
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Balance Simulation-based Experiment Tool")
font = pygame.font.Font(None, 30)
running = True
button_bess = pygame.Rect(350, 200, 160, 40)  # Toggle BESS
button_flex = pygame.Rect(535, 200, 220, 40)  # Flexibility Service
clock = pygame.time.Clock()

# Main Loop
while running:
    screen.fill(GRAY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if button_bess.collidepoint(event.pos):
                    charging_locked = not charging_locked  
                if button_flex.collidepoint(event.pos) and modification_timer == 0:
                    demand_modification = 1 + flexChng
                    modification_timer = flexTime
    
    renewable_generation = renewable_generation_function(time_clock % 24)  
    grid_demand = demand_function(time_clock % 24)  
    BM_action = BESS_control()
    if BM_action == "charge" and battery_charge < battery_capacity and not charging_locked:
        batt_chn = -charge_rate * charge_efficiency * time_interv
        battery_charge -= batt_chn
    elif BM_action == "discharge" and battery_charge > 0 and not charging_locked:
        batt_chn = discharge_rate * discharge_efficiency * time_interv
        battery_charge -= batt_chn
    else: batt_chn = 0
    grid_balance = renewable_generation - grid_demand + batt_chn  # Net energy available   
    battery_charge = max(0, min(battery_charge, battery_capacity))
    # Flexibility service
    #if time_clock % 24==6 and time_clock%(24*14) < (24*7): # Optional autorun 7days on/off
    #    demand_modification = 1 + flexChng
    #    modification_timer = flexTime
    if modification_timer > 0: 
        modification_timer,demand_modification=update_flexibility_service()
            
    # Draw UI
    text = font.render(f"BESS Energy: {battery_charge:.1f} kWh", True, ORANGE)
    screen.blit(text, (50, 50))
    text = font.render(f"Grid Demand: {grid_demand:.1f} kW", True, YELLOW)
    screen.blit(text, (50, 100))
    text = font.render(f"Renewable Gen.: {renewable_generation:.1f} kW", True, BLUE)
    screen.blit(text, (50, 150))
    text = font.render(f"Grid Balance: {grid_balance:.1f} kW", True, RED if grid_balance < 0 else GREEN)
    screen.blit(text, (50, 200))
    text = font.render(f"BESS Decision: {BM_action.upper()}", True, WHITE)
    screen.blit(text, (350, 50))
    text = font.render(f"Simulation time: {int(time_clock/24)} days", True, WHITE)
    screen.blit(text, (350, 100))
    text = font.render(f"Flexibility service time: {modification_timer:.1f} modifier: {demand_modification:.1f}", True, ORANGE if demand_modification!=1 else WHITE)
    screen.blit(text, (350, 150))
    # Buttons
    bess_color = RED if charging_locked else GREEN
    flex_color = ORANGE if modification_timer > 0 else GREEN
    pygame.draw.rect(screen, bess_color, button_bess)
    pygame.draw.rect(screen, flex_color, button_flex)
    bess_text = font.render("Toggle BESS", True, BLACK)
    flex_text = font.render("Flexibility Service", True, BLACK)
    screen.blit(bess_text, (button_bess.x + 20, button_bess.y + 10))
    screen.blit(flex_text, (button_flex.x + 20, button_flex.y + 10))
    # X~Y Plots
    # Save and Update graph data for multiple variables
    time_data.append(time_clock % 24)  # Time in hours (modulo 24)
    generation_data.append(renewable_generation)
    battery_data.append(battery_charge)
    demand_data.append(grid_demand)
    balance_data.append(grid_balance)
    mag.append(charging_locked)
    flex.append(True if demand_modification!=1 else False)
    # Plot idx and scale
    if len(time_data) > max_points:
        start_index = len(time_data) - max_points
    else:
        start_index = 0
    time_view, generation_view, battery_view, demand_view, balance_view = [data[start_index:] for data in [time_data, generation_data, battery_data, demand_data, balance_data]]
    min_y = min(min(generation_view), min(battery_view), min(demand_view), min(balance_view))
    max_y = max(max(generation_view), max(battery_view), max(demand_view), max(balance_view))
    # Plot Draw
    pygame.draw.rect(screen, BLACK, (start_x, start_y, graph_width, graph_height))
    for i in range(1, len(time_view)):
        x1, x2 = start_x + (i - 1) * (graph_width / max_points), start_x + i * (graph_width / max_points)
        y1_gen, y1_batt, y1_demand, y1_balance = [start_y + (1 - (x - min_y) / (max_y - min_y)) * graph_height for x in [generation_view[i - 1], battery_view[i - 1], demand_view[i - 1], balance_view[i - 1]]]
        y2_gen, y2_batt, y2_demand, y2_balance = [start_y + (1 - (x - min_y) / (max_y - min_y)) * graph_height for x in [generation_view[i], battery_view[i], demand_view[i], balance_view[i]]]
        #Draw lines
        pygame.draw.line(screen, ORANGE, (x1, y1_batt), (x2, y2_batt), 2)    # Battery Charge
        pygame.draw.line(screen, BLUE, (x1, y1_gen), (x2, y2_gen), 2)      # Renewable Generation
        pygame.draw.line(screen, YELLOW, (x1, y1_demand), (x2, y2_demand), 2)  # Grid Demand
        pygame.draw.line(screen, RED, (x1, y1_balance), (x2, y2_balance), 3)   # Grid Balance
    state_var_start_y = start_y + graph_height + 10
    # Refresh
    pygame.display.flip()
    clock.tick(FPS)  # Control the FPS rate
    time_clock += time_interv
pygame.quit()

# Exp. data summary
if time_clock>24:
    mag = np.array(mag, dtype=bool)
    flex = np.array(flex, dtype=bool)
    window_size = int(24/time_interv)
    kernel = np.ones(window_size, dtype=bool)
    convolved = np.convolve(flex.astype(int), kernel, mode='same')
    runmax_flex = convolved > 0 
    balance_data = np.array(balance_data)
    time_data = np.array(time_data)
    idx_ff, idx_ft, idx_tf, idx_tt = (~mag) & (~runmax_flex), (~mag) & runmax_flex, mag & (~runmax_flex), mag & runmax_flex
    balance_ff, balance_ft, balance_tf, balance_tt = balance_data[idx_ff], balance_data[idx_ft], balance_data[idx_tf], balance_data[idx_tt]
    time_ff, time_ft, time_tf, time_tt = time_data[idx_ff], time_data[idx_ft], time_data[idx_tf], time_data[idx_tt]
    
    # Figure 1
    sorted_balance1, sorted_balance2, sorted_balance3, sorted_balance4 = np.sort(balance_tf), np.sort(balance_tt), np.sort(balance_ff), np.sort(balance_ft)
    # Calculate the ECDF values
    ecdf_y1, ecdf_y2, ecdf_y3, ecdf_y4 = [np.arange(1, len(sorted_balance) + 1) / len(sorted_balance) for sorted_balance in [sorted_balance1, sorted_balance2, sorted_balance3, sorted_balance4]]
    # Create the ECDF plot 
    plt.figure(figsize=(8, 6))
    plt.step(sorted_balance1, ecdf_y1, where='post', color='red', label='ECDF of Grid Balance without BESS&FLEX')
    plt.step(sorted_balance2, ecdf_y2, where='post', color='orange', label='ECDF of Grid Balance with FLEX')
    plt.step(sorted_balance3, ecdf_y3, where='post', color='green', label='ECDF of Grid Balance with BESS')
    plt.step(sorted_balance4, ecdf_y4, where='post', color='blue', label='ECDF of Grid Balance with BESS&FLEX')
    plt.xlabel('Grid Balance (kW)')
    plt.ylabel('Cumulative Probability')
    plt.title('Simulation Summary - ECDF of Grid Balance')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Figure 2
    def average_y_per_x(x_values, y_values):
        sum_y = defaultdict(float)
        count_y = defaultdict(int)
        for x, y in zip(x_values, y_values):
            sum_y[x] += y
            count_y[x] += 1
        avg_x = np.array(sorted(sum_y.keys()))
        avg_y = np.array([sum_y[x] / count_y[x] for x in avg_x])
        return avg_x, avg_y
    avg_x1, avg_y1 = average_y_per_x(time_tf, balance_tf)
    avg_x2, avg_y2 = average_y_per_x(time_tt, balance_tt)
    avg_x3, avg_y3 = average_y_per_x(time_ff, balance_ff)
    avg_x4, avg_y4 = average_y_per_x(time_ft, balance_ft)
    plt.figure(figsize=(8, 6))
    plt.plot(avg_x1, avg_y1, label="Grid Balance without BESS&FLEX", color='red', linewidth=2)
    plt.plot(avg_x2, avg_y2, label="Grid Balance with FLEX", color='orange', linewidth=2)
    plt.plot(avg_x3, avg_y3, label="Grid Balance with BESS", color='green', linewidth=2)
    plt.plot(avg_x4, avg_y4, label="Grid Balance with BESS&FLEX", color='blue', linewidth=2)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Grid Balance (kW)')
    plt.title('Averaged Grid Balance Data')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Figure 3
    if avg_y1.size>=24/time_interv:
        high_ep,low_ep=500,500
        min_val = np.min(avg_y1)
        max_val = np.max(avg_y1)
        price_profile = high_ep - ((avg_y1 - min_val) * low_ep) / (max_val - min_val)
        sum_cost_y1 = np.sum(-avg_y1 * price_profile)/1000*time_interv if avg_y1.size>=24/time_interv else 0
        sum_cost_y2 = np.sum(-avg_y2 * price_profile)/1000*time_interv if avg_y2.size>=24/time_interv else 0
        sum_cost_y3 = np.sum(-avg_y3 * price_profile)/1000*time_interv if avg_y3.size>=24/time_interv else 0
        sum_cost_y4 = np.sum(-avg_y4 * price_profile)/1000*time_interv if avg_y4.size>=24/time_interv else 0
        sum_costs = np.array([sum_cost_y1, sum_cost_y2, sum_cost_y3, sum_cost_y4])
        plt.bar(range(1, 5), sum_costs)
        plt.xticks([1, 2, 3, 4], ['no BESS&FLEX', 'FLEX only', 'BESS only', 'BESS&FLEX'])
        plt.ylabel('Daily Energy Costs')
        plt.title('Energy Cost Forecast')
        plt.show()
    print("Need >1 day without BESS&FLEX to create cost profile based on grid balance")

# EOF
