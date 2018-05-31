import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Paper, TextField, Typography, Button, Grid } from '@material-ui/core'
import { withRouter } from 'react-router-dom'
import { FixedSpace } from 'components/Utils'
import classNames from 'classnames'

import { User, Post, Store } from 'models'
import { sendPost } from 'models/actions'

const styles = theme => {
    const colors = theme.palette
    return {
        paper: {
            position: 'relative',
            paddingLeft: 25,
            paddingRight: 25,
            paddingTop: 15,
            paddingBottom: 15,
        },
        title: {
            color: colors.primary.main,
            fontSize: '1.6em',
            fontWeight: 'bold',
        },
        subtitle: {
            color: colors.primary.main,
            fontSize: '1em',
            fontWeight: 600,
        },
        textField: {
            background: colors.grey[200],
            borderRadius: 5,
            paddingTop: 5,
            paddingBottom: 5,
            paddingLeft: 15,
            paddingRight: 15,
        },
        mask: {
            position: 'absolute',
            top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(255, 255, 255, 0.5)',
            zIndex: 100
        },
        loginButton: {
            fontWeight: 'bold',
        },
        filter: {
            filter: 'blur(5px)',
        },
        hidden: {
            display: 'none',
        }
    } 
}

class PostForm extends Component {
    state = {
        title: '',
        content: '',
        user: User.placeholder()
    }

    componentWillMount() {
        this.setState({ user: User.current() })
        this.unsubscribe = Store.subscribe(() => {
            this.setState({ user: Store.getState().userEvent })
        })
    }

    componentWillUnmount() {
        this.unsubscribe()
    }

    handleChangeTitle = event => {
        this.setState({ title: event.target.value })
    }

    handleChangeContent = event => {
        this.setState({ content: event.target.value })
    }

    handleSubmit = () => {
        const post = new Post({
            title: this.state.title,
            content: this.state.content,
            reply_to: this.props.post ? this.props.post.transaction_id : null,
        })
        post.submit().then(post => {
            Store.dispatch(sendPost(post))
            this.setState({ title: '', content: ''})
        })
    }

    render () {
        const { classes, type } = this.props
        const { user } = this.state
        return (
            <Paper className={classNames('paper', classes.paper)}>
                <div className={user.user_id ? classes.hidden : classes.mask}>
                    <Grid container className="full-height" justify="center" alignItems="center">
                        <Grid item><Button className={classes.loginButton} variant="raised" color="secondary" size="large" onClick={() => this.props.history.push({ pathname: '/login', state: {from: this.props.location.pathname} })}>Login</Button></Grid>
                    </Grid>
                </div>
                <div className={user.user_id ? '' : classes.filter}>
                    <Typography className={classes.title}>Post a new {type}</Typography>
                    <FixedSpace size="sm"/>
                    <Typography className={classes.subtitle}>Title</Typography>
                    <TextField fullWidth className={classes.textField} InputProps={{disableUnderline: true}} onChange={this.handleChangeTitle}/>
                    <FixedSpace size="sm"/>
                    <Typography className={classes.subtitle}>Content</Typography>
                    <TextField fullWidth multiline rows="10" className={classes.textField} InputProps={{disableUnderline: true}} onChange={this.handleChangeContent} />
                    <FixedSpace size="sm"/>
                    <Button fullWidth variant="raised" color="secondary" size="large" onClick={this.handleSubmit}>
                        <Typography color="primary" style={{fontWeight: 'bold'}}>Publish {type}</Typography>
                    </Button>
                </div>
            </Paper>
        )
    }
}

export default withRouter(withStyles(styles)(PostForm))
