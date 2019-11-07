import React, { Fragment } from 'react';
import {
  BrowserRouter,
  Switch,
  Route,
  Link
} from "react-router-dom";

import './App.css';
import Home from './containers/Home';
import Settings from './containers/Settings';
import Grid from '@material-ui/core/Grid';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import PhoneIcon from '@material-ui/icons/Phone';
import FavoriteIcon from '@material-ui/icons/Favorite';
import PersonPinIcon from '@material-ui/icons/PersonPin';

function App() {
  return (
      <BrowserRouter>
        <div className="App">
          {/* <Grid container justify="center" className="App-menu">
            <Grid item xs><Link to="/">Home</Link></Grid>
            <Grid item xs><Link to="/recipes">Recipes</Link></Grid>
            <Grid item xs><Link to="/settings">Settings</Link></Grid>
            <Grid item xs><Link to="/powerOff">Power off</Link></Grid>
          </Grid> */}

          <Route
            path="/"
            render={({ location }) => (
              <Fragment>
                <Tabs
                  value={location.pathname}
                  // onChange={handleTabChange}
                  variant="fullWidth"
                  indicatorColor="secondary"
                  textColor="secondary"
                  aria-label="icon tabs"
                >
                  <Tab component={Link} value="/" to="/" label="Home" icon={<PhoneIcon />} aria-label="home" />
                  <Tab component={Link} value="/recipes" to="/recipes" label="Recipes" icon={<PersonPinIcon />} aria-label="recipes" />
                  <Tab component={Link} value="/settings" to="/settings" label="Settings" icon={<FavoriteIcon />} aria-label="settings" />
                  <Tab component={Link} value="/powerOff" to="/powerOff" label="Power Off" icon={<PersonPinIcon />} aria-label="poweroff" />
                </Tabs>
                <Grid container justify="center" className="App-main">
                  <Switch>
                    <Route path="/settings" push component={Settings} />
                    <Route path="/" push component={Home} />
                  </Switch>
                </Grid>
              </Fragment>
            )}
          />
        </div>
      </BrowserRouter>
  );
}

export default App;