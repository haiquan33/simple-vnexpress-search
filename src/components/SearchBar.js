import React from 'react';
import { Input } from 'antd';
import './SearchBar.css';
const Search = Input.Search;
class SearchBar extends React.Component {
    constructor() {
        super();
        this.state = { someKey: 'someValue' };
    }

    render() {
        return <div class="SearchContainer">
            <Search
                placeholder="Tìm kiếm trên Vnexpress"
                enterButton="Search"
                size="large"
                onSearch={value => this.props.Search(value)}
            />
        </div>;
    }

    componentDidMount() {
        this.setState({ someKey: 'otherValue' });
    }
}

export default SearchBar;
