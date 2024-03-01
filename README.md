
---

# Racing Simulation for TTRPGs (Early Development Build)

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

### Data Files

- `drivers_data.json`: Contains information about drivers including their skills and teams.
- `teams_data.json`: Defines the teams participating in the races along with their cars.
- `cars_data.json`: Specifies the attributes of the cars used by the teams.
- `tracks_data.json`: Describes the tracks available for racing, including segment details.

Feel free to customize these files according to your preferences.

## Known Issues and Improvements

- **Limited Simulation Features**: The simulation aspect is very basic and very far away from realism.
- **Spagetthi code**: Re-factoring of the code base will come when i can sort the horror of simulation.
- **User Experience**: Its intented to make a workable ui for this tool.
- **Implement funcinalty to be actual ttrpg**: I know it is just a sim tool atm but i can assure you i will add the ttrpg elemts (even rules!) i think it will come around maybe 0.3.0 updt not sure tho

## OTW (version 0.1.3)
- Worknig pitstop system this will work as manual mod and a ai led one (prox 0.1.6)
- Making current tyre system better by 

## Contributing

Contributions are welcome! If you have any ideas, improvements, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
