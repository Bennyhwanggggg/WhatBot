import React from 'react';
import { configure, shallow, mount } from 'enzyme';
import chai, { expect } from 'chai';
import App from '../src/components/App';
import Input from '../src/components/Input';
import Header from '../src/components/Header';
import Messages from '../src/components/Messages';
import chaiEnzyme from 'chai-enzyme';

import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('App Component testing', function() {

  it('App renders properly', () => {
    const wrapper = shallow(<App />);
    expect(wrapper).to.have.className('App');
  });

  it('App contains core components', () => {
    const wrapper = mount(<App />);
    expect(wrapper.find(Header)).to.have.lengthOf(1);
    expect(wrapper.find(Input)).to.have.lengthOf(1);
    expect(wrapper.find(Messages)).to.have.lengthOf(1);
  });

  chai.use(chaiEnzyme());

})