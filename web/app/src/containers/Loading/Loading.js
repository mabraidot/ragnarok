import React, { Component } from 'react';
import './Loading.scss';
import Grow from '@material-ui/core/Grow';
import Socket from './../../components/Socket/Socket';

class Loading extends Component {
    constructor(props) {
        super(props);
        this.state = {
          socket: new Socket(),
        };
    }

    render() {
        return(
            <Grow in={true}>
                <div className="Loading"></div>
            </Grow>
        );
    }

}

export default Loading;