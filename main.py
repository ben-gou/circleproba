import numpy as np
import matplotlib.pyplot as plt

#random comment

# Sample 2 random points between 0 and 2 pi
def generate_points(num_points=4):
    p0 = 0
    p1 = np.random.uniform(0, np.pi)
    points = [p0, p1]
    for _ in range(num_points - 2):
        new_point = np.random.uniform(0, 2 * np.pi)
        points.append(new_point)
    points.sort()
    return points


# function to compute maximum angle (radian) betwenn the number of points on the circle
def max_angle(points, printing=True):
    angles = []
    points_angle = []
    N = len(points)
    for i in range(1, N + 1):
        i1 = i
        i2 = (i - 1 + N) % N
        if i2 == 0:
            i2 = N
        p1 = points[i1 - 1]
        p2 = points[i2 - 1]
        angle = (p2 - p1) % (2 * np.pi)
        angles.append(angle)
        points_angle.append((i1 - 1, i2 - 1))
        if printing:
            print(
                f"Angle between point {i1} ({np.degrees(p1):.2f} degrees) and point {i2} ({np.degrees(p2):.2f} degrees): {np.degrees(angle):.2f} degrees"
            )
    max_ang = min(angles)
    # Rotate points so that the largest angle is between the last and first point
    max_index = angles.index(max_ang)
    two_points = points_angle[max_index]
    if printing:
        print(f"Max angle: {np.degrees(max_ang):.2f} degrees between point {two_points[0]} and point {two_points[1]}")
    return max_ang, two_points


def plot(points, max_ang=None, rotated_points=None):
    # plot the points on a circle
    plt.figure(figsize=(6, 6))
    circle = plt.Circle((0, 0), 1, color="lightgray", fill=False)
    if max_ang is None:
        max_ang, rotated_points = max_angle(points)
    elif rotated_points is None:
        _, rotated_points = max_angle(points)
    plt.title(f"Max Angle: {np.degrees(max_ang):.2f} degrees")
    plt.gca().add_artist(circle)
    COLOR = "ro" if max_ang <= np.pi else "bo"
    plt.plot(1, 0, COLOR)  # Center of the circle
    # Circle plot always same aspect ratio
    plt.gca().set_aspect("equal", adjustable="box")
    for point in points:
        x = np.cos(point)
        y = np.sin(point)
        plt.plot(x, y, COLOR)
    # plt.plot(-np.cos(points[0]), -np.sin(points[0]), "go")  # Opposite point
    # draw lines between 1st and last point
    point1 = points[rotated_points[0]]
    point_last = points[rotated_points[-1]]
    plt.plot([0, np.cos(point_last)], [0, np.sin(point_last)], "k--")
    plt.plot([0, np.cos(point1)], [0, np.sin(point1)], "k--")
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.grid()
    plt.show()


def history_plot(history, p_th, N):
    plt.plot(history)
    # plt.axhline(p_th, color="red", linestyle="--", label="Theoretical Probability")
    plt.title("Convergence of Valid Configuration Probability (N=" + str(N) + ")")
    plt.xlabel("Number of Trials")
    plt.ylabel("Estimated Probability")
    plt.legend()
    plt.grid()
    plt.show()


# Generate random points and compute max angle
N_mc = 20000
# N_points = 20
solutions = []
printing_ = False

for N_points in range(3, 18):
    valid_count = 0
    history = []
    for _ in range(N_mc):  # Run multiple times to see different configurations
        points = generate_points(N_points)
        max_ang, rotated_points = max_angle(points, printing=printing_)

        # print(f"Points: {points}")
        if max_ang <= np.pi:
            valid_count += 1
        history.append(valid_count / (len(history) + 1))
        # plot(points, max_ang=max_ang, rotated_points=rotated_points
    print(f"Valid configurations: {valid_count}/{N_mc}, Probability: {valid_count/N_mc}")
    solutions.append((N_points, valid_count / N_mc))


def empirical_probability(solutions):
    plt.plot([s[0] for s in solutions], [s[1] for s in solutions], marker="o")
    plt.title("Probability of Valid Configuration vs Number of Points")
    plt.xscale("linear")
    plt.yscale("log")
    plt.xlabel("Number of Points")
    plt.ylabel("Estimated Probability")
    plt.grid()
    plt.show()

def theoretical_probability(solutions):
    N_points = [s[0] for s in solutions]
    p_th = [ (3/4)*(1/2**(n-2)) for n in N_points]
    plt.plot(N_points, p_th, marker="o", color="red")
    plt.title("Theoretical Probability of Valid Configuration vs Number of Points")
    plt.xscale("linear")
    plt.yscale("log")
    plt.xlabel("Number of Points")
    plt.ylabel("Theoretical Probability")
    plt.grid()
    plt.show()


def empirical_vs_theoretical(solutions):
    N_points = [s[0] for s in solutions]
    p_emp = [s[1] for s in solutions]
    p_th_1 = [ (3/4)*((7/12)**(n-3)) for n in N_points]
    plt.plot(N_points, p_emp, marker="o", label="Empirical Probability")
    plt.plot(N_points, p_th_1, marker="o", color="blue", label="Theoretical Probability 1")
    plt.title("Empirical vs Theoretical Probability of Valid Configuration")
    plt.xscale("linear")
    plt.yscale("log")
    plt.xlabel("Number of Points")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid()
    plt.show()


empirical_vs_theoretical(solutions)

# theoretical_probability(solutions)
# empirical_probability(solutions)
# print(f"Theoretical probability: {p_th}")

# history_plot(history, p_th, N_points)
