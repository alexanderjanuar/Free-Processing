import streamlit as st
from PIL import Image
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Free-Process</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📑Preprocess Image File📑 </h3>", unsafe_allow_html=True)
st.text('')
st.text('')
col1, col2 = st.columns((1.2,1.8))


with col1:
    uploaded_files = st.file_uploader("Choose a file", type=['png', 'jpg'])
    show_file = st.empty()
    if uploaded_files is not None:
        bytes_data = uploaded_files.getvalue()
        st.image(bytes_data)
        
# for information if not uploaded files
    if not uploaded_files:
        show_file.info('Please upload a file : {}'.format(' '.join(['png ,', 'jpg'])))

with col2:
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


    #jlasjdflkjadsf
    age = st.slider('How old are you?', 0, 130, 25)
    st.write("I'm ", age, 'years old')





