from typing import Tuple

from pygame import Vector2

from ...bot import Bot
from ...linear_math import Transform

max_velocity = 200

class ComplicatedBot(Bot):

    def __init__(self, track):
        super().__init__(track)
        self.prev_position = -1
        self.initial_distance = -1

    @property
    def name(self):
        return "ComplicatedBot"

    @property
    def contributor(self):
        return "Nobleo"

    def compute_commands(self, next_waypoint: int, position: Transform, velocity: Vector2) -> Tuple:
        target = self.track.lines[next_waypoint]
        # new target acquired, initialize stuff
        if not(self.prev_position == next_waypoint):
            self.prev_position = next_waypoint
            self.initial_distance = (position.p - target).length()
            if self.initial_distance == 0:
                self.initial_distance = 1
            print("Calcuated initial distance: ", self.initial_distance)
        
        # calculate the target in the frame of the robot
        target = position.inverse() * target
        # calculate the angle to the target
        angle = target.as_polar()[1]

        # calculate the throttle
        current_distance = target.length()
        velocity_factor = (1 - abs(angle) / 180) * (current_distance / self.initial_distance)
        target_velocity = max_velocity * velocity_factor
        if velocity.length() < target_velocity:
            throttle = 1
        else:
            throttle = -1

        # calculate the steering
        if angle > 0:
            return throttle, 1
        else:
            return throttle, -1
