import React from 'react';
import { configure, shallow, mount } from 'enzyme';
import chai, { expect } from 'chai';
import Input from '../src/components/Input';
import sinon from 'sinon';
import chaiEnzyme from 'chai-enzyme';

import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Input Component testing', function() {

  it('Input component renders properly', () => {
    const input = shallow(<Input />);
    expect(input).to.have.className('Input');
  });

  it('Input contains core components', () => {
    const input = mount(<Input />);
    expect(input.find('button')).to.have.lengthOf(1);
    expect(input.find('form')).to.have.lengthOf(1);
    expect(input.find('input')).to.have.lengthOf(1);
  });

  it('OnSubmit correctly clears message', () => {
    const onSendMessage = sinon.spy(); // use spy function as a place holder since onSendMessage is from props
    const input = mount(<Input onSendMessage={onSendMessage}/>);
    input.setState({text: 'test words'});
    input.find('button').simulate('submit');
    expect(input.state().text).to.equal('');
  });  

  chai.use(chaiEnzyme());

})