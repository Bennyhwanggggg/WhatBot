import React from 'react';
import { configure, shallow, mount } from 'enzyme';
import chai, { expect } from 'chai';
import Messages from '../src/components/Messages';
import chaiEnzyme from 'chai-enzyme';

import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Messages Component testing', function() {

  it('Single message renders properly', () => {
    const wrapper = shallow(<Messages/>);

    // Set test messages
    wrapper.setProps({ messages: [{member: "You", text: 'test string 1'}], 
                       currentMember: {username: "You", color: "#fb7f0a" }});

    // Check results                   
    expect(wrapper).to.have.className('Messages-list');
    expect(wrapper.find('.Message-content')).to.have.lengthOf(1);
  });

  it('Multiple same user message renders properly', () => {
    const wrapper = shallow(<Messages/>);

    // Set test messages
    wrapper.setProps({ messages: [{member: {username: "You", color: "#fb7f0a"}, text: 'test string 1'}, 
                                {member: {username: "You", color: "#fb7f0a"}, text: 'test string 2'}], 
                       currentMember: {username: "You", color: "#fb7f0a" }});

    // Check results                     
    expect(wrapper).to.have.className('Messages-list');
    expect(wrapper.find('.Message-content')).to.have.lengthOf(2);
    expect(wrapper.find('.currentMember')).to.have.lengthOf(2);
  });

  it('Multiple different user message renders properly', () => {
    const wrapper = shallow(<Messages/>);

    // Set test messages
    wrapper.setProps({ messages: [{member: {username: "You", color: "#fb7f0a"}, text: 'test string 1'}, 
                                {member: {username: "BOT", color: "#fb7f0a"}, text: 'test string 2'}], 
                       currentMember: {username: "You", color: "#fb7f0a" }});

    // Check results  
    expect(wrapper).to.have.className('Messages-list');
    expect(wrapper.find('.Message-content')).to.have.lengthOf(2);
    expect(wrapper.find('.currentMember')).to.have.lengthOf(1);
  });    

  chai.use(chaiEnzyme());

})