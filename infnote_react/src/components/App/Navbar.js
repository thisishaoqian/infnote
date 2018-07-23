import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Link, withRouter } from 'react-router-dom'
import { AppBar, Toolbar, Avatar, Typography, Grid, IconButton, Menu, MenuItem } from '@material-ui/core'
import logo from 'assets/infnote-logo.png'
import avatar_placeholder from 'assets/avatar-placeholder.svg'

import { User, Store } from 'models'
import { HOME } from 'config'

const styles = {
    navbar: {
        height: 80,
        backgroundColor: 'white',
    },
    toolbar: {
        height: 80,
        justifyContent: 'space-between'
    },
    name: {
        fontSize: '1.2em',
        fontWeight: 'bold',
        paddingRight: 15,
        paddingLeft: 15,
    }
}


class Navbar extends Component {
    state = {
        menuAnchor: null,
        user: User.placeholder()
    }

    componentWillMount() {
        this.setState({ user: User.current() })
        this.unsubscribe = Store.subscribe(() => {
            const user = Store.getState().userEvent
            this.setState({ user })
        })
    }

    componentWillUnmount() {
        this.unsubscribe()
    }

    handleAvatarClick = event => {
        if (this.state.user.user_id) {
            this.setState({ menuAnchor: event.target })
        } else {
            this.props.history.push({ pathname: '/sign/in', state: {from: this.props.location.pathname} })
        }
    }

    handleMenuClose = () => {
        this.setState({ menuAnchor: null })
    }

    handleLogout = () => {
        this.handleMenuClose()
        User.logout()
    }

    handleProfile = () => {
        this.handleMenuClose()
        this.props.history.push({ pathname: '/userinfo/', state: {from: this.props.location.pathname} })
    }

    render() {
        const { classes } = this.props
        const { menuAnchor, user } = this.state
        return (
            <AppBar className={classes.navbar} position="static">
                <Toolbar className={classes.toolbar}>
                    <Link to={HOME}>
                        <img src={logo} alt="" srcSet={logo + ' 2x'} width="80"/>
                    </Link>
                    <Grid container justify="flex-end" alignItems="center">
                        <Typography className={classes.name}>{ user.nickname }</Typography>
                        <IconButton 
                            aria-owns={menuAnchor ? 'user-menu' : null}
                            aria-haspopup="true"
                            onClick={this.handleAvatarClick}
                        >
                            <Avatar src={avatar_placeholder} />
                        </IconButton>
                        <Menu 
                            id="user-menu" 
                            anchorEl={menuAnchor} 
                            open={Boolean(menuAnchor)} 
                            onClose={this.handleMenuClose}
                        >
                            <MenuItem onClick={this.handleProfile}>Profile</MenuItem>
                            <MenuItem onClick={this.handleLogout}>Logout</MenuItem>
                        </Menu>
                    </Grid>
                </Toolbar>
            </AppBar>
        )
    }
}

export default withRouter(withStyles(styles)(Navbar))
