import React, { Component } from 'react';
import axios from 'axios';

class ImageUpload extends Component {

  state = {
    file: null,
    base64URL: "",
    ImgReturned:false,
    img: "",
    oldImage: null
  }

  fileSelectedHandler = (event) => {

    var img = document.createElement("img");
    img.src = URL.createObjectURL(event.target.files[0]);
    img.onload = () => {
      this.setState({oldImage: URL.createObjectURL(event.target.files[0])});
    }



    let { file } = this.state

    file = event.target.files[0]

    this.getbase64(event.target.files[0])
      .then(result => {
        file["base64"] = result
        this.setState({
          base64URL: result,
          file
        })

      })
      .catch(error => {
        console.log(error)
      })

    this.setState({
      file: event.target.files[0]
    })
  }

  getbase64 = (file) => {
    return new Promise(resolve => {
      let baseURL = ""
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        baseURL = reader.result
        resolve(baseURL)
      }
    });
  }

  fileUploadHandler = () => {
    this.setState({
      img:null
    })
    console.log(this.state.file)
    axios.post('http://127.0.0.1:5000/api', {data: this.state.file})
      .then(res => {
        console.log(`response = ${typeof res.data}`)
        const name = (res.data.name)
        this.setState({
          ImgReturned:true,
          img:"http://127.0.0.1:5000/api"
        })
      })
      .catch(error => {
        console.log(`error = ${error}`)
      })
  }
  newImage = () => {
    this.setState({
      ImgReturned:false,
      file: null,
      base64URL: "",
      img:null
    })
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler}/>
        {this.state.oldImage && <img src = {this.state.oldImage} style = {{height: "500px", width: "500px", objectFit: "contain"}}/>}
        <button onClick={this.fileUploadHandler}>Upload</button>
        {this.state.img &&
        <img src= {this.state.img} alt="mask_image"/>}
        <button onClick={this.newImage}>Clear Image</button>

      </div>
    );
  }
}

export default ImageUpload;