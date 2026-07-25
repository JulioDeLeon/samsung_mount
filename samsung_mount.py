"""
Samsung Galaxy Tab A7 (10.4") IKEA Skådis Pegboard Mount
Designed for PythonSCAD (https://www.pythonscad.org)
Target Printer: Prusa MK4S (Build Build Volume: 250 x 210 x 220 mm)

Key Features:
- Orientation: Landscape Mode (perfect for Grafana Dashboards)
- Tablet State: Bare Tablet (247.6 x 157.4 x 7.0 mm)
- Modular 2-Piece Split Brackets (Left & Right)
- USB-C Port Cutout on Left Bracket (prevents camera bump interference)
- Integrated IKEA Skådis T-Hooks spaced at 240 mm (6 Skådis grid columns)
"""

from pythonscad import *

# ==============================================================================
# RENDER MODE SELECTION
# Default: "assembly" (Full preview with ghost tablet).
# Can be overridden via CLI: -D RENDER_MODE='"left"' or -D RENDER_MODE='"right"'
# ==============================================================================
if 'RENDER_MODE' not in globals():
    RENDER_MODE = "assembly"

# ==============================================================================
# PARAMETERS & DIMENSIONS (All values in millimeters)
# ==============================================================================

# USB-C Port Side Location ("left" or "right")
# Default set to "left" so tablet orientation avoids camera bump interference
USB_PORT_SIDE = "left"

# --- Samsung Galaxy Tab A7 Bare Dimensions ---
TABLET_WIDTH = 247.6
TABLET_HEIGHT = 157.4
TABLET_THICKNESS = 7.0

# --- Fit Tolerances ---
THICKNESS_TOLERANCE = 1.2    # Allowance for smooth sliding & optional felt pads
SLOT_DEPTH = TABLET_THICKNESS + THICKNESS_TOLERANCE  # 8.2 mm total slot channel

# --- Mount Bracket Geometry ---
BRACKET_WIDTH = 36.0         # Width of each holder bracket (X axis)
BRACKET_HEIGHT = 95.0        # Vertical height of bracket body
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

# USB-C Port Center in Landscape Mode (centered along 157.4mm height)
USB_PORT_CENTER_Z = WALL_THICKNESS + (TABLET_HEIGHT / 2.0)  # 81.9 mm from bracket base

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

def bracket_body(side="left"):
    """
    Creates the main U-channel holder body:
    - Backplate
    - Bottom resting shelf
    - Front retaining lip
    - Outer lateral end wall
    - Weight reduction / ventilation cutout
    - Accurately centered USB-C port cutout (if side == USB_PORT_SIDE)
    """
    is_left = (side == "left")
    is_usb_side = (side == USB_PORT_SIDE)
    total_depth = BACKPLATE_THICKNESS + SLOT_DEPTH + WALL_THICKNESS
    
    # Backplate
    backplate = cube([BRACKET_WIDTH, BACKPLATE_THICKNESS, BRACKET_HEIGHT])
    
    # Bottom Shelf
    shelf = cube([BRACKET_WIDTH, total_depth, WALL_THICKNESS])
    
    # Front Retaining Lip
    front_lip = cube([BRACKET_WIDTH, WALL_THICKNESS, FRONT_LIP_HEIGHT]) \
        .translate([0, total_depth - WALL_THICKNESS, 0])
    
    # Outer Lateral Wall (Left wall for left bracket, right wall for right bracket)
    side_wall_x = 0 if is_left else BRACKET_WIDTH - WALL_THICKNESS
    side_wall = cube([WALL_THICKNESS, total_depth, BRACKET_HEIGHT]) \
        .translate([side_wall_x, 0, 0])
    
    base = union(backplate, shelf, front_lip, side_wall)
    
    # Backplate ventilation cutout
    vent_w = 18.0
    vent_h = 40.0
    vent_x = 12.0 if is_left else 6.0
    vent_cutout = rounded_cube([vent_w, BACKPLATE_THICKNESS + 4, vent_h], r=2.5) \
        .translate([vent_x, -2, 20])
    base = difference(base, vent_cutout)
        
    # Accurately Centered USB-C Cable Pass-Through Port
    if is_usb_side:
        cable_port_h = 32.0  # 32mm clearance for USB-C cable head & strain relief
        cable_port_z = USB_PORT_CENTER_Z - (cable_port_h / 2.0)  # Starts at Z = 65.9 mm
        cable_port_x = -2.0 if is_left else (BRACKET_WIDTH - WALL_THICKNESS - 2.0)
        cable_port = cube([WALL_THICKNESS + 4, total_depth + 4, cable_port_h + 10.0]) \
            .translate([cable_port_x, -2, cable_port_z])
        base = difference(base, cable_port)
        
    return base

# ==============================================================================
# MAIN EXPORTABLE BRACKET MODULES
# ==============================================================================

def create_left_bracket():
    """Generates the Complete Left Skådis Bracket."""
    body = bracket_body(side="left")
    
    # Attach upper Skådis hook
    hook = skadis_top_hook() \
        .translate([LEFT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16])
        
    # Attach lower stabilizing bumper pin at 40mm vertical grid spacing
    bumper = skadis_lower_bumper() \
        .translate([LEFT_HOOK_X_OFFSET, 0, BRACKET_HEIGHT - 16 - SKADIS_PITCH_Y])
        
    return union(body, hook, bumper).color("DarkSlateGray")

def create_right_bracket():
    """Generates the Complete Right Skådis Bracket."""
    body = bracket_body(side="right")
    
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

# Tablet X position (centered within channel with 3.0 mm lateral padding on each side)
TABLET_POS_X = -6.8 + 3.0  # -3.8 mm

if str(RENDER_MODE).lower() == "left":
    create_left_bracket().show()
elif str(RENDER_MODE).lower() == "right":
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
