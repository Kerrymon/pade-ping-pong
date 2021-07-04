import turtle

from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
import random


class ComportTemporal_Left(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal_Left, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal_Left, self).on_time()
        display_message(self.agent.aid.localname, 'Двигаю левый щит')

        self.y = left_pad.ycor()
        self.y += random.randint(-20, 20)
        left_pad.sety(self.y)
        sc.update()


class AgentLeftPlayer(Agent):

    def __init__(self, aid):
        super(AgentLeftPlayer, self).__init__(aid=aid, debug=True)

        comp_temp_left = ComportTemporal_Left(self, 0.01)
        self.behaviours.append(comp_temp_left)





class ComportTemporal_Right(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal_Right, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal_Right, self).on_time()
        display_message(self.agent.aid.localname, 'Двигаю правый щит')

        self.y = right_pad.ycor()
        self.y += random.randint(-20, 20)
        right_pad.sety(self.y)
        sc.update()


class AgentRightPlayer(Agent):

    def __init__(self, aid):
        super(AgentRightPlayer, self).__init__(aid=aid, debug=False)

        comp_temp_right = ComportTemporal_Right(self, 0.01)
        self.behaviours.append(comp_temp_right)



class ComportTemporal_Ball(TimedBehaviour):

    def __init__(self, agent, time):
        super(ComportTemporal_Ball, self).__init__(agent, time)


    def on_time(self):
        super(ComportTemporal_Ball, self).on_time()
        display_message(self.agent.aid.localname, 'Двигаю шар')


        sc.update()

        left_player = 0
        right_player = 0

        hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
        hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

        # Checking borders
        if hit_ball.ycor() > 280:
            hit_ball.sety(280)
            hit_ball.dy *= -1

        if hit_ball.ycor() < -280:
            hit_ball.sety(-280)
            hit_ball.dy *= -1

        if hit_ball.xcor() > 500:
            hit_ball.goto(0, 0)
            hit_ball.dy *= -1
            left_player += 1
            sketch.clear()
            sketch.write("Left_player : {}    Right_player: {}".format(
                left_player, right_player), align="center",
                font=("Courier", 24, "normal"))

        if hit_ball.xcor() < -500:
            hit_ball.goto(0, 0)
            hit_ball.dy *= -1
            right_player += 1
            sketch.clear()
            sketch.write("Left_player : {}    Right_player: {}".format(
                left_player, right_player), align="center",
                font=("Courier", 24, "normal"))

        # Paddle ball collision

        if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) \
                and (hit_ball.ycor() < right_pad.ycor() + 40 and hit_ball.ycor() > right_pad.ycor() - 40):
            hit_ball.setx(360)
            hit_ball.dx *= -1

        if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) \
                and (hit_ball.ycor() < left_pad.ycor() + 40 and hit_ball.ycor() > left_pad.ycor() - 40):
            hit_ball.setx(-360)
            hit_ball.dx *= -1


class AgentBall(Agent):

    def __init__(self, aid):
        super(AgentBall, self).__init__(aid=aid, debug=False)

        comp_temp_ball = ComportTemporal_Ball(self, 0.01)
        self.behaviours.append(comp_temp_ball)



if __name__ == "__main__":

    # Create screen
    sc = turtle.Screen()
    sc.title("Pong game")
    sc.bgcolor("white")
    sc.setup(width=1000, height=600)

    # Left paddle
    left_pad = turtle.Turtle()
    left_pad.speed(0)
    left_pad.shape("square")
    left_pad.color("black")
    left_pad.shapesize(stretch_wid=6, stretch_len=2)
    left_pad.penup()
    left_pad.goto(-400, 0)

    # Right paddle
    right_pad = turtle.Turtle()
    right_pad.speed(0)
    right_pad.shape("square")
    right_pad.color("black")
    right_pad.shapesize(stretch_wid=6, stretch_len=2)
    right_pad.penup()
    right_pad.goto(400, 0)

    # Ball of circle shape
    hit_ball = turtle.Turtle()
    hit_ball.speed(40)
    hit_ball.shape("circle")
    hit_ball.color("blue")
    hit_ball.penup()
    hit_ball.goto(0, 0)
    hit_ball.dx = 5
    hit_ball.dy = -5

    # Initialize the score
    left_player = 0
    right_player = 0

    # Displays the score
    sketch = turtle.Turtle()
    sketch.speed(0)
    sketch.color("blue")
    sketch.penup()
    sketch.hideturtle()
    sketch.goto(0, 260)
    sketch.write("Left_player : 0    Right_player: 0",
                 align="center", font=("Courier", 24, "normal"))


    agents_per_process = 2
    c = 0
    agents = list()

    for i in range(agents_per_process):

        port = int(argv[1]) + c
        left_player_name = 'left_player_{}@localhost:{}'.format(port, port)
        agent_left = AgentLeftPlayer(AID(name=left_player_name))
        agents.append(agent_left)

        port += 1
        right_player_name = 'right_player_{}@localhost:{}'.format(port, port)
        agent_right = AgentRightPlayer(AID(name=right_player_name))
        agents.append(agent_right)

        port += 1
        ball = 'ball_{}@localhost:{}'.format(port, port)
        agent_ball = AgentBall(AID(name=ball))
        agents.append(agent_ball)
        c += 1000

    start_loop(agents)
