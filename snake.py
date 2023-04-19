import time
import turtle
import random
import logging


class SnakeGame:  

    def __init__(self):
        # properties
        self.win = turtle.Screen()
        self.snake_segments = []
        self.change_direction_points = {}
        self.food = turtle.Turtle()
        self.food_segment = False
        logging.basicConfig(filename="mysnake.log",
                    filemode="a"                    
                    )
        
    absolute_to_relative_map = {
        0: {
            "right": "right",
            "left": "left"
        },
        90: {
            "up": "left",
            "down": "right"
        },
        180: {
            "right": "left",
            "left": "right"
        },
        270: {
            "up": "right",
            "down": "left"
        }
    }

    def create_snake(self, segments_count, snake_width=20):
        # add initial segments of the snake
        segment_index = 0
        while segment_index < segments_count:
            self.add_snake_segment(0,segment_index*-20)
            segment_index += 1
        self.win.update()
    
    def add_food(self):        
        self.food.shape("square")
        self.food.color("white")
        self.food.penup()
        max_x = 36
        max_y = 27
        self.food.goto(float(round(random.randint(-1*max_x, max_x)*20)), float(round(random.randint(-1*max_y, max_y)*20)))

    def listener(self):
        # start listening for keyboard events
        self.win.listen()
        possible_key = ["Up", "Down", "Right", "Left"]
        for key in possible_key:
            self.win.onkeypress(lambda key=key: self.move_recorder(key.lower()), key)

    def move_recorder(self, absolute_direction):
        relative_direction = self.relative_direction(self.snake_segments[0],
                                                     absolute_direction)
        if relative_direction:
            
            x, y = map(float, self.snake_segments[0].pos())
            x=round(x,2)
            y=round(y,2)
            
            logging.critical(type(x))
            self.change_direction_points.update({(x, y): relative_direction})
              
    def move_snake(self):
        # windows update
        self.win.update()



        game_is_on = True

        # make the snake move continuously
        while game_is_on: 
            for segment in self.snake_segments:
                logging.critical(segment.pos())           
            segment_index = 0
            while segment_index < len(self.snake_segments):
                logging.critical("----------------------")
                logging.critical("inside move snake fun")
                logging.critical("----------------------")
                logging.critical("len(self.snake_segments)")
                logging.critical(len(self.snake_segments))
                logging.critical("segment_index")
                logging.critical(segment_index)
                              
                self.move_segment(segment_index)
                segment_index += 1
                
            # update windows each 0.1 second
            self.win.update()
            time.sleep(0.05)

    def move_segment(self, segment_index):
        logging.critical("----------------------")
        logging.critical("inside move segment fun")
        logging.critical("----------------------")

        if self.is_food_segment(segment_index):
            return False
        # get segment position
        segment = self.snake_segments[segment_index]   
        
        x, y = map(float, segment.pos())
        x=round(x,2)
        y=round(y,2)
            
        logging.critical(type(x))                
             
        # check if there is any change direction records on the current
        # snake segment position and return segment next direction         
        if (x, y) in self.change_direction_points:
            change_direction = self.change_direction_points[(x, y)]
            
            self.delete_if_last(segment_index, x, y) 

            # change segment direction and exit from function
            eval("self.go_" + change_direction + f"({str(segment_index)})")
            return True             
         
        self.go_forward(segment_index)

    def check_food(self, segment_index): 

        if segment_index != 0:
            logging.critical("checkfoodfalse")
            return False
                      
        if (not self.is_same_position(self.snake_segments[0],
                                      self.food)):
            logging.critical("checkfoodfalse")
            return False

        logging.critical("checkfoodTrue")
        return True
    
    def is_food_segment(self, segment_index):
        logging.critical("----------------------")
        logging.critical("inside is food segment fun")
        logging.critical("----------------------")
        logging.critical("self.change_direction_points")        
        logging.critical(self.change_direction_points.keys())

        if ((segment_index == len(self.snake_segments) - 1) and
                (self.food_segment == True)):
            self.food_segment = False
            return True
        return False
     
    def eat_food(self):     
        heading = self.snake_segments[-1].heading()
        x, y = map(float, self.snake_segments[-1].pos())
        x=round(x,2)
        y=round(y,2)

        
        self.add_snake_segment(x, y, heading = heading)
        self.food_segment = True

    def is_same_position(self, segment_1, segment_2):
        if segment_1.distance(segment_2) < 10:
            return True
        return False

    def delete_if_last(self, segment_index, x, y):
        if segment_index == len(self.snake_segments) - 1:
            del self.change_direction_points[(x, y)]       
    
    def go_forward(self, segment_index):
        self.snake_segments[segment_index].forward(20)

        if self.check_food(segment_index):
            self.eat_food()
    
    def go_left(self, segment_index):
        self.snake_segments[segment_index].left(90)
        self.go_forward(segment_index)

    def go_right(self, segment_index):
        self.snake_segments[segment_index].right(90)
        self.go_forward(segment_index) 
 
    def relative_direction(self, segment, absolute_direction):
                
        if (segment.heading() in self.absolute_to_relative_map and
                absolute_direction in self.absolute_to_relative_map[segment.heading()]):
            return self.absolute_to_relative_map[segment.heading()][absolute_direction]
    
    def add_snake_segment(self, x_pose, y_pose, heading=0):
        # add new segment
        snake_segment = turtle.Turtle()
        snake_segment.shape('square')
        snake_segment.color("white")
        snake_segment.penup()
        snake_segment.setpos(float(round(x_pose, 2)), float(round(y_pose, 2)))
        snake_segment.setheading(heading)
        self.snake_segments.append(snake_segment)
   
    def win_set_up(self):
        # setup windows size and bgcolor
        self.win.setup(1440, 1080)
        self.win.bgcolor("black")
        self.win.tracer(0)
        turtle.mode("logo")
        turtle.register_shape("square", ((-10, -10), (-10, 10),
                                         (10, 10), (10, -10)))

    def keep_win_live(self):        
        turtle.exitonclick()



# make turtle upwards
snake = SnakeGame()



snake.win_set_up()
snake.create_snake(4)
snake.add_food()
snake.listener()
snake.move_snake()
snake.keep_win_live()
