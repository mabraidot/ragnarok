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
      unfinishedCooking: false,
      dialogOpen: false,
      dialogRecipeId: 0,
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: ''
    }
    this.fileUploadHandler = this.fileUploadHandler.bind(this);
    this.getRecipesHandler = this.getRecipesHandler.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  componentDidMount() {
    this.getRecipesHandler();
  }

  getRecipesHandler() {
    ApiClient.getRecipes().then((resp) => {
      const response = JSON.parse(resp);
      console.log('[API]', response);

      if (response.unfinished) {
        this.setState({ dialogOpen: true, 
          dialogRecipeId: response.unfinished.recipe_id, 
          dialogAction: 'unfinished',
          dialogTitle: 'There is an unfinished cooking process',
          dialogDescription: `You can resume the cooking process or delete it to stop seing this message.` 
        });
      }


      this.setState({ 
        unfinishedCooking: response.unfinished, 
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
          variant: 'success',
        });
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
      if (resp.persistent_notice) {
        this.props.enqueueSnackbar(resp.persistent_notice, { 
          variant: 'success',
          persist: true,
        });
      }
      if (resp.persistent_error) {
        this.props.enqueueSnackbar(resp.persistent_error, { 
          variant: 'error',
          persist: true,
        });
      }
      this.getRecipesHandler();
    });

  }

  handleClose = () => {
    this.setState({ 
      dialogOpen: false, 
      dialogRecipeId: 0, 
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: '' 
    });
  };

  handleSeeClick = (recipeId) => {
    const recipe = JSON.parse(this.state.recipes[recipeId].beer_json);

    let description = '';
    let item = '';
    description += `Boil Time: <strong>${parseFloat(recipe.RECIPES.RECIPE.BOIL_TIME).toFixed(2)} minutes</strong><br />`;
    description += `Boil Size: <strong>${parseFloat(recipe.RECIPES.RECIPE.BOIL_SIZE).toFixed(2)} liters</strong>`;

    description += '<h3>MASH</h3>';
    description += `<strong>${recipe.RECIPES.RECIPE.MASH.NAME}</strong><br />`;
    for (let i in recipe.RECIPES.RECIPE.MASH.MASH_STEPS.MASH_STEP) {
      item = recipe.RECIPES.RECIPE.MASH.MASH_STEPS.MASH_STEP[i];
      description += `${(parseInt(i)+1)}). ${item.NAME} ${item.DISPLAY_STEP_TEMP}: <strong>${item.DESCRIPTION}</strong><br />`;
    }

    
    let descriptionMash = '';
    let orderMash = 0;
    let descriptionBoil = '';
    let orderBoil = 0;
    let descriptionMisc = '';
    let orderMisc = 0;
    if (typeof recipe.RECIPES.RECIPE.HOPS.HOP.length === 'undefined') {
      const hopsObj = recipe.RECIPES.RECIPE.HOPS.HOP;
      recipe.RECIPES.RECIPE.HOPS.HOP = [];
      recipe.RECIPES.RECIPE.HOPS.HOP.push(hopsObj);
    }
    if (typeof recipe.RECIPES.RECIPE.MISCS.MISC.length === 'undefined') {
      const adjunctsObj = recipe.RECIPES.RECIPE.MISCS.MISC;
      recipe.RECIPES.RECIPE.MISCS.MISC = [];
      recipe.RECIPES.RECIPE.MISCS.MISC.push(adjunctsObj);
    }
    let adjuncts = [...recipe.RECIPES.RECIPE.HOPS.HOP, ...recipe.RECIPES.RECIPE.MISCS.MISC];
    adjuncts.sort((a, b) => (parseFloat(a.TIME) < parseFloat(b.TIME)) ? 1 : -1);
    description += '<h3>HOPS and ADJUNCTS</h3>';
    for (let i in adjuncts) {
      item = adjuncts[i];
      if (item.USE === 'Mash') {
        orderMash += 1;
        descriptionMash += `${orderMash}). ${item.DISPLAY_TIME}: <strong>${item.NAME}</strong> ${item.USE} ${item.DISPLAY_AMOUNT}<br />`;
      } else if (item.USE === 'First Wort') {
        orderMash += 1;
        descriptionMash += `${orderBoil}). ${0.1} mins: <strong>${item.NAME}</strong> ${item.USE} ${item.DISPLAY_AMOUNT}<br />`;
      } else if (item.USE === 'Boil' || item.USE === 'Aroma') {
        orderBoil += 1;
        descriptionBoil += `${orderBoil}). ${item.DISPLAY_TIME}: <strong>${item.NAME}</strong> ${item.USE} ${item.DISPLAY_AMOUNT}<br />`;
      } else {
        orderMisc += 1;
        descriptionMisc += `${orderMisc}). ${item.DISPLAY_TIME}: <strong>${item.NAME}</strong> ${item.USE} ${item.DISPLAY_AMOUNT}<br />`;
      }
    }
    if (descriptionMash !== '') {
      description += 'Mash ----------------------------------------<br />';
      description += descriptionMash;
    }
    if (descriptionBoil !== '') {
      description += 'Boil ----------------------------------------<br />';
      description += descriptionBoil;
    }
    if (descriptionMisc !== '') {
      description += 'Misc ----------------------------------------<br />';
      description += descriptionMisc;
    }


    this.setState({ 
      dialogOpen: true, 
      dialogRecipeId: recipeId, 
      dialogAction: 'cook',
      dialogTitle: this.state.recipes[recipeId].name,
      dialogDescription: description
    });

  }

  handleSeeAction = (recipeId) => {
    this.setState({ 
      dialogOpen: false, 
      dialogRecipeId: 0, 
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: '' 
    });
    console.log('see ', this.state.recipes[recipeId]);

    if (typeof this.state.recipes[recipeId].id !== 'undefined') {
      
      this.props.enqueueSnackbar('Setting up everything for the cooking process. Please wait ...', { 
        variant: 'success',
      });

      ApiClient.cook(this.state.recipes[recipeId].id).then((resp) => {
        console.log('[API]', resp);
        if (resp.notice) {
          this.props.enqueueSnackbar(resp.notice, { 
            variant: 'success',
          });
          this.props.history.push('/')
        }
        if (resp.error) {
          this.props.enqueueSnackbar(resp.error, { 
            variant: 'error',
          });
        }
        if (resp.persistent_notice) {
          this.props.enqueueSnackbar(resp.persistent_notice, { 
            variant: 'success',
            persist: true,
          });
          this.props.history.push('/')
        }
        if (resp.persistent_error) {
          this.props.enqueueSnackbar(resp.persistent_error, { 
            variant: 'error',
            persist: true,
          });
        }
      });
    }

  }

  handleDeleteClick = (recipeId) => {
    this.setState({ dialogOpen: true, 
      dialogRecipeId: recipeId, 
      dialogAction: 'delete',
      dialogTitle: 'Delete the selected recipe?',
      dialogDescription: `This operation is going to delete the recipe from the database. It can't be undone.` 
    });
  }

  handleDeleteAction = (recipeId) => {
    this.setState({ 
      dialogOpen: false, 
      dialogRecipeId: 0, 
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: '' 
    });

    if (recipeId > 0) {
      ApiClient.deleteRecipe(recipeId).then((resp) => {
        console.log('[API]', resp);
        if (resp.notice) {
          this.props.enqueueSnackbar(resp.notice, { 
            variant: 'success',
          });
        }
        if (resp.error) {
          this.props.enqueueSnackbar(resp.error, { 
            variant: 'error',
          });
        }
        if (resp.persistent_notice) {
          this.props.enqueueSnackbar(resp.persistent_notice, { 
            variant: 'success',
            persist: true,
          });
        }
        if (resp.persistent_error) {
          this.props.enqueueSnackbar(resp.persistent_error, { 
            variant: 'error',
            persist: true,
          });
        }
        this.getRecipesHandler();
      });
    }
  };


  handleSeeUnfinishedAction = (recipeId) => {
    this.setState({ 
      dialogOpen: false, 
      dialogRecipeId: 0, 
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: '' 
    });
    console.log('resume cooking ', this.state.unfinishedCooking.recipe_id);

    if (typeof this.state.unfinishedCooking.recipe_id !== 'undefined') {
      ApiClient.cookUnfinished(this.state.unfinishedCooking.recipe_id).then((resp) => {
        console.log('[API]', resp);
        if (resp.notice) {
          this.props.enqueueSnackbar(resp.notice, { 
            variant: 'success',
          });
          this.props.history.push('/')
        }
        if (resp.error) {
          this.props.enqueueSnackbar(resp.error, { 
            variant: 'error',
          });
        }
        if (resp.persistent_notice) {
          this.props.enqueueSnackbar(resp.persistent_notice, { 
            variant: 'success',
            persist: true,
          });
          this.props.history.push('/')
        }
        if (resp.persistent_error) {
          this.props.enqueueSnackbar(resp.persistent_error, { 
            variant: 'error',
            persist: true,
          });
        }
      });
    }

  }


  handleDeleteUnfinishedAction = (recipeId) => {
    this.setState({ 
      dialogOpen: false, 
      dialogRecipeId: 0, 
      dialogAction: '',
      dialogTitle: '',
      dialogDescription: '' 
    });

    ApiClient.deleteUnfinishedRecipe().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'success',
        });
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
      if (resp.persistent_notice) {
        this.props.enqueueSnackbar(resp.persistent_notice, { 
          variant: 'success',
          persist: true,
        });
      }
      if (resp.persistent_error) {
        this.props.enqueueSnackbar(resp.persistent_error, { 
          variant: 'error',
          persist: true,
        });
      }
      this.getRecipesHandler();
    });
  };

  render() {
    return(
      <Grow in={true}>
        <div className="Recipes">
          <Dialog
            open={this.state.dialogOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{this.state.dialogTitle}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                <span dangerouslySetInnerHTML={{__html: this.state.dialogDescription}} />
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="secondary" autoFocus>Cancel</Button>
              {(this.state.dialogAction === 'delete') && (
                <Button onClick={() => this.handleDeleteAction(this.state.dialogRecipeId)} color="primary">Delete</Button>
              )}
              {(this.state.dialogAction === 'cook') && (
                <Button onClick={() => this.handleSeeAction(this.state.dialogRecipeId)} color="primary">Cook</Button>
              )}
              {(this.state.unfinishedCooking && this.state.dialogAction === 'unfinished') ? (
                <div>
                  <Button onClick={() => this.handleDeleteUnfinishedAction(this.state.dialogRecipeId)} color="primary">Delete</Button>
                  <Button onClick={() => this.handleSeeUnfinishedAction(this.state.dialogRecipeId)} color="primary">Cook</Button>
                </div>
              ) : ('')}
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
                  <Fab className="button-see" onClick={() => this.handleSeeClick(key)} size="small" aria-label="see">
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