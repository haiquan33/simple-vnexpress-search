import React from 'react';
import { List } from 'antd';
import './ResultShow.css';
class ResultShow extends React.Component {
    constructor() {
        super();
        this.state = { someKey: 'someValue' };
    }

    render() {
        return <div>
            <List
                
                itemLayout="horizontal"
                dataSource={this.props.result}
                renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                           
                            title={<a target="_blank" rel="noopener noreferrer" href={item[0]}>{item[1]}</a>}
                            description={item[2]}
                        />
                    </List.Item>
                )}
            />
        </div>;
    }

    componentDidMount() {
        this.setState({ someKey: 'otherValue' });
    }
}

export default ResultShow;
