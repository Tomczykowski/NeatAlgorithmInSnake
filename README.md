# NeatAlgorithmInSnake
## Description
This is a Python project that uses the NEAT algorithm to teach a snake how to play the game of Snake. 
The project consists of main parts:  
1. snake.py and food.py - a files containing the code for the Snake game. 
2. attributes.py - in this file is the code needed to create the attributes for the snake.
3. config_file.txt - a text file with all the configuration for the algorithm.
4. main.py - a main file containing the code for the NEAT algorithm that teaches the snake how to play.

## Game
1. Generations 1 to 5  
<img src="https://user-images.githubusercontent.com/45266568/230426793-1ba72b44-d01c-434d-9bfc-afbe14772390.gif" width="300" height="323" />


2. Generations 15 to 20  
<img src="https://user-images.githubusercontent.com/45266568/230427129-8574cde0-9ec8-4edb-8161-16961abcfa32.gif" width="300" height="323" />


3. Generations 50 to 55  
<img src="https://user-images.githubusercontent.com/45266568/230428658-134d8291-bca8-4e0c-ac26-894bed420709.gif" width="300" height="323" />

4. Bigger board  
<img src="https://user-images.githubusercontent.com/45266568/230427201-ce278505-55d1-443d-a005-263d05518898.gif" width="300" height="323" />


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
- `pop_size` - the size of the population in the NEAT algorithm. Now the value is 300. This is to make the population as large as possible with the smooth operation of the algorithm. It also allows you to observe individual individuals.
- `fitness_threshold` - the minimum fitness value at which the algorithm will stop learning. Now the value is 100. This is so that the algorithm does not stop. With a 10x10 board, this is the highest score possible.
- `activation_default` - the default activation function for neurons. Now the value is relu because it is the best feature for games of this type.
- `num_hidden` - the numer of hidden nodes. Now there are 3. Experiments with this parameter have shown that this is the optimal value.
- `num_inputs` - the number of inpyts. Now there are 6 of them:  
Distance to the obstacle in each side (4 attributes)  
Distance to food x and y coordinate (2 attributes)

The rest of the attributes in the config_file have not been changed from the basic ones and are described in the neat documentation.
## Conclusion
Snake for a 10x10 board with the given parameters achieves a maximum score of 28. This is a better result than the average person. A better adjustment of the attributes could improve the results of the algorithm, but you should not overly complicate them because the algorithm will not learn.
The algorithm achieved significantly better results for the attributes given against the snake. For example, the distance from the apple instead of the coordinates of the apple and the coordinates of the head.

## Similar works
- [neat-snake](https://github.com/lia-univali/neat-snake)

## Authors
- Kacper Tomczykowski ([Tomczykowski](https://github.com/Tomczykowski))
- Bartosz Pawlak ([Benji08](https://github.com/Benji08))

