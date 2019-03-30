import React from 'react';

const Header = () => {
    return (
      <div className="ui pointing menu App-header">
        <div className="header item">
            WhatBot
        </div>
        <div className="item Card">
          <Upload />
        </div>
        <div className="right item">
            Login
        </div>
      </div>
    );
  };
  
  export default Header;