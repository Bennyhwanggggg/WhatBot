import React, { Component } from 'react';
import { connect } from 'react-redux';


class Messages extends Component {

    renderMessages() {
        return this.props.messages.map( message => {
            // TODO: remove hardcoded classname by getting them from msg data
            // These are "Messages-message currentMember" and username, color
            return (
                <li className="Messages-message currentMember" key={message.id}> 
                    <span className="avatar" 
                    style={{backgroundColor: "red"}}/>
                    <div className="Message-content">
                        <div className="username">
                            You
                        </div>
                        <div className="text">{message.inputValue}</div>
                    </div>
                </li>
            )
        });
    }

    render() {
        return (
            <ul className="Messages-list">
                {this.renderMessages()}
            </ul>
        );  
        // const {messages} = this.props;
        // if (messages){
        //     return (
        //         <ul className="Messages-list">
        //             {messages.map(m => this.renderMsg(m))}
        //         </ul>
        //     );
        // } else {
        //     return (
        //         <ul className="Messages-list">
        //         </ul>
        //     );
        // }
    }
    // // get list of message from redux store?
    // renderMsg(message) {
    //     const {member, text} = message;
    //     const {currentMember} = this.props;
    //     const messageFromMe = currentMember.username === member.username;
    //     const className = messageFromMe ?  "Messages-message currentMember" : "Messages-message";
    //     return (
    //         <li className={className}>
    //             <span className="avatar" 
    //             style={{backgroundColor: member.color}}/>
    //             <div className="Message-content">
    //                 <div className="username">
    //                     {member.username}
    //                 </div>
    //                 <div className="text">{text}</div>
    //             </div>
    //         </li>
    //     )
    // }
}

const mapStateToProps = (state) => {
    return {messages: Object.values(state.messages) }
}

export default connect(mapStateToProps)(Messages);