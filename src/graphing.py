import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_court(ax=None, color='#262626', lw=2, outer_lines=True):
    """
    Draws an absolute, mathematically accurate NBA half-court.
    All coordinates match NBA API standards (tenths of a foot).
    Origin (0,0) is the exact center of the hoop.
    """
    if ax is None:
        ax = plt.gca()

    # --- 1. THE HOOP & BACKBOARD (FIXED) ---
    # Rim: 1.5 ft diameter -> 0.75 ft radius (7.5 units) centered at (0,0)
    hoop = patches.Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False, zorder=2)
    
    # Backboard: 6 ft wide (-30 to 30). Exactly 15 inches (1.25 ft = 12.5 units) behind hoop center
    ax.plot([-30, 30], [-12.5, -12.5], color=color, linewidth=lw, zorder=2)
    ax.add_patch(hoop)

    # --- 2. THE PAINT & BASELINE (FIXED) ---
    # Baseline: 4 ft behind the backboard -> y = -12.5 - 40 = -52.5
    # Paint Box: 16 ft wide (-80 to 80), 19 ft deep from baseline (-52.5 + 190 = 137.5)
    paint_outer = patches.Rectangle((-80, -52.5), 160, 190, linewidth=lw, color=color, fill=False, zorder=2)
    paint_inner = patches.Rectangle((-60, -52.5), 120, 190, linewidth=lw, color=color, fill=False, zorder=1)
    
    # Free Throw Line sits at y = 137.5 (Exactly 15 ft from the backboard line at -12.5)
    ft_top_arc = patches.Arc((0, 137.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False, zorder=2)
    ft_bottom_arc = patches.Arc((0, 137.5), 120, 120, theta1=180, theta2=360, linewidth=lw, color=color, linestyle='--', fill=False, zorder=2)
    
    ax.add_patch(paint_outer)
    ax.add_patch(paint_inner)
    ax.add_patch(ft_top_arc)
    ax.add_patch(ft_bottom_arc)

    # --- 3. RESTRICTED AREA (FIXED) ---
    # 4 ft radius arc (40 units) centered at the hoop (0,0)
    restricted_arc = patches.Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color, fill=False, zorder=2)
    # Straight lines connect the restricted arc directly to the backboard at y = -12.5
    ax.plot([-40, -40], [-12.5, 0], color=color, linewidth=lw, zorder=2)
    ax.plot([40, 40], [-12.5, 0], color=color, linewidth=lw, zorder=2)
    ax.add_patch(restricted_arc)

    # --- 4. THE 3-POINT LINE (FIXED) ---
    # Corner 3s: 22 ft (220 units) from center, extending straight up from the baseline (y = -52.5)
    ax.plot([-220, -220], [-52.5, 89.48], color=color, linewidth=lw, zorder=2)
    ax.plot([220, 220], [-52.5, 89.48], color=color, linewidth=lw, zorder=2)
    
    # 3-Point Arc: 23.75 ft radius (237.5 units) centered at (0,0)
    three_point_arc = patches.Arc((0, 0), 475, 475, theta1=22.13, theta2=157.87, linewidth=lw, color=color, fill=False, zorder=2)
    ax.add_patch(three_point_arc)

    # --- 5. CENTER COURT (FIXED) ---
    # Half-court line is 47 ft from the baseline (-52.5 + 470 = 417.5)
    center_outer = patches.Arc((0, 417.5), 120, 120, theta1=180, theta2=360, linewidth=lw, color=color, fill=False, zorder=2)
    center_inner = patches.Arc((0, 417.5), 40, 40, theta1=180, theta2=360, linewidth=lw, color=color, fill=False, zorder=2)
    ax.add_patch(center_outer)
    ax.add_patch(center_inner)

    # --- 6. COURT BOUNDARIES ---
    if outer_lines:
        # Full half-court boundary box: 50 ft wide, 47 ft deep
        boundary = patches.Rectangle((-250, -52.5), 500, 470, linewidth=lw, color=color, fill=False, zorder=2)
        ax.add_patch(boundary)

    # Tight viewport limits centered around the fresh baseline coordinate
    ax.set_xlim(-260, 260)
    ax.set_ylim(-70, 440)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    return ax

def plot_shot_chart(shot_df, player_name: str):
    """Combines court lines with the player's scattered shot data."""
    fig, ax = plt.subplots(figsize=(8, 6))
    draw_court(ax)
    
    # Separate makes and misses
    made_shots = shot_df[shot_df['SHOT_MADE_FLAG'] == 1]
    missed_shots = shot_df[shot_df['SHOT_MADE_FLAG'] == 0]
    
    # Plot 'em
    ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'], c='green', label='Made', alpha=0.6)
    ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'], c='red', label='Missed', marker='x', alpha=0.5)
    
    ax.set_title(f"{player_name} Shot Chart")
    ax.legend()
    plt.tight_layout()
    plt.savefig("./visualizations/wemby_shots.png")
    plt.show()