###
#
# This script generates a set of templates for building the mold. You give the positions, face half-widths, and
# bowl depths of the sections and it will generate the outlines given a number of ribs. There is freedom here,
# so I chose to generate ellipses to have a consistent way of generating these plots that is not so hard to
# do on paper either.
#
# In the case where the face and back profiles are same, this script will simply generate semi-circles and you 
# probably don't need this tool.
###
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def generate_template_for_single_section(face_radius, back_radius, num_ribs, width_section=35, dpi=300, for_printing=False, save_to_file=None):
    """Generate template for a single section

    Args:
        face_radius (float): Face radius in mm at the section position
        back_radius (float): Bowl depth in mm at the section position
        num_ribs (int): Total number of ribs
        width_section (float, optional): Size in mm of the section, drawn as a semi-circle. Defaults to 35 mm.
        dpi (int, optional): Pixels per inch. Defaults to 300.
        for_printing (bool, optional): If True, generate plot for printing.
        save_to_file (str, optional): If other than None, this is the output filename. Defaults to None.
    """
    def plot_half_circle(r):
        # Generate half circle
        x = np.arange(0, r+0.01, 0.01)
        y = np.sqrt(r**2 - x**2)
        plt.plot(x, y, "--", c="k", alpha=0.5)

        x = -x[::-1]
        y = y[::-1]
        plt.plot(x, y, "--", c="k", alpha=0.5)

    fig = plt.figure(figsize=(2*face_radius/25.4,back_radius/25.4), dpi=dpi)

    # This is the number of divisions for the quarter circle, not counting the center rib
    num_divisions = num_ribs // 2

    # Draw all 3 circles
    if not for_printing:
        plot_half_circle(face_radius)
        plot_half_circle(back_radius)
        plot_half_circle((face_radius+back_radius)/2)

    # Plot width of section
    plot_half_circle(face_radius - width_section)

    # Generate divisions
    delta_angle = 180 / num_ribs # Assumes ribs are linearly spaced in phase space

    x_coords = []  
    y_coords = [] 

    for i in range(num_divisions):
        angle = np.radians(delta_angle * i)
        
        # Parametric equations of an ellipse - Here is the freedom I took
        x = face_radius * np.cos(angle)
        y = back_radius * np.sin(angle)

        x_coords.append(x)
        y_coords.append(y)

    # Add the right point of the central rib (since it's flat)
    x_coords.append(back_radius*np.tan(np.radians(delta_angle/2)))
    y_coords.append(back_radius)

    # Connect the points between the two quarter circles
    x_coords.append(-x_coords[-1])
    y_coords.append(back_radius)

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    plt.plot(x_coords, y_coords, ".-", c="tab:blue", markersize=5 if for_printing else 20, linewidth=1 if for_printing else 3)
    plt.plot(-x_coords[::-1][1:], y_coords[::-1][1:], ".-", c="tab:blue", markersize=5 if for_printing else 20, linewidth=1 if for_printing else 3)

    for i in range(len(x_coords)-1):
        # Plot rib line
        plt.plot([0,x_coords[i]], [0, y_coords[i]], "--", c="tab:blue")
        plt.plot([0,-x_coords[i]], [0, y_coords[i]], "--", c="tab:blue")

        # Plot text
        if not for_printing:
            plt.text(x_coords[i], y_coords[i]+0.03*max(face_radius, back_radius), f"({round(x_coords[i],1)}, {round(y_coords[i],1)})", color="k", fontsize=12, fontweight="bold")

    # Plot
    fig.axes[0].xaxis.set_major_locator(plticker.MultipleLocator(20))
    fig.axes[0].xaxis.set_minor_locator(plticker.MultipleLocator(5))
    fig.axes[0].yaxis.set_major_locator(plticker.MultipleLocator(20))
    fig.axes[0].yaxis.set_minor_locator(plticker.MultipleLocator(5))
    plt.grid(which="major", linewidth=1)
    plt.grid(which="minor", linewidth=0.2)

    if not for_printing:
        plt.xlabel("x coordinate (mm)", fontsize=16)
        plt.ylabel("y coordinate (mm)", fontsize=16)

        plt.margins(0)
    else:
        fig.axes[0].xaxis.set_ticklabels([])
        fig.axes[0].yaxis.set_ticklabels([])

        plt.xlim(-face_radius, face_radius)
        plt.ylim(0, back_radius)

        fig.subplots_adjust(
            left=0,
            bottom=0,
            right=1,
            top=1
        )

    # Save to file if asked
    if save_to_file is not None:
        plt.savefig(save_to_file, dpi=dpi)
    else:
        plt.show()

if __name__ == "__main__":
    # Generate all sections - here is an example
    N = 15
    pos = np.arange(1,10+1)
    face = [94,118,148,168,181,181,164,153,139,119]
    back = [109,133,160,177,186,183,168,156,143,122]

    # Generate separate sections
    for i in range(len(pos)):
        generate_template_for_single_section(face[i], back[i], N, for_printing=True, save_to_file=f"{pos[i]}.png")

    generate_template_for_single_section(76, 91, N, for_printing=True, save_to_file=f"front.png")
    generate_template_for_single_section(82, 86, N, for_printing=True, save_to_file=f"back.png")