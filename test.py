import streamlit as st
import pandas as pd
import numpy as np

st.title("vgi")
# Display a header and some text
st.header('Hello, Streamlit!')
st.write('This is a simple app to demonstrate how Streamlit works.')

# Add a slider widget
number = st.slider('Pick a number', 0, 100)
st.write(f'You selected: {number}')

# Add an interactive chart
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(data)
