import logo from './logo.svg';
import './App.css';

function App() {

  const fileSelectedHandler = (event) =>{
    console.log(event);
  }

  return (
    <div className="App">
      <input type="file" onChange={fileSelectedHandler}/>
    </div>
  );
}

export default App;
