import React, { Component } from 'react';
import './App.css';
import ImageUpload from './components/ImageUpload.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <ImageUpload/>
      </div>
    );
  }
}

export default App;
