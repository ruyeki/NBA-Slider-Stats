import os
def generate_streamlit_config():
    # Define the theme settings
    theme_settings = """
    [theme]
    primaryColor="#C084FC"
    backgroundColor="#000000"
    secondaryBackgroundColor="#3830A3"
    textColor="#FFFFFF"
    font="sans serif"
    """

    # Path to the Streamlit configuration directory
    streamlit_config_dir = os.path.expanduser("~/.streamlit")

    # Ensure the Streamlit config directory exists
    if not os.path.exists(streamlit_config_dir):
        os.makedirs(streamlit_config_dir)

    # Path to the config file
    config_file_path = os.path.join(streamlit_config_dir, "config.toml")

    # Write the theme settings to the config file
    with open(config_file_path, "w") as config_file:
        config_file.write(theme_settings)
