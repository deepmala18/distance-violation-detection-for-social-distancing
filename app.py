import os
import streamlit as st
from db import Video
from social_distance_detector import use_video
from social_distancing_webcam import use_webcam
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        vid = Video(path=path)
        db.add(vid)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

st.title("Distance Violation Detection for Social Distancing")
st.info('This project is used to provide data to maintain social distancing ')
if st.checkbox("Videos"):
        video=st.file_uploader('Upload a video',type=['mp4','3gp'])
        if video and st.button("UPLOAD"):
          path=os.path.join('uploads',f'{video.name}')
          with open(path,'wb') as f:
            f.write(video.getbuffer())
            save_file(path)
            st.info('Upload Succesfully') 
if st.checkbox("Detect Video File"):
  db = opendb()
  videos=db.query(Video).all()
  db.close()
  vid = st.selectbox('Select a Video to Play',videos)
  if vid and os.path.exists(vid.path) and st.button('Start Detection')and st.warning('press esc to exit'):
      use_video(vid.path,"output/out.mp4")
      st.success('Detection Successful')

if st.checkbox("Webcam"):
   if st.button('open webcam')and st.warning('press esc to exit'):
       use_webcam()
       st.success('Detection Successful')
       
    
if st.checkbox("About Project"):
    st.image('gif2.gif')
    st.info('Social distancing is important in times of epidemics and pandemics to prevent the spread of disease. Can we build a social distancing detector with OpenCV. ')
    st.image('gif1.gif')
    st.info(' Social distancing is crucial to preventing the spread of disease. Using computer vision technology based on OpenCV and YOLO-based deep learning, we are able to estimate the social distance of people in video streams. ')
    st.image('flow chart.png')
    st.info(' The steps involved in an OpenCV-based social distancing application.')

if st.checkbox("Creator info"):
    st.header("About The Project Creators")
    st.write('Anchal Singh')
    st.write('Deepmala')
    st.image('g.gif')

    

