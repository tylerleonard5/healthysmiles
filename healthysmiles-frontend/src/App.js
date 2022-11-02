import React, { Component } from 'react';
import './App.css';
import ImageUpload from './components/ImageUpload.js';
import { Button, Icon } from 'semantic-ui-react';
import { FileUploader } from "react-drag-drop-files";

import womanClose from './assets/womanCloseup.jpg';
import manTeeth from './assets/manTeeth.jpg';
import womanTeeth from './assets/womanTeeth.jpg';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.uploadRef = React.createRef();
    this.state = {
      imageFile: null,
      imageToDisplay: null,
    }
  }

  scrollToUpload = () => {
    this.uploadRef.current.scrollIntoView({behavior: 'smooth'});
  }

  imageFileUpload = (file: any) => {
    console.log(file);
    this.setState({imageFile: file});
    var img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.onload = () => {
      this.setState({imageToDisplay: URL.createObjectURL(file)});
    }
  };

  resetPhoto = () => {
    this.setState({imageToDisplay: null});
    this.setState({imageFile: null});
  }

  render() {
    return (
      <div className="App">
        <header className="AppMain">
          <div className="headerSection">
            <h1 className="headerText">Healthy Smiles</h1>
          </div>
        
          <div className="Banner">
            <img src={manTeeth} className="bannerImage"/>
            <img src={womanClose} className="bannerImage"/>
            <img src={womanTeeth} className="bannerImage"/>
          </div>

          <div className="downButtonSection">
            <Button icon className="downButton" size="huge" onClick={(e) => this.scrollToUpload()}>
              <Icon className="downIcon" name="chevron down" size="huge"/>
            </Button>
          </div>
        </header>

        <div className="uploadSection">
          { this.state.imageToDisplay === null ?
            <div className='uploadContainer' ref={this.uploadRef}>
              <FileUploader
                name="userImage"
                types={['JPG', 'JPEG', 'PNG']}
                handleChange={(file) => this.imageFileUpload(file)}
                children={
                  <div className="uploadContent">
                    <Icon name="images" size="massive" color="pink"/>
                    <p style={{color: "black", fontSize: "1.8vw", fontWeight: "700"}}>
                      Click or Drag a Photo of you smiling
                    </p>
                    <p style={{color: "black", fontSize: "1.1vw", fontStyle: "italic", fontWeight: "600", color: 'gray'}}>
                      **For best results use a clear photo showing your smile**
                    </p>
                    <Button inverted color="violet" size="huge">
                      Choose Picture
                    </Button>
                  </div>
                }
              />
            </div>
            :
            <div className="imageUploadedContainer">
              <img src={this.state.imageToDisplay} className="uploadedImage"/>
              <Button animated color="pink" size="massive" style={{marginTop: "5%"}}>
                <Button.Content visible>Perfect my Smile!</Button.Content>
                <Button.Content hidden>Go</Button.Content>
              </Button>
              <Button animated color="red" className="downButton" size="medium" style={{marginTop: "5%"}} onClick={(e) => this.resetPhoto()}>
                <Button.Content visible>Clear Photo</Button.Content>
                <Button.Content hidden>
                  <Icon name="trash" />
                </Button.Content>
              </Button>
            </div>
          }
          <ImageUpload />
        </div>
        
      </div>
    );
  }
}

export default App;
