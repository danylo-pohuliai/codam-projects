import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        u_input = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = u_input.split(',')

        if len(parts) != 3:
            print("Invalid syntax")
            continue

        coords = []
        has_error = False
        for p in parts:
            clean_p = p.strip()
            try:
                coords.append(float(clean_p))
            except ValueError as error:
                print(f"Error on parameter '{clean_p}': {error}")
                has_error = True
                break
        if not has_error:
            return (coords[0], coords[1], coords[2])


if __name__ == "__main__":
    print("=== Game Coordinate System ===\nGet a first set of coordinates")
    pos1 = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_center = math.sqrt(pos1[0]**2 + pos1[1]**2 + pos1[2]**2)
    print(f"Distance to center: {round(dist_center, 4)}")

    print("\nGet a second set of coordinates")
    pos2 = get_player_pos()
    posX = pos2[0] - pos1[0]
    posY = pos2[1] - pos1[1]
    posZ = pos2[2] - pos1[2]
    dist = math.sqrt((posX)**2 + (posY)**2 + (posZ)**2)
    print(f"Distance between the 2 sets of coordinates: {round(dist, 4)}")
