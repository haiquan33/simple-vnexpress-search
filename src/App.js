import React, { Component } from 'react';
import logo from './logo.svg';
import Home from './components/Home';
import './App.css';
import 'antd/dist/antd.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Home/>
      </div>
    );
  }
}

export default App;
