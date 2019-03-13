import React from 'react';
import { configure, shallow } from 'enzyme';
import chai, { expect } from 'chai';
import chaiEnzyme from 'chai-enzyme';

import Adapter from 'enzyme-adapter-react-16';
import ChatRoom from '../src/components/ChatRoom';
import Input from '../src/components/Input';
import Messages from '../src/components/Messages';

configure({ adapter: new Adapter() });

describe('Chatroom Component testing', function() {

  it('Chatroom renders properly', () => {
    const wrapper = shallow(<ChatRoom />);
    expect(wrapper).not.to.have.className('App');
    expect(wrapper.find(Input)).to.have.lengthOf(1);
    expect(wrapper.find(Messages)).to.have.lengthOf(1);
  });

  chai.use(chaiEnzyme());

})