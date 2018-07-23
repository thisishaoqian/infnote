import React, { Component } from 'react'
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core'
import { AlertStore } from 'models'
import { alertAction } from 'models/actions'

class Alert extends Component {
    state = {
        status: {
            open: false,
            title: '',
            content: '',
        }
    }

    componentWillMount() {
        this.unsubscribe = AlertStore.subscribe(() => {
            let status = AlertStore.getState()
            this.setState({ status })
        })
    }

    componentWillUnmount() {
        this.unsubscribe()
    }

    handleClose = () => {
        let status = this.state.status
        this.setState({ 
            status: {
                open: false,
                title: status.title,
                content: status.content
            } 
        })
    }

    render() {
        const { status } = this.state
        return (
            <Dialog
                open={status.open}
                onClose={this.handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">{ status.title }</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        { status.content }
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={this.handleClose} color="primary" autoFocus>
                        OK
                    </Button>
                </DialogActions>
            </Dialog>
        )
    }
}

export default Alert
export const showAlert = (title = 'API Server Error', content = 'An internal server error occured. Please try later.') => {
    AlertStore.dispatch(alertAction({
        open: true,
        title,
        content
    }))
}
