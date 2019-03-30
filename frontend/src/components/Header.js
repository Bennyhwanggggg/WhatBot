import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
      <div className="ui pointing menu App-header">
        <div className="header item">
            <Link to="/">
                WhatBot
            </Link>
        </div>
        <div className="item">
          <Link to="/upload">
            Upload training data
          </Link>
        </div>
        <div className="right item">
            Login
        </div>
      </div>
    );
};
  
export default Header;