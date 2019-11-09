import React, { Component } from 'react';
import './Recipes.scss';
import Grow from '@material-ui/core/Grow';

class Recipes extends Component {

  render() {
    return(
      <Grow in={true}>
        <div className="Recipes">
          <h1>Recipes</h1>
          <p>
            Recipes' page
          </p>
        </div>
      </Grow>
    );
  }
}

export default Recipes;