"""
Samsung Galaxy Tab A7 (10.4") IKEA Skådis Pegboard Mount
Designed for PythonSCAD (https://www.pythonscad.org)
Target Printer: Prusa MK4S (Build Volume: 250 x 210 x 220 mm)

Key Features:
- Orientation: Landscape Mode (perfect for Grafana Dashboards)
- Tablet State: Bare Tablet (247.6 x 157.4 x 7.0 mm)
- Modular 2-Piece Split Brackets (Left & Right)
- Open USB-C Port Cutout on Right Bracket for continuous 24/7 charging
- Integrated IKEA Skådis T-Hooks spaced at 240 mm (6 Skådis grid columns)
"""

from pythonscad import *

# ==============================================================================
# RENDER MODE SELECTION
# Options: "assembly" (Full preview with ghost tablet), "left", "right"
# ==============================================================================
RENDER_MODE = "assembly"

# ==============================================================================
# PARAMETERS & DIMENSIONS (All values in millimeters)
# ==============================================================================

# --- Samsung Galaxy Tab A7 Bare Dimensions ---
TABLET_WIDTH = 247.6
TABLET_HEIGHT = 157.4
TABLET_THICKNESS = 7.0

# --- Fit Tolerances ---
THICKNESS_TOLERANCE = 1.2    # Allowance for smooth sliding & optional felt pads
SLOT_DEPTH = TABLET_THICKNESS + THICKNESS_TOLERANCE  # 8.2 mm total slot channel

# --- Mount Bracket Geometry ---
BRACKET_WIDTH = 36.0         # Width of each holder bracket (X axis)
BRACKET_HEIGHT = 90.0        # Vertical height of bracket body
WALL_THICKNESS = 3.2         # Heavy-duty wall thickness
FRONT_LIP_HEIGHT = 9.0       # Grips bezel securely without obscuring display (~9.3mm bezel)
BACKPLATE_THICKNESS = 3.5    # Back wall thickness between tablet and pegboard

# --- IKEA Skådis Pegboard Standard Dimensions ---
SKADIS_SLOT_WIDTH = 5.0
SKADIS_SLOT_HEIGHT = 15.0
SKADIS_PITCH_X = 40.0        # Horizontal center-to-center slot pitch
SKADIS_PITCH_Y = 40.0        # Vertical center-to-center slot pitch
SKADIS_HOOK_SPAN_COLUMNS = 6 # Spans 6 grid columns = 240.0 mm hook-to-hook distance

# Hook & Bumper Dimensions
HOOK_STEM_W = 4.4            # Fits 5.0mm slot smoothly without lateral slop
HOOK_STEM_DEPTH = 5.3        # Reaches through 5.0mm board + clearance
HOOK_LIP_H = 7.5             # Upper retention lip
HOOK_DROP = 9.0              # Lower drop lock behind board

BUMPER_RADIUS = 2.45         # Lower peg radius (4.9mm diameter for tight slot fit)
BUMPER_LENGTH = 7.0          # Stabilizer pin length into lower slot

# Hook offset from bracket origin
LEFT_HOOK_X_OFFSET = 10.0    # Hook center relative to left bracket left edge
RIGHT_HOOK_X_OFFSET = 26.0   # Hook center relative to right bracket left edge

# ==============================================================================
# HELPER GEOMETRY MODULES
# ==============================================================================

def skadis_top_hook():
    """Generates an IKEA Skådis T-Hook extending backward (-Y) for slot mounting."""
    stem = cube([HOOK_STEM_W, HOOK_STEM_DEPTH + WALL_THICKNESS, HOOK_STEM_W], center=True) \
        .translate([0, -(HOOK_STEM_DEPTH + WALL_THICKNESS) / 2, 0])
    
    up_lip = cube([HOOK_STEM_W, HOOK_STEM_W, HOOK_LIP_H], center=True) \
        .translate([0, -(HOOK_STEM_DEPTH + WALL_THICKNESS - HOOK_STEM_W / 2), HOOK_LIP_H / 2 - HOOK_STEM_W / 2])
    
    drop_lip = cube([HOOK_STEM_W, HOOK_STEM_W, HOOK_DROP], center=True) \
        .translate([0, -(HOOK_STEM_DEPTH + WALL_THICKNESS - HOOK_STEM_W / 2), -HOOK_DROP / 2 + HOOK_STEM_W / 2])
    
    return union(stem, up_lip, drop_lip)

def skadis_lower_bumper():
    """Generates a lower stabilizing pin (at 40mm Y-pitch) extending backward (-Y) into lower Skådis slot."""
    pin = cylinder(h=BUMPER_LENGTH, r=BUMPER_RADIUS, center=False) \
        .rotate([90, 0, 0])
    return pin

