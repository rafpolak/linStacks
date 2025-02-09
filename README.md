# **GBSET - Grid Balance Simulation-based Experiment Tool**  

![GBSET Main window](https://github.com/user-attachments/assets/ac02e1a5-6820-40da-b0ba-da623f2193cf)  
fig. 1 GBSET Main window

## **Overview**  
GBSET is a simple, easy-to-use simulation tool (fig. 1) for analyzing energy balance in a power grid, incorporating energy storage (BESS) and flexibility services. The application visualizes renewable generation, demand, and battery state, allowing users to test different energy management scenarios.

In a simple yet powerful way, you can modify the behavior of flexibility services or other components. The tool can be expanded with dedicated time-based features, such as load profiles, advanced behavioral logic, or AI-driven decision-making. Potential enhancements include GAN-based learning, reinforcement learning agents, and other adaptive control strategies for more advanced energy management.

At the end of the simulation, the program generates key statistics and presents them through detailed visualizations and charts. The database of data recorded during the experiment is partitioned according to the specific conditions of the test, based on the activation status of various options (fig 2-4).

![GBSET ECDF plots](https://github.com/user-attachments/assets/b9181fc8-75df-4a1d-83ab-4b1a021a9737)  
fig. 2 GBSET ECDF plots


![GBSET Time Average profile](https://github.com/user-attachments/assets/23ab68a7-b8aa-4f40-86ef-4802763955be)  
fig. 3 GBSET Time Average


![GBSET Cost Forecast](https://github.com/user-attachments/assets/ebf07e4c-32ee-43c8-ac5a-9cc62aa3a65f)  
fig. 4 GBSET Cost Forecast


## **Features**  
✅ **Grid balance simulation** – dynamic analysis of energy generation and consumption  
✅ **Battery Energy Storage System (BESS) management** – charge/discharge algorithm  
✅ **Flexibility services** – modify energy demand during specific time periods  
✅ **Real-time visualization** – dynamic graphs displaying power flows and grid balance  
✅ **Simulation summary** – Grid balance ECDF, profile and energy cost analysis  

## **Requirements**  
- Python 3.x  
- Pygame  
- NumPy  
- Matplotlib  

Install dependencies:  
```sh
pip install pygame numpy matplotlib
```

## **How to Run**  
To start the simulation, simply run the script:  
```sh
python GBSET.py
```

## **Simulation Configuration**  
The simulation parameters can be adjusted in the `GBSET.py` script to customize the scenario.

### **Battery Energy Storage System (BESS) Parameters**  
| Parameter           | Description                                       | Default Value |
|---------------------|---------------------------------------------------|---------------|
| `battery_capacity`  | Maximum battery storage capacity (kWh)            | `180`         |
| `charge_rate`       | Charging power (kW per time step)                 | `30`          |
| `discharge_rate`    | Discharging power (kW per time step)              | `35`          |
| `charge_efficiency` | Efficiency of charging (0-1 scale)                | `0.9`         |
| `discharge_efficiency` | Efficiency of discharging (0-1 scale)          | `0.9`         |
| `chrgTresh`         | Grid balance threshold for charging (kW)          | `10`          |
| `dischTresh`        | Grid balance threshold for discharging (kW)       | `-35`         |
| `battery_charge`    | Initial battery charge level (kWh)                | `0`           |
| `charging_locked`   | Prevents charging when enabled                    | `False`       |

### **Grid and Renewable Generation Parameters**  
| Parameter             | Description                                     | Default Value |
|-----------------------|-------------------------------------------------|---------------|
| `base_demand`         | Base grid demand level (kW)                     | `50`          |
| `max_generation`      | Maximum possible renewable generation (kW)      | `130`         |
| `sun_hours`           | Hours of sunlight per day (affects solar gen.)  | `14`          |
| `time_shift`          | Time offset for demand function                 | `7`           |

### **Flexibility Service Parameters**  
| Parameter               | Description                                   | Default Value |
|-------------------------|-----------------------------------------------|---------------|
| `flexChng`              | Demand flexibility change factor              | `0.33`        |
| `flexTime`              | Duration of flexibility service (time steps)  | `12`          |

### **Simulation Timing and Display**  
| Parameter      | Description                                         | Default Value |
|----------------|-----------------------------------------------------|---------------|
| `time_interv`  | Time step in hours                                  | `0.5`         |
| `FPS`          | Frames per second (higher = smoother animation)     | `8`           |
| `max_points`   | Maximum number of time steps shown in graphs        | `7 * 24/t_int`|

### **Time or state-based process config.**  
| Function                         | Description                                           |
|----------------------------------|-------------------------------------------------------|
| renewable_generation_function(t) | Renewable generation (time-function)                  |
| demand_function(t)               | Grid demand (time-function)                           |
| BESS_control()                   | BESS control logic (state-based function)             |
| update_flexibility_service()     | Flexability service (simple or more complex behavior) |

## **How It Works**  
🔴 **Toggle BESS** – Enables/disables battery energy storage (BESS)  
🟠 **Flexibility Service** – Activates demand-side flexibility  

## **Simulation Summary**  
At the end of the simulation, the following plots are generated:  
📈 **ECDF of grid balance** – statistical comparing different energy management scenarios  
📉 **Time Average of grid balance** – evaluating the impact of BESS and flexibility services to base profile  
💰 **Energy cost forecast** – comparing energy costs under different strategies  

## **License**  
This project is licensed under the MIT License.  
