import numpy as np

class Game:
    
    def __init__(self, inputs):
        self.game_over = False
        self.parse(inputs)
        self.turn = 0

    def parse(self, inputs):
        self.parse_lawn(inputs[0])
        self.parse_zombies(inputs[1])        
        
    def parse_lawn(self, lawn):
        '''
        convert string into an array that holds information about plants
        ----
        params:
            lawn: list of strings that describes the 'lawn'

        returns:
            None
        '''
        # Parse one line at a time?
        print('parsing the lawn')
        self.lawn = np.array([list(row) for row in lawn])
    
    def parse_zombies(self, zombies):
        '''
        convert list into a numpy array that holds information about zombies
        ----
        params:
            zombies: list of lists that contain integers describing the zombie

        returns:
            None
        '''    
        # we could use a dictionary {zombie_id: int, location: tuple (row,col), hp:int}
        # we could use a numpy array for the zombies with location by row/col and value = hp
        # we could leave as is, and reference it later
        print('parsing zombies')
        self.zombie_waiting_list = zombies
        self.zombies = np.zeros(self.lawn.shape)
        
    def play(self):
        '''
        plays game to completion
        
        '''
        while self.game_over is False:
            self.play_one_turn()

    def play_one_turn(self):
        '''
        plays one turn of the game
        
        '''
        print('Playing turn', self.turn)
        self.move_zombies()
        self.enter_zombies()
        self.plants_shoot()
        self.turn += 1
        print('Turn', self.turn)
        print('Lawn:')
        print(self.lawn)
        print('Zombies:')        
        print(self.zombies)       
            
    def enter_zombies(self):
        '''
        bring zombies onto the board if it's their turn
        '''
        # loop through zombie waiting list
        # if zombie[0] is this turn, move it onto board
        
        # for every zombie in the waiting list
        for zombie in self.zombie_waiting_list:
            # if it's the zombie's turn
            if zombie[0] == self.turn:
                print('Placing zombie', zombie, 'at row', zombie[1], 'on turn', self.turn, 'with', zombie[2], 'hp')
                # the row it should enter in is zombie[1]
                row = zombie[1]
                # place this zombie on the board at row, in the last column.
                # the value we are putting there is the zombie's health
                self.zombies[row, -1] = zombie[2] 
        
        
    def move_zombies(self):
        '''
        moves zombies forward
        '''
        print('Moving Zombies')
        # if the first item in zombie list is the right turn, then put it on the board
        if self.zombies[:, 0].sum() > 0:
            self.game_over = True
        else:
            # shift all zombies to the left one square
            new_board = np.zeros_like(self.zombies)
            new_board[:, :-1] = self.zombies[:, 1:]
            self.zombies = new_board

    
    def plants_shoot(self):
        '''
        makes all plants shoot
        shooting should decrease zombie hp
        'number' shooters go first
        then 'S' shooters, right to left then top to bottom
        
        '''
        print('Plants are shooting')
        self.number_shooters()
        self.s_shooters()
        
    def number_shooters(self):
        # if the row of shooter is row of zombie, then health points decrease by the amount shooter is
        # if shots > zombie hp, then overflow to next zombie
        # get shots per row, and do things to zombies based on that
        for row in range(self.lawn.shape[0]):
            # get number of shots
            # decrement zombie health by number of shots
            self.shots_shots_shots(row)
    
    def shots_shots_shots(self, row):
        '''
        handles shots on a single row.
        ---
        params:
            row: intger specifying row of the lawn numpy array
        '''
        shots = sum([int(item) for item in self.lawn[row] if item.isdigit()])
        print('Firing', shots, 'shots on row', row)
        
        # have we hit any zombies?
        
        while (shots > 0) & (sum(self.zombies[row, :]) > 0):
            # then we need to do shots
            for i, zombie in enumerate(self.zombies[row, :]):
                if zombie <= shots:
                    self.zombies[row, :][i] = 0
                    shots = shots - zombie            
                else:
                    self.zombies[row, :][i] = zombie - shots
                    shots = 0      
    
    def s_shooters(self):
        pass