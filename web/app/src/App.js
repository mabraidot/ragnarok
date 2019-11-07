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
import Power from './containers/Power';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

import HomeIcon from '@material-ui/icons/HomeRounded';
import RecipesIcon from '@material-ui/icons/ListAltRounded';
import SettingsIcon from '@material-ui/icons/SettingsRounded';
import PowerIcon from '@material-ui/icons/PowerSettingsNewRounded';

function App() {
  return (
      <BrowserRouter>
        <div className="App">
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
                  <Tab component={Link} value="/" to="/" label="Home" icon={<HomeIcon />} aria-label="home" />
                  <Tab component={Link} value="/recipes" to="/recipes" label="Recipes" icon={<RecipesIcon />} aria-label="recipes" />
                  <Tab component={Link} value="/settings" to="/settings" label="Settings" icon={<SettingsIcon />} aria-label="settings" />
                  <Tab component={Link} value="/power" to="/power" label="Power" icon={<PowerIcon />} aria-label="power" />
                </Tabs>
                <div className="App-main">
                  <Switch>
                    <Route path="/" push component={Home} />
                    <Route path="/recipes" push component={Home} />
                    <Route path="/settings" push component={Settings} />
                    <Route path="/power" push component={Power} />
                  </Switch>
                </div>
              </Fragment>
            )}
          />
        </div>
      </BrowserRouter>
  );
}

export default App;