import React from 'react';
import Login from './Login';

const Header = () => {
    return (
      <div className="ui pointing menu App-header">
        <div class="header item">
            WhatBot
        </div>
        <Login/>
      </div>
    );
  };
  
  export default Header;