import React, { useEffect, useState } from 'react';
import '../App.css';
import axios from 'axios';
import { useLocation, useNavigate } from "react-router-dom";
import { Dna } from  'react-loader-spinner';
import { Button, Icon } from 'semantic-ui-react';


const ViewImage = ({}) => {

  const { state } = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [oldImage, setOldImage] = useState();
  const [newImage, setNewImage] = useState();

  useEffect(() => {
    if (state === null) {
      navigate("/");
    } else {
      const { imageProcessed } = state;
      if (imageProcessed !== true)
        navigate("/");
    
      //Get Image from server
      const { oldImage } = state;
      setOldImage(oldImage);
      setNewImage("http://127.0.0.1:5000/get");
      // axios.get("http://127.0.0.1:5000/get").then(res => {
      //   if (res.data === "error")
      //     navigate("/");

      //   setNewImage("http://127.0.0.1:5000/get");
      // })
      setTimeout(() => {
        setLoading(false);
      }, 3000);
    }
  }, []);

  return (
    <div className="App" style={{height: "100vh"}}>
      <header className="App-header">
        <div className="headerSection">
          <h1 className="headerText">Healthy Smiles</h1>
        </div>

        <div style={{marginTop: "30vh"}}>
          { loading ?
            <div>
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
                </div>
              </div>

              <Button animated color="green" size="massive" style={{marginTop: "5%"}} onClick={(e) => navigate("/")}>
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