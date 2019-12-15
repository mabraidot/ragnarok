import React, { Component } from 'react';
import './Recipes.scss';
import ApiClient from './../../apiClient/ApiClient';
import Grow from '@material-ui/core/Grow';
import Button from '@material-ui/core/Button';
import Fab from '@material-ui/core/Fab';
import VisibilityIcon from '@material-ui/icons/Visibility';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import { withSnackbar } from 'notistack';

class Recipes extends Component {

  constructor(props) {
    super(props);
    this.state = {
      totalRows: 0,
      recipes: [],
      dialogOpen: false,
      dialogRecipeId: 0

    }
    this.fileUploadHandler = this.fileUploadHandler.bind(this);
    this.getRecipesHandler = this.getRecipesHandler.bind(this);
    this.handleDeleteClose = this.handleDeleteClose.bind(this);
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
      this.getRecipesHandler();
    });

  }

  handleSeeClick = (recipeId) => {
    console.log('see ', recipeId);
  }

  handleDeleteClick = (recipeId) => {
    this.setState({ dialogOpen: true, dialogRecipeId: recipeId });
  }

  handleDeleteClose = () => {
    this.setState({ dialogOpen: false, dialogRecipeId: 0 });
  };

  handleDeleteAction = (recipeId) => {
    this.setState({ dialogOpen: false, dialogRecipeId: 0 });
    if (recipeId > 0){
      ApiClient.deleteRecipe(recipeId).then((resp) => {
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
        this.getRecipesHandler();
      });
    }
  };

  render() {
    return(
      <Grow in={true}>
        <div className="Recipes">
          <Dialog
            open={this.state.dialogOpen}
            onClose={this.handleDeleteClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{"Delete the selected recipe?"}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                This operation is going to delete the recipe from the database. It can't be undone.
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleDeleteClose} color="secondary" autoFocus>Cancel</Button>
              <Button onClick={() => this.handleDeleteAction(this.state.dialogRecipeId)} color="primary">Delete</Button>
            </DialogActions>
          </Dialog>
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
              <div className="title">
                <h1>{recipe.name}</h1>
                <div className="icons">
                  <Fab className="button-see" onClick={() => this.handleSeeClick(recipe.id)} size="small" aria-label="see">
                    <VisibilityIcon fontSize="large" />
                  </Fab>
                  <Fab className="button-delete" onClick={() => this.handleDeleteClick(recipe.id)} size="small" aria-label="delete">
                    <DeleteForeverIcon fontSize="large" />
                  </Fab>
                </div>
              </div>
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