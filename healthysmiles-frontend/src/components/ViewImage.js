import React, { useEffect, useRef, useState } from 'react';
import '../App.css';
import axios from 'axios';
import { useLocation, useNavigate } from "react-router-dom";
import { Dna } from  'react-loader-spinner';
import { Button, Icon } from 'semantic-ui-react';


const ViewImage = ({props}) => {

  const { state } = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [oldImage, setOldImage] = useState();
  const [newImage, setNewImage] = useState();
  const [images, setImages] = useState();
  const index = useRef(0);

  useEffect(() => {
    if (state === null) {
      navigate("/");
    } else {
      const { imageProcessed } = state;
      if (imageProcessed !== true)
        navigate("/");
    
      //Get Image from server
      const { oldImage } = state;
      console.log(oldImage);
      setOldImage(oldImage);
      pullImages();
      setTimeout(() => {
        setLoading(false);
      }, 3000);
    }
  }, []);

  const pullImages = () => {
    let images = [];
    for (let i = 0; i < 5; i++) {
      images.push(`http://127.0.0.1:500/get${i}`);
    }

    setImages(images);
    setNewImage(images[0]);
  }

  const nextImage = () => {
    if (index.current === images.length ) {
      setNewImage(images[0]);
      index.current = 0;
    } else {
      setNewImage(images[index.current + 1]);
      index.current++;
    }
  }

  return (
    <div className="App" style={{minHeight: "100vh"}}>
      <header className="App-header">
        <div className="headerSection">
          <h1 className="headerText">Healthy Smiles</h1>
        </div>

        <div>
          { loading ?
            <div style={{marginTop: "30vh"}}>
              <h1>Making your smile :)</h1>
              <Dna
                visible={true}
                height="15vw"
                width="15vw"
                ariaLabel="dna-loading"
                wrapperStyle={{}}
                wrapperClass="dna-wrapper"
              />
            </div>
            :
            <div className="imageDisplayContainer">
              <div className="imageDisplay">
                <div>
                  <img src={oldImage} className="viewNewImage"/>
                </div>
                <div>
                  <img src={newImage} className="viewNewImage"/>
                  <h2>Check out your new photo!</h2>
                </div>
              </div>

              <Button animated color="green" size="massive" style={{marginTop: "1vh"}} onClick={(e) => navigate("/")}>
                <Button.Content visible>Again!</Button.Content>
                <Button.Content hidden>
                  <Icon name="redo" />
                </Button.Content>
              </Button>
            </div>
          }
        </div>
      </header>
    </div>
  );
};

export default ViewImage;