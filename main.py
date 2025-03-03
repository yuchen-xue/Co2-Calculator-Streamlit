import pandas as pd
import streamlit as st

from calculator import Calculator

# Initialize the calculator (default values are necessary for the demo)
cal = Calculator(transportation="bus", distance=0.0)

if __name__ == "__main__":
    # Create a title
    st.title("Simple CO2 Emission Calculator")

    # Create a description
    st.write(
        "This is a simple calculator that calculates the CO2 emission of a trip based on the method of transportation and the distance of the travel."
    )

    # Create selectors
    transportation_selector, distance_unit_selector, output_unit_selector = st.columns(
        3
    )

    # Set mean of transportation
    with transportation_selector:
        transportation = st.selectbox(
            "Select a method of transportation", cal.emission_data
        )
        cal.transportation = transportation

    # Set unit of distance
    with distance_unit_selector:
        distance_unit = st.radio(
            "Select a unit of distance",
            cal.supported_distance_unit,
            help="The unit of distance of the travel",
        )
        cal.distance_unit = distance_unit

    # Set unit of output
    with output_unit_selector:
        output_unit = st.radio(
            "Select a unit of output",
            cal.supported_output_unit,
            help="auto means the unit will be automatically selected based on the distance",
        )
        cal.ouptput_unit = output_unit

    # Set distance of travel
    st.number_input(
        "Distance of travel",
        key="distance",
        step=1.0,
        help="The distance is automatically rounded to 2 decimal places",
    )
    cal.distance = st.session_state.distance

    # Auto calculate
    emission, result_unit = cal.calculate_emission()
    st.write("CO2 emmision of this trip is around: ", emission, result_unit)

    # Show the data if needed (by using a checkbox)
    st.subheader("Want to know how the emission is calculated?")
    data = pd.DataFrame.from_dict(
        cal.emission_data, columns=["CO2 Emission"], orient="index"
    )
    data.index.name = "Transportation Method"
    if st.checkbox("Show the data"):
        st.write("CO2 emission per km for each transportation method")
        st.write(data)
