import React from 'react';
import Upload from './Upload';

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