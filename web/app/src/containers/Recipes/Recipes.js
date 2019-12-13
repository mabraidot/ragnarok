import React, { Component } from 'react';
import './Recipes.scss';
import ApiClient from './../../apiClient/ApiClient';
import Grow from '@material-ui/core/Grow';
import Button from '@material-ui/core/Button';
import { withSnackbar } from 'notistack';

class Recipes extends Component {

  constructor(props) {
    super(props);
    this.state = {
      totalRows: 0,
      recipes: []
    }
    this.fileUploadHandler = this.fileUploadHandler.bind(this);
    this.getRecipesHandler = this.getRecipesHandler.bind(this);
  }

  componentDidMount() {
    this.getRecipesHandler();
  }

  getRecipesHandler() {
    ApiClient.getRecipes().then((resp) => {
      const response = JSON.parse(resp);
      console.log('[API]', response);
      this.setState({ 
        totalRows: response.totalRows, 
        recipes: response.recipes 
      });
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
          <div className="total-rows">
            <div>Total: <strong>{this.state.totalRows}</strong></div>
            <div className="import-button">
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
          {this.state.recipes.map((recipe, key) => (
            <div className="row" key={key}>
              <div className="title">{recipe.name}</div>
              <div className="style">{recipe.style_name} (<strong>{recipe.style_category}</strong>)</div>
              <div className="data">
                <div className="type"><strong>{recipe.type_name}</strong></div>
                <div className="og">OG: <strong>{recipe.original_gravity}</strong></div>
                <div className="fg">FG: <strong>{recipe.final_gravity}</strong></div>
                <div className="ibu"><strong>{recipe.ibu}</strong></div>
                <div className="abv">ABV: <strong>{recipe.abv}</strong></div>
                <div className="color">Color: <strong>{recipe.color}</strong></div>
              </div>
              <div className="dates">
                <div className="created">Created: <strong>{recipe.created}</strong></div>
                <div className="cooked">Cooked: <strong>{recipe.cooked || '--'}</strong></div>
              </div>
            </div>
          ))}
        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Recipes);