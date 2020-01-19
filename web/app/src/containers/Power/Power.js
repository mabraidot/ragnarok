import React, { Component } from 'react';
import './Power.scss';
import Grow from '@material-ui/core/Grow';
import ApiClient from './../../apiClient/ApiClient';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import PowerIcon from '@material-ui/icons/PowerSettingsNewRounded';

import { withSnackbar } from 'notistack';

class Power extends Component {
  
  constructor(props) {
    super(props)
    this.state = {
      hover: false,
      dialogOpen: false,
      dialogTitle: '',
      dialogDescription: ''
    }
  }
  

  handleClick = () => {
    this.setState({ hover: !this.state.hover });
  }

  handleOpen = () => {
      this.setState({ 
        dialogOpen: true, 
        dialogTitle: 'Power Off',
        dialogDescription: 'Are you sure to turn the machine off?', 
      });
  }


  handleClose = () => {
    this.setState({ 
      dialogOpen: false, 
      dialogTitle: '',
      dialogDescription: ''
    });
  };

  handleContinueAction = () => {
    if (this.state.dialogOpen) {
      this.handleClose();
      ApiClient.powerOff().then((resp) => {
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
      });
    }
  }
  
  render() {
    return(
      <Grow in={true}>
        <div className="Power-button">
          <Dialog
            open={this.state.dialogOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{this.state.dialogTitle}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                {this.state.dialogDescription}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="secondary" autoFocus>Cancel</Button>
              <Button onClick={this.handleContinueAction} color="primary">Continue</Button>
            </DialogActions>
          </Dialog>
          
          <PowerIcon className={(this.state.hover) ? "button-hover" : "button"} onClick={this.handleOpen} onTouchStart={this.handleClick} onTouchEnd={this.handleClick} />
          <p>Power Off</p>
        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Power);