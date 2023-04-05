# NeatAlgorithmInSnake
## Description
This is a Python project that uses the NEAT algorithm to teach a snake how to play the game of Snake. 
The project consists of main parts:  
1. snake.py and food.py - a files containing the code for the Snake game. 
2. attributes.py - in this file is the code needed to create the attributes for the snake.
3. config_file.txt - a text file with all the configuration for the algorithm.
4. main.py - a main file containing the code for the NEAT algorithm that teaches the snake how to play.

## Used libraries
1. Pygame
2. Neat
3. Random  

You can install them using: 
Run comend:
```python
pip install -r requirements.txt
```
This will automatically install pygame and neat-python and their dependencies.

## Runing the Project

Simply run the main file.
To run the project, simply run the `neat_snake.py` file. Upon running the program, the NEAT algorithm will begin learning how to play the game of Snake.  
You can modify the learning parameters in the `config-file.txt` file.



## Configuration
- `pop_size` - the size of the population in the NEAT algorithm.
- `fitness_threshold` - the minimum fitness value at which the algorithm will stop learning.
- `activation_default` - the default activation function for neurons.
- `activation_options` - a list of available activation functions.
- `weight_stdev` - the standard deviation of the normal distribution from which connection weights are randomly drawn.
## Conclusion

## Similar works
- [neat-snake](https://github.com/lia-univali/neat-snake)

## Authors
- Kacper Tomczykowski ([Tomczykowski](https://github.com/Tomczykowski))
- Bartosz Pawlak ([Benji08](https://github.com/Benji08))

