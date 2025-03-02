#import math
def reward_function(params):

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    SPEED_THRESHOLD = 1
    FAST_SPEED_THRESHOLD = 3
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steps = params['steps']
    progress = params["progress"]

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.8 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1 and all_wheels_on_track:   
        reward = 1
    elif distance_from_center <= marker_2 and all_wheels_on_track:
        reward = 0.7
    elif distance_from_center <= marker_3 and all_wheels_on_track:
        reward = 0.3
    elif all_wheels_on_track:
        reward = 0.1  # likely crashed/ close to off track
    elif distance_from_center <= marker_4:
        return float(1e-3)
    else: # too far from the track
        return float(1e-5)
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 25

     # Penalize reward if the car is steering too much
    if steering > ABS_STEERING_THRESHOLD and distance_from_center >= marker_1:
        reward *= 0.8
        
    # Speed penalty threshold
    if speed < SPEED_THRESHOLD:
        # Penalty
        reward = reward + 0.4
    elif speed < FAST_SPEED_THRESHOLD:
        # High reward
        reward = reward + 1.0
    else:
        reward = reward + 2.0

    '''# Self-motivator: motivating the model to stay on track and get around in as few steps as possible
    if all_wheels_on_track and steps > 0:
        reward = ((progress/steps)*100)+(speed**2)
    
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize if the difference between the track direction and the heading direction of the car is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5'''

    return float(reward)