def bracket_body(is_right_side=False):
    """
    Creates the main U-channel holder body:
    - Backplate
    - Bottom resting shelf
    - Front retaining lip
    - Outer lateral end wall
    - Weight reduction / ventilation cutout
    - USB-C port cutout (right side)
    """
    total_depth = BACKPLATE_THICKNESS + SLOT_DEPTH + WALL_THICKNESS
    
    # Backplate
    backplate = cube([BRACKET_WIDTH, BACKPLATE_THICKNESS, BRACKET_HEIGHT])
    
    # Bottom Shelf
    shelf = cube([BRACKET_WIDTH, total_depth, WALL_THICKNESS])
    
    # Front Retaining Lip
    front_lip = cube([BRACKET_WIDTH, WALL_THICKNESS, FRONT_LIP_HEIGHT]) \
        .translate([0, total_depth - WALL_THICKNESS, 0])
    
    # Outer Lateral Wall (Left wall for left bracket, right wall for right bracket)
    side_wall_x = 0 if not is_right_side else BRACKET_WIDTH - WALL_THICKNESS
    side_wall = cube([WALL_THICKNESS, total_depth, BRACKET_HEIGHT]) \
        .translate([side_wall_x, 0, 0])
    
    base = union(backplate, shelf, front_lip, side_wall)
    
    # Backplate ventilation cutout (avoid cutting into side wall)
    vent_w = 18.0
    vent_h = BRACKET_HEIGHT - 36
    if vent_h > 10:
        vent_x = 12.0 if not is_right_side else 6.0
        vent_cutout = rounded_cube([vent_w, BACKPLATE_THICKNESS + 4, vent_h], r=2.5) \
            .translate([vent_x, -2, 24])
        base = difference(base, vent_cutout)
        
    # USB-C Cable Pass-Through Port on Right Bracket
    if is_right_side:
        cable_port_h = 28.0
        cable_port = cube([WALL_THICKNESS + 4, total_depth + 4, cable_port_h]) \
            .translate([BRACKET_WIDTH - WALL_THICKNESS - 2, -2, 14])
        base = difference(base, cable_port)
        
    return base

# ==============================================================================
# MAIN EXPORTABLE BRACKET MODULES
# ==============================================================================

def create_left_bracket():
    """Generates the Complete Left Skådis Bracket."""
    body = bracket_body(is_right_side=False)
    
    # Attach upper Skådis hook
    hook = skadis_top_hook() \
        .translate([LEFT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16])
        
    # Attach lower stabilizing bumper pin at 40mm vertical grid spacing
    bumper = skadis_lower_bumper() \
        .translate([LEFT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16 - SKADIS_PITCH_Y])
        
    return union(body, hook, bumper).color("DarkSlateGray")

def create_right_bracket():
    """Generates the Complete Right Skådis Bracket."""
    body = bracket_body(is_right_side=True)
    
    # Attach upper Skådis hook
    hook = skadis_top_hook() \
        .translate([RIGHT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16])
        
    # Attach lower stabilizing bumper pin at 40mm vertical grid spacing
    bumper = skadis_lower_bumper() \
        .translate([RIGHT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16 - SKADIS_PITCH_Y])
        
    return union(body, hook, bumper).color("DarkSlateGray")

def create_ghost_tablet():
    """Generates a reference 3D ghost model of the Samsung Galaxy Tab A7 (10.4")."""
    tablet = rounded_cube([TABLET_WIDTH, TABLET_THICKNESS, TABLET_HEIGHT], r=2.5) \
        .color("DeepSkyBlue", 0.45)
    return tablet

# ==============================================================================
# OUTPUT / ASSEMBLY DISPLAY CONTROL
# ==============================================================================

# Distance between hooks = 6 Skådis columns = 240.0 mm
SKADIS_HOOK_SPAN_MM = SKADIS_HOOK_SPAN_COLUMNS * SKADIS_PITCH_X  # 240.0 mm

# Left Bracket origin placed at X = -LEFT_HOOK_X_OFFSET so its hook is at X = 0.0
LEFT_BRACKET_X = -LEFT_HOOK_X_OFFSET  # -10.0 mm

# Right Bracket origin placed so its hook is at X = 240.0 mm
RIGHT_BRACKET_X = SKADIS_HOOK_SPAN_MM - RIGHT_HOOK_X_OFFSET  # 214.0 mm

# Inner clearance between left and right outer walls:
# Left inner wall face at X = -10.0 + 3.2 = -6.8 mm
# Right inner wall face at X = 214.0 + 36.0 - 3.2 = 246.8 mm
# Total channel width = 246.8 - (-6.8) = 253.6 mm (spacious fit for 247.6 mm tablet)

# Tablet X position (centered within channel with 3.0 mm lateral padding on each side)
TABLET_POS_X = -6.8 + 3.0  # -3.8 mm

if RENDER_MODE == "left":
    create_left_bracket().show()
elif RENDER_MODE == "right":
    create_right_bracket().show()
else:
    left_b = create_left_bracket().translate([LEFT_BRACKET_X, 0, 0])
    right_b = create_right_bracket().translate([RIGHT_BRACKET_X, 0, 0])
    
    tablet_preview = create_ghost_tablet().translate([
        TABLET_POS_X,
        BACKPLATE_THICKNESS,
        WALL_THICKNESS
    ])
    
    full_assembly = union(left_b, right_b, tablet_preview)
    full_assembly.show()
