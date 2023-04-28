import streamlit as st

st.markdown("<h1 style='text-align: center;'>Free-Process</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📑Preprocess Image File📑 </h3>", unsafe_allow_html=True)
st.text('')
st.text('')

option = st.selectbox(
    'What do you want to process?',
    ('Image Adjusment', 'Image Transformation', 'Image Colorspaces'))


if option == 'Image Adjusment':
    st.selectbox(
        'Select',
        ['Hue','Saturation','Brightness']
    )
elif option == 'Image Transformation':
    st.selectbox(
        'Select',
        ['Flipp','Rotate','Transpose']
    )
else :
    st.selectbox(
        'Select',
        ['HSV','Grayscale']
    )

st.write('You selected:', option)

#asdfsadfadsfdasfadsfdsf
import streamlit as st

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
