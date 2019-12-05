import React, { Component } from 'react';
import './Recipes.scss';
import Grow from '@material-ui/core/Grow';
import Button from '@material-ui/core/Button';

class Recipes extends Component {

  constructor(props) {
    super(props);
      this.state = {
        importedFile: null
      }
      this.fileUploadHandler = this.fileUploadHandler.bind(this);
  }

  fileUploadHandler(event){
    this.setState({
      importedFile: event.target.files[0],
    });
    console.log('[RECIPES] File upload: ', event.target.files[0]);
  }

  render() {
    return(
      <Grow in={true}>
        <div className="Recipes">
          <h1>Recipes</h1>
          <div>
            <Button
              variant="contained"
              component="label"
              size="large" 
              className="button-upload"
            >
              Import new Recipe
              <input
                type="file"
                onChange={this.fileUploadHandler}
                style={{ display: "none" }}
              />
            </Button>
          </div>
        </div>
      </Grow>
    );
  }
}

export default Recipes;