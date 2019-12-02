import React, { Fragment } from 'react';
import {
  BrowserRouter,
  Switch,
  Route,
  Link
} from "react-router-dom";

import './App.css';
import Home from './containers/Home';
import Recipes from './containers/Recipes';
import Settings from './containers/Settings';
import Power from './containers/Power';
import Advanced from './containers/Advanced';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

import HomeIcon from '@material-ui/icons/HomeRounded';
import RecipesIcon from '@material-ui/icons/ListAltRounded';
import SettingsIcon from '@material-ui/icons/SettingsRounded';
import PowerIcon from '@material-ui/icons/PowerSettingsNewRounded';

import { SnackbarProvider } from 'notistack';

function App() {

  const pages = [
    '/',
    '/recipes',
    '/settings',
    '/power',
  ];

  return (
    <SnackbarProvider 
      dense
      autoHideDuration={3000}
      maxSnack={5} 
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'left',
      }}
    >
      <BrowserRouter>
        <div className="App">
          <Route
            path="/"
            render={({ location }) => (
              <Fragment>
                <div className="App-header">
                  <Tabs
                    value={(pages.indexOf(location.pathname) === -1) ? '/' : location.pathname}
                    // onChange={handleTabChange}
                    variant="fullWidth"
                    aria-label="icon tabs"
                  >
                    <Tab component={Link} value="/" to="/" label="Home" icon={<HomeIcon />} aria-label="home" />
                    <Tab component={Link} value="/recipes" to="/recipes" label="Recipes" icon={<RecipesIcon />} aria-label="recipes" />
                    <Tab component={Link} value="/settings" to="/settings" label="Settings" icon={<SettingsIcon />} aria-label="settings" />
                    <Tab component={Link} value="/power" to="/power" label="Power" icon={<PowerIcon />} aria-label="power" />
                  </Tabs>
                </div>
                <div className="App-main">
                  <Switch>
                    <Route path="/advanced" push component={Advanced} />
                    <Route path="/recipes" push component={Recipes} />
                    <Route path="/settings" push component={Settings} />
                    <Route path="/power" push component={Power} />
                    <Route path="/" push component={Home} />
                  </Switch>
                </div>
              </Fragment>
            )}
          />
        </div>
      </BrowserRouter>
    </SnackbarProvider>
  );
}

export default App;