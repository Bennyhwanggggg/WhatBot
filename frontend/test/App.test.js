import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import { configure, shallow, mount } from 'enzyme';
import chai, { expect } from 'chai';
import App from '../src/components/App';
import Header from '../src/components/Header';
import chaiEnzyme from 'chai-enzyme';

import Adapter from 'enzyme-adapter-react-16';
import ChatRoom from '../src/components/ChatRoom';

configure({ adapter: new Adapter() });

describe('App Component testing', function() {

  it('App renders properly', () => {
    const wrapper = shallow(<App />);
    expect(wrapper).to.have.className('App');
  });

  it('App correctly render router', () => {
    const wrapper = mount(<App />);
    const test_router = wrapper.find(Router);
    expect(test_router).to.have.lengthOf(1);
    expect(test_router.find(Header)).to.have.lengthOf(1);
    expect(test_router.find(Switch)).to.have.lengthOf(1);
  });

  it('App correctly render routes', () => {
    const wrapper = shallow(<App />);
    const routes = wrapper.find(Route);
    expect(routes).not.to.have.lengthOf(0);

    const pathMap = routes.reduce((pathMap, route) => {
      const routeProp = route.props();
      pathMap[routeProp.path] = routeProp.component;
      return pathMap;
    }, {})
    expect(pathMap['/']).equal(ChatRoom);
  });

  chai.use(chaiEnzyme());

})