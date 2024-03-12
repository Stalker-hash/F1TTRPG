
---

# Racing Simulation for TTRPGs (Early Development Build) Our RPG BOX!BOX!

**Note: This project is in its early development stage and is primarily intended for use in custom tabletop role-playing games (TTRPGs). It is not a professional simulation tool and may not accurately reflect real-world racing dynamics.**

This project is a Python-based racing simulation game designed to facilitate custom tabletop role-playing game scenarios involving races between drivers and teams on various tracks.

## Features

- **Basic Race Simulation**: Simulate races between drivers and teams on different tracks.
- **Initial Lap Time Calculation**: Preliminary lap time calculation based on simplified models.
- **Customizable Data**: Easily customize drivers, teams, cars, and track data using JSON files.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.

### Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Stalker-hash/F1TTRPG.git
```

2. Navigate to the project directory:

```bash
cd F1TTRPG
```

3. Run the main script to start the simulation:

```bash
python main.py
```

Follow the on-screen prompts to navigate through the simulation.

## Customization

## Modules

### `Scripts/models.py`

This module contains the classes that represent the various components of the simulation:

- `Team`: Represents a team participating in the race. Each team has a name, a driver, a state, and a list of cars.
- `Car`: Represents a car in the race. Each car has various attributes such as power, handling, downforce, tyre wear, fuel load, and reliability. It also includes a DRS factor and an ERS.
- `Driver`: Represents a driver in the race. Each driver has various skills such as overtaking, breaking, consistency, adaptability, smoothness, defence, and cornering.
- `Track`: Represents the track on which the race takes place. Each track has a name, length, number of turns, and various factors that affect the race.
- `Tyre`: Represents the tyres of a car. Each tyre has a compound, grip, tyre life, and wear rate.

### `Scripts/helper.py`

This module contains various utility functions for loading JSON data, formatting lap times, and finding the index of a driver or team in a list.

### `Scripts/simulation.py`

This module contains the main logic of the race simulation. It includes functions for simulating a race, checking the reliability of a car, performing a pit stop, and calculating the lap time of a car.

### `Scripts/grid.py`

This module is a helper function that creates `Team`'s, `Car`'s,`Driver`'s and match them.

## Usage

To run the simulation, you need to create a `Track` object and a dictionary of `Team` objects, and then call the `simulate_race` function with these objects and the number of laps. The `simulate_race` function will print the results of each lap and return the final results of the race.

## Future Work

This project will be extended in various ways, such as adding more factors to the simulation (e.g., weather conditions), creating the user interface, or adding the ability to simulate a series of races (i.e., a championship).
We are currently working on a tailor made **RPG** named **BOX!BOX!** Noxire will share the detail's of this project very soon but just you know we are very passionet Motorsports fans.  

## Known Issues and Improvements

- **Limited Simulation Features**: The simulation aspect is very basic and very far away from realism.
- **Spagetthi code**: Re-factoring of the code base will come when I can sort the horror of simulation.
- **User Experience**: Its intented to make a workable ui for this tool.
- **Implement functionality to be actual ttrpg**: I know it is just a sim tool atm but i can assure you i will add the ttrpg elements (even rules!) i think it will come around maybe 0.3.0 updt not sure tho

## On The Way
- Better UI/UX
- Better Tyre Wear
- Better Aero
- Car setups

## Contributing

Contributions are welcome! If you have any ideas, improvements, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
