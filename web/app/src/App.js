import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import './App.css';
import Home from './containers/Home';
import Settings from './containers/Settings';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/settings">Settings</Link></li>
            </ul>
          </nav>
        </header>
        <main className="App-main">
          <Switch>
            <Route path="/settings" push component={Settings} />
            <Route path="/" push component={Home} />
          </Switch>
        </main>
        <footer className="App-footer">
          <p>Footer</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;