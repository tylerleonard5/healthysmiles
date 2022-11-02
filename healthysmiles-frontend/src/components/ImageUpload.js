import React, { Component } from 'react';
import axios from 'axios';

class ImageUpload extends Component {

  state = {
    file: null,
    base64URL: "",
    ImgReturned:false
  }

  fileSelectedHandler = (event) => {
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
    console.log(this.state.file)
    axios.post('http://127.0.0.1:5000/api', {data: this.state.file})
      .then(res => {
        console.log(`response = ${typeof res.data}`)
        const name = (res.data.name)
        this.setState({
          ImgReturned:true,
          img:res.data
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
    })
  }

  render() {
    return (
      <div>
        <input type="file" onChange={this.fileSelectedHandler}/>
        <button onClick={this.fileUploadHandler}>Upload</button>
        {this.state.ImgReturned &&
        <img src= "http://localhost:5000/api" alt="mask_image"/>}
        <button onClick={this.newImage}>Clear Image</button>

      </div>
    );
  }
}

export default ImageUpload;