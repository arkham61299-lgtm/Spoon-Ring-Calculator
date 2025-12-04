import streamlit as st
import math

def get_ring_diameter(size):
    """
    Returns the inner diameter (mm) for standard US ring sizes, 
    including quarter and half sizes, based on industry charts.
    """
    # Dictionary mapping US size to Inner Diameter in mm (US sizes 3.0 to 16.0)
    sizes = {
        # Sizes 3.0 to 5.0
        3.0: 14.05, 3.25: 14.25, 3.5: 14.45, 3.75: 14.65,
        4.0: 14.86, 4.25: 15.04, 4.5: 15.27, 4.75: 15.53,
        5.0: 15.70, 5.25: 15.90, 5.5: 16.10, 5.75: 16.30,
        
        # Sizes 6.0 to 8.0
        6.0: 16.51, 6.25: 16.71, 6.5: 16.92, 6.75: 17.13,
        7.0: 17.35, 7.25: 17.45, 7.5: 17.75, 7.75: 17.97,
        8.0: 18.19, 8.25: 18.35, 8.5: 18.53, 8.75: 18.69,

        # Sizes 9.0 to 11.0
        9.0: 18.89, 9.25: 19.22, 9.5: 19.41, 9.75: 19.62,
        10.0: 19.84, 10.25: 20.02, 10.5: 20.20, 10.75: 20.44,
        11.0: 20.68, 11.25: 20.85, 11.5: 21.08, 11.75: 21.24,

        # Sizes 12.0 to 14.0
        12.0: 21.49, 12.25: 21.69, 12.5: 21.89, 12.75: 22.10,
        13.0: 22.33, 13.25: 22.40, 13.5: 22.60, 13.75: 22.80,
        14.0: 23.00, 14.25: 23.20, 14.5: 23.41, 14.75: 23.60,

        # Sizes 15.0 to 16.0
        15.0: 23.81, 15.25: 24.00, 15.5: 24.22, 15.75: 24.40,
        16.0: 24.63
    }
    
    # Check for direct match
    if size in sizes:
        return sizes[size]
    
    # Handle sizes that are not perfectly on the .25, .5, .75, or .0 mark by interpolation
    if 3.0 <= size <= 16.0:
        # Find the next lower and next higher sizes in the dictionary
        lower_size = max([s for s in sizes.keys() if s < size], default=None)
        upper_size = min([s for s in sizes.keys() if s > size], default=None)

        if lower_size is not None and upper_size is not None:
            # Linear interpolation for non-standard quarter sizes (e.g., 7.1)
            lower_dia = sizes[lower_size]
            upper_dia = sizes[upper_size]
            
            # Ratio of distance: (size - lower_size) / (upper_size - lower_size)
            ratio = (size - lower_size) / (upper_size - lower_size)
            
            # Interpolated diameter
            interpolated_dia = lower_dia + (upper_dia - lower_dia) * ratio
            return interpolated_dia
            
    return None # Return None if size is outside the 3.0 to 16.0 range

# --- Streamlit App Layout ---

st.set_page_config(page_title="Spoon Ring Calculator", layout="centered")

st.markdown("""
<style>
.st-emotion-cache-18ni7ap {
    background-color: #f0f0f5; /* Light grey background for the app */
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #45a049;
}
.stSuccess > div {
    border-left: 8px solid #4CAF50;
    font-size: 1.1em;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🥄 Spoon Ring Cut Calculator")
st.markdown("---")
st.markdown("### 📏 Enter Measurements")

# Input Section
col_size, col_thickness = st.columns(2)

with col_size:
    # Allows quarter-size inputs
    ring_size = st.number_input(
        "Target US Ring Size:", 
        min_value=3.0, 
        max_value=16.0, 
        value=7.0, 
        step=0.25, 
        format="%.2f",
        help="Select or type the US ring size (e.g., 7.5 or 8.25)."
    )

with col_thickness:
    thickness_mm = st.number_input(
        "Spoon Thickness (mm):", 
        min_value=0.5, 
        max_value=5.0, 
        value=1.5, 
        step=0.1, 
        format="%.1f",
        help="Measure the thickness of the handle exactly where you plan to cut."
    )

st.markdown("---")

if st.button("Calculate Final Cut Length", use_container_width=True):
    inner_diameter = get_ring_diameter(ring_size)
    
    if inner_diameter is None:
        st.error(f"⚠️ Error: Ring Size {ring_size} is outside the supported range (3.0 - 16.0).")
    else:
        # The Core Math: Neutral Axis Calculation
        # Cut Length = Pi * (Inner Diameter + Thickness)
        cut_length = math.pi * (inner_diameter + thickness_mm)
        
        # Display Results
        st.subheader("✅ Calculated Results")
        
        col_dia, col_thick, col_pi = st.columns(3)
        col_dia.metric("Inner Diameter (D)", f"{inner_diameter:.2f} mm")
        col_thick.metric("Thickness (T)", f"{thickness_mm:.2f} mm")
        col_pi.metric("Calculation", f"$\pi \\times (D + T)$")

        st.markdown("\n")
        st.success(
            f"### **REQUIRED FLAT CUT LENGTH:** {cut_length:.2f} mm"
        )
        
        st.markdown("\n")
        st.info(
            """
            **Tip for Bypass Rings:** This length is for a closed-band ring. If you are making a popular 
            'bypass' (overlapping) style, **you must add extra length** (usually 15mm - 25mm) for the desired overlap.
            """
        )
        st.balloons()
