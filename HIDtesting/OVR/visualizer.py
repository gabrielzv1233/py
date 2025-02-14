import openvr
import pygame
import math
import threading
import os

os.system("cls" if os.name == "nt" else "clear")
print("Initializing CLI...")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALE = 100
CIRCLE_RADIUS = 10
TEXT_SIZE = 16
LINE_WIDTH = 1

SHOW_DISTANCE_TEXT = True
SCALING_MODE_AUTO = True
SCALING_TARGET = "space"  # Default to auto and space scaling
DEPTH_SCALING = False  # Disabled by default
DEPTH_MULTIPLIER = 1.5  # Default multiplier for depth scaling
ORIGIN_DEVICE_INDEX = 0  # Default to headset


def map_to_screen_coordinates(position, origin, scale):
    relative_position = (position[0] - origin[0], position[1] - origin[1], position[2] - origin[2])
    return int(SCREEN_WIDTH // 2 + relative_position[0] * scale), int(SCREEN_HEIGHT // 2 - relative_position[1] * scale)


def calculate_distance(position1, position2):
    return math.sqrt(
        (position1[0] - position2[0]) ** 2 +
        (position1[1] - position2[1]) ** 2 +
        (position1[2] - position2[2]) ** 2
    )


def calculate_depth_scale(z_position, centered_depth):
    relative_depth = z_position - centered_depth
    return DEPTH_MULTIPLIER / (relative_depth + 1)


def center_devices(vr_system, device_index):
    global ORIGIN_DEVICE_INDEX
    ORIGIN_DEVICE_INDEX = device_index

    poses = vr_system.getDeviceToAbsoluteTrackingPose(
        openvr.TrackingUniverseStanding,
        0,
        openvr.k_unMaxTrackedDeviceCount
    )

    if poses[device_index].bDeviceIsConnected and poses[device_index].bPoseIsValid:
        matrix = poses[device_index].mDeviceToAbsoluteTracking
        origin = [matrix[0][3], matrix[1][3], matrix[2][3]]
        centered_depth = matrix[2][3]
        return origin, centered_depth
    else:
        print(f"Device {device_index} is not valid or not connected.")
        return [0, 0, 0], 0


def command_window(vr_system, update_origin_callback):
    global SHOW_DISTANCE_TEXT, SCALING_MODE_AUTO, SCALING_TARGET, DEPTH_SCALING, DEPTH_MULTIPLIER, SCREEN_WIDTH, SCREEN_HEIGHT, centered_depth

    os.system("cls" if os.name == "nt" else "clear")
    print("CLI Ready. Type 'Help' or '?' for a list of commands.")
    while True:
        try:
            command = input("> ").strip()
            if not command:
                continue

            command_parts = command.lower().split()
            cmd = command_parts[0]
            args = command_parts[1:]

            if cmd == "toggledistancevalues":
                SHOW_DISTANCE_TEXT = not SHOW_DISTANCE_TEXT
                print(f"Distance values {'enabled' if SHOW_DISTANCE_TEXT else 'disabled'}.")
            elif cmd == "togglescalingmode":
                if len(args) == 2 and args[0].isdigit() and args[1].isdigit():
                    SCREEN_WIDTH = int(args[0])
                    SCREEN_HEIGHT = int(args[1])
                    SCALING_MODE_AUTO = False
                    print(f"Manual scaling set to width={SCREEN_WIDTH}, height={SCREEN_HEIGHT}.")
                elif len(args) == 1 and args[0] in ("all", "space", "icons"):
                    SCALING_MODE_AUTO = True
                    SCALING_TARGET = args[0]
                    print(f"Auto scaling mode enabled for '{SCALING_TARGET}'.")
                else:
                    SCALING_MODE_AUTO = not SCALING_MODE_AUTO
                    SCALING_TARGET = "space" if SCALING_MODE_AUTO else SCALING_TARGET
                    print(f"Scaling mode {'automatic' if SCALING_MODE_AUTO else 'manual'}, target='{SCALING_TARGET}'.")
            elif cmd == "toggledepthscaling":
                if len(args) == 1:
                    multiplier = float(args[0])
                    if multiplier == 0:
                        DEPTH_SCALING = False
                        DEPTH_MULTIPLIER = 1.5
                        print("Depth scaling disabled and objects reset to original scale.")
                    else:
                        DEPTH_SCALING = True
                        DEPTH_MULTIPLIER = multiplier
                        print(f"Depth scaling enabled with multiplier={DEPTH_MULTIPLIER}.")
                else:
                    DEPTH_SCALING = not DEPTH_SCALING
                    if DEPTH_SCALING:
                        print(f"Depth scaling enabled with multiplier={DEPTH_MULTIPLIER}.")
                    else:
                        print("Depth scaling disabled and objects reset to original scale.")
            elif cmd == "centerdevices":
                device_index = int(args[0]) if args else 0
                origin, new_centered_depth = center_devices(vr_system, device_index)
                update_origin_callback(origin)
                centered_depth = new_centered_depth
                print(f"Centered devices to device {device_index}.")
            elif cmd in ("help", "?"):
                if args:
                    specific_command = args[0]
                    if specific_command == "toggledistancevalues":
                        print("ToggleDistanceValues: Toggles the visibility of distance values.")
                    elif specific_command == "togglescalingmode":
                        print(
                            "ToggleScalingMode [width height|all|space|icons]:"
                            " Toggles scaling mode or defines the target for auto scaling.\n"
                            "    - 'all': Both play space and icons scale dynamically.\n"
                            "    - 'space': Only the play space scales dynamically.\n"
                            "    - 'icons': Only icons (circles, text, lines) scale dynamically."
                        )
                    elif specific_command == "toggledepthscaling":
                        print(
                            "ToggleDepthScaling [multiplier]: Toggles scaling of icons based on forward/backward movement.\n"
                            "    - multiplier (optional): Sets the depth multiplier (default is 1.5).\n"
                            "    - 0: Disables depth scaling and resets to original scale."
                        )
                    elif specific_command == "centerdevices":
                        print("CenterDevices [device index]: Centers the display based on the specified device index (default is 0).")
                    elif specific_command == "clearconsole":
                        print("ClearConsole/cls: Clears the command history.")
                    else:
                        print(f"No help available for '{specific_command}'.")
                else:
                    print("Available commands: ToggleDistanceValues, ToggleScalingMode, ToggleDepthScaling, CenterDevices, ClearConsole/cls, Help/?")
            elif cmd in ("clearconsole", "cls"):
                os.system("cls" if os.name == "nt" else "clear")
                print("Console cleared.")
            elif cmd in ("exit", "close"):
                print("Exiting command window.")
                break
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("Exiting command window.")
            break


def render_visualizer():
    global SCALE, SCREEN_WIDTH, SCREEN_HEIGHT, SHOW_DISTANCE_TEXT, ORIGIN_DEVICE_INDEX, SCALING_TARGET, DEPTH_SCALING, centered_depth

    openvr.init(openvr.VRApplication_Scene)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("VR Device Tracking Visualizer")
    clock = pygame.time.Clock()
    origin = [0, 0, 0]
    centered_depth = 0

    try:
        vr_system = openvr.VRSystem()

        origin, centered_depth = center_devices(vr_system, ORIGIN_DEVICE_INDEX)

        threading.Thread(
            target=command_window,
            args=(vr_system, lambda new_origin: origin.__setitem__(slice(None), new_origin)),
            daemon=True,
        ).start()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                    if SCALING_MODE_AUTO:
                        SCALE = SCREEN_WIDTH / 800 * 100

            screen.fill((0, 0, 0))

            icon_scale = SCALE if SCALING_MODE_AUTO and SCALING_TARGET in ("all", "icons") else 100
            space_scale = SCALE if SCALING_MODE_AUTO and SCALING_TARGET in ("all", "space") else 100

            poses = vr_system.getDeviceToAbsoluteTrackingPose(
                openvr.TrackingUniverseStanding,
                0,
                openvr.k_unMaxTrackedDeviceCount
            )

            valid_positions = []

            for device_index in range(openvr.k_unMaxTrackedDeviceCount):
                pose = poses[device_index]

                if pose.bDeviceIsConnected and pose.bPoseIsValid:
                    matrix = pose.mDeviceToAbsoluteTracking
                    position = (matrix[0][3], matrix[1][3], matrix[2][3])

                    screen_position = map_to_screen_coordinates(position, origin, space_scale)

                    depth_scale = calculate_depth_scale(position[2], centered_depth) if DEPTH_SCALING else 1
                    valid_positions.append((screen_position, position, device_index, depth_scale))

            for i in range(len(valid_positions)):
                for j in range(i + 1, len(valid_positions)):
                    pos1, world_pos1, _, _ = valid_positions[i]
                    pos2, world_pos2, _, _ = valid_positions[j]

                    pygame.draw.line(screen, (255, 255, 255), pos1, pos2, LINE_WIDTH)

                    distance = calculate_distance(world_pos1, world_pos2)

                    if SHOW_DISTANCE_TEXT:
                        mid_point = ((pos1[0] + pos2[0]) // 2, (pos1[1] + pos2[1]) // 2)
                        font = pygame.font.SysFont(None, int(TEXT_SIZE * (icon_scale / 100)))
                        distance_text = font.render(f"{distance:.2f}", True, (255, 0, 0))
                        screen.blit(distance_text, mid_point)

            for screen_position, position, device_index, depth_scale in valid_positions:
                adjusted_radius = int(CIRCLE_RADIUS * icon_scale / 100 * depth_scale)
                adjusted_text_size = int(TEXT_SIZE * icon_scale / 100 * depth_scale)

                pygame.draw.circle(screen, (0, 255, 0), screen_position, adjusted_radius)

                font = pygame.font.SysFont(None, adjusted_text_size)
                text_color = (0, 0, 0)
                text = str(device_index)
                text_rect = font.render(text, True, text_color).get_rect(center=screen_position)
                screen.blit(font.render(text, True, text_color), text_rect)

            pygame.display.flip()

            clock.tick(30)
    finally:
        openvr.shutdown()
        pygame.quit()


if __name__ == "__main__":
    render_visualizer()
