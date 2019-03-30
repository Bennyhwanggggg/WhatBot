import React, { Component } from 'react';
import Dropzone from './Dropzone';
import './Upload.css';
import Progress from './Progress';
import baseline_check_circle from "./baseline-check_circle-24px.svg";

class Upload extends Component {
    constructor (props) {
        super(props)
        this.state = {
            files: [],
            uploading: false,
            uploadProgress: {},
            successfullUploaded: false,
            alert: ""
        }

        this.onFilesAdded = this.onFilesAdded.bind(this)
        this.uploadFiles = this.uploadFiles.bind(this)
        this.sendRequest = this.sendRequest.bind(this)
        this.renderActions = this.renderActions.bind(this)
    }

    onFilesAdded = (files) => {
        this.setState(prevState => ({
            files: prevState.files.concat(files)
        }))
        this.setState({alert: ""})
    }

    async uploadFiles () {
        if (!this.state.files.length) {
            this.setState({alert: "No files selected"})
            return;
        }
        this.setState({ uploadProgress: {}, uploading: true, alert: "" })
        const promises = []
        this.state.files.forEach(file => {
            promises.push(this.sendRequest(file))
        })
        try {
            await Promise.all(promises)
            this.setState({ successfullUploaded: true, uploading: false })
        } catch (e) {
            this.setState({ successfullUploaded: true, uploading: false })
        }
    }

    sendRequest = (file) => {
        return new Promise((resolve, reject) => {
            const req = new XMLHttpRequest()

            req.upload.addEventListener('progress', event => {
                if (event.lengthComputable) {
                    const copy = { ...this.state.uploadProgress }
                    copy[file.name] = {
                        state: 'pending',
                        percentage: (event.loaded / event.total) * 100
                    }
                    this.setState({ uploadProgress: copy })
                }
            })

            req.upload.addEventListener('load', event => {
                const copy = { ...this.state.uploadProgress }
                copy[file.name] = { state: 'done', percentage: 100 }
                this.setState({ uploadProgress: copy })
                resolve(req.response)
            })

            req.upload.addEventListener('error', event => {
                const copy = { ...this.state.uploadProgress }
                copy[file.name] = { state: 'error', percentage: 0 }
                this.setState({ uploadProgress: copy })
                reject(req.response)
            })

            const formData = new FormData()
            formData.append('file', file, file.name)

            const dev = 'http://localhost:9999';
            const prod = `https://${process.env.REACT_APP_BACKEND_NAME}.herokuapp.com`
            const backendURL = process.env.NODE_ENV === 'development' ? dev : prod

            req.open('POST', `${backendURL}/upload`)
            req.send(formData)
        })
    }

    renderProgress = (file) => {
        const uploadProgress = this.state.uploadProgress[file.name]
        if (this.state.uploading || this.state.successfullUploaded) {
            return (
                <div className='ProgressWrapper'>
                <Progress progress={uploadProgress ? uploadProgress.percentage : 0} />
                <img
                    className='CheckIcon'
                    alt='done'
                    src={baseline_check_circle}
                    style={{opacity: uploadProgress && uploadProgress.state === 'done' ? 0.5 : 0}}
                />
                </div>
            )
        }
    }

    renderActions = () => {
        if (this.state.successfullUploaded) {
            return (
                <button
                    onClick={() => this.setState({ files: [], successfullUploaded: false })}
                    className="Dropzone-upload"
                >
                Clear
                </button>
            )
        } else {
            return (
                <button
                    disabled={this.state.files.length < 0 || this.state.uploading}
                    onClick={this.uploadFiles}
                    className="Dropzone-upload"
                >
                Upload
                </button>
            )
         }
    }

    renderError = () => {
        if (this.state.alert !== "") {
            return (
                <div className='ui warning message'>{this.state.alert}</div>
            )
        }
    }

    render () {
        return (
            <div className='Upload'>
                <div className='Content'>
                    <div>
                        <Dropzone
                        onFilesAdded={this.onFilesAdded}
                        disabled={this.state.uploading || this.state.successfullUploaded}
                        />
                    </div>
                    <div className='Files'>
                        {this.state.files.map(file => {
                        return (
                            <div key={file.name} className='Row'>
                            <span className='Filename'>{file.name}</span>
                            {this.renderProgress(file)}
                            </div>
                        )
                        })}
                    </div>
                </div>
                {this.renderError()}
                <div className='Actions'>{this.renderActions()}</div>
            </div>
        )
    }
}

export default Upload;
