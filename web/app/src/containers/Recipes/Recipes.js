import React, { Component } from 'react';
import './Recipes.scss';
import ApiClient from './../../apiClient/ApiClient';
import Grow from '@material-ui/core/Grow';
import Button from '@material-ui/core/Button';
import { withSnackbar } from 'notistack';

class Recipes extends Component {

  constructor(props) {
    super(props);
      // this.state = {
      //   importedFile: null
      // }
      this.fileUploadHandler = this.fileUploadHandler.bind(this);
      this.getRecipesHandler();
  }

  getRecipesHandler() {
    ApiClient.getRecipes().then((resp) => {
      console.log('[API]', resp);
    });
  }

  fileUploadHandler(event) {

    const data = new FormData();
    data.append('file', event.target.files[0]);
    ApiClient.sendBeerXML(data).then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'info',
          persist: true,
        });
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });

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

export default withSnackbar(Recipes);