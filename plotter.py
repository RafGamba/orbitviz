def plot_orbit(ax, orbit_data):
    ax.plot(orbit_data[:, 0], orbit_data[:, 1], orbit_data[:, 2], label='Orbita')
    ax.scatter(0, 0, 0, color='yellow', label='Terra (centro)', s=100)

    ax.set_title("Orbita Satellitare")
    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.legend()
    ax.grid(True)
