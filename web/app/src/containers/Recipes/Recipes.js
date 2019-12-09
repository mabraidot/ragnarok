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

    // this.setState({
    //   importedFile: event.target.files[0],
    // });
    
    // let fileReader = new FileReader();
    // fileReader.onloadend = (e) => {
    //   // console.log('[RECIPES] File upload: ', fileReader.result);
    //   ApiClient.sendBeerXML(fileReader.result).then((resp) => {
    //     console.log('[API]', resp);
    //     if (resp.notice) {
    //       this.props.enqueueSnackbar(resp.notice, { 
    //         variant: 'info',
    //         persist: true,
    //       });
    //     }
    //     if (resp.error) {
    //       this.props.enqueueSnackbar(resp.error, { 
    //         variant: 'error',
    //       });
    //     }
    //   });
    // };
    // fileReader.readAsText(event.target.files[0]);
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