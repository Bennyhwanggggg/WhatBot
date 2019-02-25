import React, {Component} from 'react'

const data = [
    {
        senderId: "perborgen",
        text: "who'll win?"
    },
    {
        senderId: "janedoe",
        text: "who'll win?"
    }
]

class MessageList extends Component {
    render() {
        return (
            <div className="message-list">
                {data.map((message, index) => {
                    return (
                        <div key={"message-"+index} className="message">
                            <div>{message.senderId}</div>
                            <div>{message.text}</div>
                        </div>
                    )
                })}
            </div>
        )
    }
}

export default MessageList