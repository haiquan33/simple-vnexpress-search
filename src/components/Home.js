import React from 'react';
import SearchBar from './SearchBar'
import ResultShow from './ResultShow'
class Home extends React.Component {
  constructor() {
    super();
    this.state = { someKey: 'someValue' ,result:[]};
    this.Search=this.Search.bind(this);
  }


  componentDidMount() {

    // var data={keyword:'Việt Nam'}
    // fetch('http://127.0.0.1:5000/query', {
    //   method: "POST", // *GET, POST, PUT, DELETE, etc.

    //   headers: {
    //       "Content-Type": "application/json; charset=utf-8",
    //       // "Content-Type": "application/x-www-form-urlencoded",
    //   },
    //   redirect: "follow", // manual, *follow, error
    //   referrer: "no-referrer", // no-referrer, *client
    //   body: JSON.stringify(data), // body data type must match "Content-Type" header
    // })
    // .then((response) => response.json())
    // .then(data => console.log(data))

  }

  Search(keyword) {
    var data = { keyword}
    fetch('http://127.0.0.1:5000/query', {
      method: "POST", // *GET, POST, PUT, DELETE, etc.

      headers: {
        "Content-Type": "application/json; charset=utf-8",
        // "Content-Type": "application/x-www-form-urlencoded",
      },
      redirect: "follow", // manual, *follow, error
      referrer: "no-referrer", // no-referrer, *client
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
      .then((response) => response.json())
      .then(result => this.setState({result}))
      // .then(data => console.log(data))
  }
  render() {
    return <div>
      <SearchBar Search={this.Search}/>
      <ResultShow result={this.state.result.articles}/>
    </div>;
  }


}

export default Home;
