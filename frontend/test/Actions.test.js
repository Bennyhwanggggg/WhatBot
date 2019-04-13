import configureStore from 'redux-mock-store'
import thunk from 'redux-thunk';
import nock from 'nock';
import * as actions from '../src/actions';
import { MESSAGE_SENT, MESSAGE_RECIEVED } from '../src/actions/types';
import chai, { expect } from 'chai';
import chaiEnzyme from 'chai-enzyme';
import sinon from 'sinon';

const middlewares = [thunk]
const mockStore = configureStore(middlewares)


describe('Actions tests', function() {

    it('Send message action test', () => {
        const initialState = {}
        const store = mockStore(initialState)

        const fakeServer = sinon.fakeServer.create()
        fakeServer.respondWith('POST', '/message', 
                                [200, { "Content-Type": "application/json"},
                                '{ "type": "MESSAGE_SENT" }'])

        store.dispatch(actions.sendMessage({inputValue: 'Test message 1'})).then(() => {
        const actions = store.getActions();
        expect(actions[0].type).to.be.equal(MESSAGE_SENT);
        expect(actions[1].type).to.be.equal(MESSAGE_RECIEVED);
        })    
        
    });

    chai.use(chaiEnzyme());

})