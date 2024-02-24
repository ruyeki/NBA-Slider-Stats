import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def main():
    st.title('Welcome to SliderStats!')
    st.write('SliderStats allows you to explore data using sliders.')
    st.write("Select the desired year from the drop-down menu labeled 'Select a Year'")
    st.write("Ex. 2016-2017")

    # Choose Total Stats, Per Game Stats, or Team Stats
    st.write("Choose Total Stats, Per Game Stats, or Team Stats")
    st.write("Ex. Per Game Stats")

    #   Choose a position
    st.write("Choose a position")
    st.write("Ex. Forward")

# Choose the stats you want to compare
    st.write("Choose the stats you want to compare")
    st.write("Ex. Points, Assists, and Rebounds")

# Drag importance sliders
    st.write("Drag importance sliders")
    st.write("Ex. 0.6 Points, 0.4 Assists, 0.3 Rebounds")

# Drag range sliders
    st.write("Drag range sliders")
    st.write("Ex. 20 to 28 ppg, 3 to 9 apg, 4-12 rpg")


# Look at the table to compare players
    st.write("Look at the table to compare players")
    st.write("Ex. Lebron James")

    
    st.write("Select the desired year from the drop-down menu labeled 'Select a Year'")
    st.write("Ex. 2016-2017")

# Choose Total Stats, Per Game Stats, or Team Stats
    st.write("Choose Total Stats, Per Game Stats, or Team Stats")
    st.write("Ex. Per Game Stats")

# Choose a position
    st.write("Choose a position")
    st.write("Ex. Forward")

# Choose the stats you want to compare
    st.write("Choose the stats you want to compare")
    st.write("Ex. Points, Assists, and Rebounds")

    # Drag importance sliders
    st.write("Drag importance sliders")
    st.write("Ex. 0.6 Points, 0.4 Assists, 0.3 Rebounds")
    importance_sliders = {}

# Drag range sliders
    st.write("Drag range sliders")
    st.write("Ex. 20 to 28 ppg, 3 to 9 apg, 4-12 rpg")


# Look at the table to compare players
    st.write("Look at the table to compare players")
    st.write("Ex. Lebron James")

if __name__ == "__main__":
    main()