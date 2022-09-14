import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';

class App extends Component {

  state = {
    file: null,
    base64URL: ""
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
    console.log(this.state.base64URL)
    axios.post('http://127.0.0.1:5000/api', {data: this.state.file})
      .then(res => {
        console.log(`response = ${res.data}`)
        const name = (res.data.name)
      })
      .catch(error => {
        console.log(`error = ${error}`)
      })
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler}/>
        <button onClick={this.fileUploadHandler}>Upload</button>
      </div>
    );
  }
}

export default App;
